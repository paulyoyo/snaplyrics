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

from difflib import SequenceMatcher


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

    # Animation timing (in frames)
    animation_in_frames: int = 6
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
        """Find a _vocals file next to the audio (same name + '_vocals', same extension).

        Example: Song.wav → Song_vocals.wav
        """
        p = Path(audio_path)
        candidate = p.with_name(f"{p.stem}_vocals{p.suffix}")
        return candidate if candidate.exists() else None

    # ── Transcription ──────────────────────────────────────

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            print("  Loading Whisper model (medium)...")
            cls._model = whisper.load_model("medium")
        return cls._model

    def transcribe(self, vocals_path):
        """Transcribe vocals file with Whisper, returning segments with timestamps."""
        model = self._get_model()
        print(f"  Transcribing vocals...")
        result = model.transcribe(
            str(vocals_path),
            word_timestamps=True,
            language="es",
        )
        segments = []
        for seg in result.get("segments", []):
            text = seg.get("text", "").strip()
            if text:
                segments.append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": text,
                })
        print(f"  Whisper: {len(segments)} segments transcribed")
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
        print(f"  Matched {matched}/{len(segments)} segments to LRC lines ({100 * matched // max(len(segments), 1)}%)")
        return aligned, matched

    # ── Sync ────────────────────────────────────────────────

    def sync(self, audio_path, lyrics, metadata, acapella_path):
        """Sync lyrics to audio using Whisper transcription + global LRC alignment.

        Returns (synced_lyrics, metadata, info_dict).
        """
        if not lyrics:
            return lyrics, metadata, None

        segments = self.transcribe(acapella_path)
        if not segments:
            print("  No segments transcribed")
            return lyrics, metadata, None

        aligned, matched = self.align(segments, lyrics)

        info = {
            "segments_transcribed": len(segments),
            "segments_matched": matched,
            "synced_count": len(aligned),
            "match_rate": matched / max(len(segments), 1),
        }

        print(f"  Synced {len(aligned)} lines")
        return aligned, metadata, info


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
        durations = []
        for i, lyric in enumerate(lyrics):
            if i < len(lyrics) - 1:
                dur = lyrics[i + 1]["time"] - lyric["time"] - self.c.text_gap_before_next
                dur = max(dur, 0.5)
            else:
                dur = 3.0
            durations.append({
                "index": i,
                "lyric": lyric,
                "start_time": lyric["time"],
                "end_time": lyric["time"] + dur,
                "duration": dur,
            })
        return durations


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Animation Library  (OCP: registry pattern, open for extension)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AnimationLibrary:
    EASING_TYPES = ["Quad", "Cubic", "Quart", "Quint", "Sine",
                    "Expo", "Circ", "Back", "Elastic", "Bounce"]
    EASING_DIRS = ["In", "Out", "InOut"]

    def __init__(self, config: VideoConfig):
        self.c = config
        self._animations = []
        self._register_defaults()

    def register(self, animation):
        self._animations.append(animation)

    def random(self):
        template = random.choice(self._animations)
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
        ]
        for a in defaults:
            a.setdefault("easing", None)
            self.register(a)


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
        // FUNCIONES HELPER
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
        // IMPORTAR AUDIO
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
        // CREAR CAMERA NULL GLOBAL
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
        // SHAKE EN MOMENTOS DE ENERGIA
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
        // ARRAYS PARA CAPAS
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
            {name}.name = "{name}";
            {name}.startTime = {line_in};
            {name}.outPoint = {out_time + c.null_exit_duration};
            {name}.parent = chorusNull{group_idx};
            var rect_{name} = {name}.sourceRectAtTime({line_in}, false);
            var anchorX_{name} = rect_{name}.left + rect_{name}.width / 2;
            var anchorY_{name} = rect_{name}.top + rect_{name}.height / 2;
            {name}.property("Anchor Point").setValue([anchorX_{name}, anchorY_{name}]);
            {name}.property("Position").setValue([{layer_x}, {layer_y}]);
            {name}.motionBlur = true;
            textLayers.push({name});
