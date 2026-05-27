"""
SnapLyrics — Snap lyrics to any DJ edit via Whisper transcription.

Reads audio files (.aiff, .wav, .mp3, .flac, .m4a, .ogg, .aac) and matching
.lrc lyric files.  When a matching _vocals file is present (e.g.
Song_vocals.wav alongside Song.wav), lyrics are automatically synced
to the audio via Whisper transcription + global LRC alignment before generating
After Effects .jsx scripts with animated text layers, chorus grouping, camera
motion, DOF effects, and a macOS batch runner.
"""

from __future__ import annotations

import argparse
import random
import re
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path

# Optional transcription deps (only needed when _vocals sync is used)
try:
    import whisper
    _HAS_WHISPER = True
except ImportError:
    _HAS_WHISPER = False

try:
    import demucs.separate
    _HAS_DEMUCS = True
except ImportError:
    _HAS_DEMUCS = False

try:
    import lyricsgenius
    _HAS_GENIUS = True
except ImportError:
    _HAS_GENIUS = False

from difflib import SequenceMatcher
import os
import sys

# Load .env file if present
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Console colors (SnapLyrics palette)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _hex(h):
    """Convert hex color to ANSI escape."""
    r, g, b = int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"

_RESET = "\033[0m"
_BOLD = "\033[1m"
_LILAC = _hex("8956BA")      # Deep Lilac — headers, branding
_SNOW = _hex("F7F7F5")       # Bright Snow — general text
_GOLD = _hex("EAD82F")       # Golden Glow — success, highlights
_BLACK = _hex("060100")      # Black
_WISTERIA = _hex("C599E2")   # Wisteria — secondary info, progress
_RED = "\033[38;2;220;60;60m" # errors


