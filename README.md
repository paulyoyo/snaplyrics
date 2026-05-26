# SnapLyrics

Snap lyrics to any DJ edit. Drop an audio file, get a fully animated After Effects lyrics video — synced, split, and ready for the big screen.

Built for DJs who need lyrics on screen during live sets. No karaoke vibes — bold, punchy text blocks with 70 kinetic typography animations designed for high-energy shows.

## What it does

1. **Extracts vocals** from any audio file (Demucs)
2. **Transcribes** the vocals with word-level timestamps (Whisper)
3. **Cleans up text** using reference lyrics from LRC/TXT files or auto-fetched from the internet (Genius, lyrics.ovh, AZLyrics)
4. **Splits long lines** into 3-4 word blocks for big-screen readability
5. **Generates After Effects JSX** with animated text layers, chorus detection, camera motion, DOF effects, and a macOS batch runner

### The pipeline

```
Audio file (.aiff/.wav/.mp3/...)
    |
    +-- Demucs --> vocals extraction (auto, cached)
    |
    +-- Whisper --> transcription with timestamps
    |
    +-- Reference lyrics (LRC/TXT/internet) --> text correction
    |
    +-- SnapLyrics --> After Effects .jsx
```

An audio file alone is enough. No lyrics file needed — Whisper transcribes, reference lyrics just fix spelling.

## Install

```bash
pip install openai-whisper demucs torchcodec lyricsgenius
```

For auto-fetching lyrics from Genius, create a `.env` file:

```
GENIUS_API_TOKEN=your_token_here
```