""")
                # Opacity (in only, null handles exit)
                if use_hard:
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

                # Short text zoom
                if len(line_text.strip()) <= 10:
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
        // TEXTOS INDIVIDUALES (no chorus)
        // =====================
        var dofCameraLayers = [];
"""]
        dof_candidates = []

        for ld in analysis.lyric_durations:
            idx = ld["index"]
            if idx in analysis.chorus_indices:
                continue

            lyric = ld["lyric"]
            in_time = ld["start_time"]
            out_time = ld["end_time"]
            duration = ld["duration"]
            text = lyric["text"]
            fs, text_lines = self.layout.calculate_font_size(text)
            use_hard = self.layout.is_short_text(text, duration)
            add_mid = self.layout.should_add_mid_effect(duration)
            animation = self.anim.random()
            easing = animation["easing"]
            use_dof = random.random() < c.dof_camera_probability

            if use_dof:
                dof_candidates.append({
                    "layer_name": f"txt{idx}_0",
                    "in_time": in_time,
                    "out_time": out_time,
                })

            # Staggered line times (midpoint of remaining for individual)
            line_times = []
            cur = in_time
            for li in range(len(text_lines)):
                line_times.append(cur)
                if li < len(text_lines) - 1:
                    cur = cur + (out_time - cur) / 2

            for li, line_text in enumerate(text_lines):
                total_h = len(text_lines) * fs * 1.2
                start_y = (c.height - total_h) / 2 + fs / 2
                y_pos = start_y + li * fs * 1.2
                line_in = line_times[li]
                line_dur = out_time - line_in
                escaped = self._escape_text(line_text)
                name = f"txt{idx}_{li}"
                dur_frames = line_dur * c.fps
                out_anim = self.anim.get_out_animation(dur_frames)

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
            {name}.name = "{name}";
            {name}.property("Position").setValue([{cx}, {y_pos}]);
            {name}.startTime = {line_in};
            {name}.outPoint = {out_time};
            {name}.parent = cameraNull;
            {name}.motionBlur = true;
            textLayers.push({name});
""")
                if use_dof:
                    jsx.append(f"""
            {name}.threeDLayer = true;
""")

                # Opacity with out animation
                if use_hard:
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

                # Scale (in + inverted out)
                if "scale" in animation and not use_hard:
                    jsx.append(f"""
            {name}.property("Scale").setValueAtTime({line_in}, {animation['scale']['from']});
            {name}.property("Scale").setValueAtTime({line_in + c.animation_duration}, {animation['scale']['to']});
            {name}.property("Scale").setValueAtTime({out_time - c.animation_duration}, {animation['scale']['to']});
            {name}.property("Scale").setValueAtTime({out_time}, {animation['scale']['from']});
            applyEaseToKeyframes({name}.property("Scale"), "{easing}");
""")
                elif (len(line_text.strip()) <= 10 and not use_hard
                      and not animation.get("elastic_pop")):
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

                # Mid-duration effect
                if add_mid and not use_hard:
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

                jsx.append(f"""
        }} catch(e) {{}}
