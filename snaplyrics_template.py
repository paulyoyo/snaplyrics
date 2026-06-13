"""
SnapLyrics Template Modifier — Full pipeline + AE template injection.

Adapted for "ALL KINETIC TITLES" style AE templates with structure:
    Title XX (folder)
        Edit Text (folder)
            TEXT XX (comp)
            TEXT MODULE XX (comp)

Original Title bins are NEVER modified — they are duplicated per lyric.
Duplicated TEXT MODULE comps are renamed with the lyric text for visual
feedback in the AE timeline. A new "render" comp is created matching
the audio duration with all lyrics placed sequentially.

Usage:
    python snaplyrics_template.py <template.aep> <folder_with_audio>
    python snaplyrics_template.py <template.aep> <folder> --slots 8

Also available via the main CLI:
    python snaplyrics.py <folder> --template <template.aep>
"""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path

from snaplyrics import (
    VideoConfig, LrcParser, LrcSyncer, LrcWriter, LyricsFetcher,
    SongAnalyzer, DrumAnalyzer, TextLayout,
    _find_audio_files, _split_lyrics_into_blocks,
    _hex, _RESET, _BOLD, _LILAC, _SNOW, _GOLD, _WISTERIA, _RED,
    _progress_bar, _HAS_LIBROSA, AUDIO_EXTENSIONS,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Template config
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class TemplateConfig:
    """Describes the naming convention of an AE titles template.

    Two layouts supported:

    "kinetic" (nested — ALL KINETIC TITLES style):
        Title XX (folder)
            Edit Text (folder)
                TEXT XX (comp) — the text source
                TEXT MODULE XX (comp) — the animated module

    "flat" (direct — Stomp Lyrics style):
        1. Placeholders (folder)
            Text Placeholder 1 (comp — text + animation baked in)
            Text Placeholder 2
            ...
    """
    # Layout: "kinetic" (nested folders) or "flat" (comps in one folder)
    layout: str = "kinetic"

    # Folder containing all title bins (empty string = project root)
    root_folder: str = ""

    # ── Kinetic layout patterns ──
    title_folder_pattern: str = "Title {n}"
    edit_text_folder: str = "Edit Text"
    text_comp_pattern: str = "TEXT {n}"
    text_module_pattern: str = "TEXT MODULE {n}"

    # ── Flat layout patterns ──
    # comp_pattern: the comp name pattern (comp IS the module)
    flat_comp_pattern: str = "Text Placeholder {n}"

    # Render comp
    render_comp_name: str = "render"

    # ── Main comp reuse (Stomp) ──
    # When True, uses existing Main comp instead of creating a new render comp
    use_main_comp: bool = False
    main_comp_name: str = "Main"
    main_comp_folder: str = "2. Render"

    # Timing: "in" animation offset — lyric starts this many seconds
    # BEFORE its sync time so the animation completes on beat
    anim_in_offset: float = 1.0
    # Duration multiplier (0.5 = half duration between lyrics)
    duration_multiplier: float = 0.5

    # Text overflow: max characters per line before wrapping
    max_chars_per_line: int = 20

    existing_slots: int = 9
    pad_width: int = 2

    @classmethod
    def stomp(cls, slots: int = 5) -> "TemplateConfig":
        """Preset for Stomp Lyrics style templates (videohive-38665595)."""
        return cls(
            layout="flat",
            root_folder="1. Placeholders",
            flat_comp_pattern="Text Placeholder {n}",
            render_comp_name="render",
            existing_slots=slots,
            pad_width=1,
            anim_in_offset=1.0,
            duration_multiplier=0.5,
            max_chars_per_line=20,
            use_main_comp=True,
            main_comp_name="Main",
            main_comp_folder="2. Render",
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# JSX Template Renderer
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TemplateRenderer:
    """Generates ExtendScript (JSX) that modifies an AE kinetic titles project.

    Workflow:
    1. Open the .aep template
    2. Find the 8 original Title bins (used as style references only)
    3. For each lyric line, duplicate a Title bin (cycling 1..8)
    4. In each duplicate: replace text in TEXT comp, rename TEXT MODULE with lyric
    5. Create a "render" comp matching audio duration
    6. Place all duplicated TEXT MODULE comps sequentially on the render timeline
    """

    def __init__(self, config: TemplateConfig | None = None):
        self.c = config or TemplateConfig()

    @staticmethod
    def _wrap_text(text: str, max_chars: int) -> str:
        """Wrap text at word boundaries to fit within max_chars per line."""
        words = text.split()
        if not words:
            return text
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if len(current_line) + 1 + len(word) <= max_chars:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return "\n".join(lines)

    @staticmethod
    def _esc(text: str) -> str:
        return (text.replace("\\", "\\\\").replace('"', '\\"')
                    .replace("'", "\\'").replace("\n", "\\n"))

    @staticmethod
    def _esc_path(path) -> str:
        return str(path).replace("\\", "/").replace('"', '\\"')

    def render(self, aep_path: Path, audio_path: Path,
               lyrics: list[dict], song_name: str,
               output_folder: Path) -> str:
        """Generate JSX content to modify the AE template with lyrics.

        lyrics: list of {"time": float, "text": str} — already synced + split
        """
        total = len(lyrics)

        # Comp duration: last lyric + 5s buffer
        comp_duration = (lyrics[-1]["time"] + 5.0) if lyrics else 30.0

        # Calculate display duration per lyric (halved, with anim-in offset)
        c = self.c
        for i, lyric in enumerate(lyrics):
            if i < len(lyrics) - 1:
                gap = lyrics[i + 1]["time"] - lyric["time"]
            else:
                gap = 3.0
            lyric["duration"] = gap * c.duration_multiplier

            # Wrap long text into multiple lines
            lyric["text"] = self._wrap_text(lyric["text"], c.max_chars_per_line)
            # Flag if text is likely to overflow even after wrapping
            longest_line = max(len(line) for line in lyric["text"].split("\\n")) if lyric["text"] else 0
            lyric["needs_pan"] = longest_line > c.max_chars_per_line

        aep_jsx = self._esc_path(aep_path.absolute())
        audio_jsx = self._esc_path(audio_path.absolute())
        output_jsx = self._esc_path(output_folder.absolute())

        parts = [
            self._header(aep_jsx, audio_jsx, song_name, comp_duration),
            self._find_existing_items(),
            self._duplicate_and_inject(lyrics),
            self._build_render_comp(lyrics, audio_jsx, comp_duration),
            self._save_and_close(output_jsx, song_name),
            self._footer(),
        ]
        return "".join(parts)

    # ── JSX sections ──────────────────────────────────────────

    def _header(self, aep_path: str, audio_path: str,
                song_name: str, comp_duration: float) -> str:
        return f"""// SnapLyrics Template Modifier — Kinetic Titles
// Song: {song_name}
// Auto-generated — run inside After Effects

(function() {{
    app.beginUndoGroup("SnapLyrics - {self._esc(song_name)}");

    try {{

    // =============================================
    // CONFIG
    // =============================================
    var songName = "{self._esc(song_name)}";
    var aepPath = "{aep_path}";
    var audioPath = "{audio_path}";
    var compDuration = {comp_duration:.3f};

    // =============================================
    // OPEN TEMPLATE
    // =============================================
    var templateFile = new File(aepPath);
    if (!templateFile.exists) {{
        alert("Template not found:\\n" + aepPath);
        return;
    }}
    app.open(templateFile);
    var proj = app.project;

"""

    def _find_existing_items(self) -> str:
        c = self.c
        # Common helpers used by both layouts
        common = f"""
    // =============================================
    // FIND EXISTING TEMPLATE ITEMS
    // =============================================

    function findItem(name, type) {{
        for (var i = 1; i <= proj.numItems; i++) {{
            var item = proj.item(i);
            if (item.name === name) {{
                if (type === "comp" && item instanceof CompItem) return item;
                if (type === "folder" && item instanceof FolderItem) return item;
                if (!type) return item;
            }}
        }}
        return null;
    }}

    function findItemInFolder(folder, name, type) {{
        for (var i = 1; i <= folder.numItems; i++) {{
            var item = folder.item(i);
            if (item.name === name) {{
                if (type === "comp" && item instanceof CompItem) return item;
                if (type === "folder" && item instanceof FolderItem) return item;
                if (!type) return item;
            }}
        }}
        return null;
    }}

    // Find root container (folder or project root)
    var rootFolderName = "{c.root_folder}";
    var rootFolder = null;
    if (rootFolderName !== "") {{
        rootFolder = findItem(rootFolderName, "folder");
        if (!rootFolder) {{
            alert("Cannot find '" + rootFolderName + "' folder in template.");
            return;
        }}
    }}

    // Search function: looks in rootFolder if set, otherwise project root
    function findInRoot(name, type) {{
        if (rootFolder) return findItemInFolder(rootFolder, name, type);
        return findItem(name, type);
    }}

"""
        if c.layout == "flat":
            result = common + self._find_flat_items()
            if c.use_main_comp:
                result += self._find_main_comp_layers()
            return result
        return common + self._find_kinetic_items()

    def _find_flat_items(self) -> str:
        """Find items in flat layout: comps directly in a folder."""
        c = self.c
        return f"""
    // ── Flat layout: comps directly in root folder ──
    var sourceTextComps = {{}};
    var sourceModuleComps = {{}};  // same as textComps in flat layout

    for (var slot = 1; slot <= {c.existing_slots}; slot++) {{
        var pad = ("0" + slot).slice(-{c.pad_width});
        // For single-digit pad_width, use raw number
        if ({c.pad_width} <= 1) pad = "" + slot;
        var compName = "{c.flat_comp_pattern}".replace("{{n}}", pad);

        var comp = findInRoot(compName, "comp");
        if (!comp) {{
            alert("Missing comp: " + compName);
            return;
        }}
        // In flat layout, the comp IS both the text source and the module
        sourceTextComps[slot] = comp;
        sourceModuleComps[slot] = comp;
    }}

    // Measure original text length in each source comp
    var styleTextLengths = {{}};
    for (var s = 1; s <= {c.existing_slots}; s++) {{
        var srcComp = sourceTextComps[s];
        var origLen = 0;
        // Search all layers (flat comps may nest text in precomps)
        for (var tl = 1; tl <= srcComp.numLayers; tl++) {{
            var tlyr = srcComp.layer(tl);
            if (tlyr instanceof TextLayer) {{
                origLen = tlyr.property("Source Text").value.text.length;
                break;
            }}
        }}
        styleTextLengths[s] = origLen;
        $.writeln("Style " + s + " (" + srcComp.name + ") text length: " + origLen);
    }}

    // Build sorted array for matching lyric length → style
    var styleLengthPairs = [];
    for (var sl = 1; sl <= {c.existing_slots}; sl++) {{
        styleLengthPairs.push({{slot: sl, len: styleTextLengths[sl]}});
    }}
    styleLengthPairs.sort(function(a, b) {{ return a.len - b.len; }});

    function pickStyleForLength(lyricLen) {{
        var best = styleLengthPairs[0].slot;
        var bestDiff = Math.abs(lyricLen - styleLengthPairs[0].len);
        for (var k = 1; k < styleLengthPairs.length; k++) {{
            var diff = Math.abs(lyricLen - styleLengthPairs[k].len);
            if (diff < bestDiff) {{
                bestDiff = diff;
                best = styleLengthPairs[k].slot;
            }}
        }}
        return best;
    }}

    // ── Analyze "in" animation per style ──
    // For flat comps: read the comp's layers for transform/animator KFs
    var styleAnimData = {{}};

    for (var sa = 1; sa <= {c.existing_slots}; sa++) {{
        var srcComp = sourceTextComps[sa];
        var anim = {{
            posX: 0, posY: 0,
            scaleX: 0, scaleY: 0,
            rotation: 0,
            opacity: 0,
            duration: 0.5
        }};

        // Check ALL layers in the comp (text, shapes, precomps)
        for (var atl = 1; atl <= srcComp.numLayers; atl++) {{
            var aLyr = srcComp.layer(atl);

            // ── Transform keyframes ──
            try {{
                var tPos = aLyr.property("Position");
                if (tPos && tPos.numKeys >= 2) {{
                    var pStart = tPos.keyValue(1);
                    var pEnd = tPos.keyValue(tPos.numKeys);
                    if (Math.abs(pStart[0] - pEnd[0]) > Math.abs(anim.posX)) anim.posX = pStart[0] - pEnd[0];
                    if (Math.abs(pStart[1] - pEnd[1]) > Math.abs(anim.posY)) anim.posY = pStart[1] - pEnd[1];
                    var tDur = tPos.keyTime(tPos.numKeys) - tPos.keyTime(1);
                    if (tDur > anim.duration) anim.duration = tDur;
                }}
            }} catch(ep) {{}}

            try {{
                var tScale = aLyr.property("Scale");
                if (tScale && tScale.numKeys >= 2) {{
                    var sStart = tScale.keyValue(1);
                    var sEnd = tScale.keyValue(tScale.numKeys);
                    if (Math.abs(sStart[0] - sEnd[0]) > Math.abs(anim.scaleX)) anim.scaleX = sStart[0] - sEnd[0];
                    if (Math.abs(sStart[1] - sEnd[1]) > Math.abs(anim.scaleY)) anim.scaleY = sStart[1] - sEnd[1];
                    var sDur = tScale.keyTime(tScale.numKeys) - tScale.keyTime(1);
                    if (sDur > anim.duration) anim.duration = sDur;
                }}
            }} catch(es) {{}}

            try {{
                var tRot = aLyr.property("Rotation");
                if (tRot && tRot.numKeys >= 2) {{
                    if (Math.abs(tRot.keyValue(1) - tRot.keyValue(tRot.numKeys)) > Math.abs(anim.rotation)) {{
                        anim.rotation = tRot.keyValue(1) - tRot.keyValue(tRot.numKeys);
                    }}
                    var rDur = tRot.keyTime(tRot.numKeys) - tRot.keyTime(1);
                    if (rDur > anim.duration) anim.duration = rDur;
                }}
            }} catch(er) {{}}

            try {{
                var tOpac = aLyr.property("Opacity");
                if (tOpac && tOpac.numKeys >= 2) {{
                    anim.opacity = tOpac.keyValue(1) - tOpac.keyValue(tOpac.numKeys);
                    var oDur = tOpac.keyTime(tOpac.numKeys) - tOpac.keyTime(1);
                    if (oDur > anim.duration) anim.duration = oDur;
                }}
            }} catch(eo) {{}}

            // ── Text animators (only on TextLayers) ──
            if (!(aLyr instanceof TextLayer)) continue;
            try {{
                var textProp = aLyr.property("ADBE Text Properties");
                var animators = textProp.property("ADBE Text Animators");
                if (animators && animators.numProperties > 0) {{
                    for (var ai = 1; ai <= animators.numProperties; ai++) {{
                        var animator = animators.property(ai);
                        var aprops = animator.property("ADBE Text Animator Properties");
                        try {{
                            var aPos = aprops.property("ADBE Text Position 3D");
                            if (aPos) {{
                                var apVal = aPos.value;
                                if (Math.abs(apVal[0]) > Math.abs(anim.posX)) anim.posX = apVal[0];
                                if (Math.abs(apVal[1]) > Math.abs(anim.posY)) anim.posY = apVal[1];
                            }}
                        }} catch(ep2) {{}}
                        try {{
                            var aScl = aprops.property("ADBE Text Scale 3D");
                            if (aScl) {{ anim.scaleX = aScl.value[0] - 100; anim.scaleY = aScl.value[1] - 100; }}
                        }} catch(es2) {{}}
                        try {{
                            var aRotZ = aprops.property("ADBE Text Rotation");
                            if (aRotZ && Math.abs(aRotZ.value) > Math.abs(anim.rotation)) anim.rotation = aRotZ.value;
                        }} catch(er2) {{}}
                        try {{
                            var aOpac = aprops.property("ADBE Text Opacity");
                            if (aOpac) anim.opacity = aOpac.value - 100;
                        }} catch(eo2) {{}}
                        try {{
                            var selectors = animator.property("ADBE Text Selectors");
                            if (selectors && selectors.numProperties > 0) {{
                                var sel = selectors.property(1);
                                try {{ var so = sel.property("ADBE Text Percent Offset"); if (so && so.numKeys >= 2) {{ var sd = so.keyTime(so.numKeys) - so.keyTime(1); if (sd > anim.duration) anim.duration = sd; }} }} catch(e1) {{}}
                                try {{ var ss = sel.property("ADBE Text Percent Start"); if (ss && ss.numKeys >= 2) {{ var sd2 = ss.keyTime(ss.numKeys) - ss.keyTime(1); if (sd2 > anim.duration) anim.duration = sd2; }} }} catch(e2) {{}}
                                try {{ var se = sel.property("ADBE Text Percent End"); if (se && se.numKeys >= 2) {{ var sd3 = se.keyTime(se.numKeys) - se.keyTime(1); if (sd3 > anim.duration) anim.duration = sd3; }} }} catch(e3) {{}}
                            }}
                        }} catch(esel) {{}}
                    }}
                }}
            }} catch(etxt) {{}}
        }}

        if (anim.posX === 0 && anim.posY === 0 && anim.scaleX === 0 && anim.rotation === 0) {{
            anim.posY = -50;
            anim.opacity = -100;
        }}

        styleAnimData[sa] = anim;
        $.writeln("Style " + sa + " in-anim: pos(" + anim.posX.toFixed(0) + "," + anim.posY.toFixed(0)
            + ") scale(" + anim.scaleX.toFixed(0) + "," + anim.scaleY.toFixed(0)
            + ") rot(" + anim.rotation.toFixed(1) + ") opac(" + anim.opacity.toFixed(0)
            + ") dur(" + anim.duration.toFixed(2) + "s)");
    }}

    $.writeln("Found {c.existing_slots} source comps (flat layout).");

"""

    def _find_main_comp_layers(self) -> str:
        """Find the existing Main comp and identify template layers for duplication."""
        c = self.c
        return f"""
    // =============================================
    // FIND MAIN COMP TEMPLATE LAYERS
    // =============================================

    var mainCompFolder = findItem("{c.main_comp_folder}", "folder");
    if (!mainCompFolder) {{
        alert("Cannot find '{c.main_comp_folder}' folder in template.");
        return;
    }}
    var mainComp = findItemInFolder(mainCompFolder, "{c.main_comp_name}", "comp");
    if (!mainComp) {{
        alert("Cannot find '{c.main_comp_name}' comp in '{c.main_comp_folder}' folder.");
        return;
    }}

    // Identify template layers: those whose source matches a Text Placeholder comp
    var templateLayerRefs = [];
    for (var ml = 1; ml <= mainComp.numLayers; ml++) {{
        var mLyr = mainComp.layer(ml);
        if (!mLyr.source) continue;
        for (var ts = 1; ts <= {c.existing_slots}; ts++) {{
            if (mLyr.source === sourceTextComps[ts]) {{
                templateLayerRefs.push(mLyr);
                break;
            }}
        }}
    }}

    if (templateLayerRefs.length === 0) {{
        alert("No template layers found in Main comp referencing Text Placeholders.");
        return;
    }}

    $.writeln("Main comp: " + mainComp.name + " (" + mainComp.numLayers + " layers, "
        + templateLayerRefs.length + " template layers)");

"""

    def _find_kinetic_items(self) -> str:
        """Find items in kinetic layout: nested Title > Edit Text > TEXT / TEXT MODULE."""
        c = self.c
        return f"""
    // ── Kinetic layout: nested folder structure ──
    var sourceTitleFolders = {{}};
    var sourceTextComps = {{}};
    var sourceModuleComps = {{}};

    for (var slot = 1; slot <= {c.existing_slots}; slot++) {{
        var pad = ("0" + slot).slice(-{c.pad_width});
        var titleName = "{c.title_folder_pattern}".replace("{{n}}", pad);
        var textName = "{c.text_comp_pattern}".replace("{{n}}", pad);
        var moduleName = "{c.text_module_pattern}".replace("{{n}}", pad);

        var titleFolder = findInRoot(titleName, "folder");
        if (!titleFolder) {{
            alert("Missing folder: " + titleName);
            return;
        }}
        sourceTitleFolders[slot] = titleFolder;

        // Find Edit Text subfolder
        var editFolder = findItemInFolder(titleFolder, "{c.edit_text_folder}", "folder");
        if (!editFolder) {{
            alert("Missing 'Edit Text' folder in " + titleName);
            return;
        }}

        var textComp = findItemInFolder(editFolder, textName, "comp");
        if (!textComp) {{
            alert("Missing comp: " + textName + " in " + titleName);
            return;
        }}
        sourceTextComps[slot] = textComp;

        // TEXT MODULE is directly inside Title folder, NOT in Edit Text
        var moduleComp = findItemInFolder(titleFolder, moduleName, "comp");
        if (!moduleComp) {{
            alert("Missing comp: " + moduleName + " in " + titleName);
            return;
        }}
        sourceModuleComps[slot] = moduleComp;
    }}

    // Measure original text length in each source TEXT comp
    var styleTextLengths = {{}};
    for (var s = 1; s <= {c.existing_slots}; s++) {{
        var srcComp = sourceTextComps[s];
        var origLen = 0;
        for (var tl = 1; tl <= srcComp.numLayers; tl++) {{
            var tlyr = srcComp.layer(tl);
            if (tlyr instanceof TextLayer) {{
                origLen = tlyr.property("Source Text").value.text.length;
                break;
            }}
        }}
        styleTextLengths[s] = origLen;
        $.writeln("Style " + s + " original text length: " + origLen);
    }}

    // Build sorted array of [slot, length] for matching
    var styleLengthPairs = [];
    for (var sl = 1; sl <= {c.existing_slots}; sl++) {{
        styleLengthPairs.push({{slot: sl, len: styleTextLengths[sl]}});
    }}
    styleLengthPairs.sort(function(a, b) {{ return a.len - b.len; }});

    // Pick the best style for a given lyric length
    function pickStyleForLength(lyricLen) {{
        var best = styleLengthPairs[0].slot;
        var bestDiff = Math.abs(lyricLen - styleLengthPairs[0].len);
        for (var k = 1; k < styleLengthPairs.length; k++) {{
            var diff = Math.abs(lyricLen - styleLengthPairs[k].len);
            if (diff < bestDiff) {{
                bestDiff = diff;
                best = styleLengthPairs[k].slot;
            }}
        }}
        return best;
    }}

    // =============================================
    // ANALYZE "IN" ANIMATION PER STYLE
    // Reads text animators + transform keyframes from each TEXT comp
    // to determine direction, offset, and duration of the "in" anim.
    // =============================================

    var styleAnimData = {{}};

    for (var sa = 1; sa <= {c.existing_slots}; sa++) {{
        var srcComp = sourceTextComps[sa];
        var anim = {{
            posX: 0, posY: 0,       // position offset (from → rest)
            scaleX: 0, scaleY: 0,   // scale offset (delta from 100%)
            rotation: 0,             // rotation offset degrees
            opacity: 0,             // opacity offset (delta from 100)
            duration: 0.5            // animation duration in seconds
        }};

        for (var atl = 1; atl <= srcComp.numLayers; atl++) {{
            var aLyr = srcComp.layer(atl);
            if (!(aLyr instanceof TextLayer)) continue;

            // ── 1. Check TRANSFORM keyframes (layer-level) ──
            var tPos = aLyr.property("Position");
            if (tPos && tPos.numKeys >= 2) {{
                var pStart = tPos.keyValue(1);
                var pEnd = tPos.keyValue(tPos.numKeys);
                anim.posX = pStart[0] - pEnd[0];
                anim.posY = pStart[1] - pEnd[1];
                var tDur = tPos.keyTime(tPos.numKeys) - tPos.keyTime(1);
                if (tDur > anim.duration) anim.duration = tDur;
            }}

            var tScale = aLyr.property("Scale");
            if (tScale && tScale.numKeys >= 2) {{
                var sStart = tScale.keyValue(1);
                var sEnd = tScale.keyValue(tScale.numKeys);
                anim.scaleX = sStart[0] - sEnd[0];
                anim.scaleY = sStart[1] - sEnd[1];
                var sDur = tScale.keyTime(tScale.numKeys) - tScale.keyTime(1);
                if (sDur > anim.duration) anim.duration = sDur;
            }}

            var tRot = aLyr.property("Rotation");
            if (tRot && tRot.numKeys >= 2) {{
                anim.rotation = tRot.keyValue(1) - tRot.keyValue(tRot.numKeys);
                var rDur = tRot.keyTime(tRot.numKeys) - tRot.keyTime(1);
                if (rDur > anim.duration) anim.duration = rDur;
            }}

            var tOpac = aLyr.property("Opacity");
            if (tOpac && tOpac.numKeys >= 2) {{
                anim.opacity = tOpac.keyValue(1) - tOpac.keyValue(tOpac.numKeys);
                var oDur = tOpac.keyTime(tOpac.numKeys) - tOpac.keyTime(1);
                if (oDur > anim.duration) anim.duration = oDur;
            }}

            // ── 2. Check TEXT ANIMATORS (per-character "in" presets) ──
            try {{
                var textProp = aLyr.property("ADBE Text Properties");
                var animators = textProp.property("ADBE Text Animators");
                if (animators && animators.numProperties > 0) {{
                    for (var ai = 1; ai <= animators.numProperties; ai++) {{
                        var animator = animators.property(ai);
                        var aprops = animator.property("ADBE Text Animator Properties");

                        // Position offset from text animator
                        try {{
                            var aPos = aprops.property("ADBE Text Position 3D");
                            if (aPos) {{
                                var apVal = aPos.value;
                                if (Math.abs(apVal[0]) > Math.abs(anim.posX)) anim.posX = apVal[0];
                                if (Math.abs(apVal[1]) > Math.abs(anim.posY)) anim.posY = apVal[1];
                            }}
                        }} catch(ep) {{}}

                        // Scale offset from text animator
                        try {{
                            var aScl = aprops.property("ADBE Text Scale 3D");
                            if (aScl) {{
                                var asVal = aScl.value;
                                anim.scaleX = asVal[0] - 100;
                                anim.scaleY = asVal[1] - 100;
                            }}
                        }} catch(es) {{}}

                        // Rotation from text animator
                        try {{
                            var aRotZ = aprops.property("ADBE Text Rotation");
                            if (aRotZ && Math.abs(aRotZ.value) > Math.abs(anim.rotation)) {{
                                anim.rotation = aRotZ.value;
                            }}
                        }} catch(er) {{}}

                        // Opacity from text animator
                        try {{
                            var aOpac = aprops.property("ADBE Text Opacity");
                            if (aOpac) {{
                                anim.opacity = aOpac.value - 100;
                            }}
                        }} catch(eo) {{}}

                        // Duration from selector offset keyframes
                        try {{
                            var selectors = animator.property("ADBE Text Selectors");
                            if (selectors && selectors.numProperties > 0) {{
                                var sel = selectors.property(1);
                                var selOffset = sel.property("ADBE Text Percent Offset");
                                if (selOffset && selOffset.numKeys >= 2) {{
                                    var selDur = selOffset.keyTime(selOffset.numKeys) - selOffset.keyTime(1);
                                    if (selDur > anim.duration) anim.duration = selDur;
                                }}
                                // Also check Start/End for duration
                                var selStart = sel.property("ADBE Text Percent Start");
                                if (selStart && selStart.numKeys >= 2) {{
                                    var ssDur = selStart.keyTime(selStart.numKeys) - selStart.keyTime(1);
                                    if (ssDur > anim.duration) anim.duration = ssDur;
                                }}
                                var selEnd = sel.property("ADBE Text Percent End");
                                if (selEnd && selEnd.numKeys >= 2) {{
                                    var seDur = selEnd.keyTime(selEnd.numKeys) - selEnd.keyTime(1);
                                    if (seDur > anim.duration) anim.duration = seDur;
                                }}
                            }}
                        }} catch(esel) {{}}
                    }}
                }}
            }} catch(etxt) {{}}

            break; // only first text layer
        }}

        // If no movement detected, default to a fade-slide-down
        if (anim.posX === 0 && anim.posY === 0 && anim.scaleX === 0 && anim.rotation === 0) {{
            anim.posY = -50;
            anim.opacity = -100;
        }}

        styleAnimData[sa] = anim;
        $.writeln("Style " + sa + " in-anim: pos(" + anim.posX.toFixed(0) + "," + anim.posY.toFixed(0)
            + ") scale(" + anim.scaleX.toFixed(0) + "," + anim.scaleY.toFixed(0)
            + ") rot(" + anim.rotation.toFixed(1) + ") opac(" + anim.opacity.toFixed(0)
            + ") dur(" + anim.duration.toFixed(2) + "s)");
    }}

    $.writeln("Found {c.existing_slots} original Title bins (style references).");

"""

    def _duplicate_and_inject(self, lyrics: list[dict]) -> str:
        c = self.c
        total = len(lyrics)

        # Build the lyric text array for JS
        lyric_texts = []
        for lyric in lyrics:
            lyric_texts.append(f'        "{self._esc(lyric["text"])}"')
        lyrics_array_js = ",\n".join(lyric_texts)

        header = f"""
    // =============================================
    // DUPLICATE & INJECT LYRICS
    // Original comps are NEVER touched — only duplicated.
    // =============================================

    var totalLyrics = {total};
    var lyricTexts = [
{lyrics_array_js}
    ];

    // Create a folder for all generated lyric comps
    var lyricsFolder = proj.items.addFolder(songName + " — Lyrics");
    if (rootFolder) lyricsFolder.parentFolder = rootFolder;

    var lyricModules = [];
    var lyricStyles = [];

"""
        if c.layout == "flat":
            return header + self._inject_flat(total)
        return header + self._inject_kinetic(total)

    def _inject_flat(self, total: int) -> str:
        """Flat layout: each comp IS both text source and module.
        Duplicate the comp, find text layers inside, replace text."""
        c = self.c
        return f"""
    // ── Flat layout: duplicate comp, replace text inside ──
    for (var idx = 0; idx < totalLyrics; idx++) {{
        var lyricText = lyricTexts[idx];
        var sourceSlot = pickStyleForLength(lyricText.length);
        var num = idx + 1;

        // Duplicate the source comp (it contains text + animation)
        var newComp = sourceModuleComps[sourceSlot].duplicate();
        newComp.name = lyricText;
        newComp.parentFolder = lyricsFolder;

        // Find and replace text in ALL text layers inside the comp
        for (var L = 1; L <= newComp.numLayers; L++) {{
            var lyr = newComp.layer(L);
            if (lyr instanceof TextLayer) {{
                var textDoc = lyr.property("Source Text").value;
                textDoc.text = lyricText;
                textDoc.font = "Heavitas";
                lyr.property("Source Text").setValue(textDoc);
            }}
        }}

        lyricModules.push(newComp);
        lyricStyles.push(sourceSlot);
        $.writeln("Lyric " + num + " [style " + sourceSlot + "]: " + lyricText);
    }}

    $.writeln("Created " + totalLyrics + " lyric modules (flat).");

"""

    def _inject_kinetic(self, total: int) -> str:
        """Kinetic layout: separate TEXT comp (source) and TEXT MODULE (animated).
        Duplicate both, relink module to new text comp."""
        c = self.c
        return f"""
    // ── Kinetic layout: duplicate TEXT + TEXT MODULE, relink ──
    for (var idx = 0; idx < totalLyrics; idx++) {{
        var lyricText = lyricTexts[idx];
        var sourceSlot = pickStyleForLength(lyricText.length);
        var num = idx + 1;
        var pad = ("0" + num).slice(-{c.pad_width});
        if (num >= 100) pad = "" + num;

        // Duplicate the TEXT comp (text source)
        var newTextComp = sourceTextComps[sourceSlot].duplicate();
        newTextComp.name = "TEXT " + pad;
        newTextComp.parentFolder = lyricsFolder;

        // Replace text content and font
        for (var L = 1; L <= newTextComp.numLayers; L++) {{
            var lyr = newTextComp.layer(L);
            if (lyr instanceof TextLayer) {{
                var textDoc = lyr.property("Source Text").value;
                textDoc.text = lyricText;
                textDoc.font = "Heavitas";
                lyr.property("Source Text").setValue(textDoc);
            }}
        }}

        // Duplicate the TEXT MODULE comp (animated module)
        var newModuleComp = sourceModuleComps[sourceSlot].duplicate();
        newModuleComp.name = lyricText;
        newModuleComp.parentFolder = lyricsFolder;

        // Relink: replace layers referencing source TEXT with new TEXT
        for (var M = 1; M <= newModuleComp.numLayers; M++) {{
            var mLyr = newModuleComp.layer(M);
            if (mLyr.source && mLyr.source === sourceTextComps[sourceSlot]) {{
                mLyr.replaceSource(newTextComp, false);
            }}
        }}

        lyricModules.push(newModuleComp);
        lyricStyles.push(sourceSlot);
        $.writeln("Lyric " + num + " [style " + sourceSlot + "]: " + lyricText);
    }}

    $.writeln("Created " + totalLyrics + " lyric modules (kinetic).");

"""

    def _build_render_comp(self, lyrics: list[dict],
                           audio_path: str, comp_duration: float) -> str:
        if self.c.use_main_comp:
            return self._build_from_main_comp(lyrics, audio_path, comp_duration)
        c = self.c
        placement_lines = []
        for i, lyric in enumerate(lyrics):
            # Start earlier by anim_in_offset so animation completes on beat
            start = max(0, lyric["time"] - c.anim_in_offset)
            dur = lyric["duration"] + c.anim_in_offset
            needs_pan = "true" if lyric.get("needs_pan") else "false"
            placement_lines.append(
                f'        {{startTime: {start:.3f}, duration: {dur:.3f}, needsPan: {needs_pan}}}'
            )
        placements_js = ",\n".join(placement_lines)

        return f"""
    // =============================================
    // CREATE RENDER COMP
    // =============================================

    // Get dimensions from first source module comp
    var refComp = sourceModuleComps[1];
    var renderComp = proj.items.addComp(
        songName,
        refComp.width,
        refComp.height,
        refComp.pixelAspect,
        compDuration,
        refComp.frameRate
    );
    if (rootFolder) renderComp.parentFolder = rootFolder;

    // Import and add audio track
    var audioFile = new File(audioPath);
    if (audioFile.exists) {{
        var audioImport = proj.importFile(new ImportOptions(audioFile));
        var audioLayer = renderComp.layers.add(audioImport);
        audioLayer.name = "Audio - " + songName;
        audioLayer.startTime = 0;
    }} else {{
        $.writeln("WARNING: Audio file not found: " + audioPath);
    }}

    // Anim-in offset: layers start {c.anim_in_offset}s early so text
    // animation completes by the actual sync time.
    // Duration is halved ({c.duration_multiplier}x) for snappier pacing.
    var placements = [
{placements_js}
    ];

    // ── Place layers with null parents for out-animation ──
    var placedLayers = [];
    var placedNulls = [];

    for (var p = 0; p < placements.length; p++) {{
        var info = placements[p];
        var moduleComp = lyricModules[p];
        if (!moduleComp) continue;

        // Add the lyric module layer
        var layer = renderComp.layers.add(moduleComp);
        layer.startTime = info.startTime;

        // Trim out-point to lyric duration or module comp length
        var maxDur = Math.min(info.duration, moduleComp.duration);
        layer.outPoint = info.startTime + maxDur;

        // Create null parent for out-animation control
        var nullLayer = renderComp.layers.addNull();
        nullLayer.name = "Out_" + (p + 1);
        nullLayer.startTime = info.startTime;
        nullLayer.outPoint = layer.outPoint;
        // Hide null in timeline
        nullLayer.shy = true;

        // Parent the lyric layer to the null
        layer.parent = nullLayer;

        placedLayers.push(layer);
        placedNulls.push(nullLayer);

        $.writeln("Placed lyric " + (p + 1) + " at " + info.startTime.toFixed(2) + "s");
    }}

    // ── Animate nulls: push current layer "out" using NEXT layer's "in" direction ──
    // Text animator offsets are per-character (small), so we detect the
    // DIRECTION and push by full comp width/height to move off-screen.
    // Opacity is animated on the LAYER (not the null — AE parenting
    // does not cascade opacity).

    var cW = renderComp.width;
    var cH = renderComp.height;

    // Helper: apply ease matching property dimensions
    function applyEase(prop, keyIdx) {{
        var easeVal = new KeyframeEase(0, 80);
        try {{
            var dims = prop.value.length;
            if (typeof dims === "number" && dims >= 3) {{
                prop.setTemporalEaseAtKey(keyIdx, [easeVal, easeVal, easeVal]);
            }} else if (typeof dims === "number" && dims >= 2) {{
                prop.setTemporalEaseAtKey(keyIdx, [easeVal, easeVal]);
            }} else {{
                prop.setTemporalEaseAtKey(keyIdx, [easeVal]);
            }}
        }} catch(ee) {{}}
    }}

    for (var q = 0; q < placedLayers.length - 1; q++) {{
        var curLayer = placedLayers[q];
        var curNull = placedNulls[q];
        var nextStyle = lyricStyles[q + 1];
        var nextAnim = styleAnimData[nextStyle];

        // Out-animation starts near the end of current layer's duration
        // and lasts as long as the next layer's "in" animation
        var outEnd = curLayer.outPoint;
        var outStart = outEnd - nextAnim.duration;
        if (outStart < curLayer.startTime + 0.2) outStart = curLayer.startTime + 0.2;

        // Extend null to cover the out-animation
        curNull.outPoint = outEnd;

        // ── Position: detect direction, push full comp width/height ──
        if (nextAnim.posX !== 0 || nextAnim.posY !== 0) {{
            var nPos = curNull.property("Position");
            var restPos = nPos.value;

            // Normalize direction → push by full comp dimension
            var pushX = 0;
            var pushY = 0;
            if (Math.abs(nextAnim.posX) >= Math.abs(nextAnim.posY)) {{
                // Horizontal dominant
                pushX = (nextAnim.posX > 0) ? cW : -cW;
            }} else {{
                // Vertical dominant
                pushY = (nextAnim.posY > 0) ? cH : -cH;
            }}

            nPos.setValueAtTime(outStart, restPos);
            nPos.setValueAtTime(outEnd, [restPos[0] + pushX, restPos[1] + pushY]);
            applyEase(nPos, 1);
            applyEase(nPos, 2);
        }}

        // ── Scale: detect direction, scale to 0% or 200% ──
        if (nextAnim.scaleX !== 0 || nextAnim.scaleY !== 0) {{
            var nScale = curNull.property("Scale");
            var restScale = nScale.value;
            // If "in" scales up from small → "out" should shrink to 0
            // If "in" scales down from big → "out" should grow
            var targetSX = (nextAnim.scaleX < 0) ? 0 : restScale[0] + nextAnim.scaleX;
            var targetSY = (nextAnim.scaleY < 0) ? 0 : restScale[1] + nextAnim.scaleY;
            nScale.setValueAtTime(outStart, restScale);
            nScale.setValueAtTime(outEnd, [targetSX, targetSY]);
            applyEase(nScale, 1);
            applyEase(nScale, 2);
        }}

        // ── Rotation: amplify to full spin ──
        if (nextAnim.rotation !== 0) {{
            var nRot = curNull.property("Rotation");
            // Use same sign but ensure at least 45 degrees
            var rotOut = nextAnim.rotation;
            if (Math.abs(rotOut) < 45) rotOut = (rotOut > 0) ? 45 : -45;
            nRot.setValueAtTime(outStart, 0);
            nRot.setValueAtTime(outEnd, rotOut);
            applyEase(nRot, 1);
            applyEase(nRot, 2);
        }}

        // ── Opacity: animate on the LAYER itself (not the null) ──
        // AE parenting does NOT cascade opacity.
        var layerOpac = curLayer.property("Opacity");
        layerOpac.setValueAtTime(outStart, 100);
        layerOpac.setValueAtTime(outEnd, 0);
        applyEase(layerOpac, 1);
        applyEase(layerOpac, 2);

        $.writeln("Out-anim " + (q + 1) + " → style " + nextStyle
            + " dir(" + (nextAnim.posX > 0 ? "R" : nextAnim.posX < 0 ? "L" : "")
            + (nextAnim.posY > 0 ? "D" : nextAnim.posY < 0 ? "U" : "")
            + ") dur(" + nextAnim.duration.toFixed(2) + "s)");
    }}

    // Enable shy mode to hide null layers from view
    renderComp.hideShyLayers = true;

    $.writeln("Render comp: " + placedLayers.length + " layers + " + placedNulls.length + " nulls, " + compDuration.toFixed(1) + "s");

"""

    def _build_from_main_comp(self, lyrics: list[dict],
                              audio_path: str, comp_duration: float) -> str:
        """Use the existing Main comp: duplicate its animated layers for each lyric."""
        c = self.c
        placement_lines = []
        for i, lyric in enumerate(lyrics):
            start = max(0, lyric["time"] - c.anim_in_offset)
            dur = lyric["duration"] + c.anim_in_offset
            placement_lines.append(
                f'        {{startTime: {start:.3f}, duration: {dur:.3f}}}'
            )
        placements_js = ",\n".join(placement_lines)

        return f"""
    // =============================================
    // POPULATE MAIN COMP WITH LYRICS
    // =============================================

    // Capture "general" layers (everything that is NOT a lyric template layer)
    // BEFORE we add audio / lyric duplicates. These are the structural layers
    // such as the background solid (Dark Gray Solid 1), Color Correction
    // adjustment layer, Controls null, etc. that must span the whole song.
    var generalLayers = [];
    for (var gl = 1; gl <= mainComp.numLayers; gl++) {{
        var gLyr = mainComp.layer(gl);
        var isTemplate = false;
        for (var tr = 0; tr < templateLayerRefs.length; tr++) {{
            if (templateLayerRefs[tr] === gLyr) {{ isTemplate = true; break; }}
        }}
        if (!isTemplate) generalLayers.push(gLyr);
    }}

    // Rename the render-target comp to the song filename so it sends to the
    // render queue with the correct name (avoids manual spelling errors).
    mainComp.name = songName;

    // Extend Main comp to match song duration
    mainComp.duration = {comp_duration:.3f};

    // Stretch general layers across the full (new) comp duration. AE does NOT
    // auto-extend a layer's out-point when the comp grows, so do it explicitly.
    for (var ge = 0; ge < generalLayers.length; ge++) {{
        var gExt = generalLayers[ge];
        var wasLocked = gExt.locked;
        try {{
            if (wasLocked) gExt.locked = false;
            gExt.startTime = 0;
            gExt.inPoint = 0;                 // 0 <= current outPoint, safe
            gExt.outPoint = {comp_duration:.3f};
            $.writeln("Extended general layer: " + gExt.name + " -> 0.." + {comp_duration:.1f} + "s");
        }} catch(eExt) {{
            $.writeln("Could not extend general layer '" + gExt.name + "': " + eExt.toString());
        }}
        if (wasLocked) gExt.locked = true;
    }}

    // Import and add audio track
    var audioFile = new File("{audio_path}");
    if (audioFile.exists) {{
        var audioImport = proj.importFile(new ImportOptions(audioFile));
        var audioLayer = mainComp.layers.add(audioImport);
        audioLayer.name = "Audio - " + songName;
        audioLayer.startTime = 0;
    }} else {{
        $.writeln("WARNING: Audio file not found: " + "{audio_path}");
    }}

    var placements = [
{placements_js}
    ];

    var numTemplates = templateLayerRefs.length;

    // Duplicate template layers for each lyric, cycling through styles
    var placedLayers = [];
    for (var p = 0; p < placements.length; p++) {{
        var info = placements[p];
        var lyricComp = lyricModules[p];
        if (!lyricComp) continue;

        // Cycle through template layers for Corner Pin variety
        var srcLayer = templateLayerRefs[p % numTemplates];

        // Duplicate preserves all effects (Corner Pin, Fill) + keyframes
        var newLayer = srcLayer.duplicate();

        // Re-source to the new lyric comp
        newLayer.replaceSource(lyricComp, false);
        newLayer.name = lyricComp.name;

        // Shift timing: move entire layer (with all keyframes) to lyric time
        var timeOffset = info.startTime - srcLayer.inPoint;
        newLayer.startTime = srcLayer.startTime + timeOffset;
        newLayer.inPoint = srcLayer.inPoint + timeOffset;
        newLayer.outPoint = Math.min(
            srcLayer.outPoint + timeOffset,
            info.startTime + info.duration
        );

        placedLayers.push(newLayer);
        $.writeln("Placed lyric " + (p + 1) + " at " + info.startTime.toFixed(2)
            + "s (template " + ((p % numTemplates) + 1) + "/" + numTemplates + ")");
    }}

    // Disable original template layers (keep for reference)
    for (var d = 0; d < templateLayerRefs.length; d++) {{
        templateLayerRefs[d].enabled = false;
    }}

    $.writeln("Main comp: " + placedLayers.length + " lyric layers placed, "
        + numTemplates + " templates cycled, " + generalLayers.length
        + " general layers extended, " + {comp_duration:.1f} + "s duration");

"""

    def _save_and_close(self, output_path: str, song_name: str) -> str:
        return f"""
    // =============================================
    // SAVE AS NEW PROJECT
    // =============================================
    var outputFile = new File("{output_path}/{self._esc(song_name)}.aep");
    proj.save(outputFile);
    $.writeln("Saved: " + outputFile.fsName);

"""

    def _footer(self) -> str:
        return """
    } catch(e) {
        alert("SnapLyrics Template Error:\\n" + e.toString());
        $.writeln("ERROR: " + e.toString());
    }

    app.endUndoGroup();
})();
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Full Pipeline (template mode)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TemplatePipeline:
    """Full SnapLyrics pipeline that outputs template-modifier JSX.

    Runs the same Demucs + Whisper + Genius + LRC sync as the standard
    pipeline, but instead of generating compositions from scratch, it
    injects synced lyrics into an existing .aep kinetic titles template.
    """

    def __init__(self, source_folder: str, template_path: str,
                 output_folder: str = "OUTPUT",
                 config: VideoConfig | None = None,
                 template_config: TemplateConfig | None = None):
        self.config = config or VideoConfig()
        self.source_folder = Path(source_folder)
        self.output_folder = self.source_folder / output_folder
        self.template_path = Path(template_path).resolve()

        # Full pipeline components (same as SnapLyricsPipeline)
        self.parser = LrcParser()
        self.syncer = LrcSyncer() if LrcSyncer.available() else None
        self.writer = LrcWriter()
        self.fetcher = LyricsFetcher() if LyricsFetcher.available() else None

        # Template renderer
        self.template_config = template_config or TemplateConfig()
        self.renderer = TemplateRenderer(self.template_config)

    def process_all_songs(self):
        self.output_folder.mkdir(exist_ok=True)

        layout_label = "flat (comps in folder)" if self.template_config.layout == "flat" else "kinetic (nested folders)"
        print(f"\n{_BOLD}{_LILAC}  SnapLyrics — Template Mode{_RESET}")
        print(f"{_LILAC}  ─────────────────────────────────────{_RESET}")
        print(f"{_SNOW}  Source:    {_WISTERIA}{self.source_folder}{_RESET}")
        print(f"{_SNOW}  Template:  {_WISTERIA}{self.template_path.name}{_RESET}")
        print(f"{_SNOW}  Layout:    {_WISTERIA}{layout_label}{_RESET}")
        print(f"{_SNOW}  Output:    {_WISTERIA}{self.output_folder}{_RESET}")
        print(f"{_SNOW}  Styles:    {_WISTERIA}{self.template_config.existing_slots} slots (cycled){_RESET}\n")

        if not self.template_path.exists():
            print(f"{_RED}  Template not found: {self.template_path}{_RESET}")
            return

        audio_files = _find_audio_files(self.source_folder)
        if not audio_files:
            fmts = ", ".join(AUDIO_EXTENSIONS)
            print(f"{_RED}  No audio files found ({fmts}) in {self.source_folder}{_RESET}")
            return

        # Check sync dependencies
        if not self.syncer:
            print(f"{_RED}  openai-whisper not installed — sync disabled{_RESET}")
            print(f"{_WISTERIA}  pip install openai-whisper{_RESET}")
            print(f"{_RED}  Sync is required — aborting.{_RESET}\n")
            return

        vocals_count = sum(
            1 for f in audio_files if LrcSyncer.find_vocals(f) is not None
        )
        need_separation = len(audio_files) - vocals_count

        print(f"{_SNOW}  Found {_GOLD}{len(audio_files)}{_SNOW} songs, "
              f"{_GOLD}{vocals_count}{_SNOW} _vocals files{_RESET}")
        if need_separation > 0 and LrcSyncer.can_separate():
            print(f"{_WISTERIA}  {need_separation} will be separated with Demucs{_RESET}")
        elif need_separation > 0:
            print(f"{_WISTERIA}  {need_separation} missing _vocals (install demucs){_RESET}")
        print(f"{_GOLD}  Auto-sync ENABLED{_RESET}\n")

        success = 0
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
                # ── Step 1: Stems (Demucs) ─────────────────────
                vocals_file = LrcSyncer.find_vocals(audio_file)
                drums_file = LrcSyncer.find_drums(audio_file)
                if (not vocals_file or not drums_file) and LrcSyncer.can_separate():
                    stems = LrcSyncer.separate_stems(audio_file)
                    if not vocals_file:
                        vocals_file = stems.get("vocals")
                    if not drums_file:
                        drums_file = stems.get("drums")
                if not vocals_file:
                    print(f"{_RED}    No _vocals file and Demucs not installed{_RESET}")
                    errors += 1
                    continue

                # ── Step 2: Check for cached sync first ─────
                synced_lrc = song_folder / f"{song_name}.lrc"
                if synced_lrc.exists():
                    lyrics, _ = self.parser.parse(synced_lrc)
                    print(f"{_WISTERIA}    Cached sync: {len(lyrics)} lines{_RESET}")
                else:
                    # ── Step 2b: Reference lyrics (LRC / TXT / Genius) ──
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
                            print(f"{_WISTERIA}    Reference: Genius ({len(reference)} lines){_RESET}")

                    # ── Step 3: Whisper transcription + LRC sync ───
                    lyrics, sync_info = self.syncer.sync(vocals_file, reference)
                    if lyrics and sync_info is not None:
                        self.writer.write(lyrics, [], synced_lrc)
                if not lyrics:
                    print(f"{_RED}    Sync failed — no lyrics{_RESET}")
                    errors += 1
                    continue

                # ── Step 4: Split into word blocks ─────────────
                lyrics = _split_lyrics_into_blocks(
                    lyrics,
                    self.config.max_words_per_block,
                    self.config.anticipation_seconds,
                    self.template_config.max_chars_per_line,
                )

                # ── Step 5: Generate template JSX ──────────────
                jsx_content = self.renderer.render(
                    self.template_path, audio_file.absolute(),
                    lyrics, song_name, song_folder.absolute(),
                )

                jsx_file = song_folder / f"{song_name}_template.jsx"
                jsx_file.write_text(jsx_content, encoding="utf-8")

                # Copy audio to output
                shutil.copy2(audio_file, song_folder / audio_file.name)

                print(f"{_GOLD}    Done{_RESET} {_WISTERIA}{len(lyrics)} blocks"
                      f" ({self.template_config.existing_slots} styles cycled){_RESET}"
                      f" {_SNOW}→ {jsx_file.name}{_RESET}")
                success += 1

            except Exception as e:
                print(f"{_RED}    Error: {e}{_RESET}")
                errors += 1

        # Summary
        print(f"\n{_LILAC}  {'━' * 45}{_RESET}")
        print(f"{_BOLD}{_GOLD}  SNAPLYRICS KINETIC TITLES COMPLETE{_RESET}")
        print(f"{_LILAC}  {'━' * 45}{_RESET}")
        print(f"{_GOLD}  Successful: {success}{_RESET}")
        if errors:
            print(f"{_RED}  Errors: {errors}{_RESET}")
        print(f"{_SNOW}  Output: {_WISTERIA}{self.output_folder.absolute()}{_RESET}")
        print(f"\n{_SNOW}  To apply in After Effects:{_RESET}")
        print(f"{_WISTERIA}    1. Open After Effects{_RESET}")
        print(f"{_WISTERIA}    2. File > Scripts > Run Script File...{_RESET}")
        print(f"{_WISTERIA}    3. Select [song]_template.jsx{_RESET}")
        print(f"{_WISTERIA}    4. Template opens → lyrics injected → saved as new .aep{_RESET}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="SnapLyrics Template Mode — full pipeline + AE template injection"
    )
    parser.add_argument(
        "template", help="Path to .aep template file"
    )
    parser.add_argument(
        "folder", nargs="?", default=".",
        help="Folder containing audio + .lrc files (default: current directory)",
    )
    parser.add_argument(
        "--slots", type=int, default=None,
        help="Number of existing title styles in template (auto-detected if omitted)",
    )
    parser.add_argument(
        "--layout", default=None, choices=["kinetic", "flat"],
        help="Template layout: 'kinetic' (nested) or 'flat' (comps in folder). Auto-detected if omitted.",
    )
    args = parser.parse_args()

    # Auto-detect layout from template name
    template_name = Path(args.template).stem.lower()
    if args.layout:
        layout = args.layout
    elif "stomp" in template_name or "placeholder" in template_name:
        layout = "flat"
    else:
        layout = "kinetic"

    if layout == "flat":
        template_config = TemplateConfig.stomp(slots=args.slots or 5)
    else:
        template_config = TemplateConfig(existing_slots=args.slots or 9)

    pipeline = TemplatePipeline(
        source_folder=args.folder,
        template_path=args.template,
        template_config=template_config,
    )
    pipeline.process_all_songs()


if __name__ == "__main__":
    main()
