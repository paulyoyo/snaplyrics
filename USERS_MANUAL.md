# User's Manual: LRC Lyrics Tools

This project contains two tools for working with `.lrc` lyric files for DJ sets:

1. **Lyrics Video Generator** -- Creates After Effects projects with animated lyrics
2. **Lyrics Syncer** -- Adjusts LRC timestamps to match DJ edit audio files

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Tool 1: Lyrics Video Generator](#tool-1-lyrics-video-generator)
  - [Overview](#overview)
  - [Folder Setup](#folder-setup)
  - [Running the Generator](#running-the-generator)
  - [Output Structure](#output-structure)
  - [Running in After Effects](#running-in-after-effects)
  - [Batch Processing](#batch-processing)
  - [Configuration Reference](#configuration-reference)
  - [Animation Types](#animation-types)
- [Tool 2: Lyrics Syncer](#tool-2-lyrics-syncer)
  - [Overview](#syncer-overview)
  - [Folder Setup](#syncer-folder-setup)
  - [Running the Syncer](#running-the-syncer)
  - [How It Works](#how-it-works)
  - [Output](#syncer-output)
- [LRC File Format](#lrc-file-format)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Python 3.8+**
- **Adobe After Effects 2025** (for the video generator)
- **macOS** (batch script uses AppleScript/osascript)

For the Lyrics Syncer only:
```bash
pip install librosa numpy
```

No additional dependencies are needed for the Video Generator.

---

## Tool 1: Lyrics Video Generator

### Overview

Takes `.aiff` audio files and matching `.lrc` lyric files, and generates After Effects `.jsx` scripts that create fully animated lyrics videos with:

- Per-word timed text layers with randomized entrance/exit animations
- Automatic chorus detection and stacked group animation
- Global camera movement (pan, zoom, rotation, shake)
- Depth of Field camera effects on random text layers
- Motion blur on all animated layers
- Mid-duration zoom/position punches on long-display text
- Smart text splitting for long lines
- Adaptive font sizing

### Folder Setup

Place your files in the same folder as `lrc.py`:

```
canciones/                    # or perreo/
  lrc.py                      # The generator script
  Song Name.aiff              # Audio file
  Song Name.lrc               # Matching lyrics file
  Another Song.aiff
  Another Song.lrc
```

**Important:** The `.aiff` and `.lrc` files must share the exact same filename (minus extension).

### Running the Generator

```bash
cd canciones/       # or perreo/
python3 lrc.py
```

The script will:
1. Scan the current folder for all `.aiff` files
2. Look for a matching `.lrc` for each
3. Generate a JSX script and copy source files into `OUTPUT/<song name>/`
4. Create a batch runner script

### Output Structure

```
canciones/
  OUTPUT/
    Song Name/
      Song Name.jsx           # After Effects script
      Song Name.aiff          # Copy of audio
      Song Name.lrc           # Copy of lyrics
    Another Song/
      Another Song.jsx
      Another Song.aiff
      Another Song.lrc
    run_batch.command          # Batch processor (double-click to run)
```

### Running in After Effects

**Single song:**
1. Open After Effects
2. `File > Scripts > Run Script File...`
3. Navigate to `OUTPUT/<song name>/<song name>.jsx`
4. The script creates a new composition, imports audio, adds all text layers with animations, and saves a `.aep` project file

**What gets created in After Effects:**
- A 1920x1080 @ 30fps composition
- Audio layer
- `CAMERA_GLOBAL` null with subtle pan/zoom/rotation
- Chorus group nulls (for repeated lyric sections)
- Individual text layers with randomized animations
- DOF cameras on ~15% of non-chorus text layers

### Batch Processing

Double-click `OUTPUT/run_batch.command` to process all songs sequentially. This:
1. Opens After Effects if not running
2. Executes each `.jsx` script via AppleScript
3. Waits between each for AE to finish
4. Shows a macOS notification when complete

### Configuration Reference

All settings are in `LyricsVideoGenerator.__init__()`. Modify these before running:

| Setting | Default | Description |
|---|---|---|
| **Composition** | | |
| `width` | 1920 | Comp width in pixels |
| `height` | 1080 | Comp height in pixels |
| `fps` | 30 | Frames per second |
| **Text** | | |
| `font` | "Heavitas" | Font family name (must be installed) |
| `base_font_size` | 120 | Default font size in pixels |
| `min_font_scale` | 0.5 | Minimum scale factor for long text |
| `max_line_width` | 1632 (85%) | Max text width before splitting |
| `text_split_threshold` | 25 | Character count to trigger 2-line split |
| **Animation Timing** | | |
| `animation_in_frames` | 6 | Frames for entrance animation |
| `animation_out_frames` | 6 | Frames for exit animation |
| `text_gap_before_next` | 0.5s (15fr) | Gap before next text appears |
| `blink_out_min_frames` | 90 | Min duration to allow blink-out exit |
| **Chorus Groups** | | |
| `group_transition_duration` | 0.2s (6fr) | Transition between chorus layers |
| `null_exit_duration` | 0.4s (12fr) | Chorus exit slide-up duration |
| **Camera** | | |
| `camera_zoom_range` | [98, 102] | Sinusoidal zoom range (%) |
| `camera_pan_range` | 30 | Max pan offset in pixels |
| `camera_tilt_range` | 0.3 | Max rotation in degrees |
| `shake_intensity` | 5 | Camera shake pixel intensity |
| `shake_duration` | 0.5 | Shake duration in seconds |
| **Energy Detection** | | |
| `bar_duration` | 2.0 | Assumed bar duration (4 beats @ 120 BPM) |
| `low_energy_threshold` | 4 | Bars of silence to trigger energy event |
| **Mid-Duration Effects** | | |
| `mid_duration_threshold` | 2.0 | Seconds before adding mid-effect |
| `mid_zoom_range` | [120, 135] | Mid-punch zoom range (%) |
| `mid_position_range` | 150 | Mid-punch position range (px) |
| **Short Text** | | |
| `hard_inout_max_chars` | 8 | Max chars for instant in/out (no easing) |
| `hard_inout_max_duration` | 1.0 | Max seconds for instant in/out |
| **DOF Camera** | | |
| `dof_camera_probability` | 0.15 | Chance of DOF camera per text (15%) |
| `dof_camera_zoom` | 2000 | Camera zoom value |
| `dof_camera_aperture` | 300 | Aperture for DOF blur |
| `dof_camera_blur_level` | 150 | Blur level percentage |
| `dof_camera_position_drift` | 1000 | Max drift in pixels during animation |

### Animation Types

Each text layer gets a random entrance animation from this pool:

| Animation | Effect |
|---|---|
| `fadeIn` | Simple opacity fade |
| `scaleIn` | Scale from 0% to 100% + fade |
| `slideUp` | Slide up 200px + fade |
| `slideDown` | Slide down 200px + fade |
| `bounceIn` | Scale from 130% to 100% + fade |
| `slideFromLeft` | Slide from -300px + fade |
| `slideFromRight` | Slide from +300px + fade |
| `typewriter` | Character-by-character reveal |
| `wave` | Wave motion per character |
| `blurReveal` | Gaussian blur 50 to 0 + fade |
| `zoomBlur` | Scale 150% + blur + fade |
| `flipX` | 3D X-axis rotation 90 to 0 |
| `flipY` | 3D Y-axis rotation 90 to 0 |
| `glitch` | Random position jitter + fade |
| `dropShadowPulse` | Drop shadow + subtle scale |
| `extremeZoomIn` | Scale from 3000% to 100% |
| `elasticPop` | Scale 0 -> 120 -> 100 (elastic) |

Exit animations: **fade out** (default) or **blink out** (50% chance for text > 90 frames).

Each animation uses a random easing function from 30 options (10 types x 3 directions).

### Smart Features

- **Chorus Detection:** Consecutive identical lyrics are grouped under a shared null. Each new repetition triggers: zoom-out previous layer to 50%, slide null up, new layer appears at full size.
- **Energy Events:** Large gaps between lyrics (> 4 bars) trigger camera shake when lyrics resume.
- **Adaptive Font Size:** Text <= 10 chars gets 50% bigger. Text >= 25 chars splits into 2 lines at the word boundary nearest to center.
- **Staggered Multi-line:** When text splits into 2 lines, line 2 appears at the midpoint of line 1's remaining duration (individual text) or after a fixed 0.5s delay (chorus text).

---

## Tool 2: Lyrics Syncer

### <a name="syncer-overview"></a>Overview

DJ edits typically add drum intro bars before the song begins. This tool detects where vocals actually start using an acapella extraction, then shifts all LRC timestamps by the appropriate offset.

### <a name="syncer-folder-setup"></a>Folder Setup

```
my_dj_set/
  Song Name.aiff              # DJ edit (full mix with drum intro)
  Song Name.lrc               # Original song lyrics (pre-intro timing)
  acapella/
    Song Name.aiff            # Acapella of the DJ edit (same duration)
```

**Requirements:**
- The acapella must have the **same duration** as the DJ edit
- Filenames must match exactly between the edit and acapella
- Each `.aiff` must have a matching `.lrc`

### Running the Syncer

```bash
python3 sync_lyrics.py /path/to/my_dj_set
```

### How It Works

1. **Load acapella** at 22050 Hz mono
2. **Detect BPM** from the full DJ edit (first 30s)
3. **Compute RMS energy** of the acapella (first 45s), smoothed with a 0.3s window
4. **Establish noise floor** from first 1.5s (guaranteed drums-only = silence in acapella)
5. **Find vocal onset** -- first point where RMS exceeds threshold for 0.2s sustained
6. **Calculate offset** = `vocal_onset - first_lyric_timestamp`
7. **Shift all timestamps** by the offset, dropping any that go negative
8. **Write synced .lrc** preserving metadata

**Confidence metric:** The ratio of energy after vocal onset vs. before. Higher = clearer detection. A ratio of `inf` means the pre-vocal section was pure silence (ideal).

### <a name="syncer-output"></a>Output

For each processed file, the console shows:
```
[1/5] Song Name
  BPM: 128.0
  Vocal onset in acapella: 8.52s
  First lyric in .lrc: 0.24s
  Offset: +8.28s (confidence: 45.2x)
  42 lines synced (offset: +8.28s)
```

The synced `.lrc` file overwrites the original (once the output_path bug in the code is fixed -- see CODE_REVIEW.md).

---

## LRC File Format

Both tools support standard LRC format:

```
[ar:Artist Name]
[ti:Song Title]
[00:12.45]First line of lyrics
[00:15.80]Second line of lyrics
[01:02.33]Later in the song
```

Supported timestamp formats:
- `[MM:SS.xx]` -- standard (e.g., `[01:23.45]`)
- `[M:SS.xx]` -- single-digit minutes (e.g., `[1:23.45]`)
- `[MM:SS:xx]` -- colon separator variant (e.g., `[01:23:45]`)

Encoding auto-detection: UTF-8, Latin-1, CP1252, ISO-8859-1.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| "No .aiff files found" | Run the script from the folder containing your .aiff files, or check that the script's `__file__` parent is correct |
| "No se encontro archivo LRC" | Ensure the .lrc filename matches the .aiff filename exactly |
| Font not appearing in AE | Install the "Heavitas" font, or change `self.font` in the config |
| Batch script fails | Check that `AE_VERSION` matches your installed After Effects version |
| LRC not parsed | Check file encoding; the tool tries UTF-8/Latin-1/CP1252/ISO-8859-1 |
| Lyrics out of sync (syncer) | Verify the acapella is the same duration as the DJ edit |
| "No acapella/ subfolder" | Create an `acapella/` folder inside your DJ set folder with matching .aiff files |
| `NameError: output_path` | Known bug in `sync_lyrics.py:231` -- see CODE_REVIEW.md for fix |
| Text overlaps in AE | Reduce `base_font_size` or increase `text_split_threshold` |
| Animations too fast/slow | Adjust `animation_in_frames` and `animation_out_frames` |