""")

        if dof_candidates:
            jsx.append(self._dof_cameras(dof_candidates))

        return "".join(jsx)

    # ── shared animation effects ────────────────────────────

    def _render_effects(self, name, animation, in_time, out_time,
                        use_hard, pos_x, pos_y, include_out=False):
        if use_hard:
            return ""
        c = self.c
        jsx = []

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
        // GUARDAR PROYECTO
        // =====================
        var saveFile = new File(projectFolder + "/" + projectName + ".aep");
        app.project.save(saveFile);

        $.writeln("Proyecto creado: " + projectName);
        $.writeln("Chorus groups: " + chorusNulls.length);
        $.writeln("Total textos: " + textLayers.length);

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
# Batch processor para After Effects

OUTPUT_DIR="{output_folder.absolute()}"
AE_VERSION="2025"

echo "After Effects Batch Processor"
echo "================================"
echo "Procesando proyectos en: $OUTPUT_DIR"
echo ""

if ! osascript -e 'tell application "System Events" to name of every application process' | grep -q "After Effects"; then
    echo "After Effects no esta abierto. Abriendo..."
    open -a "Adobe After Effects $AE_VERSION"
    sleep 5
fi

process_project() {{
    local jsx_file="$1"
    local project_name="$2"
    echo "  Ejecutando: $project_name"
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
            echo "[$TOTAL] Procesando: $folder_name"
            if process_project "$jsx_file" "$folder_name"; then
                SUCCESS=$((SUCCESS + 1))
                echo "  Completado"
            else
                echo "  Error"
            fi
            echo ""
            sleep 2
        fi
    fi
done

echo "================================"
echo "Proceso completado!"
echo "   Total procesados: $SUCCESS de $TOTAL"
echo "================================"

osascript -e 'display notification "Procesamiento completado: '$SUCCESS' de '$TOTAL' proyectos" with title "After Effects Batch" sound name "Glass"'
"""
        path = output_folder / "run_batch.command"
        with open(path, "w") as f:
            f.write(script)
        path.chmod(path.stat().st_mode | stat.S_IEXEC)
        print(f"\nScript de batch generado: {path.name}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pipeline  (SRP: orchestrates all components, owns I/O)
# DIP: all dependencies are injected or created from config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SnapLyricsPipeline:
    def __init__(self, source_folder, output_folder="OUTPUT", config=None):
        self.config = config or VideoConfig()
        self.source_folder = Path(source_folder)
        self.output_folder = self.source_folder / output_folder

        # Compose components (DIP)
        self.parser = LrcParser()
        self.layout = TextLayout(self.config)
        self.analyzer = SongAnalyzer(self.config)
        self.animations = AnimationLibrary(self.config)
        self.renderer = JsxRenderer(self.config, self.layout, self.animations)
        self.batch_writer = BatchScriptWriter()
        self.syncer = LrcSyncer() if LrcSyncer.available() else None
        self.writer = LrcWriter()

    def process_all_songs(self):
        self.output_folder.mkdir(exist_ok=True)

        print(f"Carpeta de trabajo: {self.source_folder}")
        print(f"Carpeta de salida: {self.output_folder}")

        audio_files = _find_audio_files(self.source_folder)
        if not audio_files:
            fmts = ", ".join(AUDIO_EXTENSIONS)
            print(f"No se encontraron archivos de audio ({fmts}) en {self.source_folder}")
            return

        # Check for _vocals sync
        has_any_vocals = any(
            Path(f).with_name(f"{Path(f).stem}_vocals{Path(f).suffix}").exists()
            for f in audio_files
        )

        if has_any_vocals and not self.syncer:
            print(f"_vocals files found but openai-whisper not installed")
            print(f"  pip install openai-whisper")
            print(f"Sync is required -- aborting.\n")
            return

        vocals_count = sum(
            1 for f in audio_files if LrcSyncer.find_vocals(f) is not None
        ) if self.syncer else 0

        if vocals_count:
            print(f"Encontradas {len(audio_files)} canciones, {vocals_count} _vocals files")
            print(f"Auto-sync ENABLED\n")
        else:
            print(f"Encontradas {len(audio_files)} canciones\n")

        success = 0
        synced_count = 0
        errors = 0

        for idx, audio_file in enumerate(audio_files, 1):
            lrc_file = audio_file.with_suffix(".lrc")
            print(f"[{idx}/{len(audio_files)}] {audio_file.name}")

            if not lrc_file.exists():
                print(f"  No se encontro archivo LRC")
                errors += 1
                continue

            song_name = audio_file.stem
            song_folder = self.output_folder / song_name
            song_folder.mkdir(exist_ok=True)

            try:
                lyrics, metadata = self.parser.parse(lrc_file)
                if not lyrics:
                    print(f"  No se encontraron lyrics validas en el LRC")
                    errors += 1
                    continue

                # Sync lyrics if _vocals file exists
                if self.syncer:
                    vocals_file = LrcSyncer.find_vocals(audio_file)
                    if vocals_file:
                        lyrics, metadata, sync_info = self.syncer.sync(
                            audio_file, lyrics, metadata, vocals_file,
                        )
                        synced_lrc = song_folder / f"{song_name}.lrc"
                        self.writer.write(lyrics, metadata, synced_lrc)
                        synced_count += 1

                analysis = self.analyzer.analyze(lyrics)
                jsx_content = self.renderer.render(
                    audio_file.absolute(), analysis,
                    song_name, song_folder.absolute(),
                )

                jsx_file = song_folder / f"{song_name}.jsx"
                with open(jsx_file, "w", encoding="utf-8") as f:
                    f.write(jsx_content)

                shutil.copy2(audio_file, song_folder / audio_file.name)
                # Copy original .lrc (synced version already in output if applicable)
                if not (song_folder / f"{song_name}.lrc").exists():
                    shutil.copy2(lrc_file, song_folder / lrc_file.name)

                print(f"  Generado exitosamente")
                print(f"     {len(lyrics)} lineas de texto")
                print(f"     {song_folder.name}/")
                success += 1

            except Exception as e:
                print(f"  Error: {e}")
                errors += 1

        self.batch_writer.write(self.output_folder)

        print(f"\n{'='*50}")
        print(f"PROCESO COMPLETADO")
        print(f"{'='*50}")
        print(f"Exitosos: {success}")
        if synced_count:
            print(f"Sincronizados: {synced_count}")
        print(f"Errores: {errors}")
        print(f"Archivos generados en: {self.output_folder.absolute()}")
        print(f"\nPara procesar en After Effects:")
        print(f"   1. Abre After Effects")
        print(f"   2. File > Scripts > Run Script File...")
        print(f"   3. Navega a OUTPUT/[cancion]/[cancion].jsx")
        print(f"   4. El proyecto se creara automaticamente")


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
    args = parser.parse_args()

    pipeline = SnapLyricsPipeline(source_folder=args.folder)
    pipeline.process_all_songs()


if __name__ == "__main__":
    main()