Get a free token at [genius.com/api-clients](https://genius.com/api-clients). Without it, lyrics.ovh and AZLyrics are used as fallback (no key needed).

### Requirements

- Python 3.10+
- Adobe After Effects (for rendering the JSX)
- macOS (batch script uses AppleScript)
- ffprobe (optional, for transcription progress bar)

## Usage

### Just drop files in a folder and run

```
my-set/
  Song Name.aiff          # audio (any format)
  Song Name_vocals.wav    # optional: pre-extracted vocals
  Song Name.lrc           # optional: reference lyrics
  Song Name.txt           # optional: plain text lyrics
```

```bash
python3 snaplyrics.py my-set/
```

That's it. SnapLyrics handles everything:

- No `_vocals` file? Extracts with Demucs (cached for next run)
- No `.lrc` or `.txt`? Fetches lyrics from the internet
- No lyrics anywhere? Uses Whisper's transcription as-is

### Output

```
my-set/OUTPUT/
  Song Name/
    Song Name.jsx         # After Effects script
    Song Name.aiff        # audio copy
    Song Name.lrc         # synced lyrics
  run_batch.command       # process all songs at once
```

### Open in After Effects

**Single song:** File > Scripts > Run Script File > pick the `.jsx`

**All songs:** Double-click `run_batch.command`

### Folder wrappers

```bash
cd canciones/ && python3 lrc.py    # runs on canciones/
cd perreo/ && python3 lrc.py       # runs on perreo/
```

## How it works

### Anticipation timing

Text appears **1 second before** the vocal moment. The entrance animation plays for 0.5s, then the text sits readable for 0.5s before it's time to sing. The crowd reads ahead, not behind.

### Word blocks, not karaoke lines

Long lines are split into **3-4 word chunks**, each with its own timestamp and animation. Big text, maximum impact — designed for screens, not subtitles.

### Overlapping vocals

When studio vocals overdub (one line starts before the previous ends), both lyrics stay visible simultaneously. They stack vertically and exit together via a shared null object.

### Character-based duration

Each text block stays visible based on its character count (0.06s per character, minimum 0.8s). Short text = short display. Long text = long display. No more lyrics disappearing before you can read them.

## Animations

**70 animations** across 4 categories, randomly assigned per text layer:

### Classic (motion + effects)
fadeIn, scaleIn, slideUp, slideDown, bounceIn, slideFromLeft, slideFromRight, typewriter, wave, blurReveal, zoomBlur, flipX, flipY, glitch, dropShadowPulse, extremeZoomIn, elasticPop, and more slide/blur/diagonal/dramatic combos.

### Kinetic typography (per-character)
charCascade, charRotateIn, charScaleStagger, charBlurSweep, charSpiral, charBounceUp, char3dFlip — each character animates individually with staggered timing.

### Tracking & wipe
trackingExpand, trackingCompress, lineWipe — letter spacing and reveal animations.

### 3D pop-out titles
pop3dToward, pop3dAway, pop3dSpinX, pop3dSpinY, pop3dTumble, pop3dSlam, pop3dShatterIn, pop3dWaveZ, pop3dCardFan, pop3dZoomRotate — text flies through 3D space with depth, rotation, and perspective.

Plus combo variants that layer multiple effects together (cascadeBlur, spiralShadow, pop3dSlamShadow, pop3dCardCascade, etc.)

## Configuration

Override any setting via `VideoConfig`:

```python
from snaplyrics import SnapLyricsPipeline, VideoConfig

config = VideoConfig(
    font="Arial",
    fps=60,
    base_font_size=100,
    max_words_per_block=3,
    anticipation_seconds=1.5,
    dof_camera_probability=0.25,
)
pipeline = SnapLyricsPipeline("my-set/", config=config)
pipeline.process_all_songs()
```

| Setting | Default | What it controls |
|---------|---------|-----------------|
| `font` | Heavitas | Font family (must be installed) |
| `base_font_size` | 120 | Text size in pixels |
| `fps` | 30 | Frames per second |
| `max_words_per_block` | 4 | Words per text block |
| `anticipation_seconds` | 1.0 | How early text appears before vocals |
| `animation_in_frames` | 15 | Entrance animation duration |
| `dof_camera_probability` | 0.15 | Chance of DOF camera per text |
| `shake_intensity` | 5 | Camera shake pixel intensity |
| `reading_speed_per_char` | 0.06 | Min display time per character |

## Supported formats

`.aiff` `.aif` `.wav` `.mp3` `.flac` `.m4a` `.ogg` `.aac`

## After Effects output

- 1920x1080 @ 30fps composition
- Audio layer imported and placed
- Global camera null with subtle pan/zoom/rotation
- Camera shake at energy return moments
- Chorus detection with stacking + zoom transitions
- DOF cameras on ~15% of text layers
- Motion blur on all animated layers

## Rendering in After Effects

### Step 1 — Run the JSX

1. Open After Effects
2. **File > Scripts > Run Script File...**
3. Select `OUTPUT/Song Name/Song Name.jsx`
4. The composition, audio, text layers, and all animations are created automatically
5. Review the timeline — all layers are named with their lyrics text

For batch processing, double-click `OUTPUT/run_batch.command` to process all songs sequentially.

### Step 2 — Add to Render Queue

1. Select the composition in the Project panel
2. **Composition > Add to Render Queue** (Ctrl/Cmd + M)
3. Configure output:

| Setting | Value |
|---------|-------|
| **Output Module** | QuickTime |
| **Format** | Apple ProRes 422 |
| **Resolution** | 1920x1080 |
| **Channels** | RGB |
| **Audio Output** | Off (lyrics video only, audio plays from DJ software) |

4. **Output To:** click and save to the same song folder in OUTPUT
5. Click **Render**

### Step 3 — Batch render all compositions

1. Run all JSX scripts first (use `run_batch.command`)
2. Select all compositions in the Project panel
3. **Composition > Add to Render Queue**
4. Apply the same Output Module preset to all
5. Click **Render**

**Tip:** Save an Output Module preset called "SnapLyrics ProRes" with the settings above so you can apply it to all compositions in one click.

### Step 4 — Convert to HAP for live performance

After rendering ProRes files, convert them to HAP codec for GPU-accelerated playback in openFrameworks, Resolume, VDMX, or any real-time video engine:

```bash
python3 convert_to_hap.py my-set/
```

This converts all `.mov` files in `my-set/OUTPUT/` to HAP codec. See the section below.

## HAP conversion for openFrameworks

The `convert_to_hap.py` script converts all rendered ProRes videos to HAP codec for optimal real-time playback performance.

### Install ffmpeg with HAP support

```bash
brew install ffmpeg
```

### Usage

```bash
python3 convert_to_hap.py my-set/
```

This finds all `.mov` files in `my-set/OUTPUT/*/` and converts them to `_hap.mov` in the same folder.

| Input | Output |
|-------|--------|
| `OUTPUT/Song Name/Song Name.mov` | `OUTPUT/Song Name/Song Name_hap.mov` |

### HAP variants

| Codec | Quality | Speed | Use case |
|-------|---------|-------|----------|
| **HAP** (default) | Good | Fastest decode | Standard lyrics playback |
| **HAP Q** | Better | Fast decode | When you need higher quality |
| **HAP Alpha** | Good + alpha | Fast decode | Overlay on live visuals |

Pass `--codec` to choose:

```bash
python3 convert_to_hap.py my-set/ --codec hapq      # HAP Q (higher quality)
python3 convert_to_hap.py my-set/ --codec hapalpha   # HAP Alpha (with transparency)
```

## License

MIT
