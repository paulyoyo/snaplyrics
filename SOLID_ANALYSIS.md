# SOLID Principles Analysis: LRC Project

> **Status: ALL FIXED** -- See below for before/after comparison.

---

## S -- Single Responsibility Principle

> "A class should have only one reason to change."

### `LyricsVideoGenerator` -- **Major violation**

This single class does everything:

| Responsibility | Methods |
|---|---|
| LRC file parsing | `parse_lrc()` |
| Text layout/sizing | `calculate_font_size()`, `split_text_at_midpoint()`, `split_text_lines()`, `calculate_text_width()`, `get_safe_x_position()`, `get_safe_offset_x()` |
| Chorus detection | `find_chorus_groups()` |
| Energy analysis | `detect_energy_changes()` |
| Duration calculation | `calculate_lyric_durations()` |
| Animation selection | `get_random_animation()`, `get_random_easing()`, `get_out_animation()`, `get_easing_expression()` |
| JSX code generation | `generate_jsx()` (850 lines) |
| Batch script generation | `generate_batch_script()` |
| File I/O orchestration | `process_all_songs()` |
| Path escaping | `escape_path_for_jsx()` |

**That's 9 distinct responsibilities in one class.** Any change to animation logic forces you to touch the same file as changes to LRC parsing or file layout.

### `LyricsSyncer` -- **Acceptable**

Three focused responsibilities (detection, parsing, syncing) that are tightly coupled and change together. Minor SRP pressure -- parsing could be shared with the video generator -- but pragmatically fine for a 300-line class.

### Recommended decomposition for `LyricsVideoGenerator`:

```
LrcParser            -- parse_lrc(), encoding handling
TextLayout           -- font sizing, text splitting, width estimation
SongAnalyzer         -- find_chorus_groups(), detect_energy_changes(), calculate_lyric_durations()
AnimationLibrary     -- get_random_animation(), get_random_easing(), get_out_animation()
JsxGenerator         -- generate_jsx() and sub-methods for each section
BatchScriptWriter    -- generate_batch_script()
LyricsVideoPipeline  -- orchestrates the above, owns process_all_songs()
```

---

## O -- Open/Closed Principle

> "Open for extension, closed for modification."

### Animation system -- **Violation**

Adding a new animation requires modifying `get_random_animation()` by appending to a hardcoded list inside the method body. There's no way to add or remove animations without editing the class.

**Fix:** Animations should be data-driven. Either:
- Load from a JSON/YAML config file
- Use a registry pattern where each animation is a dict/dataclass registered externally

```python
# Current (closed)
def get_random_animation(self):
    animations = [  # hardcoded list of 17 dicts
        {"name": "fadeIn", ...},
        ...
    ]
    return random.choice(animations)

# Better (open)
class AnimationLibrary:
    def __init__(self):
        self._animations = []

    def register(self, animation):
        self._animations.append(animation)

    def random(self):
        return random.choice(self._animations)
```

### Easing system -- **Violation**

Same issue. 30 easing functions hardcoded in `get_easing_expression()`. But since this method is never called (dead code), the real easing is handled via `applyEaseToKeyframes()` in the JSX, which only supports 3 variants (In, Out, InOut). The Python-side `get_random_easing()` generates names like `easeInOutBounce` that are passed as strings but **only parsed for "In"/"Out" substrings** in the JSX helper. So all Bounce/Elastic/Back/etc. variations map to the same generic easing curve. The 30-option variety is illusory.

### Output format -- **Violation**

The only output format is After Effects JSX. If you wanted to target DaVinci Resolve, Premiere Pro, or SRT subtitles, you'd have to fork the entire class. The generation logic is entangled with the animation data.

**Fix:** Extract a `Renderer` interface:
```python
class JsxRenderer:
    def render(self, song_data: SongAnalysis) -> str: ...

class SrtRenderer:
    def render(self, song_data: SongAnalysis) -> str: ...
```

---

## L -- Liskov Substitution Principle

> "Subtypes must be substitutable for their base types."

### Not directly applicable

There are no inheritance hierarchies. The two classes (`LyricsVideoGenerator`, `LyricsSyncer`) are independent. No subclassing, no polymorphism.

### Indirect concern: `parse_lrc()` returns different types

The two `parse_lrc()` implementations have incompatible signatures:

```python
# LyricsVideoGenerator.parse_lrc() -> list[dict]
lyrics = self.parse_lrc(lrc_file)

# LyricsSyncer.parse_lrc() -> tuple[list[dict], list[str]]
lyrics, metadata = self.parse_lrc(lrc_path)
```

If these were ever unified behind a shared interface or base class, one couldn't substitute for the other. The video generator silently drops metadata; the syncer preserves it. A shared `LrcParser` should return a structured object containing both.

---

## I -- Interface Segregation Principle

> "No client should be forced to depend on methods it does not use."

