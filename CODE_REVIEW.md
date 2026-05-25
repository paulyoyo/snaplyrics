# Code Review: LRC Lyrics Video Generator & Sync Tool

**Date:** 2026-05-23
**Files reviewed:**
- `canciones/lrc.py` (1588 lines) - After Effects JSX generator
- `perreo/lrc.py` (1588 lines) - Identical copy
- `sync_lyrics.py` (327 lines) - LRC timestamp syncer

---

## Critical Bugs

### 1. `output_path` undefined in `sync_file()` (sync_lyrics.py:231)

```python
# Line 231 - output_path is used but never defined
self.write_lrc(synced, metadata, output_path)  # NameError at runtime
```

The method receives `edit_path`, `lrc_path`, and `acapella_path` but never constructs `output_path`. Likely intended:

```python
output_path = lrc_path  # overwrite original
# or
output_path = lrc_path.with_stem(lrc_path.stem + "_synced")
```

**This will crash every time `sync_file()` processes a valid file.**

### 2. `canciones/lrc.py` and `perreo/lrc.py` are byte-identical copies

100% duplicated code. If a bug is fixed in one, the other stays broken. Should be a single shared module with per-folder invocation.

---

## Unused / Dead Code

| Location | What | Impact |
|---|---|---|
| `canciones/lrc.py:360-405` | `get_easing_expression()` - 30 easing functions dict | Never called anywhere. ~45 lines of dead code. |
| `canciones/lrc.py:1402-1410` | `_generate_easing_library()` | Never called. Returns a stub comment. |
| `canciones/lrc.py:235-257` | `get_safe_x_position()`, `get_safe_offset_x()` | Defined but never invoked. |
| `canciones/lrc.py:1` | `import json, math, os` | Imported but never used. |

---

## Code Quality Issues

### 3. `generate_jsx()` is ~850 lines long

This single method (lines 534-1400) generates the entire After Effects script. It's the longest method I've encountered in a single-class project. It handles:
- Chorus group creation
- Individual text creation
- Camera null setup
- DOF camera generation
- Shake/energy events
- All animation types
- File save

**Recommendation:** Break into sub-methods: `_generate_chorus_group()`, `_generate_individual_text()`, `_generate_camera_setup()`, `_generate_dof_cameras()`.

### 4. Duplicate pan keyframe generation (canciones/lrc.py:667-679)

The JSX loop on line 667 populates `panKeyTimes` in JavaScript, but then Python also generates keyframes on lines 673-679. The `panKeyTimes` array in JSX is populated but **never used** -- it's dead JS code. The actual keyframes come from the Python loop.

### 5. Imports inside loops / methods

```python
# Line 1465 - inside for loop, re-imported every iteration
import shutil
shutil.copy2(audio_file, song_folder / audio_file.name)

# Line 1576 - inside method
import stat
```

Should be at module level.

### 6. LRC parsing differs between the two parsers

`sync_lyrics.py:parse_lrc()` processes line-by-line with metadata extraction and returns `(lyrics, metadata)`.
`canciones/lrc.py:parse_lrc()` uses `re.findall()` on entire content and returns only `lyrics`.

The `canciones` version has a subtle bug: it tries patterns sequentially and **breaks on the first match**, meaning if a file has mixed formats (e.g., `[MM:SS.xx]` and `[M:SS.xx]`), the strict `\d{2}` pattern will silently skip single-digit-minute lines. The `sync_lyrics.py` version handles this correctly by trying all patterns per-line.

### 7. No `requirements.txt`

`sync_lyrics.py` depends on `librosa` and `numpy`, but there's no requirements file documenting this.

---

## Potential Issues

### 8. Path injection in generated scripts

Song filenames are interpolated directly into JSX and bash scripts without sanitization:

```python
# canciones/lrc.py:567 - song name goes straight into JSX
jsx_content = f"""var projectName = "{project_name}";"""
```

A filename like `My Song"; alert("pwned");//` would break the JSX. The `escape_path_for_jsx()` method handles paths but `project_name` (from `audio_file.stem`) is not escaped.

### 9. Hardcoded After Effects version in batch script

```bash
AE_VERSION="2025"  # Line 1503
```

The generated `run_batch.command` hardcodes AE 2025. Should be configurable or auto-detected.

### 10. Text width estimation is rough

```python
def calculate_text_width(self, text, font_size):
    return len(text) * font_size * 0.6  # Line 233
```

This assumes all characters are 0.6x the font size wide. Works for Latin alphabets with Heavitas, but will be wrong for CJK characters, emoji, or variable-width fonts. Acceptable given the use case (DJ lyrics in Spanish/English) but worth noting.

### 11. BPM detection returns array inconsistently

```python
tempo, _ = librosa.beat.beat_track(y=y_edit, sr=sr)
if isinstance(tempo, np.ndarray):
    tempo = tempo[0]  # Lines 52-54
```

This is a workaround for librosa version differences. Works, but fragile.

---

## Architecture Summary

```
lrc/
  canciones/lrc.py    # LyricsVideoGenerator - LRC -> After Effects JSX
  perreo/lrc.py       # (identical copy)
  sync_lyrics.py      # LyricsSyncer - Shift LRC timestamps to DJ edits
```

The project is two independent tools sharing the `.lrc` format:
1. **Video Generator** (`lrc.py`): Reads `.lrc` + `.aiff`, generates After Effects `.jsx` scripts with animated text layers, chorus grouping, camera motion, DOF effects, and a batch runner.
2. **Lyrics Syncer** (`sync_lyrics.py`): Uses librosa to detect vocal onset in acapella files, calculates time offset, and rewrites `.lrc` timestamps.

---

## Recommendations (Priority Order)

1. **Fix the `output_path` bug** in `sync_lyrics.py:231` -- this is a runtime crash
2. **Deduplicate** `canciones/lrc.py` and `perreo/lrc.py` into a shared module
3. **Add `requirements.txt`** with `librosa` and `numpy`
4. **Remove dead code** (`get_easing_expression`, `_generate_easing_library`, unused imports)
5. **Sanitize `project_name`** before interpolating into JSX strings
6. **Move imports** to module level
7. **Break up `generate_jsx()`** into smaller methods (long-term maintainability)