def _progress_bar(current, total, width=30, label=""):
    """Print an inline progress bar."""
    pct = current / max(total, 1)
    filled = int(width * pct)
    bar = f"{_GOLD}{'█' * filled}{_WISTERIA}{'░' * (width - filled)}{_RESET}"
    text = f"\r  {bar} {_SNOW}{current}/{total}{_RESET}"
    if label:
        text += f" {_WISTERIA}{label}{_RESET}"
    sys.stdout.write(text)
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write("\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuration  (DIP: injectable dataclass, no side effects)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class VideoConfig:
    # Composition
    width: int = 1920
    height: int = 1080
    fps: int = 30

    # Text
    font: str = "Heavitas"
    base_font_size: int = 120
    min_font_scale: float = 0.5
    line_margin: int = 20
    text_split_threshold: int = 25
    max_words_per_block: int = 4

    # Anticipation (text appears before vocal moment)
    anticipation_seconds: float = 1.0

    # Animation timing (in frames)
    animation_in_frames: int = 15       # 0.5s at 30fps (half of anticipation)
    animation_out_frames: int = 6
    text_gap_before_next_frames: int = 15
    group_transition_frames: int = 6
    null_exit_frames: int = 12
    blink_out_min_frames: int = 90

    # Camera
    camera_pan_range: int = 30
    camera_tilt_range: float = 0.3
    shake_intensity: int = 5
    shake_duration: float = 0.5

    # Energy detection
    bar_duration: float = 2.0
    low_energy_threshold: int = 4

    # Mid-duration effects
    mid_duration_threshold: float = 2.0
    mid_zoom_range: tuple = (120, 135)
    mid_position_range: int = 150

    # Short text hard in/out
    hard_inout_max_chars: int = 8
    hard_inout_max_duration: float = 1.0

    # Reading speed: seconds per character for minimum display duration
    reading_speed_per_char: float = 0.06  # ~16 chars/sec, generous for big screen

    # DOF Camera
    dof_camera_probability: float = 0.15
    dof_camera_zoom: int = 2000
    dof_camera_aperture: int = 300
    dof_camera_blur_level: int = 150
    dof_camera_x_rotation_range: tuple = (-5, 5)
    dof_camera_y_rotation_range: tuple = (-3, 3)
    dof_camera_z_rotation_range: tuple = (-8, 8)
    dof_camera_position_drift: int = 1000

    # Derived (computed from frames / fps)
    @property
    def max_line_width(self):
        return self.width * 0.85

    @property
    def animation_duration(self):
        return self.animation_in_frames / self.fps

    @property
    def fade_duration(self):
        return self.animation_out_frames / self.fps

    @property
    def text_gap_before_next(self):
        return self.text_gap_before_next_frames / self.fps

    @property
    def null_exit_duration(self):
        return self.null_exit_frames / self.fps


# DJ-friendly audio formats
AUDIO_EXTENSIONS = (".aiff", ".aif", ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".aac")


def _find_audio_files(folder):
    """Find all audio files in a folder, sorted by name.

    Skips _vocals (acapella) files so they aren't treated as songs.
    """
    files = [f for f in Path(folder).iterdir()
             if f.is_file()
             and f.suffix.lower() in AUDIO_EXTENSIONS
             and not f.stem.endswith("_vocals")]
    return sorted(files)


def _split_lyrics_into_blocks(lyrics, max_words, anticipation):
    """Split lyric lines into word blocks and apply anticipation offset.

    Each line is split into chunks of max_words. Time is distributed evenly
    across sub-blocks within the original line's duration. All times are shifted
    earlier by anticipation_seconds so text is visible before the vocal moment.
    """
    if not lyrics:
        return lyrics

    blocks = []
    for i, lyric in enumerate(lyrics):
        words = lyric["text"].split()
        vocal_time = lyric["time"]

        # Determine duration of this lyric (until next lyric starts)
        if i < len(lyrics) - 1:
            line_duration = lyrics[i + 1]["time"] - vocal_time
        else:
            line_duration = 3.0

        # Split words into chunks
        chunks = []
        for j in range(0, len(words), max_words):
            chunk_words = words[j:j + max_words]
            chunks.append(" ".join(chunk_words))

        if len(chunks) <= 1:
            # Single block — just apply anticipation
            display_time = max(0, vocal_time - anticipation)
            blocks.append({"time": display_time, "text": lyric["text"]})
        else:
            # Distribute time evenly across sub-blocks
            block_duration = line_duration / len(chunks)
            for ci, chunk in enumerate(chunks):
                chunk_vocal_time = vocal_time + ci * block_duration
                display_time = max(0, chunk_vocal_time - anticipation)
                blocks.append({"time": display_time, "text": chunk})

    blocks.sort(key=lambda x: x["time"])
    return blocks


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LRC Writer  (SRP: only writes .lrc files)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LrcWriter:
    @staticmethod
    def write(lyrics, metadata, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            for meta in metadata:
                f.write(meta + "\n")
            if metadata:
                f.write("\n")
            for lyric in lyrics:
                total_seconds = lyric["time"]
                minutes = int(total_seconds // 60)
                remaining = total_seconds % 60
                secs = int(remaining)
                centis = int((remaining - secs) * 100)
                f.write(f"[{minutes:02d}:{secs:02d}.{centis:02d}]{lyric['text']}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Lyrics Fetcher  (SRP: fetch lyrics from internet)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LyricsFetcher:
    """Fetch lyrics from Genius API, with AZLyrics scraping as fallback."""

    @staticmethod
    def available():
        return _HAS_GENIUS

    @staticmethod
    def parse_artist_title(filename):
        """Parse 'Artist - Title' from filename, stripping tags like (Remix), [DJ X], etc."""
        name = Path(filename).stem
        # Remove common DJ edit tags: [DJ X], (Acapella Hype), (Remix), etc.
        clean = re.sub(r"\[.*?\]", "", name)
        clean = re.sub(r"\(.*?\)", "", clean)
        clean = clean.strip(" -")
        parts = clean.split(" - ", 1)
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return None, clean.strip()

    @staticmethod
    def _fetch_genius(artist, title):
        """Fetch lyrics from Genius API."""
        token = os.environ.get("GENIUS_API_TOKEN") or os.environ.get("GENIUS_TOKEN")
        if not token:
            return None
        try:
            genius = lyricsgenius.Genius(
                token, verbose=False, remove_section_headers=True,
                skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
            )
            genius.timeout = 10
            # Use search_song with the title only if artist parsing failed
            search_term = f"{title} {artist}" if artist else title
            song = genius.search_song(title, artist) if artist else genius.search_song(search_term)
            if song and song.lyrics:
                lines = song.lyrics.split("\n")
                if lines and "Lyrics" in lines[0]:
                    lines = lines[1:]
                if lines and "Embed" in lines[-1]:
                    lines[-1] = re.sub(r"\d*Embed$", "", lines[-1]).strip()
                cleaned = [l.strip() for l in lines if l.strip() and not re.match(r"^\[.*\]$", l.strip())]
                return "\n".join(cleaned)
        except Exception as e:
            # Log but don't crash — fallback sources will try next
            print(f"{_WISTERIA}    Genius: {e}{_RESET}")
        return None

    @staticmethod
    def _ssl_context():
        """Unverified SSL context for scraping (macOS cert issues)."""
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    @staticmethod
    def _fetch_azlyrics(artist, title):
        """Scrape lyrics from AZLyrics as fallback."""
        try:
            from urllib.request import urlopen, Request

            a = re.sub(r"[^a-z]", "", artist.lower())
            t = re.sub(r"[^a-z]", "", title.lower())
            url = f"https://www.azlyrics.com/lyrics/{a}/{t}.html"

            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            html = urlopen(req, timeout=10, context=LyricsFetcher._ssl_context()).read().decode("utf-8")

            match = re.search(
                r'<!-- Usage of azlyrics\.com content.*?-->\s*<div>(.*?)</div>',
                html, re.DOTALL
            )
            if match:
                raw = match.group(1)
                text = re.sub(r"<br\s*/?>", "\n", raw)
                text = re.sub(r"<.*?>", "", text)
                lines = [l.strip() for l in text.split("\n") if l.strip()]
                return "\n".join(lines)
        except Exception:
            pass
        return None

    @staticmethod
    def _fetch_lyrics_ovh(artist, title):
        """Fetch from lyrics.ovh free API (no key needed)."""
        try:
            from urllib.request import urlopen, Request
            from urllib.parse import quote
            import json

            url = f"https://api.lyrics.ovh/v1/{quote(artist)}/{quote(title)}"
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urlopen(req, timeout=10, context=LyricsFetcher._ssl_context()).read().decode("utf-8")
            data = json.loads(resp)
            if data.get("lyrics"):
                lines = [l.strip() for l in data["lyrics"].split("\n") if l.strip()]
                return "\n".join(lines)
        except Exception:
            pass
        return None

    def fetch(self, audio_path):
        """Fetch lyrics for an audio file. Returns text string or None."""
        artist, title = self.parse_artist_title(audio_path)
        print(f"{_WISTERIA}    Fetching lyrics: {artist or '?'} — {title}{_RESET}")

        # Try Genius first
        if _HAS_GENIUS:
            text = self._fetch_genius(artist, title)
            if text:
                print(f"{_GOLD}    Found on Genius{_RESET}")
                return text

        # Fallback to lyrics.ovh (free, no key)
        if artist:
            text = self._fetch_lyrics_ovh(artist, title)
            if text:
                print(f"{_GOLD}    Found on lyrics.ovh{_RESET}")
                return text

        # Fallback to AZLyrics scraping
        if artist:
            text = self._fetch_azlyrics(artist, title)
            if text:
                print(f"{_GOLD}    Found on AZLyrics{_RESET}")
                return text

        print(f"{_RED}    Lyrics not found online{_RESET}")
        return None

    def fetch_and_save(self, audio_path):
        """Fetch lyrics and save as .txt next to the audio file. Returns Path or None."""
        text = self.fetch(audio_path)
        if text:
            txt_path = Path(audio_path).with_suffix(".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"{_WISTERIA}    Saved → {txt_path.name}{_RESET}")
            return txt_path
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LRC Syncer  (SRP: sync lyrics to audio via Whisper transcription)
# Requires: openai-whisper.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LrcSyncer:
    SIMILARITY_THRESHOLD = 0.5
    _model = None

    @staticmethod
    def available():
        return _HAS_WHISPER

    @staticmethod
    def find_vocals(audio_path):
        """Find a _vocals file next to the audio (same name + '_vocals').

        Checks same extension first, then .wav (Demucs always outputs .wav).
        Example: Song.mp3 → Song_vocals.mp3 or Song_vocals.wav
        """
        p = Path(audio_path)
        candidate = p.with_name(f"{p.stem}_vocals{p.suffix}")
        if candidate.exists():
            return candidate
        wav_candidate = p.with_name(f"{p.stem}_vocals.wav")
        if wav_candidate.exists():
            return wav_candidate
        return None

    # ── Vocal separation (Demucs) ──────────────────────────

    @staticmethod
    def can_separate():
        return _HAS_DEMUCS

    @staticmethod
    def separate_vocals(audio_path):
        """Extract vocals from audio using Demucs. Returns path to vocals file."""
        import subprocess
        import time as _time
        p = Path(audio_path).resolve()
        out_dir = p.parent / "_demucs_tmp"

        proc = subprocess.Popen(
            ["python3", "-m", "demucs", "--two-stems", "vocals",
             "-o", str(out_dir), str(p)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        # Read stderr in a thread to parse Demucs tqdm progress
        import threading
        pct_box = [0.0]
        stderr_lines = []

        def _read_stderr():
            for raw in iter(proc.stderr.readline, b""):
                line = raw.decode("utf-8", errors="replace")
                stderr_lines.append(line)
                # tqdm writes lines like "  5%|███  | 8.8/175.5 [00:02..."
                m = re.search(r"(\d+)%\|", line)
                if m:
                    pct_box[0] = int(m.group(1)) / 100.0

        reader = threading.Thread(target=_read_stderr, daemon=True)
        reader.start()

        while proc.poll() is None:
            pct = pct_box[0]
            filled = int(30 * pct)
            bar = f"{_GOLD}{'█' * filled}{_WISTERIA}{'░' * (30 - filled)}{_RESET}"
            sys.stdout.write(f"\r    {bar} {_SNOW}Separating vocals...{_RESET} ")
            sys.stdout.flush()
            _time.sleep(0.5)

        reader.join(timeout=2)
        stdout_out = proc.stdout.read().decode("utf-8", errors="replace")

        if proc.returncode != 0:
            err = "".join(stderr_lines).strip() or stdout_out.strip()
            # Clear progress bar line before error
            sys.stdout.write(f"\r{' ' * 60}\r")
            raise RuntimeError(f"Demucs failed:\n{err}")

        bar = f"{_GOLD}{'█' * 30}{_RESET}"
        sys.stdout.write(f"\r    {bar} {_GOLD}Separated{_RESET}          \n")
        sys.stdout.flush()
        # Demucs outputs to: out_dir/htdemucs/stem_name/vocals.wav
        vocals_path = out_dir / "htdemucs" / p.stem / "vocals.wav"
        if not vocals_path.exists():
            # Try mdx_extra model path
            for model_dir in out_dir.iterdir():
                candidate = model_dir / p.stem / "vocals.wav"
                if candidate.exists():
                    vocals_path = candidate
                    break
        if not vocals_path.exists():
            raise FileNotFoundError(f"Demucs did not produce vocals at {vocals_path}")
        # Copy to _vocals file next to the audio for caching
        cached = p.with_name(f"{p.stem}_vocals.wav")
        shutil.copy2(vocals_path, cached)
        # Clean up temp dir
        shutil.rmtree(out_dir, ignore_errors=True)
        print(f"{_GOLD}    Vocals extracted → {cached.name}{_RESET}")
        return cached

    # ── Transcription ──────────────────────────────────────

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            print(f"{_WISTERIA}    Loading Whisper model (medium)...{_RESET}")
            cls._model = whisper.load_model("medium")
        return cls._model

    def transcribe(self, vocals_path, reference_lyrics=None):
        """Transcribe vocals file with Whisper, returning segments with timestamps."""
        import threading

        model = self._get_model()

        # Build initial_prompt from reference lyrics to guide Whisper
        initial_prompt = None
        if reference_lyrics:
            sample = [l["text"] for l in reference_lyrics[:8]]
            initial_prompt = ", ".join(sample)[:200]

        # Get audio duration for progress bar
        duration = None
        try:
            import subprocess as _sp
            out = _sp.run(
                ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                 "-of", "csv=p=0", str(vocals_path)],
                capture_output=True, text=True,
            )
            if out.returncode == 0 and out.stdout.strip():
                duration = float(out.stdout.strip())
        except Exception:
            pass

        # Run transcription in a thread with progress bar
        result_box = [None]

        def _run():
            kwargs = {
                "word_timestamps": True,
                "language": "es",
                "fp16": False,
                "no_speech_threshold": 0.95,
                "logprob_threshold": -1.0,
                "compression_ratio_threshold": 3.0,
                "condition_on_previous_text": False,
            }
            if initial_prompt:
                kwargs["initial_prompt"] = initial_prompt
            result_box[0] = model.transcribe(str(vocals_path), **kwargs)

        thread = threading.Thread(target=_run)
        thread.start()

        import time as _time
        start = _time.time()
        while thread.is_alive():
            elapsed = _time.time() - start
            if duration and duration > 0:
                # Estimate: whisper processes ~1x realtime on CPU, faster on GPU
                pct = min(elapsed / duration, 0.99)
                filled = int(30 * pct)
                bar = f"{_GOLD}{'█' * filled}{_WISTERIA}{'░' * (30 - filled)}{_RESET}"
                sys.stdout.write(f"\r    {bar} {_SNOW}Transcribing...{_RESET} ")
                sys.stdout.flush()
            else:
                sys.stdout.write(f"\r    {_WISTERIA}Transcribing... {_SNOW}{elapsed:.0f}s{_RESET} ")
                sys.stdout.flush()
            thread.join(timeout=0.5)

        # Complete the bar
        bar = f"{_GOLD}{'█' * 30}{_RESET}"
        sys.stdout.write(f"\r    {bar} {_GOLD}Transcribed{_RESET}     \n")
        sys.stdout.flush()

        result = result_box[0]
        segments = []
        for seg in result.get("segments", []):
            text = seg.get("text", "").strip()
            if text:
                segments.append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": text,
                })

        # Detect missed beginning: if first segment starts late, retry early portion
        if segments and segments[0]["start"] > 15:
            gap = segments[0]["start"]
            print(f"{_WISTERIA}    First segment at {gap:.0f}s — retrying early portion...{_RESET}")
            try:
                audio = whisper.load_audio(str(vocals_path))
                sr = 16000
                # Trim to just before the first detected segment + overlap
                trim_end = int(min(gap + 5, len(audio) / sr) * sr)
                early_audio = audio[:trim_end]
                early_result = model.transcribe(
                    early_audio,
                    word_timestamps=True,
                    language="es",
                    fp16=False,
                    no_speech_threshold=0.99,
                    logprob_threshold=-1.0,
                    compression_ratio_threshold=3.5,
                    condition_on_previous_text=False,
                    initial_prompt=initial_prompt,
                )
                early_segs = []
                for seg in early_result.get("segments", []):
                    text = seg.get("text", "").strip()
                    if text and seg["start"] < gap:
                        early_segs.append({
                            "start": seg["start"],
                            "end": seg["end"],
                            "text": text,
                        })
                if early_segs:
                    print(f"{_GOLD}    Recovered {len(early_segs)} early segments{_RESET}")
                    segments = early_segs + segments
                    segments.sort(key=lambda s: s["start"])
            except Exception:
                pass

        print(f"{_SNOW}    Whisper: {_GOLD}{len(segments)}{_SNOW} segments transcribed{_RESET}")
        return segments

    # ── Global alignment ───────────────────────────────────

    @staticmethod
    def _normalize(text):
        """Normalize text for comparison: lowercase, strip punctuation."""
        return re.sub(r"[^\w\s]", "", text.lower()).strip()

    def align(self, segments, lrc_lyrics):
        """Global alignment: match each Whisper segment to best LRC line by text similarity.

        Each segment gets the best-matching LRC line's text but keeps Whisper's timestamp.
        Same LRC line can be matched multiple times (handles repeated sections).
        """
        lrc_normalized = [self._normalize(l["text"]) for l in lrc_lyrics]
        lrc_texts = [l["text"] for l in lrc_lyrics]

        aligned = []
        matched = 0

        for seg in segments:
            seg_norm = self._normalize(seg["text"])
            best_ratio = 0.0
            best_idx = -1

            for i, lrc_norm in enumerate(lrc_normalized):
                ratio = SequenceMatcher(None, seg_norm, lrc_norm).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_idx = i

            if best_ratio >= self.SIMILARITY_THRESHOLD and best_idx >= 0:
                aligned.append({
                    "time": seg["start"],
                    "text": lrc_texts[best_idx],
                })
                matched += 1
            else:
                aligned.append({
                    "time": seg["start"],
                    "text": seg["text"],
                })

        aligned.sort(key=lambda x: x["time"])
        pct = 100 * matched // max(len(segments), 1)
        print(f"{_SNOW}    Matched {_GOLD}{matched}/{len(segments)}{_SNOW} segments to lyrics ({_GOLD}{pct}%{_SNOW}){_RESET}")
        return aligned, matched

    # ── Sync ────────────────────────────────────────────────

    def sync(self, acapella_path, reference_lyrics=None):
        """Transcribe vocals and optionally clean up text with reference lyrics.

        Args:
            acapella_path: Path to vocals file.
            reference_lyrics: Optional list of {"time": ..., "text": ...} from LRC/TXT/internet.
                Used only to fix Whisper's text — timestamps always come from transcription.

        Returns (lyrics, info_dict) or (None, None) if transcription fails.
        """
        segments = self.transcribe(acapella_path, reference_lyrics)
        if not segments:
            print(f"{_RED}    No segments transcribed{_RESET}")
            return None, None

        # Build lyrics from transcription
        if reference_lyrics:
            aligned, matched = self.align(segments, reference_lyrics)
            lyrics = aligned
        else:
            lyrics = [{"time": seg["start"], "text": seg["text"]} for seg in segments]
            matched = 0
            print(f"{_WISTERIA}    No reference lyrics — using Whisper text as-is{_RESET}")

        info = {
            "segments_transcribed": len(segments),
            "segments_matched": matched,
            "synced_count": len(lyrics),
        }

        print(f"{_GOLD}    Synced {len(lyrics)} lines{_RESET}")
        return lyrics, info


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Song Analysis Result  (value object passed between components)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class SongAnalysis:
    lyrics: list
    chorus_groups: list
    chorus_indices: set
    energy_events: list
    lyric_durations: list
    comp_duration: float


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LRC Parser  (SRP: only parses .lrc files)
# LSP: unified return type (lyrics, metadata) usable by both tools
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LrcParser:
    ENCODINGS = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
    TIMESTAMP_PATTERNS = [
        r"\[(\d{1,2}):(\d{2})\.(\d{2})\](.*)",   # [M:SS.xx] or [MM:SS.xx]
        r"\[(\d{2}):(\d{2}):(\d{2})\](.*)",       # [MM:SS:xx]
    ]

    def parse(self, lrc_path):
        """Parse .lrc file → (lyrics list[dict], metadata list[str])."""
        content = self._read_with_fallback(lrc_path)
        if content is None:
            return [], []

        lyrics = []
        metadata = []

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue

            if re.match(r"\[([a-z]{2,}):(.+)\]", line):
                metadata.append(line)
                continue

            for pattern in self.TIMESTAMP_PATTERNS:
                match = re.match(pattern, line)
                if match:
                    minutes = int(match.group(1))
                    seconds = int(match.group(2))
                    centis = int(match.group(3))
                    time = minutes * 60 + seconds + centis / 100
                    text = match.group(4).strip()
                    if text:
                        lyrics.append({"time": time, "text": text})
                    break

        lyrics.sort(key=lambda x: x["time"])
        return lyrics, metadata

    def parse_txt(self, txt_path):
        """Parse plain .txt file → (lyrics list[dict], metadata list[str]).

        Each non-empty line becomes a lyric with time=0 (timestamps come from Whisper).
        """
        content = self._read_with_fallback(txt_path)
        if content is None:
            return [], []
        lyrics = []
        for line in content.split("\n"):
            text = line.strip()
            if text:
                lyrics.append({"time": 0, "text": text})
        return lyrics, []

    def _read_with_fallback(self, path):
        for enc in self.ENCODINGS:
            try:
                with open(path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Text Layout  (SRP: font sizing, splitting, positioning)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TextLayout:
    def __init__(self, config: VideoConfig):
        self.c = config

    def calculate_text_width(self, text, font_size):
        return len(text) * font_size * 0.6

    def is_short_text(self, text, duration):
        return (len(text.strip()) < self.c.hard_inout_max_chars
                and duration < self.c.hard_inout_max_duration)

    def should_add_mid_effect(self, duration):
        return duration > self.c.mid_duration_threshold

    def split_text_at_midpoint(self, text):
        if len(text) < self.c.text_split_threshold:
            return [text]
        words = text.split()
        if len(words) < 2:
            return [text]
        mid_char = len(text) // 2
        best_split = 0
        best_distance = len(text)
        current_pos = 0
        for i, word in enumerate(words[:-1]):
            current_pos += len(word) + 1
            distance = abs(current_pos - mid_char)
            if distance < best_distance:
                best_distance = distance
                best_split = i + 1
        line1 = " ".join(words[:best_split])
        line2 = " ".join(words[best_split:])
        return [line1, line2] if line1 and line2 else [text]

    def split_text_lines(self, text, max_width, font_size):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if self.calculate_text_width(test_line, font_size) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def calculate_font_size(self, text):
        c = self.c
        # Very short text (<=10 chars): 50% bigger
        if len(text.strip()) <= 10:
            big = int(c.base_font_size * 1.5)
            w = self.calculate_text_width(text, big)
            if w <= c.max_line_width:
                return big, [text]
            return int(big * c.max_line_width / w), [text]

        # Long text (>=25 chars): split into 2 lines
        if len(text) >= c.text_split_threshold:
            lines = self.split_text_at_midpoint(text)
            max_line = max(lines, key=len)
            w = self.calculate_text_width(max_line, c.base_font_size)
            if w <= c.max_line_width:
                return c.base_font_size, lines
            scale = c.max_line_width / w
            if scale >= c.min_font_scale:
                return int(c.base_font_size * scale), lines
            return int(c.base_font_size * c.min_font_scale), lines

        # Normal text (11-24 chars)
        w = self.calculate_text_width(text, c.base_font_size)
        if w <= c.max_line_width:
            return c.base_font_size, [text]
        scale = c.max_line_width / w
        if scale >= c.min_font_scale:
            return int(c.base_font_size * scale), [text]
        adjusted = int(c.base_font_size * 0.7)
        lines = self.split_text_lines(text, c.max_line_width, adjusted)
        return adjusted, lines


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Song Analyzer  (SRP: chorus detection, energy analysis, duration calc)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SongAnalyzer:
    def __init__(self, config: VideoConfig):
        self.c = config

    def analyze(self, lyrics):
        chorus_groups = self.find_chorus_groups(lyrics)
        chorus_indices = set()
        for group in chorus_groups:
            for item in group["items"]:
                chorus_indices.add(item["index"])
        return SongAnalysis(
            lyrics=lyrics,
            chorus_groups=chorus_groups,
            chorus_indices=chorus_indices,
            energy_events=self.detect_energy_changes(lyrics),
            lyric_durations=self.calculate_lyric_durations(lyrics),
            comp_duration=max(l["time"] for l in lyrics) + 5 if lyrics else 30,
        )

    def find_chorus_groups(self, lyrics):
        if not lyrics:
            return []
        groups = []
        i = 0
        while i < len(lyrics):
            current_text = lyrics[i]["text"].strip()
            matching = [{"index": i, "lyric": lyrics[i]}]
            j = i + 1
            while j < len(lyrics) and lyrics[j]["text"].strip() == current_text:
                matching.append({"index": j, "lyric": lyrics[j]})
                j += 1
            if len(matching) >= 2:
                groups.append({
                    "start_index": i,
                    "end_index": j - 1,
                    "items": matching,
                    "text": current_text,
                })
                i = j
            else:
                i += 1
        return groups

    def detect_energy_changes(self, lyrics):
        if len(lyrics) < 2:
            return []
        events = []
        low_start = None
        for i in range(1, len(lyrics)):
            gap = lyrics[i]["time"] - lyrics[i - 1]["time"]
            if gap > self.c.bar_duration * self.c.low_energy_threshold:
                if low_start is None:
                    low_start = lyrics[i - 1]["time"]
            else:
                if low_start is not None:
                    events.append({
                        "time": lyrics[i]["time"],
                        "type": "energy_return",
                        "low_energy_duration": lyrics[i]["time"] - low_start,
                    })
                    low_start = None
        return events

    def calculate_lyric_durations(self, lyrics):
        """Calculate durations with character-based minimum and overlap detection.

        Minimum display time = chars * reading_speed_per_char.
        When a lyric's minimum duration extends past the next lyric's start,
        they overlap — both stay visible and exit together via a shared null.
        """
        c = self.c
        durations = []

        for i, lyric in enumerate(lyrics):
            char_count = len(lyric["text"])
            min_dur = max(char_count * c.reading_speed_per_char, 0.8)

            if i < len(lyrics) - 1:
                gap_to_next = lyrics[i + 1]["time"] - lyric["time"]
                dur = max(gap_to_next, min_dur)
            else:
                dur = max(3.0, min_dur)

            durations.append({
                "index": i,
                "lyric": lyric,
                "start_time": lyric["time"],
                "end_time": lyric["time"] + dur,
                "duration": dur,
            })

        # Detect overlap groups: lyrics visible at the same time exit together
        overlap_groups = []
        used = set()
        for i, ld in enumerate(durations):
            if i in used:
                continue
            group = [i]
            used.add(i)
            group_end = ld["end_time"]
            j = i + 1
            while j < len(durations) and durations[j]["start_time"] < group_end:
                group.append(j)
                used.add(j)
                # Extend group end to the latest member
                group_end = max(group_end, durations[j]["end_time"])
                j += 1
            if len(group) >= 2:
                # All members of the group share the same end time
                for idx in group:
                    durations[idx]["end_time"] = group_end
                    durations[idx]["duration"] = group_end - durations[idx]["start_time"]
                overlap_groups.append({
                    "indices": group,
                    "end_time": group_end,
                })

        # Store overlap groups on durations for the renderer
        for ld in durations:
            ld["overlap_group"] = None
        for gi, og in enumerate(overlap_groups):
            for idx in og["indices"]:
                durations[idx]["overlap_group"] = gi

        return durations


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Animation Library  (OCP: registry pattern, open for extension)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AnimationLibrary:
    EASING_TYPES = ["Quad", "Cubic", "Quart", "Quint", "Sine",
                    "Expo", "Circ", "Back", "Elastic", "Bounce"]
    EASING_DIRS = ["In", "Out", "InOut"]

    def __init__(self, config: VideoConfig, style=None):
        self.c = config
        self._styles = {}          # style_name → [animation dicts]
        self._register_defaults()
        self._register_isokinetic()
        self._register_newton()
        self._register_unique()
        # Pick style: explicit, or random across all registered styles
        if style and style in self._styles:
            self._active_style = style
        elif style:
            available = ", ".join(sorted(self._styles.keys()))
            raise ValueError(f"Unknown style '{style}'. Available: {available}")
        else:
            self._active_style = random.choice(list(self._styles.keys()))

    @property
    def active_style(self):
        return self._active_style

    @property
    def available_styles(self):
        return sorted(self._styles.keys())

    def register(self, animation, style="standard"):
        self._styles.setdefault(style, []).append(animation)

    def random(self):
        pool = self._styles[self._active_style]
        template = random.choice(pool)
        anim = dict(template)
        if anim.get("easing") is None:
            anim["easing"] = self.random_easing()
        return anim

    def random_easing(self):
        t = random.choice(self.EASING_TYPES)
        d = random.choice(self.EASING_DIRS)
        return f"ease{d}{t}"

    def get_out_animation(self, duration_frames):
        if duration_frames > self.c.blink_out_min_frames and random.random() < 0.5:
            return {"name": "blinkOut", "type": "blink"}
        return {"name": "fadeOut", "type": "fade"}

    def _register_defaults(self):
        # easing=None → randomised per call.  Fixed easing for elasticPop.
        defaults = [
            {"name": "fadeIn",
             "opacity": {"from": 0, "to": 100}},
            {"name": "scaleIn",
             "scale": {"from": [0, 0], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideUp",
             "position_offset": {"from": [0, 200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideDown",
             "position_offset": {"from": [0, -200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "bounceIn",
             "scale": {"from": [130, 130], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideFromLeft",
             "position_offset": {"from": [-300, 0], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideFromRight",
             "position_offset": {"from": [300, 0], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "typewriter",
             "text_animator": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "wave",
             "wave_animator": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "blurReveal",
             "blur": {"from": 50, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "zoomBlur",
             "scale": {"from": [150, 150], "to": [100, 100]},
             "blur": {"from": 30, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "flipX",
             "rotationX": {"from": 90, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "flipY",
             "rotationY": {"from": 90, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "glitch",
             "glitch": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "dropShadowPulse",
             "shadow": {"from": 0, "to": 20},
             "scale": {"from": [95, 95], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "extremeZoomIn",
             "scale": {"from": [3000, 3000], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "elasticPop",
             "elastic_pop": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeInOutElastic"},
            # ── slide + blur combos ──
            {"name": "slideUpBlur",
             "position_offset": {"from": [0, 150], "to": [0, 0]},
             "blur": {"from": 25, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideDownBlur",
             "position_offset": {"from": [0, -150], "to": [0, 0]},
             "blur": {"from": 25, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideLeftBlur",
             "position_offset": {"from": [-250, 0], "to": [0, 0]},
             "blur": {"from": 20, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideRightBlur",
             "position_offset": {"from": [250, 0], "to": [0, 0]},
             "blur": {"from": 20, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            # ── 3D rotations ──
            {"name": "flipXZoom",
             "rotationX": {"from": -180, "to": 0},
             "scale": {"from": [50, 50], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "flipYZoom",
             "rotationY": {"from": -180, "to": 0},
             "scale": {"from": [50, 50], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "tiltIn",
             "rotationX": {"from": 45, "to": 0},
             "position_offset": {"from": [0, 100], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            # ── scale variations ──
            {"name": "shrinkIn",
             "scale": {"from": [200, 200], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "squishX",
             "scale": {"from": [0, 120], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "squishY",
             "scale": {"from": [120, 0], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "popShrink",
             "scale": {"from": [160, 160], "to": [100, 100]},
             "blur": {"from": 15, "to": 0},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            # ── diagonal slides ──
            {"name": "slideDiagonalTL",
             "position_offset": {"from": [-200, -200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideDiagonalBR",
             "position_offset": {"from": [200, 200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideDiagonalTR",
             "position_offset": {"from": [200, -200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "slideDiagonalBL",
             "position_offset": {"from": [-200, 200], "to": [0, 0]},
             "opacity": {"from": 0, "to": 100}},
            # ── dramatic ──
            {"name": "crashZoom",
             "scale": {"from": [5000, 5000], "to": [100, 100]},
             "blur": {"from": 40, "to": 0},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "riseAndShadow",
             "position_offset": {"from": [0, 80], "to": [0, 0]},
             "shadow": {"from": 0, "to": 25},
             "opacity": {"from": 0, "to": 100}},
            {"name": "glitchBlur",
             "glitch": True,
             "blur": {"from": 30, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "heavyDrop",
             "position_offset": {"from": [0, -400], "to": [0, 0]},
             "scale": {"from": [110, 90], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBounce"},
            # ── subtle / elegant ──
            {"name": "whisperIn",
             "scale": {"from": [95, 95], "to": [100, 100]},
             "blur": {"from": 8, "to": 0},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutSine"},
            {"name": "breatheIn",
             "scale": {"from": [90, 90], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeInOutSine"},
            # ── kinetic typography ──
            {"name": "charCascade",
             "char_cascade": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "charRotateIn",
             "char_rotate_in": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "charScaleStagger",
             "char_scale_stagger": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "charBlurSweep",
             "char_blur_sweep": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "charSpiral",
             "char_spiral": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            {"name": "charBounceUp",
             "char_bounce_up": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBounce"},
            {"name": "char3dFlip",
             "char_3d_flip": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "trackingExpand",
             "tracking_expand": True,
             "scale": {"from": [80, 80], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "trackingCompress",
             "tracking_compress": True,
             "scale": {"from": [120, 120], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "lineWipe",
             "line_wipe": True,
             "opacity": {"from": 0, "to": 100}},
            # ── kinetic combos ──
            {"name": "cascadeBlur",
             "char_cascade": True,
             "blur": {"from": 20, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "rotateZoomIn",
             "char_rotate_in": True,
             "scale": {"from": [50, 50], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100}},
            {"name": "spiralShadow",
             "char_spiral": True,
             "shadow": {"from": 0, "to": 20},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            {"name": "flipBlurReveal",
             "char_3d_flip": True,
             "blur": {"from": 15, "to": 0},
             "opacity": {"from": 0, "to": 100}},
            {"name": "wipeTrackingExpand",
             "line_wipe": True,
             "tracking_expand": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "bounceGlitch",
             "char_bounce_up": True,
             "glitch": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBounce"},
            # ── 3D pop-out titles ──
            {"name": "pop3dToward",
             "pop3d_toward": True,
             "scale": {"from": [30, 30], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dAway",
             "pop3d_away": True,
             "scale": {"from": [250, 250], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            {"name": "pop3dSpinX",
             "pop3d_spin_x": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dSpinY",
             "pop3d_spin_y": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dTumble",
             "pop3d_tumble": True,
             "scale": {"from": [50, 50], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            {"name": "pop3dSlam",
             "pop3d_slam": True,
             "scale": {"from": [140, 140], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBounce"},
            {"name": "pop3dShatterIn",
             "pop3d_shatter_in": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dWaveZ",
             "pop3d_wave_z": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "pop3dCardFan",
             "pop3d_card_fan": True,
             "opacity": {"from": 0, "to": 100}},
            {"name": "pop3dZoomRotate",
             "pop3d_zoom_rotate": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            # ── 3D pop combos ──
            {"name": "pop3dTowardBlur",
             "pop3d_toward": True,
             "blur": {"from": 40, "to": 0},
             "scale": {"from": [20, 20], "to": [100, 100]},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dSlamShadow",
             "pop3d_slam": True,
             "shadow": {"from": 0, "to": 30},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBounce"},
            {"name": "pop3dTumbleBlur",
             "pop3d_tumble": True,
             "blur": {"from": 25, "to": 0},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutBack"},
            {"name": "pop3dShatterBlur",
             "pop3d_shatter_in": True,
             "blur": {"from": 15, "to": 0},
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dSpinTrack",
             "pop3d_spin_y": True,
             "tracking_expand": True,
             "opacity": {"from": 0, "to": 100},
             "easing": "easeOutExpo"},
            {"name": "pop3dCardCascade",
             "pop3d_card_fan": True,
             "char_cascade": True,
             "opacity": {"from": 0, "to": 100}},
        ]
        for a in defaults:
            a.setdefault("easing", None)
            self.register(a, style="standard")

    def _register_isokinetic(self):
        # Animations from Isokinetic AE title templates (videohive-24099586).
        # Values extracted from v3 JSON export — exact match to original scenes.
        # Each scene_type triggers a dedicated renderer in _render_scene_extras().
        isokinetic = [
            # ── Scene_01: 3D Cube Flip (rotX variant) ──
            # Rotation_02: rotX 180→0 in 0.367s + elastic overshoot + wiggle(0.5,5)
            # Text: backface cull + sourceRect anchor centering.
            # Line 0=top face, line 1=side (rotY -180→-90, Z=-90),
            # line 2=bottom (rotX 180→90). All elastic.
            {"name": "isoCubeFlipX",
             "null_rotation": {"rotationX": {"from": 180, "to": 0},
                               "elastic": True, "wiggle": True,
                               "anim_duration_override": 0.367},
             "backface_cull": True,
             "scene_type": "cube_flip",
             "easing": "easeOutExpo"},

            # ── Scene_01: 3D Cube Flip (rotY variant) ──
            {"name": "isoCubeFlipY",
             "null_rotation": {"rotationY": {"from": 180, "to": 0},
                               "elastic": True, "wiggle": True,
                               "anim_duration_override": 0.367},
             "backface_cull": True,
             "scene_type": "cube_flip",
             "easing": "easeOutExpo"},

            # ── Scene_02: 3D Perspective Drift ──
            # Rotation_02: orientation drift (0,0,0)→(25.97,326.81,352.19) over 2.069s.
            # Position drift (960,664)→(960,540). NO backface cull.
            # Text: staggered opacity 0.067s per line, even lines rotX=-90° (folded book).
            {"name": "isoPerspectiveDrift",
             "null_rotation": {"orientation_drift": {"from": [0, 0, 0],
                                                      "to": [25.97, 326.81, 352.19]},
                               "position_drift": {"from": [960, 664, 0],
                                                   "to": [960, 540, 0]},
                               "anim_duration_override": 2.069},
             "scene_type": "perspective_drift",
             "easing": "easeOutSine"},

            # ── Scene_08: Spinning 3D Cube ──
            # Cube_01: anchor=(959.73,536.39,190), rotX=25° static,
            # rotY 45→1125° over full duration (continuous spin), wiggle orientation.
            # 4 text faces: front(0°), right(-90°), back(orient 0,270,0), left(90°).
            # Backface cull + opacity expression on null.
            {"name": "isoSpinningCube",
             "null_rotation": {"rotationX": {"from": 25, "to": 25},
                               "continuous_rotation": {"axis": "Y",
                                                        "from": 45, "to": 1125},
                               "wiggle": True,
                               "anchor_override": [959.73, 536.39, 190]},
             "backface_cull": True,
             "scene_type": "spinning_cube",
             "easing": "easeOutExpo"},

            # ── Scene_10: CC Cylinder ──
            # Text layer with CC Cylinder effect: Radius=100%, RotX=-62, RotY=-102,
            # Render=Full(4). Plus Tint for color control. No rotation null needed.
            {"name": "isoCCCylinder",
             "scene_type": "cc_cylinder",
             "easing": "easeOutSine"},

            # ── Scene_12: Zigzag Accordion Fold ──
            # Rotation null: rotY 0→-45 + orient drift (30,0,0)→(0,0,0) over 1.702s.
            # Position drift (960,540,967)→(948,134,499).
            # Text: left-edge anchor (sourceRect left), per-line alternating rotY ±90°.
            # Backface cull on all layers.
            {"name": "isoChainedFold",
             "null_rotation": {"rotationY": {"from": 0, "to": -45},
                               "orientation_drift": {"from": [0, 0, 0],
                                                      "to": [30, 0, 0]},
                               "position_drift": {"from": [960, 540, 967],
                                                   "to": [948, 134, 499]},
                               "anim_duration_override": 1.702},
             "backface_cull": True,
             "scene_type": "chained_fold",
             "easing": "easeOutExpo"},

            # ── Scene_15: Scrolling Text Wall ──
            # Rotation null: static orientation=[19.98,40.81,8.19] (tilted perspective).
            # Text: horizontal position crawl over full duration, staggered opacity
            # 0.067s per line, even lines rotX=-90° (3D book fold).
            # Layers 4-6 at Z=-115.15 in original.
            {"name": "isoScrollWall",
             "null_rotation": {"orientation_static": [19.98, 40.81, 8.19]},
             "scene_type": "scrolling_wall",
             "easing": "easeInOutSine"},

            # ── Stacked Cascade (4x Title_01 parented chain) ──
            # Root: anchor=(960,225,225), X Rotation=2 full turns (0→720°),
            # Y Rotation=15° static, Z Rotation=15° static.
            # Fill effect (white) on all layers. Cascading parent chain.
            {"name": "isoStackedCascade",
             "null_rotation": {"continuous_rotation": {"axis": "X",
                                                        "from": 0, "to": 720},
                               "rotationY": {"from": 15, "to": 15},
                               "rotationZ": {"from": 15, "to": 15},
                               "anchor_override": [960, 225, 225]},
             "scene_type": "stacked_cascade",
             "easing": "easeOutExpo"},

            # ── Kinetic Typography 14: Tiled Text Wall ──
            # Rotation null: Y=-40° static, Z=10° static (tilted perspective).
            # Each text layer: Motion Tile (Output Width=600, horizontal repeat).
            # Position expression auto-stacks vertically:
            #   idx = index - parent.index; [width/2, height/2 + height*idx, idx]
            # Single word duplicated across composition copies.
            {"name": "isoTiledWall",
             "null_rotation": {"rotationY": {"from": -40, "to": -40},
                               "rotationZ": {"from": 10, "to": 10}},
             "scene_type": "tiled_wall",
             "easing": "easeOutExpo"},
        ]
        for a in isokinetic:
            a.setdefault("easing", None)
            self.register(a, style="isokinetic")

    def _register_newton(self):
        # Animations from NEWTON — Rhythmic Typography (videohive).
        # Single-word text with mega-zoom entrance (3116%→100%), optional
        # stepped shrink exit, per-character scramble (Animator 1) and
        # per-character scale/tracking (Animator 2), plus fill color flash.
        newton = [
            # ── Type A: Short zoom — fast in, brief hold, fast out ──
            # 4 KFs: 3116→100 (0.2s bezier), hold, 100→20 (0.16s bezier)
            {"name": "newtonShort",
             "scene_type": "newton_zoom",
             "newton_variant": "short",
             "easing": "easeOutExpo"},

            # ── Type B: Long with stepped exit — signature Newton look ──
            # 9-10 KFs: 3116→100 (0.2s bezier), hold, then rhythmic
            # stepped shrink 95→90→85→80→60→35 (hold interpolation)
            {"name": "newtonStepped",
             "scene_type": "newton_zoom",
             "newton_variant": "stepped",
             "easing": "easeOutExpo"},

            # ── Type C: Simple zoom — just the entrance ──
            # 2 KFs: 3116→100 (0.2s bezier)
            {"name": "newtonSimple",
             "scene_type": "newton_zoom",
             "newton_variant": "simple",
             "easing": "easeOutExpo"},
        ]
        for a in newton:
            self.register(a, style="newton")

    def _register_unique(self):
        # Animations from Unique Typography (videohive).
        # 30 scenes, 1920x1080 @ 30fps. Core mechanic: 3D null chains with
        # bounce expressions, Z-depth text copies, entrance spin + exit fly-out.
        # 7 patterns identified; 4 main ones implemented (A, C, D, F).
        unique = [
            # ── Pattern A: Spin-In / Fly-Out (18 scenes) ──
            # Entrance: position off-screen + Z rotation 360→0 + bounce
            # Exit: position fly-out + Z rotation 0→450+ + scale shrink
            {"name": "uniqueSpinFlyOut",
             "scene_type": "unique_spin",
             "unique_variant": "spin_fly",
             "easing": "easeOutExpo"},

            # ── Pattern C: Slide-In Text (4 scenes) ──
            # Text slides from opposing directions (top/bottom)
            # Exit: 3-KF hesitate-then-fly pattern with scale+rotation
            {"name": "uniqueSlideIn",
             "scene_type": "unique_spin",
             "unique_variant": "slide_in",
             "easing": "easeOutExpo"},

            # ── Pattern D: Y-Rotation Card Flip (3 scenes) ──
            # Entrance: Y rotation -90→0 + bounce + Z position depth→0
            # Exit: Y rotation 0→270 + scale 100→0 + Z fly back
            {"name": "uniqueCardFlip",
             "scene_type": "unique_spin",
             "unique_variant": "card_flip",
             "easing": "easeOutExpo"},

            # ── Pattern F: Z-Depth Fly-Through (2 scenes) ──
            # Multiple word groups with staggered entrances
            # Exit: deep Z travel (0→-4320) creating fly-through
            {"name": "uniqueZFlyThrough",
             "scene_type": "unique_spin",
             "unique_variant": "z_fly",
             "easing": "easeOutExpo"},
        ]
        for a in unique:
            self.register(a, style="unique")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JSX Renderer  (SRP: only generates After Effects JSX code)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class JsxRenderer:
    def __init__(self, config: VideoConfig, layout: TextLayout,
                 animations: AnimationLibrary):
        self.c = config
        self.layout = layout
        self.anim = animations

    # ── public ──────────────────────────────────────────────

    def render(self, audio_path, analysis: SongAnalysis,
               project_name, song_folder):
        audio_jsx = self._escape_path(audio_path)
        folder_jsx = self._escape_path(song_folder)
        parts = [
            self._header(project_name, audio_jsx, folder_jsx, analysis),
            self._camera_section(analysis.comp_duration, analysis.energy_events),
            self._chorus_section(analysis),
            self._individual_section(analysis),
            self._footer(project_name),
        ]
        return "".join(parts)

    # ── helpers ─────────────────────────────────────────────

    @staticmethod
    def _escape_path(path):
        return str(path).replace("\\", "/").replace('"', '\\"')

    @staticmethod
    def _escape_text(text):
        return (text.replace("\\", "\\\\").replace('"', '\\"')
                    .replace("'", "\\'").replace("\n", "\\n"))

    # ── header: comp + helpers + audio ──────────────────────

    def _header(self, name, audio_jsx, folder_jsx, analysis):
        c = self.c
        return f"""// Auto-generated After Effects Script
// Project: {name}
// Chorus groups: {len(analysis.chorus_groups)}
// Energy events: {len(analysis.energy_events)}
// Total lyrics: {len(analysis.lyrics)}

(function() {{
    app.beginUndoGroup("Create Lyrics Video - {name}");

    try {{
        var projectName = "{name}";
        var audioPath = "{audio_jsx}";
        var projectFolder = "{folder_jsx}";

        if (!app.project || app.project.file == null) {{
            app.newProject();
        }}

        var comp = app.project.items.addComp(
            projectName, {c.width}, {c.height}, 1,
            {analysis.comp_duration}, {c.fps}
        );
        comp.motionBlur = true;

        // =====================
        // HELPER FUNCTIONS
        // =====================
        function applyEaseToKeyframes(prop, easingType) {{
            var numKeys = prop.numKeys;
            if (numKeys < 2) return;
            for (var k = 1; k <= numKeys; k++) {{
                var easeIn = new KeyframeEase(0.5, 75);
                var easeOut = new KeyframeEase(0.5, 75);
                if (easingType.indexOf("In") !== -1 && easingType.indexOf("Out") === -1) {{
                    easeIn = new KeyframeEase(0.1, 33);
                    easeOut = new KeyframeEase(0.9, 90);
                }} else if (easingType.indexOf("Out") !== -1 && easingType.indexOf("In") === -1) {{
                    easeIn = new KeyframeEase(0.9, 90);
                    easeOut = new KeyframeEase(0.1, 33);
                }}
                try {{
                    if (prop.propertyValueType == PropertyValueType.TwoD ||
                        prop.propertyValueType == PropertyValueType.ThreeD) {{
                        prop.setTemporalEaseAtKey(k, [easeIn, easeIn], [easeOut, easeOut]);
                    }} else {{
                        prop.setTemporalEaseAtKey(k, [easeIn], [easeOut]);
                    }}
                }} catch(e) {{}}
            }}
        }}

        function applyFastEase(prop) {{
            var numKeys = prop.numKeys;
            if (numKeys < 2) return;
            for (var k = 1; k <= numKeys; k++) {{
                var fastEase = new KeyframeEase(0.9, 95);
                try {{
                    if (prop.propertyValueType == PropertyValueType.TwoD ||
                        prop.propertyValueType == PropertyValueType.ThreeD) {{
                        prop.setTemporalEaseAtKey(k, [fastEase, fastEase], [fastEase, fastEase]);
                    }} else {{
                        prop.setTemporalEaseAtKey(k, [fastEase], [fastEase]);
                    }}
                }} catch(e) {{}}
            }}
        }}

        // =====================
        // IMPORT AUDIO
        // =====================
        try {{
            var audioFile = new File(audioPath);
            if (audioFile.exists) {{
                var audioImport = app.project.importFile(new ImportOptions(audioFile));
                var audioLayer = comp.layers.add(audioImport);
                audioLayer.name = "Audio - " + projectName;
            }}
        }} catch(e) {{}}
"""

    # ── camera null + pan + shake ───────────────────────────

    def _camera_section(self, comp_duration, energy_events):
        c = self.c
        cx, cy = c.width / 2, c.height / 2
        jsx = [f"""
        // =====================
        // CREATE GLOBAL CAMERA NULL
        // =====================
        var cameraNull = comp.layers.addNull();
        cameraNull.name = "CAMERA_GLOBAL";
        cameraNull.property("Position").setValue([{cx}, {cy}]);
        cameraNull.property("Anchor Point").setValue([{cx}, {cy}]);

        cameraNull.property("Scale").expression = 'var freq = 0.05; var amp = 2; var base = 100; [base + Math.sin(time * Math.PI * 2 * freq) * amp, base + Math.sin(time * Math.PI * 2 * freq) * amp]';
"""]
        # Pan keyframes
        for i in range(int(comp_duration / 10) + 2):
            t = i * random.uniform(8, 14)
            if t < comp_duration:
                px = cx + random.uniform(-c.camera_pan_range, c.camera_pan_range)
                py = cy + random.uniform(-c.camera_pan_range, c.camera_pan_range)
                jsx.append(f"""
        cameraNull.property("Position").setValueAtTime({t}, [{px}, {py}]);""")

        jsx.append(f"""
        applyEaseToKeyframes(cameraNull.property("Position"), "easeInOutSine");

        cameraNull.property("Rotation").expression = 'var freq = 0.03; var amp = {c.camera_tilt_range}; Math.sin(time * Math.PI * 2 * freq) * amp';

        // =====================
        // SHAKE AT ENERGY MOMENTS
        // =====================
""")
        for event in energy_events:
            jsx.append(f"""
        (function() {{
            var shakeTime = {event['time']};
            var shakeDur = {c.shake_duration};
            var shakeInt = {c.shake_intensity};
            var basePos = cameraNull.property("Position").valueAtTime(shakeTime, false);
            for (var s = 0; s < 5; s++) {{
                var sTime = shakeTime + (s * shakeDur / 5);
                var offsetX = (Math.random() - 0.5) * shakeInt * 2;
                var offsetY = (Math.random() - 0.5) * shakeInt * 2;
                cameraNull.property("Position").setValueAtTime(sTime, [basePos[0] + offsetX, basePos[1] + offsetY]);
            }}
            cameraNull.property("Position").setValueAtTime(shakeTime + shakeDur, basePos);
        }})();
""")

        jsx.append("""
        // =====================
        // LAYER ARRAYS
        // =====================
        var textLayers = [];
        var chorusNulls = [];

""")
        return "".join(jsx)

    # ── chorus groups ───────────────────────────────────────

    def _chorus_section(self, analysis):
        parts = []
        for idx, group in enumerate(analysis.chorus_groups):
            parts.append(self._chorus_group(idx, group, analysis.lyrics))
        return "".join(parts)

    def _chorus_group(self, group_idx, group, lyrics):
        c = self.c
        cx, cy = c.width / 2, c.height / 2
        items = group["items"]
        first_time = items[0]["lyric"]["time"]
        last_time = items[-1]["lyric"]["time"]

        # Heights info
        heights_info = []
        for item in items:
            fs, lines = self.layout.calculate_font_size(item["lyric"]["text"])
            h = fs * len(lines) * 1.2 + c.line_margin
            heights_info.append({"font_size": fs, "lines": lines, "height": h})

        # End time
        last_idx = items[-1]["index"]
        if last_idx < len(lyrics) - 1:
            group_end_time = lyrics[last_idx + 1]["time"] - c.text_gap_before_next
        else:
            group_end_time = last_time + 3

        layer_margin = 50
        transition_frames = 6

        jsx = [f"""
        // =====================
        // CHORUS GROUP {group_idx}
        // =====================
        var chorusNull{group_idx} = comp.layers.addNull();
        chorusNull{group_idx}.name = "Chorus_{group_idx}";
        chorusNull{group_idx}.startTime = {first_time - 0.5};
        chorusNull{group_idx}.outPoint = {group_end_time + c.null_exit_duration + 0.5};
        chorusNull{group_idx}.property("Position").setValue([{cx}, {cy}]);
        chorusNull{group_idx}.parent = cameraNull;
        chorusNulls.push(chorusNull{group_idx});

"""]

        # Adjusted in-times (handle same-timestamp items)
        adjusted_in_times = []
        for item_idx, item in enumerate(items):
            t = item["lyric"]["time"]
            if item_idx > 0 and items[item_idx - 1]["lyric"]["time"] == t:
                prev = adjusted_in_times[item_idx - 1]
                t = prev + (group_end_time - prev) / 2
            adjusted_in_times.append(t)

        # Create text layers
        cumulative_offset = 0
        for item_idx, item in enumerate(items):
            lyric = item["lyric"]
            fs = heights_info[item_idx]["font_size"]
            text_lines = heights_info[item_idx]["lines"]
            in_time = adjusted_in_times[item_idx]
            out_time = group_end_time
            duration = out_time - in_time
            use_hard = self.layout.is_short_text(lyric["text"], duration)
            animation = self.anim.random()
            easing = animation["easing"]

            if item_idx > 0:
                cumulative_offset += heights_info[item_idx - 1]["height"] + layer_margin

            # Staggered line times (fixed 0.5s delay for chorus)
            line_times = [in_time + li * 0.5 for li in range(len(text_lines))]

            # Isokinetic: one rotation null per chorus item
            null_rot = animation.get("null_rotation")
            chorus_rot_null = f"cRotNull{group_idx}_{item_idx}"
            chorus_parent = f"chorusNull{group_idx}"
            if null_rot and not use_hard:
                jsx.append(f"""
        try {{""")
                jsx.append(self._create_rotation_null(
                    chorus_rot_null, chorus_parent, null_rot,
                    easing, in_time, out_time))
                chorus_text_parent = chorus_rot_null
                jsx.append(f"""
        }} catch(e) {{}}""")
            else:
                chorus_text_parent = chorus_parent

            for li, line_text in enumerate(text_lines):
                vert_off = -fs / 2
                layer_y = cumulative_offset + vert_off + li * fs * 1.2
                layer_x = 0
                line_in = line_times[li]
                escaped = self._escape_text(line_text)
                name = f"chorus{group_idx}_t{item_idx}_{li}"

                jsx.append(f"""
        try {{
            var {name} = comp.layers.addText();
            var textDoc_{name} = {name}.property("Source Text").value;
            textDoc_{name}.text = "{escaped}";
            textDoc_{name}.font = "{c.font}";
            textDoc_{name}.fontSize = {fs};
            textDoc_{name}.fillColor = [1, 1, 1];
            textDoc_{name}.justification = ParagraphJustification.CENTER_JUSTIFY;
            {name}.property("Source Text").setValue(textDoc_{name});
            {name}.name = "{escaped}";
            {name}.startTime = {line_in};
            {name}.outPoint = {out_time + c.null_exit_duration};
            {name}.parent = {chorus_text_parent};
            var rect_{name} = {name}.sourceRectAtTime({line_in}, false);
            var anchorX_{name} = rect_{name}.left + rect_{name}.width / 2;
            var anchorY_{name} = rect_{name}.top + rect_{name}.height / 2;
            {name}.property("Anchor Point").setValue([anchorX_{name}, anchorY_{name}]);
            {name}.property("Position").setValue([{layer_x}, {layer_y}]);
            {name}.motionBlur = true;
            textLayers.push({name});
""")
                # Opacity (in only, null handles exit)
                # Scenes with custom opacity stagger handle their own
                scene_handles_opacity = animation.get("scene_type") in (
                    "perspective_drift", "scrolling_wall", "stacked_cascade",
                    "newton_zoom", "unique_spin")
                chorus_backface = animation.get("backface_cull") and not use_hard
                if scene_handles_opacity and not use_hard:
                    pass  # _render_scene_extras sets opacity
                elif chorus_backface:
                    jsx.append(f"""
            {name}.property("Opacity").setValue(100);
""")
                elif use_hard:
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + 0.033}, 100);
""")
                else:
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + c.animation_duration}, 100);
            applyEaseToKeyframes({name}.property("Opacity"), "{easing}");
""")

                # Short text zoom (skip for scenes that handle own scale)
                scene_handles_scale = animation.get("scene_type") in (
                    "newton_zoom", "unique_spin")
                if (len(line_text.strip()) <= 10 and not scene_handles_scale):
                    zin = random.choice([True, False])
                    zs, ze = (100, 120) if zin else (120, 100)
                    zst = line_in + 6 / c.fps
                    zet = out_time - 6 / c.fps
                    if zet > zst:
                        jsx.append(f"""
            {name}.property("Scale").setValueAtTime({zst}, [{zs}, {zs}]);
            {name}.property("Scale").setValueAtTime({zet}, [{ze}, {ze}]);
            applyEaseToKeyframes({name}.property("Scale"), "easeInOutSine");
""")

                # Effects (entrance only for chorus)
                jsx.append(self._render_effects(
                    name, animation, line_in, out_time, use_hard,
                    layer_x, layer_y, include_out=False))
                jsx.append(self._render_scene_extras(
                    name, animation, line_in, out_time,
                    layer_x, layer_y, li))

                jsx.append(f"""
        }} catch(e) {{}}
""")

        # Null movement + zoom transitions
        jsx.append(f"""
        // Animate null movement and layer zoom for chorus {group_idx}
        try {{
""")
        null_y_offset = 0
        for item_idx in range(len(items)):
            in_time = adjusted_in_times[item_idx]
            if item_idx > 0:
                trans_time = in_time - transition_frames / c.fps
                move = heights_info[item_idx - 1]["height"] + layer_margin
                null_y_offset += move

                prev_idx = item_idx - 1
                for pli in range(len(heights_info[prev_idx]["lines"])):
                    prev = f"chorus{group_idx}_t{prev_idx}_{pli}"
                    jsx.append(f"""
            {prev}.property("Scale").setValueAtTime({trans_time}, [100, 100]);
            {prev}.property("Scale").setValueAtTime({in_time}, [50, 50]);
            applyFastEase({prev}.property("Scale"));
""")

                jsx.append(f"""
            chorusNull{group_idx}.property("Position").setValueAtTime({trans_time}, [{cx}, {cy - (null_y_offset - move)}]);
            chorusNull{group_idx}.property("Position").setValueAtTime({in_time}, [{cx}, {cy - null_y_offset}]);
            applyFastEase(chorusNull{group_idx}.property("Position"));
""")

        # Exit
        exit_y = cy - null_y_offset
        jsx.append(f"""
            chorusNull{group_idx}.property("Position").setValueAtTime({group_end_time}, [{cx}, {exit_y}]);
            chorusNull{group_idx}.property("Position").setValueAtTime({group_end_time + c.null_exit_duration}, [{cx}, {exit_y - c.height}]);
            applyFastEase(chorusNull{group_idx}.property("Position"));
        }} catch(e) {{}}
""")
        return "".join(jsx)

    # ── individual (non-chorus) texts ───────────────────────

    def _individual_section(self, analysis):
        c = self.c
        cx, cy = c.width / 2, c.height / 2
        jsx = ["""
        // =====================
        // INDIVIDUAL TEXT LAYERS (non-chorus)
        // =====================
        var dofCameraLayers = [];
"""]
        dof_candidates = []

        # Build overlap group info: which indices share a group
        overlap_groups = {}  # group_id → {indices, end_time}
        for ld in analysis.lyric_durations:
            og = ld.get("overlap_group")
            if og is not None and ld["index"] not in analysis.chorus_indices:
                if og not in overlap_groups:
                    overlap_groups[og] = {"indices": [], "end_time": ld["end_time"]}
                overlap_groups[og]["indices"].append(ld["index"])

        # Create null objects for overlap groups
        for og_id, og_info in overlap_groups.items():
            end_time = og_info["end_time"]
            first_idx = og_info["indices"][0]
            first_ld = analysis.lyric_durations[first_idx]
            start_time = first_ld["start_time"]
            jsx.append(f"""
        // OVERLAP GROUP {og_id}
        var overlapNull{og_id} = comp.layers.addNull();
        overlapNull{og_id}.name = "overlap_group_{og_id}";
        overlapNull{og_id}.property("Anchor Point").setValue([0, 0]);
        overlapNull{og_id}.property("Position").setValue([0, 0]);
        overlapNull{og_id}.startTime = {start_time};
        overlapNull{og_id}.outPoint = {end_time + c.null_exit_duration};
        overlapNull{og_id}.parent = cameraNull;
        overlapNull{og_id}.property("Opacity").setValueAtTime({end_time - c.fade_duration}, 100);
        overlapNull{og_id}.property("Opacity").setValueAtTime({end_time}, 0);
        applyEaseToKeyframes(overlapNull{og_id}.property("Opacity"), "easeInOutSine");
""")

        # Pre-compute visual line counts per overlap group for vertical stacking
        # Each lyric may produce 1 or 2 visual lines depending on text length
        overlap_slot = {}  # idx → (og_id, start_visual_line, total_visual_lines)
        for og_id, og_info in overlap_groups.items():
            visual_line_counts = []
            for idx in og_info["indices"]:
                ld = analysis.lyric_durations[idx]
                text = ld["lyric"]["text"]
                _, text_lines = self.layout.calculate_font_size(text)
                visual_line_counts.append(len(text_lines))
            total_visual = sum(visual_line_counts)
            cumulative = 0
            for i, idx in enumerate(og_info["indices"]):
                overlap_slot[idx] = (og_id, cumulative, total_visual)
                cumulative += visual_line_counts[i]

        for ld in analysis.lyric_durations:
            idx = ld["index"]
            if idx in analysis.chorus_indices:
                continue

            lyric = ld["lyric"]
            in_time = ld["start_time"]
            out_time = ld["end_time"]
            duration = ld["duration"]
            text = lyric["text"]
            in_overlap = idx in overlap_slot
            fs, text_lines = self.layout.calculate_font_size(text)
            use_hard = self.layout.is_short_text(text, duration) and not in_overlap
            add_mid = self.layout.should_add_mid_effect(duration)
            animation = self.anim.random()
            easing = animation["easing"]
            use_dof = random.random() < c.dof_camera_probability and not in_overlap

            if use_dof:
                dof_candidates.append({
                    "layer_name": f"txt{idx}_0",
                    "in_time": in_time,
                    "out_time": out_time,
                })

            # Line times: all visual lines of the same lyric appear together
            # with a tiny stagger (1 frame) for a subtle cascade effect
            line_times = [in_time + li * (1 / c.fps) for li in range(len(text_lines))]

            for li, line_text in enumerate(text_lines):
                # Y positioning: stack overlapping lyrics vertically
                if in_overlap:
                    og_id, start_vline, total_vlines = overlap_slot[idx]
                    total_h = total_vlines * fs * 1.4
                    start_y = (c.height - total_h) / 2 + fs / 2
                    y_pos = start_y + (start_vline + li) * fs * 1.4
                else:
                    total_h = len(text_lines) * fs * 1.2
                    start_y = (c.height - total_h) / 2 + fs / 2
                    y_pos = start_y + li * fs * 1.2

                line_in = line_times[li]
                line_dur = out_time - line_in
                escaped = self._escape_text(line_text)
                name = f"txt{idx}_{li}"
                dur_frames = line_dur * c.fps
                out_anim = self.anim.get_out_animation(dur_frames)

                # Parent to overlap null if in a group
                if in_overlap:
                    parent_name = f"overlapNull{og_id}"
                else:
                    parent_name = "cameraNull"

                # Isokinetic: create rotation null between parent and text
                null_rot = animation.get("null_rotation")
                rot_null_name = f"rotNull_{name}"
                text_parent = parent_name

                jsx.append(f"""
        try {{""")

                if null_rot and not use_hard:
                    jsx.append(self._create_rotation_null(
                        rot_null_name, parent_name, null_rot,
                        easing, line_in, out_time))
                    text_parent = rot_null_name

                jsx.append(f"""
            var {name} = comp.layers.addText();
            var textDoc_{name} = {name}.property("Source Text").value;
            textDoc_{name}.text = "{escaped}";
            textDoc_{name}.font = "{c.font}";
            textDoc_{name}.fontSize = {fs};
            textDoc_{name}.fillColor = [1, 1, 1];
            textDoc_{name}.justification = ParagraphJustification.CENTER_JUSTIFY;
            {name}.property("Source Text").setValue(textDoc_{name});
            {name}.name = "{escaped}";
            {name}.property("Position").setValue([{cx}, {y_pos}]);
            {name}.startTime = {line_in};
            {name}.outPoint = {out_time};
            {name}.parent = {text_parent};
            {name}.motionBlur = true;
            textLayers.push({name});
""")
                if use_dof or null_rot:
                    jsx.append(f"""
            {name}.threeDLayer = true;
""")

                # Opacity: backface_cull uses static 100% (expression controls visibility)
                has_backface = animation.get("backface_cull") and not use_hard
                scene_handles_opacity = animation.get("scene_type") in (
                    "perspective_drift", "scrolling_wall", "stacked_cascade",
                    "newton_zoom", "unique_spin")
                if scene_handles_opacity and not use_hard:
                    pass  # _render_scene_extras sets opacity
                elif has_backface:
                    jsx.append(f"""
            {name}.property("Opacity").setValue(100);
            {name}.property("Opacity").setValueAtTime({out_time - c.fade_duration}, 100);
            {name}.property("Opacity").setValueAtTime({out_time}, 0);
""")
                elif in_overlap:
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + c.animation_duration}, 100);
""")
                elif use_hard:
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + 0.033}, 100);
            {name}.property("Opacity").setValueAtTime({out_time - 0.033}, 100);
            {name}.property("Opacity").setValueAtTime({out_time}, 0);
""")
                elif out_anim["type"] == "blink":
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + c.animation_duration}, 100);
            var blinkStart = {out_time - 0.3};
            {name}.property("Opacity").setValueAtTime(blinkStart, 100);
            {name}.property("Opacity").setValueAtTime(blinkStart + 0.05, 0);
            {name}.property("Opacity").setValueAtTime(blinkStart + 0.1, 100);
            {name}.property("Opacity").setValueAtTime(blinkStart + 0.15, 0);
            {name}.property("Opacity").setValueAtTime(blinkStart + 0.2, 100);
            {name}.property("Opacity").setValueAtTime(blinkStart + 0.25, 0);
            {name}.property("Opacity").setValueAtTime({out_time}, 0);
            applyEaseToKeyframes({name}.property("Opacity"), "{easing}");
""")
                else:
                    jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({line_in}, 0);
            {name}.property("Opacity").setValueAtTime({line_in + c.animation_duration}, 100);
            {name}.property("Opacity").setValueAtTime({out_time - c.fade_duration}, 100);
            {name}.property("Opacity").setValueAtTime({out_time}, 0);
            applyEaseToKeyframes({name}.property("Opacity"), "{easing}");
""")

                # Scale (in + inverted out) — skip random zoom for backface_cull
                if "scale" in animation and not use_hard:
                    jsx.append(f"""
            {name}.property("Scale").setValueAtTime({line_in}, {animation['scale']['from']});
            {name}.property("Scale").setValueAtTime({line_in + c.animation_duration}, {animation['scale']['to']});
            {name}.property("Scale").setValueAtTime({out_time - c.animation_duration}, {animation['scale']['to']});
            {name}.property("Scale").setValueAtTime({out_time}, {animation['scale']['from']});
            applyEaseToKeyframes({name}.property("Scale"), "{easing}");
""")
                elif (len(line_text.strip()) <= 10 and not use_hard
                      and not animation.get("elastic_pop")
                      and not has_backface
                      and animation.get("scene_type") not in
                          ("newton_zoom",)):
                    zin = random.choice([True, False])
                    zs, ze = (100, 120) if zin else (120, 100)
                    zst = line_in + 6 / c.fps
                    zet = out_time - 6 / c.fps
                    if zet > zst:
                        jsx.append(f"""
            {name}.property("Scale").setValueAtTime({zst}, [{zs}, {zs}]);
            {name}.property("Scale").setValueAtTime({zet}, [{ze}, {ze}]);
            applyEaseToKeyframes({name}.property("Scale"), "easeInOutSine");
""")

                # Position offset (in + inverted out)
                if "position_offset" in animation and not use_hard:
                    fo = animation["position_offset"]["from"]
                    jsx.append(f"""
            {name}.property("Position").setValueAtTime({line_in}, [{cx + fo[0]}, {y_pos + fo[1]}]);
            {name}.property("Position").setValueAtTime({line_in + c.animation_duration}, [{cx}, {y_pos}]);
            {name}.property("Position").setValueAtTime({out_time - c.animation_duration}, [{cx}, {y_pos}]);
            {name}.property("Position").setValueAtTime({out_time}, [{cx + fo[0]}, {y_pos + fo[1]}]);
            applyEaseToKeyframes({name}.property("Position"), "{easing}");
""")

                # Elastic pop
                if animation.get("elastic_pop") and not use_hard:
                    jsx.append(f"""
            {name}.property("Scale").setValueAtTime({line_in}, [0, 0]);
            {name}.property("Scale").setValueAtTime({line_in + c.animation_duration}, [120, 120]);
            {name}.property("Scale").setValueAtTime({line_in + c.animation_duration + 0.1}, [100, 100]);
            {name}.property("Scale").setValueAtTime({out_time - c.animation_duration}, [100, 100]);
            {name}.property("Scale").setValueAtTime({out_time}, [0, 0]);
            applyEaseToKeyframes({name}.property("Scale"), "easeInOutElastic");
""")

                # Mid-duration effect (skip for backface_cull and newton — they handle own scale)
                scene_owns_scale = animation.get("scene_type") in ("newton_zoom", "unique_spin")
                if add_mid and not use_hard and not has_backface and not scene_owns_scale:
                    mid = line_in + line_dur / 2
                    choice = random.choice(["zoom", "position"])
                    tw = self.layout.calculate_text_width(line_text, fs)
                    fits = tw * 1.35 < c.width * 0.95
                    mt = 2 / c.fps

                    if choice == "zoom" and fits:
                        za = random.uniform(c.mid_zoom_range[0], c.mid_zoom_range[1])
                        jsx.append(f"""
            {name}.property("Scale").setValueAtTime({mid - mt}, [100, 100]);
            {name}.property("Scale").setValueAtTime({mid}, [{za}, {za}]);
            {name}.property("Scale").setValueAtTime({mid + mt}, [100, 100]);
""")
                    elif choice == "zoom" and not fits:
                        za = random.uniform(70, 85)
                        jsx.append(f"""
            {name}.property("Scale").setValueAtTime({mid - mt}, [100, 100]);
            {name}.property("Scale").setValueAtTime({mid}, [{za}, {za}]);
            {name}.property("Scale").setValueAtTime({mid + mt}, [100, 100]);
""")
                    else:
                        mo = min(c.mid_position_range, (c.width - tw) / 2 - 50)
                        ox = random.uniform(-mo, mo)
                        oy = random.uniform(-50, 50)
                        jsx.append(f"""
            {name}.property("Position").setValueAtTime({mid - mt}, [{cx}, {y_pos}]);
            {name}.property("Position").setValueAtTime({mid}, [{cx + ox}, {y_pos + oy}]);
            {name}.property("Position").setValueAtTime({mid + mt}, [{cx}, {y_pos}]);
""")

                # Effects (with inverted out for individual)
                jsx.append(self._render_effects(
                    name, animation, line_in, out_time, use_hard,
                    cx, y_pos, include_out=True))
                jsx.append(self._render_scene_extras(
                    name, animation, line_in, out_time,
                    cx, y_pos, li))

                jsx.append(f"""
        }} catch(e) {{}}
""")

        if dof_candidates:
            jsx.append(self._dof_cameras(dof_candidates))

        return "".join(jsx)

    # ── isokinetic rotation null ────────────────────────────

    # Velocity-based elastic overshoot expression (from Isokinetic Scene_01)
    ELASTIC_EXPR = ("'amp = 0.1;\\n'"
        "+ 'freq = 2;\\n'"
        "+ 'decay = 3;\\n'"
        "+ 'n = 0;\\n'"
        "+ 'if (numKeys > 0){{\\n'"
        "+ 'n = nearestKey(time).index;\\n'"
        "+ 'if (key(n).time > time){{ n--; }}\\n'"
        "+ '}}\\n'"
        "+ 'if (n == 0){{ t = 0; }} else {{ t = time - key(n).time; }}\\n'"
        "+ 'if (n > 0){{\\n'"
        "+ 'v = velocityAtTime(key(n).time - thisComp.frameDuration/10);\\n'"
        "+ 'value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);\\n'"
        "+ '}} else {{\\n'"
        "+ 'value;\\n'"
        "+ '}}'")

    def _create_rotation_null(self, null_name, parent_name,
                              null_rot, easing, in_time, out_time):
        """Generate JSX for a 3D rotation null (Isokinetic parent-child)."""
        c = self.c
        anim_dur = null_rot.get("anim_duration_override", c.animation_duration)
        cx, cy = c.width / 2, c.height / 2
        # Anchor override (Scene_08: cube center with Z depth)
        anchor = null_rot.get("anchor_override", [cx, cy, 0])
        ax, ay, az = anchor[0], anchor[1], anchor[2]
        jsx = []
        jsx.append(f"""
            var {null_name} = comp.layers.addNull();
            {null_name}.name = "rot_{null_name}";
            {null_name}.threeDLayer = true;
            {null_name}.startTime = {in_time - 0.1};
            {null_name}.outPoint = {out_time + 0.5};
            {null_name}.property("Anchor Point").setValue([{ax}, {ay}, {az}]);
            {null_name}.property("Position").setValue([{cx}, {cy}, 0]);
            {null_name}.parent = {parent_name};""")

        # ── Position drift (Scene_02, Scene_12: animated position on null) ──
        if "position_drift" in null_rot:
            pfr = null_rot["position_drift"]["from"]
            pto = null_rot["position_drift"]["to"]
            jsx.append(f"""
            {null_name}.property("Position").setValueAtTime({in_time}, [{pfr[0]}, {pfr[1]}, {pfr[2]}]);
            {null_name}.property("Position").setValueAtTime({in_time + anim_dur}, [{pto[0]}, {pto[1]}, {pto[2]}]);
            applyEaseToKeyframes({null_name}.property("Position"), "{easing}");""")

        # ── Rotation X keyframes ──
        if "rotationX" in null_rot:
            rf = null_rot["rotationX"]["from"]
            rt = null_rot["rotationX"]["to"]
            if rf != rt:  # animated
                jsx.append(f"""
            {null_name}.property("X Rotation").setValueAtTime({in_time}, {rf});
            {null_name}.property("X Rotation").setValueAtTime({in_time + anim_dur}, {rt});
            applyEaseToKeyframes({null_name}.property("X Rotation"), "{easing}");""")
                if null_rot.get("elastic"):
                    jsx.append(f"""
            {null_name}.property("X Rotation").expression = {self.ELASTIC_EXPR};""")
            else:  # static tilt
                jsx.append(f"""
            {null_name}.property("X Rotation").setValue({rf});""")

        # ── Rotation Y keyframes ──
        if "rotationY" in null_rot:
            rf = null_rot["rotationY"]["from"]
            rt = null_rot["rotationY"]["to"]
            if rf != rt:
                jsx.append(f"""
            {null_name}.property("Y Rotation").setValueAtTime({in_time}, {rf});
            {null_name}.property("Y Rotation").setValueAtTime({in_time + anim_dur}, {rt});
            applyEaseToKeyframes({null_name}.property("Y Rotation"), "{easing}");""")
                if null_rot.get("elastic") and "rotationX" not in null_rot:
                    jsx.append(f"""
            {null_name}.property("Y Rotation").expression = {self.ELASTIC_EXPR};""")
            else:
                jsx.append(f"""
            {null_name}.property("Y Rotation").setValue({rf});""")

        # ── Rotation Z keyframes ──
        if "rotationZ" in null_rot:
            rf = null_rot["rotationZ"]["from"]
            rt = null_rot["rotationZ"]["to"]
            if rf != rt:
                jsx.append(f"""
            {null_name}.property("Rotation").setValueAtTime({in_time}, {rf});
            {null_name}.property("Rotation").setValueAtTime({in_time + anim_dur}, {rt});
            applyEaseToKeyframes({null_name}.property("Rotation"), "{easing}");""")
            else:
                jsx.append(f"""
            {null_name}.property("Rotation").setValue({rf});""")

        # ── Continuous rotation (Scene_08: slow Y spin over full duration) ──
        if "continuous_rotation" in null_rot:
            cr = null_rot["continuous_rotation"]
            axis_map = {"X": "X Rotation", "Y": "Y Rotation", "Z": "Rotation"}
            axis_prop = axis_map.get(cr["axis"], "Y Rotation")
            cr_dur = out_time - in_time  # full lyric duration
            jsx.append(f"""
            {null_name}.property("{axis_prop}").setValueAtTime({in_time}, {cr["from"]});
            {null_name}.property("{axis_prop}").setValueAtTime({in_time + cr_dur}, {cr["to"]});""")

        # ── Static orientation (Scene_15: tilted perspective) ──
        if "orientation_static" in null_rot:
            ox, oy, oz = null_rot["orientation_static"]
            jsx.append(f"""
            {null_name}.property("Orientation").setValue([{ox}, {oy}, {oz}]);""")

        # ── Orientation drift (Scene_02: animated orientation) ──
        elif "orientation_drift" in null_rot:
            ofr = null_rot["orientation_drift"]["from"]
            oto = null_rot["orientation_drift"]["to"]
            jsx.append(f"""
            {null_name}.property("Orientation").setValueAtTime({in_time}, [{ofr[0]}, {ofr[1]}, {ofr[2]}]);
            {null_name}.property("Orientation").setValueAtTime({in_time + anim_dur}, [{oto[0]}, {oto[1]}, {oto[2]}]);
            applyEaseToKeyframes({null_name}.property("Orientation"), "{easing}");""")

        # ── Wiggle on orientation (skip if static/drift already set) ──
        elif null_rot.get("wiggle"):
            jsx.append(f"""
            {null_name}.property("Orientation").expression = 'wiggle(0.5, 5)';""")

        return "".join(jsx)

    # ── shared animation effects ────────────────────────────

    def _render_effects(self, name, animation, in_time, out_time,
                        use_hard, pos_x, pos_y, include_out=False):
        if use_hard:
            return ""
        c = self.c
        jsx = []

        # Backface culling (Isokinetic: hide text when facing away)
        if animation.get("backface_cull"):
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Opacity").expression = 'toCompVec([0, 0, 1])[2] > 0 ? value : 0';""")

        if "blur" in animation:
            bf, bt = animation["blur"]["from"], animation["blur"]["to"]
            jsx.append(f"""
            var blur_{name} = {name}.property("Effects").addProperty("ADBE Gaussian Blur 2");
            blur_{name}.property("Blurriness").setValueAtTime({in_time}, {bf});
            blur_{name}.property("Blurriness").setValueAtTime({in_time + c.animation_duration}, {bt});""")
            if include_out:
                jsx.append(f"""
            blur_{name}.property("Blurriness").setValueAtTime({out_time - c.animation_duration}, {bt});
            blur_{name}.property("Blurriness").setValueAtTime({out_time}, {bf});""")

        if "rotationX" in animation:
            rf, rt = animation["rotationX"]["from"], animation["rotationX"]["to"]
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("X Rotation").setValueAtTime({in_time}, {rf});
            {name}.property("X Rotation").setValueAtTime({in_time + c.animation_duration}, {rt});""")
            if include_out:
                jsx.append(f"""
            {name}.property("X Rotation").setValueAtTime({out_time - c.animation_duration}, {rt});
            {name}.property("X Rotation").setValueAtTime({out_time}, {rf});""")

        if "rotationY" in animation:
            rf, rt = animation["rotationY"]["from"], animation["rotationY"]["to"]
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Y Rotation").setValueAtTime({in_time}, {rf});
            {name}.property("Y Rotation").setValueAtTime({in_time + c.animation_duration}, {rt});""")
            if include_out:
                jsx.append(f"""
            {name}.property("Y Rotation").setValueAtTime({out_time - c.animation_duration}, {rt});
            {name}.property("Y Rotation").setValueAtTime({out_time}, {rf});""")

        if animation.get("text_animator"):
            jsx.append(f"""
            var animator_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var selector_{name} = animator_{name}.property("Selectors").addProperty("ADBE Text Selector");
            selector_{name}.property("Start").setValueAtTime({in_time}, 0);
            selector_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            animator_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        if animation.get("wave_animator"):
            jsx.append(f"""
            var waveAnim_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var waveSel_{name} = waveAnim_{name}.property("Selectors").addProperty("ADBE Text Selector");
            waveSel_{name}.property("Offset").setValueAtTime({in_time}, -100);
            waveSel_{name}.property("Offset").setValueAtTime({in_time + c.animation_duration}, 0);
            waveAnim_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, 50, 0]);""")

        if animation.get("glitch"):
            jsx.append(f"""
            for (var gi = 0; gi < 6; gi++) {{
                var gTime = {in_time} + (gi * {c.animation_duration} / 6);
                {name}.property("Position").setValueAtTime(gTime, [{pos_x} + (Math.random()-0.5)*40, {pos_y} + (Math.random()-0.5)*20]);
            }}
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}]);""")

        if "shadow" in animation:
            sf, st = animation["shadow"]["from"], animation["shadow"]["to"]
            jsx.append(f"""
            var shadow_{name} = {name}.property("Effects").addProperty("ADBE Drop Shadow");
            shadow_{name}.property("Distance").setValueAtTime({in_time}, {sf});
            shadow_{name}.property("Distance").setValueAtTime({in_time + c.animation_duration}, {st});""")
            if include_out:
                jsx.append(f"""
            shadow_{name}.property("Distance").setValueAtTime({out_time - c.animation_duration}, {st});
            shadow_{name}.property("Distance").setValueAtTime({out_time}, {sf});""")
            jsx.append(f"""
            shadow_{name}.property("Softness").setValue(15);""")

        # ── Kinetic typography text animators ──────────────────

        if animation.get("char_cascade"):
            # Characters cascade in one by one with position + opacity
            jsx.append(f"""
            var casc_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var cascSel_{name} = casc_{name}.property("Selectors").addProperty("ADBE Text Selector");
            cascSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            cascSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            cascSel_{name}.property("Advanced").property("Shape").setValue(5);
            casc_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            casc_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, -80, 0]);""")

        if animation.get("char_rotate_in"):
            # Each character rotates in from a random angle
            jsx.append(f"""
            var crot_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var crotSel_{name} = crot_{name}.property("Selectors").addProperty("ADBE Text Selector");
            crotSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            crotSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            crotSel_{name}.property("Advanced").property("Shape").setValue(5);
            crot_{name}.property("Properties").addProperty("ADBE Text Rotation").setValue(90);
            crot_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            crot_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([0, 0]);""")

        if animation.get("char_scale_stagger"):
            # Characters scale up one by one with slight offset
            jsx.append(f"""
            var cscl_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var csclSel_{name} = cscl_{name}.property("Selectors").addProperty("ADBE Text Selector");
            csclSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            csclSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            csclSel_{name}.property("Advanced").property("Shape").setValue(2);
            cscl_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([0, 0]);
            cscl_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        if animation.get("char_blur_sweep"):
            # Blur sweeps across characters left to right
            jsx.append(f"""
            var cbsw_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var cbswSel_{name} = cbsw_{name}.property("Selectors").addProperty("ADBE Text Selector");
            cbswSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            cbswSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            cbswSel_{name}.property("Advanced").property("Shape").setValue(5);
            cbsw_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            cbsw_{name}.property("Properties").addProperty("ADBE Text Blur").setValue(20);""")

        if animation.get("char_spiral"):
            # Characters spiral in with rotation + position
            jsx.append(f"""
            var cspi_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var cspiSel_{name} = cspi_{name}.property("Selectors").addProperty("ADBE Text Selector");
            cspiSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            cspiSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration * 1.5}, 100);
            cspiSel_{name}.property("Advanced").property("Shape").setValue(5);
            cspi_{name}.property("Properties").addProperty("ADBE Text Rotation").setValue(360);
            cspi_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([0, 0]);
            cspi_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            cspi_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, -100, 0]);""")

        if animation.get("char_bounce_up"):
            # Characters bounce up from below
            jsx.append(f"""
            var cbup_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var cbupSel_{name} = cbup_{name}.property("Selectors").addProperty("ADBE Text Selector");
            cbupSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            cbupSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            cbupSel_{name}.property("Advanced").property("Shape").setValue(5);
            cbup_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, 120, 0]);
            cbup_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([120, 120]);
            cbup_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        if animation.get("char_3d_flip"):
            # Characters flip in on Y axis one by one (3D)
            jsx.append(f"""
            {name}.threeDLayer = true;
            var c3d_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var c3dSel_{name} = c3d_{name}.property("Selectors").addProperty("ADBE Text Selector");
            c3dSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            c3dSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            c3dSel_{name}.property("Advanced").property("Shape").setValue(5);
            c3d_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            c3d_{name}.property("Properties").addProperty("ADBE Text Rotation Y").setValue(90);
            c3d_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([20, 0, 0]);""")

        if animation.get("tracking_expand"):
            # Text tracking expands from tight to normal
            jsx.append(f"""
            var trk_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var trkSel_{name} = trk_{name}.property("Selectors").addProperty("ADBE Text Selector");
            trkSel_{name}.property("Start").setValue(0);
            trkSel_{name}.property("End").setValue(100);
            trk_{name}.property("Properties").addProperty("ADBE Text Tracking Amount");
            trk_{name}.property("Properties").property("ADBE Text Tracking Amount").setValueAtTime({in_time}, -50);
            trk_{name}.property("Properties").property("ADBE Text Tracking Amount").setValueAtTime({in_time + c.animation_duration}, 0);""")

        if animation.get("tracking_compress"):
            # Text tracking compresses from wide to normal (reverse kinetic)
            jsx.append(f"""
            var trkc_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var trkcSel_{name} = trkc_{name}.property("Selectors").addProperty("ADBE Text Selector");
            trkcSel_{name}.property("Start").setValue(0);
            trkcSel_{name}.property("End").setValue(100);
            trkc_{name}.property("Properties").addProperty("ADBE Text Tracking Amount");
            trkc_{name}.property("Properties").property("ADBE Text Tracking Amount").setValueAtTime({in_time}, 80);
            trkc_{name}.property("Properties").property("ADBE Text Tracking Amount").setValueAtTime({in_time + c.animation_duration}, 0);""")

        if animation.get("line_wipe"):
            # Line mask wipe reveal from left
            jsx.append(f"""
            var lwipe_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var lwipeSel_{name} = lwipe_{name}.property("Selectors").addProperty("ADBE Text Selector");
            lwipeSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            lwipeSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            lwipeSel_{name}.property("Advanced").property("Shape").setValue(3);
            lwipeSel_{name}.property("Advanced").property("Smoothness").setValue(30);
            lwipe_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        # ── 3D pop-out effects ────────────────────────────────

        if animation.get("pop3d_toward"):
            # 3D pop: text flies toward camera from deep Z
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, 800]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");""")

        if animation.get("pop3d_away"):
            # 3D pop: text slams from in front of camera back to position
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, -600]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            applyEaseToKeyframes({name}.property("Position"), "easeOutBack");""")

        if animation.get("pop3d_spin_x"):
            # Full 360° X-axis spin flying toward camera
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("X Rotation").setValueAtTime({in_time}, -360);
            {name}.property("X Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, 500]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            applyEaseToKeyframes({name}.property("X Rotation"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");""")

        if animation.get("pop3d_spin_y"):
            # Full 360° Y-axis spin flying toward camera
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Y Rotation").setValueAtTime({in_time}, 360);
            {name}.property("Y Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, 400]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            applyEaseToKeyframes({name}.property("Y Rotation"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");""")

        if animation.get("pop3d_tumble"):
            # Multi-axis tumble: X + Y + Z rotation simultaneously
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("X Rotation").setValueAtTime({in_time}, 180);
            {name}.property("X Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            {name}.property("Y Rotation").setValueAtTime({in_time}, -90);
            {name}.property("Y Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            {name}.property("Rotation").setValueAtTime({in_time}, 45);
            {name}.property("Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, 600]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            applyEaseToKeyframes({name}.property("X Rotation"), "easeOutBack");""")

        if animation.get("pop3d_slam"):
            # Text slams down from above with 3D perspective + bounce scale
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y - 400}, 300]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration * 0.7}, [{pos_x}, {pos_y + 10}, 0]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            {name}.property("X Rotation").setValueAtTime({in_time}, -30);
            {name}.property("X Rotation").setValueAtTime({in_time + c.animation_duration * 0.7}, 5);
            {name}.property("X Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            applyEaseToKeyframes({name}.property("Position"), "easeOutBounce");""")

        if animation.get("pop3d_shatter_in"):
            # Characters fly in from scattered 3D positions
            jsx.append(f"""
            {name}.threeDLayer = true;
            var shtr_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var shtrSel_{name} = shtr_{name}.property("Selectors").addProperty("ADBE Text Selector");
            shtrSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            shtrSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration * 1.2}, 100);
            shtrSel_{name}.property("Advanced").property("Shape").setValue(5);
            shtrSel_{name}.property("Advanced").property("Randomize Order").setValue(1);
            shtr_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, 0, -400]);
            shtr_{name}.property("Properties").addProperty("ADBE Text Rotation").setValue(180);
            shtr_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([0, 0]);
            shtr_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        if animation.get("pop3d_wave_z"):
            # Characters wave along Z axis, creating a ripple depth effect
            jsx.append(f"""
            {name}.threeDLayer = true;
            var wz_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var wzSel_{name} = wz_{name}.property("Selectors").addProperty("ADBE Text Selector");
            wzSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            wzSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration}, 100);
            wzSel_{name}.property("Advanced").property("Shape").setValue(5);
            wz_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([0, 0, -300]);
            wz_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);
            wz_{name}.property("Properties").addProperty("ADBE Text Scale 3D").setValue([50, 50]);""")

        if animation.get("pop3d_card_fan"):
            # Characters fan out like a deck of cards in 3D space
            jsx.append(f"""
            {name}.threeDLayer = true;
            var cfan_{name} = {name}.property("Text").property("Animators").addProperty("ADBE Text Animator");
            var cfanSel_{name} = cfan_{name}.property("Selectors").addProperty("ADBE Text Selector");
            cfanSel_{name}.property("Start").setValueAtTime({in_time}, 0);
            cfanSel_{name}.property("Start").setValueAtTime({in_time + c.animation_duration * 1.2}, 100);
            cfanSel_{name}.property("Advanced").property("Shape").setValue(2);
            cfan_{name}.property("Properties").addProperty("ADBE Text Rotation Y").setValue(70);
            cfan_{name}.property("Properties").addProperty("ADBE Text Position 3D").setValue([30, 0, -200]);
            cfan_{name}.property("Properties").addProperty("ADBE Text Opacity").setValue(0);""")

        if animation.get("pop3d_zoom_rotate"):
            # Extreme zoom from distance + Z rotation
            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, 2000]);
            {name}.property("Position").setValueAtTime({in_time + c.animation_duration}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Rotation").setValueAtTime({in_time}, 720);
            {name}.property("Rotation").setValueAtTime({in_time + c.animation_duration}, 0);
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Rotation"), "easeOutExpo");""")

        return "".join(jsx)

    # ── isokinetic scene-specific extras ─────────────────────

    def _render_scene_extras(self, name, animation, in_time, out_time,
                             pos_x, pos_y, line_index=0):
        scene = animation.get("scene_type")
        if not scene:
            return ""
        c = self.c
        cx = c.width / 2
        jsx = []

        # ── sourceRect anchor centering expression (reused across scenes) ──
        SRC_CENTER = ("'var r = thisLayer.sourceRectAtTime(time, false); "
                      "[r.left + r.width/2, r.top + r.height/2, 0]'")
        SRC_LEFT = ("'var r = thisLayer.sourceRectAtTime(time, false); "
                    "[r.left, r.top + r.height/2, 0]'")

        if scene == "cube_flip":
            # ── Scene_01: 3D Cube Flip ──
            # Rotation null handles the main flip (rotX 180→0 or rotY 180→0).
            # Text layers form cube faces with their own per-line rotations.
            # Line 0 = TOP face (Title_01): no own rotation, just anchor centering.
            # Line 1 = SIDE face (Title_02): rotY -180→-90 + Z rot=-90° + elastic.
            #   Position offset from Title_01 bounds (+sizeX/2+20).
            # Line 2+ = BOTTOM face (Title_03): rotX 180→90 + elastic.
            #   Position offset from Title_01 bounds.
            anim_dur = animation.get("null_rotation", {}).get(
                "anim_duration_override", c.animation_duration)
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")
            if line_index == 1:
                # Side face: rotY KF -180→-90 + Z rotation=-90° static + elastic
                jsx.append(f"""
            {name}.property("Y Rotation").setValueAtTime({in_time}, -180);
            {name}.property("Y Rotation").setValueAtTime({in_time + anim_dur}, -90);
            {name}.property("Rotation").setValue(-90);
            {name}.property("Y Rotation").expression = {self.ELASTIC_EXPR};
            applyEaseToKeyframes({name}.property("Y Rotation"), "easeOutExpo");""")
                # Position expression: offset from first title bounds
                jsx.append(f"""
            {name}.property("Position").expression = 'var idx = thisLayer.index; '
                + 'var prev = thisComp.layer(idx + 1); '
                + 'var r = prev.sourceRectAtTime(time, false); '
                + '[r.width/2 + 20, 0, 0]';""")
            elif line_index >= 2:
                # Bottom face: rotX KF 180→90 + elastic
                jsx.append(f"""
            {name}.property("X Rotation").setValueAtTime({in_time}, 180);
            {name}.property("X Rotation").setValueAtTime({in_time + anim_dur}, 90);
            {name}.property("X Rotation").expression = {self.ELASTIC_EXPR};
            applyEaseToKeyframes({name}.property("X Rotation"), "easeOutExpo");""")
                # Position expression: offset below first title
                jsx.append(f"""
            {name}.property("Position").expression = 'var idx = thisLayer.index; '
                + 'var first = thisComp.layer(idx + {line_index}); '
                + 'var r = first.sourceRectAtTime(time, false); '
                + '[0, r.height/2, 0]';""")

        elif scene == "perspective_drift":
            # ── Scene_02: 3D Perspective Drift ──
            # Null handles orientation drift (0,0,0)→(25.97,326.81,352.19) and
            # position drift (960,664)→(960,540) over 2.069s.
            # Text: staggered opacity fade (0.067s per line), even lines
            # get rotX=-90° creating the folded book look. NO backface cull.
            # Scale expression from original Control slider.
            stagger = line_index * 0.067
            jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({in_time + stagger}, 0);
            {name}.property("Opacity").setValueAtTime({in_time + stagger + 0.3}, 100);
            applyEaseToKeyframes({name}.property("Opacity"), "easeOutSine");
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")
            if line_index % 2 == 1:
                # Even layers (0-indexed odd = AE even) get perpendicular fold
                jsx.append(f"""
            {name}.property("X Rotation").setValue(-90);""")

        elif scene == "spinning_cube":
            # ── Scene_08: Spinning 3D Cube ──
            # Null: anchor=(959.73,536.39,190), rotX=25° static,
            # rotY continuous spin 45→1125° over full duration, wiggle orientation.
            # 4 text faces at exact positions/rotations from original:
            #   Front (line 0): pos=(960,536,0), no rotation
            #   Right (line 1): pos=(1149,536,190), rotY=-90°
            #   Back  (line 2): pos=(960,536,380), orient=(0,270,0)
            #   Left  (line 3): pos=(770,536,190), rotY=90°
            face_positions = [
                [960, 536, 0],       # front face
                [1149, 536, 190],    # right face
                [960, 536, 380],     # back face
                [770, 536, 190],     # left face
            ]
            face_rots_y = [0, -90, 0, 90]
            face_orients = [None, None, [0, 270, 0], None]
            fi = line_index % 4
            fp = face_positions[fi]
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_CENTER};
            {name}.property("Position").setValue([{fp[0]}, {fp[1]}, {fp[2]}]);""")
            if face_rots_y[fi] != 0:
                jsx.append(f"""
            {name}.property("Y Rotation").setValue({face_rots_y[fi]});""")
            if face_orients[fi]:
                o = face_orients[fi]
                jsx.append(f"""
            {name}.property("Orientation").setValue([{o[0]}, {o[1]}, {o[2]}]);""")

        elif scene == "cc_cylinder":
            # ── Scene_10: CC Cylinder with Echo ──
            # From original: Tint + CC Cylinder (Radius=100, RotX=-62, RotY=-102,
            # Render=Full) + Echo (25 echoes, -0.168s, Composite In Front).
            # Echo creates the repeating text that fills the cylinder surface.
            jsx.append(f"""
            {name}.property("Anchor Point").setValue([{c.width / 2}, 95]);
            var tint_{name} = {name}.property("Effects").addProperty("ADBE Tint");
            tint_{name}.property("Map Black To").setValue([0, 0, 0]);
            tint_{name}.property("Map White To").setValue([1, 1, 1]);
            tint_{name}.property("Amount to Tint").setValue(100);
            var cc_{name} = {name}.property("Effects").addProperty("CC Cylinder");
            cc_{name}.property("Radius (%)").setValue(100);
            cc_{name}.property("Rotation").property("Rotation X").setValueAtTime({in_time}, -62);
            cc_{name}.property("Rotation").property("Rotation X").setValueAtTime({out_time}, -62);
            cc_{name}.property("Rotation").property("Rotation Y").setValueAtTime({in_time}, -102);
            cc_{name}.property("Rotation").property("Rotation Y").setValueAtTime({out_time}, -102);
            cc_{name}.property("Render").setValue(4);
            var echo_{name} = {name}.property("Effects").addProperty("ADBE Echo");
            echo_{name}.property("Echo Time (seconds)").setValue(-0.168);
            echo_{name}.property("Number Of Echoes").setValue(25);
            echo_{name}.property("Starting Intensity").setValue(1);
            echo_{name}.property("Decay").setValue(1);
            echo_{name}.property("Echo Operator").setValue(4);""")

        elif scene == "chained_fold":
            # ── Scene_12: Zigzag Accordion Fold ──
            # Null handles: rotY 0→-45, orient (0,0,0)→(30,0,0),
            # position (960,540,967)→(948,134,499) over 1.702s.
            # Text layers: left-edge anchor (hinge point), each line
            # folds at alternating ±90° rotY. Line 0 = root (no own fold).
            # Original: x1(+90), x2(-90), x3(+90), x4(-90) chained parents.
            anim_dur = animation.get("null_rotation", {}).get(
                "anim_duration_override", c.animation_duration)
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_LEFT};""")
            if line_index > 0:
                fold_dir = 90 if line_index % 2 == 1 else -90
                jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Y Rotation").setValueAtTime({in_time}, 0);
            {name}.property("Y Rotation").setValueAtTime({in_time + anim_dur}, {fold_dir});
            applyEaseToKeyframes({name}.property("Y Rotation"), "easeOutExpo");""")

        elif scene == "scrolling_wall":
            # ── Scene_15: Scrolling Text Wall ──
            # Null: static orientation=[19.98,40.81,8.19] (tilted perspective).
            # Text: horizontal position crawl over full duration (exact speeds
            # from original: 574, 123, 416, 654, 571, 480 px).
            # Staggered opacity 0.067s per line. Even lines rotX=-90° (3D fold).
            # Layers 4-6 in original at Z=-115.15.
            crawl_speeds = [574, 123, 416, 654, 571, 480]
            crawl = crawl_speeds[line_index % len(crawl_speeds)]
            z_depth = -115.15 if line_index >= 3 else 0
            jsx.append(f"""
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, {z_depth}]);
            {name}.property("Position").setValueAtTime({out_time}, [{pos_x + crawl}, {pos_y}, {z_depth}]);
            applyEaseToKeyframes({name}.property("Position"), "easeInOutSine");
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")
            stagger = line_index * 0.067
            jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({in_time + stagger}, 0);
            {name}.property("Opacity").setValueAtTime({in_time + stagger + 0.3}, 100);
            applyEaseToKeyframes({name}.property("Opacity"), "easeOutSine");""")
            if line_index % 2 == 1:
                jsx.append(f"""
            {name}.property("X Rotation").setValue(-90);""")

        elif scene == "stacked_cascade":
            # ── Stacked Cascade: 4x Title_01 cascading chain ──
            # Root null has continuous X rotation (0→720°), Y=15°, Z=15°,
            # anchor=(960,225,225). All text layers get Fill (white).
            # Layer 0,1,2 parent to null. Layer 3 re-parents to layer 2
            # (matching original chain: 5→3,4 and 3→2).
            # Staggered opacity for visual separation.
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")
            # Fill effect (white) — matches original composition
            jsx.append(f"""
            var fill_{name} = {name}.property("Effects").addProperty("ADBE Fill");
            fill_{name}.property("Color").setValue([1, 1, 1]);""")
            # Staggered opacity entrance
            stagger = line_index * 0.05
            jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({in_time + stagger}, 0);
            {name}.property("Opacity").setValueAtTime({in_time + stagger + 0.2}, 100);
            applyEaseToKeyframes({name}.property("Opacity"), "easeOutSine");""")
            # Re-parent line 3 to line 2's layer (sub-chain)
            if line_index == 3:
                jsx.append(f"""
            {name}.parent = comp.layer({name}.index + 1);""")

        elif scene == "tiled_wall":
            # ── Kinetic Typography 14: Tiled Text Wall ──
            # Null handles Y=-40°, Z=10° tilt. Each text layer gets
            # Motion Tile (Output Width=600) for horizontal word repetition.
            # Position expression auto-stacks copies vertically with Z offset.
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")
            # Motion Tile effect — horizontal text tiling
            jsx.append(f"""
            var mt_{name} = {name}.property("Effects").addProperty("ADBE Tile");
            mt_{name}.property("Tile Center").expression = 'var r = thisLayer.sourceRectAtTime(time, false); [r.left + r.width/2, r.top + r.height/2]';
            mt_{name}.property("Tile Width").setValue(100);
            mt_{name}.property("Tile Height").setValue(100);
            mt_{name}.property("Output Width").setValue(600);
            mt_{name}.property("Output Height").setValue(100);
            mt_{name}.property("Horizontal Phase Shift").setValue(1);""")
            # Position expression: auto-stack vertically from parent index
            jsx.append(f"""
            {name}.property("Position").expression = 'var idx = index - parent.index; [width/2, height/2 + height*idx, idx]';""")

        elif scene == "newton_zoom":
            # ── NEWTON — Rhythmic Typography ──
            # Mega-zoom entrance (3116%→100%), per-character scramble
            # (Animator 1: Character Value), per-character scale/tracking
            # (Animator 2), fill color flash, and stepped scale exit.
            variant = animation.get("newton_variant", "stepped")
            dur = out_time - in_time
            zoom_in_dur = 0.2  # bezier zoom-in time

            # ── Transform: Scale keyframes ──
            jsx.append(f"""
            {name}.property("Anchor Point").expression = {SRC_CENTER};
            {name}.property("Opacity").setValue(100);""")

            if variant == "short":
                # 4 KF: zoom-in, hold, zoom-out
                hold_end = in_time + dur * 0.75
                jsx.append(f"""
            {name}.property("Scale").setValueAtTime({in_time}, [3116, 3116]);
            {name}.property("Scale").setValueAtTime({in_time + zoom_in_dur}, [100, 100]);
            {name}.property("Scale").setValueAtTime({hold_end}, [100, 100]);
            {name}.property("Scale").setValueAtTime({out_time}, [20, 20]);
            applyEaseToKeyframes({name}.property("Scale"), "easeOutExpo");""")

            elif variant == "stepped":
                # Zoom-in (bezier), hold, then rhythmic stepped shrink (hold interp)
                hold_start = in_time + zoom_in_dur
                # Steps begin at ~55% of duration, end at out_time
                step_start = in_time + dur * 0.55
                step_dur = out_time - step_start
                steps = [95, 90, 85, 80, 75, 60, 35]
                jsx.append(f"""
            {name}.property("Scale").setValueAtTime({in_time}, [3116, 3116]);
            {name}.property("Scale").setValueAtTime({hold_start}, [100, 100]);
            {name}.property("Scale").setValueAtTime({step_start}, [100, 100]);""")
                for si, sv in enumerate(steps):
                    st = step_start + step_dur * (si + 1) / (len(steps) + 1)
                    jsx.append(f"""
            {name}.property("Scale").setValueAtTime({st}, [{sv}, {sv}]);""")
                # First 2 KFs get bezier ease, rest get hold
                jsx.append(f"""
            applyEaseToKeyframes({name}.property("Scale"), "easeOutExpo");""")
                # Convert step KFs to hold interpolation
                jsx.append(f"""
            for (var ki = 3; ki <= {name}.property("Scale").numKeys; ki++) {{
                {name}.property("Scale").setInterpolationTypeAtKey(ki, KeyframeInterpolationType.HOLD);
            }}""")

            else:  # simple
                jsx.append(f"""
            {name}.property("Scale").setValueAtTime({in_time}, [3116, 3116]);
            {name}.property("Scale").setValueAtTime({in_time + zoom_in_dur}, [100, 100]);
            applyEaseToKeyframes({name}.property("Scale"), "easeOutExpo");""")

            # ── Fill effect: white/black flash ──
            flash_t = in_time + dur * 0.65
            jsx.append(f"""
            var fill_{name} = {name}.property("Effects").addProperty("ADBE Fill");
            fill_{name}.property("Color").setValueAtTime({flash_t}, [1, 1, 1, 1]);
            fill_{name}.property("Color").setValueAtTime({flash_t + 0.04}, [0, 0, 0, 1]);
            fill_{name}.property("Color").setValueAtTime({flash_t + 0.12}, [1, 1, 1, 1]);""")
            # Set flash KFs to hold interpolation
            jsx.append(f"""
            for (var fi = 1; fi <= fill_{name}.property("Color").numKeys; fi++) {{
                fill_{name}.property("Color").setInterpolationTypeAtKey(fi, KeyframeInterpolationType.HOLD);
            }}""")

            # ── White solid behind text during black flash ──
            # For Screen mode: black text is invisible, so add a white
            # solid that appears ONLY during the black text moment.
            jsx.append(f"""
            var bg_{name} = comp.layers.addSolid([1, 1, 1], "bg_flash_{name}", comp.width, comp.height, 1);
            bg_{name}.startTime = {flash_t};
            bg_{name}.outPoint = {flash_t + 0.12};
            bg_{name}.moveAfter({name});
            bg_{name}.property("Opacity").setValueAtTime({flash_t}, 0);
            bg_{name}.property("Opacity").setValueAtTime({flash_t + 0.04}, 100);
            bg_{name}.property("Opacity").setValueAtTime({flash_t + 0.12}, 0);""")
            # Hold interpolation for crisp on/off
            jsx.append(f"""
            for (var bi = 1; bi <= bg_{name}.property("Opacity").numKeys; bi++) {{
                bg_{name}.property("Opacity").setInterpolationTypeAtKey(bi, KeyframeInterpolationType.HOLD);
            }}""")

            # ── Animator 1: Character scramble (Character Value) ──
            # Scrambles letters on entrance and exit via Character Value offset
            scramble_in_end = in_time + zoom_in_dur
            scramble_out_start = out_time - 0.24
            jsx.append(f"""
            var anim1_{name} = {name}.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
            anim1_{name}.name = "Scramble";
            var sel1_{name} = anim1_{name}.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
            sel1_{name}.property("ADBE Text Selector Max Amount").setValue(100);
            var charVal_{name} = anim1_{name}.property("ADBE Text Animator Properties").addProperty("ADBE Text Character Value");
            charVal_{name}.setValueAtTime({in_time}, 77);
            charVal_{name}.setValueAtTime({scramble_in_end}, 0);
            charVal_{name}.setValueAtTime({scramble_out_start}, 0);
            charVal_{name}.setValueAtTime({out_time}, 259);""")

            # ── Animator 2: Per-character scale + tracking ──
            # Characters scale up individually with tracking spread
            jsx.append(f"""
            var anim2_{name} = {name}.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
            anim2_{name}.name = "CharScale";
            var sel2_{name} = anim2_{name}.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
            sel2_{name}.property("ADBE Text Selector Max Amount").setValue(100);
            var a2props_{name} = anim2_{name}.property("ADBE Text Animator Properties");
            var a2anchor_{name} = a2props_{name}.addProperty("ADBE Text Anchor Point 3D");
            a2anchor_{name}.setValue([0, -116, 0]);
            var a2scale_{name} = a2props_{name}.addProperty("ADBE Text Scale 3D");
            a2scale_{name}.setValueAtTime({in_time}, [25, 25, 100]);
            a2scale_{name}.setValueAtTime({in_time + zoom_in_dur}, [100, 100, 100]);
            a2scale_{name}.setValueAtTime({out_time - 0.24}, [100, 100, 100]);
            a2scale_{name}.setValueAtTime({out_time}, [25, 25, 100]);
            applyEaseToKeyframes(a2scale_{name}, "easeOutExpo");
            var a2track_{name} = a2props_{name}.addProperty("ADBE Text Tracking Amount");
            a2track_{name}.setValueAtTime({in_time}, -30);
            a2track_{name}.setValueAtTime({in_time + zoom_in_dur + 0.04}, 37);
            a2track_{name}.setValueAtTime({in_time + dur * 0.45}, 0);
            a2track_{name}.setValueAtTime({out_time - 0.24}, 0);
            a2track_{name}.setValueAtTime({out_time}, 1678);
            applyEaseToKeyframes(a2track_{name}, "easeOutExpo");""")

        elif scene == "unique_spin":
            # ── UNIQUE TYPOGRAPHY — 3D spin/fly entrance + exit ──
            # All variants: 3D layer, bounce expression on entrance,
            # Z rotation spin, position fly-in/out.
            variant = animation.get("unique_variant", "spin_fly")
            dur = out_time - in_time
            cx = c.width / 2

            # Bounce expression template (velocity-based overshoot)
            BOUNCE = ("'var amp = {amp}; var freq = 1; var decay = {decay}; var n = 0;\\n'"
                      "+ 'if (numKeys > 0) {{ n = nearestKey(time).index; "
                      "if (key(n).time > time) {{ n--; }} }}\\n'"
                      "+ 'if (n == 0) {{ t = 0; }} else {{ t = time - key(n).time; }}\\n'"
                      "+ 'if (n > 0) {{ v = velocityAtTime(key(n).time - "
                      "thisComp.frameDuration/10); "
                      "value + (v/100)*amp*Math.sin(freq*t*2*Math.PI)/"
                      "Math.exp(decay*t); }} else {{ value; }}'")

            jsx.append(f"""
            {name}.threeDLayer = true;
            {name}.property("Anchor Point").expression = {SRC_CENTER};""")

            if variant == "spin_fly":
                # Pattern A: Spin entrance from off-screen, fly-out exit
                ent_dur = min(0.67, dur * 0.2)
                hold_end = in_time + dur * 0.7
                # Random entrance direction
                ent_y = random.choice([-1155, 1155])
                ent_rot = random.choice([-360, 255, -255, 360])
                # Exit direction
                exit_x = random.choice([-1941, 1941])
                exit_rot = random.randint(400, 550)
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y + ent_y}, 0]);
            {name}.property("Position").setValueAtTime({in_time + ent_dur}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").expression = {BOUNCE.format(amp=8, decay=4)};
            {name}.property("Rotation").setValueAtTime({in_time}, {ent_rot});
            {name}.property("Rotation").setValueAtTime({in_time + ent_dur}, 0);
            {name}.property("Rotation").expression = {BOUNCE.format(amp=8, decay=4)};
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Rotation"), "easeOutExpo");""")
                # Exit: fly out + spin + shrink
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({hold_end}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").setValueAtTime({out_time}, [{exit_x}, {pos_y}, 0]);
            {name}.property("Scale").setValueAtTime({hold_end}, [100, 100, 100]);
            {name}.property("Scale").setValueAtTime({out_time}, [30, 30, 30]);
            {name}.property("Rotation").setValueAtTime({hold_end}, 0);
            {name}.property("Rotation").setValueAtTime({out_time}, {exit_rot});""")

            elif variant == "slide_in":
                # Pattern C: Slide from opposing direction + 3KF hesitate exit
                ent_dur = min(1.0, dur * 0.3)
                hold_end = in_time + dur * 0.7
                hesitate_t = hold_end + (out_time - hold_end) * 0.2
                # Slide direction based on line index
                slide_y = 1812 if line_index % 2 == 0 else -1553
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {slide_y}, 0]);
            {name}.property("Position").setValueAtTime({in_time + ent_dur}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").expression = {BOUNCE.format(amp=12, decay=4)};
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");""")
                # 3KF hesitate-then-fly exit
                exit_x = random.choice([-329, 400])
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({hold_end}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").setValueAtTime({hesitate_t}, [{pos_x + 71}, {pos_y}, 0]);
            {name}.property("Position").setValueAtTime({out_time}, [{exit_x}, {pos_y}, 0]);
            {name}.property("Scale").setValueAtTime({hold_end}, [100, 100, 100]);
            {name}.property("Scale").setValueAtTime({hesitate_t}, [107, 107, 107]);
            {name}.property("Scale").setValueAtTime({out_time}, [0, 0, 0]);
            {name}.property("Rotation").setValueAtTime({hold_end}, 0);
            {name}.property("Rotation").setValueAtTime({hesitate_t}, -12);
            {name}.property("Rotation").setValueAtTime({out_time}, 90);""")

            elif variant == "card_flip":
                # Pattern D: Y rotation card flip entrance + exit
                ent_dur = min(0.7, dur * 0.25)
                hold_end = in_time + dur * 0.5
                jsx.append(f"""
            {name}.property("Y Rotation").setValueAtTime({in_time}, {random.choice([-90, 90])});
            {name}.property("Y Rotation").setValueAtTime({in_time + ent_dur}, 0);
            {name}.property("Y Rotation").expression = {BOUNCE.format(amp=8, decay=4)};
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y}, -1460]);
            {name}.property("Position").setValueAtTime({in_time + ent_dur}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").expression = {BOUNCE.format(amp=8, decay=4)};
            applyEaseToKeyframes({name}.property("Y Rotation"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");""")
                # Exit: flip away + shrink + Z depth
                jsx.append(f"""
            {name}.property("Scale").setValueAtTime({hold_end}, [100, 100, 100]);
            {name}.property("Scale").setValueAtTime({out_time}, [0, 0, 0]);
            {name}.property("Y Rotation").setValueAtTime({hold_end}, 0);
            {name}.property("Y Rotation").setValueAtTime({out_time}, 270);
            {name}.property("Position").setValueAtTime({hold_end}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").setValueAtTime({out_time}, [{pos_x}, {pos_y}, -1460]);""")

            elif variant == "z_fly":
                # Pattern F: Z-depth fly-through exit
                ent_dur = min(0.67, dur * 0.2)
                hold_end = in_time + dur * 0.6
                ent_rot = random.choice([-360, 360])
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({in_time}, [{pos_x}, {pos_y - 1155}, 0]);
            {name}.property("Position").setValueAtTime({in_time + ent_dur}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Rotation").setValueAtTime({in_time}, {ent_rot});
            {name}.property("Rotation").setValueAtTime({in_time + ent_dur}, 0);
            {name}.property("Position").expression = {BOUNCE.format(amp=8, decay=4)};
            {name}.property("Rotation").expression = {BOUNCE.format(amp=8, decay=4)};
            applyEaseToKeyframes({name}.property("Position"), "easeOutExpo");
            applyEaseToKeyframes({name}.property("Rotation"), "easeOutExpo");""")
                # Exit: deep Z travel
                jsx.append(f"""
            {name}.property("Position").setValueAtTime({hold_end}, [{pos_x}, {pos_y}, 0]);
            {name}.property("Position").setValueAtTime({out_time}, [{pos_x}, {pos_y}, -4320]);""")

            # ── Opacity: fade in, hold, then out via scale (no fade needed) ──
            jsx.append(f"""
            {name}.property("Opacity").setValueAtTime({in_time}, 0);
            {name}.property("Opacity").setValueAtTime({in_time + 0.1}, 100);""")

            # ── Fill effect (white) ──
            jsx.append(f"""
            var fill_{name} = {name}.property("Effects").addProperty("ADBE Fill");
            fill_{name}.property("Color").setValue([1, 1, 1]);""")

        return "".join(jsx)

    # ── DOF cameras ─────────────────────────────────────────

    def _dof_cameras(self, candidates):
        c = self.c
        cx, cy = c.width / 2, c.height / 2
        jsx = [f"""
        // =====================
        // DOF CAMERAS
        // =====================
"""]
        for ci, cam in enumerate(candidates):
            name = cam["layer_name"]
            t0, t1 = cam["in_time"], cam["out_time"]
            drift = c.dof_camera_position_drift

            poi_xs = cx + random.uniform(-100, 100)
            poi_ys = cy + random.uniform(-50, 50)
            poi_xe = poi_xs + random.uniform(-drift / 2, drift / 2)
            poi_ye = poi_ys + random.uniform(-drift / 2, drift / 2)

            pxs = cx + random.uniform(-150, 150)
            pys = cy + random.uniform(-100, 100)
            pzs = -2000 + random.uniform(-300, 300)
            pxe = pxs + random.uniform(-drift, drift)
            pye = pys + random.uniform(-drift, drift)
            pze = pzs + random.uniform(-drift / 2, drift / 2)

            xr = random.uniform(*c.dof_camera_x_rotation_range)
            yr = random.uniform(*c.dof_camera_y_rotation_range)
            zr = random.uniform(*c.dof_camera_z_rotation_range)
            fds = abs(pzs) + random.uniform(-50, 50)
            fde = abs(pze) + random.uniform(-50, 50)

            jsx.append(f"""
        try {{
            var dofCam{ci} = comp.layers.addCamera("DOF_Cam_{name}", [{cx}, {cy}]);
            dofCam{ci}.startTime = {t0};
            dofCam{ci}.outPoint = {t1};
            dofCam{ci}.property("X Rotation").setValue({xr});
            dofCam{ci}.property("Y Rotation").setValue({yr});
            dofCam{ci}.property("Z Rotation").setValue({zr});
            dofCam{ci}.property("Point of Interest").setValueAtTime({t0}, [{poi_xs}, {poi_ys}, 0]);
            dofCam{ci}.property("Point of Interest").setValueAtTime({t1}, [{poi_xe}, {poi_ye}, 0]);
            applyEaseToKeyframes(dofCam{ci}.property("Point of Interest"), "easeInOutSine");
            dofCam{ci}.property("Position").setValueAtTime({t0}, [{pxs}, {pys}, {pzs}]);
            dofCam{ci}.property("Position").setValueAtTime({t1}, [{pxe}, {pye}, {pze}]);
            applyEaseToKeyframes(dofCam{ci}.property("Position"), "easeInOutSine");
            dofCam{ci}.property("Camera Options").property("Zoom").setValue({c.dof_camera_zoom});
            dofCam{ci}.property("Camera Options").property("Depth of Field").setValue(1);
            dofCam{ci}.property("Camera Options").property("Aperture").setValue({c.dof_camera_aperture});
            dofCam{ci}.property("Camera Options").property("Blur Level").setValue({c.dof_camera_blur_level});
            dofCam{ci}.property("Camera Options").property("Focus Distance").setValueAtTime({t0}, {fds});
            dofCam{ci}.property("Camera Options").property("Focus Distance").setValueAtTime({t1}, {fde});
            applyEaseToKeyframes(dofCam{ci}.property("Camera Options").property("Focus Distance"), "easeInOutSine");
        }} catch(e) {{}}
""")
        return "".join(jsx)

    # ── footer: save + close ────────────────────────────────

    def _footer(self, project_name):
        return f"""

        // =====================
        // SAVE PROJECT
        // =====================
        var saveFile = new File(projectFolder + "/" + projectName + ".aep");
        app.project.save(saveFile);

        $.writeln("Project created: " + projectName);
        $.writeln("Chorus groups: " + chorusNulls.length);
        $.writeln("Total text layers: " + textLayers.length);

    }} catch(e) {{
        $.writeln("Error: " + e.toString());
    }}

    app.endUndoGroup();
}})();
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Batch Script Writer  (SRP: only writes macOS batch script)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BatchScriptWriter:
    def write(self, output_folder):
        script = f"""#!/bin/bash
# SnapLyrics — After Effects Batch Processor

OUTPUT_DIR="{output_folder.absolute()}"
AE_VERSION="2025"

echo "SnapLyrics — After Effects Batch Processor"
echo "================================"
echo "Processing projects in: $OUTPUT_DIR"
echo ""

if ! osascript -e 'tell application "System Events" to name of every application process' | grep -q "After Effects"; then
    echo "After Effects not running. Opening..."
    open -a "Adobe After Effects $AE_VERSION"
    sleep 5
fi

process_project() {{
    local jsx_file="$1"
    local project_name="$2"
    echo "  Running: $project_name"
    osascript <<EOF
    tell application "Adobe After Effects $AE_VERSION"
        activate
        DoScriptFile POSIX file "$jsx_file"
    end tell
EOF
    sleep 3
}}

TOTAL=0
SUCCESS=0

for folder in "$OUTPUT_DIR"/*/; do
    if [ -d "$folder" ]; then
        folder_name=$(basename "$folder")
        jsx_file="${{folder}}${{folder_name}}.jsx"
        if [ -f "$jsx_file" ]; then
            TOTAL=$((TOTAL + 1))
            echo "[$TOTAL] Processing: $folder_name"
            if process_project "$jsx_file" "$folder_name"; then
                SUCCESS=$((SUCCESS + 1))
                echo "  Done"
            else
                echo "  Error"
            fi
            echo ""
            sleep 2
        fi
    fi
done

echo "================================"
echo "SnapLyrics complete!"
echo "   Processed: $SUCCESS of $TOTAL"
echo "================================"

osascript -e 'display notification "SnapLyrics complete: '$SUCCESS' of '$TOTAL' projects" with title "SnapLyrics" sound name "Glass"'
"""
        path = output_folder / "run_batch.command"
        with open(path, "w") as f:
            f.write(script)
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"\n{_WISTERIA}  Batch script generated: {path.name}{_RESET}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pipeline  (SRP: orchestrates all components, owns I/O)
# DIP: all dependencies are injected or created from config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SnapLyricsPipeline:
    def __init__(self, source_folder, output_folder="OUTPUT", config=None,
                 style=None):
        self.config = config or VideoConfig()
        self.source_folder = Path(source_folder)
        self.output_folder = self.source_folder / output_folder

        # Compose components (DIP)
        self.parser = LrcParser()
        self.layout = TextLayout(self.config)
        self.analyzer = SongAnalyzer(self.config)
        self.animations = AnimationLibrary(self.config, style=style)
        self.renderer = JsxRenderer(self.config, self.layout, self.animations)
        self.batch_writer = BatchScriptWriter()
        self.syncer = LrcSyncer() if LrcSyncer.available() else None
        self.writer = LrcWriter()
        self.fetcher = LyricsFetcher() if LyricsFetcher.available() else None

    def process_all_songs(self):
        self.output_folder.mkdir(exist_ok=True)

        print(f"\n{_BOLD}{_LILAC}  SnapLyrics{_RESET}")
        print(f"{_LILAC}  ─────────────────────────────────{_RESET}")
        print(f"{_SNOW}  Source:  {_WISTERIA}{self.source_folder}{_RESET}")
        print(f"{_SNOW}  Output:  {_WISTERIA}{self.output_folder}{_RESET}")
        print(f"{_SNOW}  Style:   {_WISTERIA}{self.animations.active_style}{_RESET}\n")

        audio_files = _find_audio_files(self.source_folder)
        if not audio_files:
            fmts = ", ".join(AUDIO_EXTENSIONS)
            print(f"{_RED}  No audio files found ({fmts}) in {self.source_folder}{_RESET}")
            return

        # Check sync dependencies
        if not self.syncer:
            print(f"{_RED}  openai-whisper not installed -- sync disabled{_RESET}")
            print(f"{_WISTERIA}  pip install openai-whisper{_RESET}")
            print(f"{_RED}  Sync is required -- aborting.{_RESET}\n")
            return

        vocals_count = sum(
            1 for f in audio_files if LrcSyncer.find_vocals(f) is not None
        )
        need_separation = len(audio_files) - vocals_count

        print(f"{_SNOW}  Found {_GOLD}{len(audio_files)}{_SNOW} songs, {_GOLD}{vocals_count}{_SNOW} _vocals files{_RESET}")
        if need_separation > 0 and LrcSyncer.can_separate():
            print(f"{_WISTERIA}  {need_separation} will be separated with Demucs{_RESET}")
        elif need_separation > 0:
            print(f"{_WISTERIA}  {need_separation} missing _vocals (install demucs to auto-extract){_RESET}")
            print(f"{_WISTERIA}  pip install demucs{_RESET}")
        print(f"{_GOLD}  Auto-sync ENABLED{_RESET}\n")

        success = 0
        synced_count = 0
        errors = 0

        total = len(audio_files)
        for idx, audio_file in enumerate(audio_files, 1):
            lrc_file = audio_file.with_suffix(".lrc")
            txt_file = audio_file.with_suffix(".txt")
            _progress_bar(idx, total, label=audio_file.stem)
            print(f"{_LILAC}  [{idx}/{total}]{_SNOW} {audio_file.name}{_RESET}")

            song_name = audio_file.stem
            song_folder = self.output_folder / song_name
            song_folder.mkdir(exist_ok=True)

            try:
                # Step 1: Get or extract vocals (skip if _vocals already exists)
                vocals_file = LrcSyncer.find_vocals(audio_file)
                if not vocals_file and LrcSyncer.can_separate():
                    vocals_file = LrcSyncer.separate_vocals(audio_file)
                if not vocals_file:
                    print(f"{_RED}    No _vocals file and Demucs not installed{_RESET}")
                    print(f"{_WISTERIA}    pip install demucs{_RESET}")
                    errors += 1
                    continue

                # Step 2: Load reference lyrics (skip fetch if .txt already exists)
                reference = None
                if lrc_file.exists():
                    reference, _ = self.parser.parse(lrc_file)
                    print(f"{_WISTERIA}    Reference: .lrc ({len(reference)} lines){_RESET}")
                elif txt_file.exists():
                    reference, _ = self.parser.parse_txt(txt_file)
                    print(f"{_WISTERIA}    Reference: .txt ({len(reference)} lines){_RESET}")
                elif self.fetcher:
                    fetched = self.fetcher.fetch_and_save(audio_file)
                    if fetched:
                        txt_file = fetched
                        reference, _ = self.parser.parse_txt(txt_file)
                        print(f"{_WISTERIA}    Reference: internet ({len(reference)} lines){_RESET}")

                # Step 3: Transcribe + align (skip if synced .lrc already in output)
                synced_lrc = song_folder / f"{song_name}.lrc"
                if synced_lrc.exists():
                    lyrics, _ = self.parser.parse(synced_lrc)
                    print(f"{_WISTERIA}    Cached sync: {len(lyrics)} lines{_RESET}")
                    sync_info = None
                else:
                    lyrics, sync_info = self.syncer.sync(vocals_file, reference)
                if not lyrics:
                    errors += 1
                    continue

                if sync_info is not None:
                    self.writer.write(lyrics, [], synced_lrc)
                synced_count += 1

                # Step 4: Split into word blocks + generate JSX
                lyrics = _split_lyrics_into_blocks(
                    lyrics,
                    self.config.max_words_per_block,
                    self.config.anticipation_seconds,
                )
                analysis = self.analyzer.analyze(lyrics)
                jsx_content = self.renderer.render(
                    audio_file.absolute(), analysis,
                    song_name, song_folder.absolute(),
                )

                jsx_file = song_folder / f"{song_name}.jsx"
                with open(jsx_file, "w", encoding="utf-8") as f:
                    f.write(jsx_content)

                shutil.copy2(audio_file, song_folder / audio_file.name)

                print(f"{_GOLD}    Done{_RESET} {_WISTERIA}{len(lyrics)} lines{_RESET} {_SNOW}→ {song_folder.name}/{_RESET}")
                success += 1

            except Exception as e:
                print(f"{_RED}    Error: {e}{_RESET}")
                errors += 1

        self.batch_writer.write(self.output_folder)

        print(f"\n{_LILAC}  {'━' * 40}{_RESET}")
        print(f"{_BOLD}{_GOLD}  SNAPLYRICS COMPLETE{_RESET}")
        print(f"{_LILAC}  {'━' * 40}{_RESET}")
        print(f"{_GOLD}  Successful: {success}{_RESET}")
        if synced_count:
            print(f"{_WISTERIA}  Synced: {synced_count}{_RESET}")
        if errors:
            print(f"{_RED}  Errors: {errors}{_RESET}")
        print(f"{_SNOW}  Output: {_WISTERIA}{self.output_folder.absolute()}{_RESET}")
        print(f"\n{_SNOW}  To process in After Effects:{_RESET}")
        print(f"{_WISTERIA}    1. Open After Effects{_RESET}")
        print(f"{_WISTERIA}    2. File > Scripts > Run Script File...{_RESET}")
        print(f"{_WISTERIA}    3. Browse to OUTPUT/[song]/[song].jsx{_RESET}")
        print(f"{_WISTERIA}    4. The project will be created automatically{_RESET}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Backwards-compatible alias
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SnapLyricsGenerator(SnapLyricsPipeline):
    """Backwards-compatible alias so existing scripts keep working."""
    pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="SnapLyrics — Snap lyrics to any DJ edit via Whisper transcription + After Effects JSX"
    )
    parser.add_argument(
        "folder", nargs="?", default=".",
        help="Folder containing audio + .lrc files (default: current directory)",
    )
    parser.add_argument(
        "--style", default=None,
        help="Animation style (e.g. standard, isokinetic). Random if omitted.",
    )
    args = parser.parse_args()

    pipeline = SnapLyricsPipeline(source_folder=args.folder, style=args.style)
    pipeline.process_all_songs()


if __name__ == "__main__":
    main()