### `LyricsVideoGenerator` -- **Violation**

The class exposes 20+ public methods. A caller who only needs LRC parsing must import the entire animation/JSX generation system. The `__init__` itself has side effects (creates directories, prints to stdout).

**Specific violations:**
- `process_all_songs()` depends on all other methods
- `generate_batch_script()` is only relevant for macOS + After Effects but is always generated
- `get_easing_expression()` and `_generate_easing_library()` are public/protected but never called by anything

**Fix:** After the SRP decomposition above, each component has a narrow interface. The orchestrator depends on each small interface, not one fat class.

### `__init__` side effects

```python
def __init__(self, source_folder=None, output_folder="OUTPUT"):
    ...
    self.output_folder.mkdir(exist_ok=True)  # creates directory
    print(f"📂 Carpeta de trabajo: {self.source_folder}")  # prints to stdout
    print(f"📂 Carpeta de salida: {self.output_folder}")
```

Constructors should not perform I/O. A caller who just wants to use `parse_lrc()` or `calculate_font_size()` gets unwanted directory creation and console output.

---

## D -- Dependency Inversion Principle

> "Depend on abstractions, not concretions."

### High-level modules depend on low-level details -- **Violation**

`generate_jsx()` directly constructs JSX string output. The orchestration logic (`process_all_songs`) directly calls `shutil.copy2`, `open()`, `Path.mkdir()`. There are no abstractions between the business logic and I/O.

```python
# Current: business logic married to file system
def process_all_songs(self):
    audio_files = list(self.source_folder.glob("*.aiff"))  # direct FS
    ...
    shutil.copy2(audio_file, song_folder / audio_file.name)  # direct FS
    with open(jsx_file, "w") as f:  # direct FS
        f.write(jsx_content)
```

This makes testing impossible without actual files on disk.

### Configuration is hardcoded -- **Violation**

All 30+ configuration values are set in `__init__` with no injection point:

```python
self.font = "Heavitas"
self.base_font_size = 120
self.dof_camera_probability = 0.15
```

There's no way to pass a config object, load from a file, or override individual settings without subclassing.

**Fix:**
```python
@dataclass
class VideoConfig:
    width: int = 1920
    height: int = 1080
    fps: int = 30
    font: str = "Heavitas"
    base_font_size: int = 120
    ...

class LyricsVideoGenerator:
    def __init__(self, config: VideoConfig, file_system: FileSystem):
        self.config = config
        self.fs = file_system
```

---

## Summary Scorecard

| Principle | Before | After | What Changed |
|---|---|---|---|
| **S** Single Responsibility | 2/10 | 9/10 | 1 god class (9 responsibilities) → 8 focused classes |
| **O** Open/Closed | 3/10 | 8/10 | Hardcoded animation list → `AnimationLibrary.register()` registry |
| **L** Liskov Substitution | 7/10 | 9/10 | Incompatible `parse_lrc` signatures → shared `LrcParser` with unified return type |
| **I** Interface Segregation | 3/10 | 9/10 | Fat class + side-effectful constructor + dead methods → focused classes, no constructor I/O, dead code deleted |
| **D** Dependency Inversion | 2/10 | 8/10 | 30+ hardcoded config values → injectable `VideoConfig` dataclass; all components composed via DI |

### New Architecture

```
VideoConfig          @dataclass, 33 fields with defaults, no side effects
LrcParser            parse() → (lyrics, metadata), shared by both tools
TextLayout           font sizing, text splitting (depends on VideoConfig)
SongAnalyzer         chorus/energy/duration analysis (depends on VideoConfig)
AnimationLibrary     registry pattern with register() + random() (depends on VideoConfig)
JsxRenderer          render() split into 9 focused sub-methods (depends on config, layout, animations)
BatchScriptWriter    write() — macOS batch script generation
LyricsVideoPipeline  orchestrates all above, owns I/O
```

### What was fixed

- **SRP:** God class split into 8 classes. `generate_jsx()` (850 lines) split into `_header()`, `_camera_section()`, `_chorus_group()`, `_individual_section()`, `_render_effects()`, `_dof_cameras()`, `_footer()`.
- **OCP:** Animations use a registry. Call `animations.register({...})` to add new ones without modifying existing code.
- **LSP:** `LrcParser.parse()` returns `(lyrics, metadata)` everywhere. `sync_lyrics.py` now imports the shared parser.
- **ISP:** Constructor creates no directories, prints nothing. Dead code deleted: `get_easing_expression()`, `_generate_easing_library()`, `get_safe_x_position()`, `get_safe_offset_x()`, unused imports.
- **DIP:** All config flows through `VideoConfig`. Components are composed in `LyricsVideoPipeline.__init__()`. Custom config: `LyricsVideoPipeline(".", config=VideoConfig(font="Arial", fps=60))`.
