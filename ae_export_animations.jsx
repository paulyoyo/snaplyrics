// SnapLyrics — After Effects Full Animation Exporter v4
// ONE recursive walker for everything. No hardcoded property lists.
// Run: File > Scripts > Run Script File

(function () {
    if (!app.project || !app.project.file) {
        alert("Save your project first, then run this script.");
        return;
    }

    var projectName = app.project.file.name.replace(/\.(aep|aepx)$/i, "");
    var outputFolder = app.project.file.parent;
    var outputFile = new File(outputFolder.fullName + "/" + projectName + "_animations.json");

    var result = { project: projectName, fps: 30, compositions: [] };

    var comps = [];
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem) comps.push(item);
    }

    for (var c = 0; c < comps.length; c++) {
        var comp = comps[c];
        result.fps = comp.frameRate;
        var compData = {
            name: comp.name, width: comp.width, height: comp.height,
            duration: comp.duration, frameRate: comp.frameRate, layers: []
        };
        for (var l = 1; l <= comp.numLayers; l++) {
            compData.layers.push(extractLayer(comp.layer(l)));
        }
        result.compositions.push(compData);
    }

    outputFile.open("w");
    outputFile.encoding = "UTF-8";
    outputFile.write(jsonStringify(result, 0));
    outputFile.close();
    alert("v4 Exported " + comps.length + " comps to:\n" + outputFile.fullName);

    // ═══════════════════════════════════════════════════════════════
    // Layer extraction — flags + recursive property walk
    // ═══════════════════════════════════════════════════════════════

    function extractLayer(layer) {
        var data = {
            name: layer.name, index: layer.index, type: getLayerType(layer),
            enabled: layer.enabled, inPoint: layer.inPoint, outPoint: layer.outPoint,
            startTime: layer.startTime
        };

        // Flags
        try { data.threeDLayer = layer.threeDLayer; } catch (e) {}
        try { data.shy = layer.shy; } catch (e) {}
        try { data.locked = layer.locked; } catch (e) {}
        try { data.guideLayer = layer.guideLayer; } catch (e) {}
        try { data.adjustmentLayer = layer.adjustmentLayer; } catch (e) {}
        try { data.collapseTransformation = layer.collapseTransformation; } catch (e) {}
        try { data.motionBlur = layer.motionBlur; } catch (e) {}
        try { data.blendingMode = blendModeName(layer.blendingMode); } catch (e) {}
        try { data.label = layer.label; } catch (e) {}

        // Parent
        if (layer.parent) {
            data.parent = { name: layer.parent.name, index: layer.parent.index };
        }

        // Source comp
        try {
            if (layer.source && layer.source instanceof CompItem)
                data.sourceComp = layer.source.name;
        } catch (e) {}

        // Markers
        try {
            var mp = layer.property("Marker");
            if (mp && mp.numKeys > 0) data.markers = extractMarkers(mp);
        } catch (e) {}

        // Text document (special — not a normal property)
        if (layer instanceof TextLayer) {
            try {
                var srcText = layer.property("ADBE Text Properties").property("ADBE Text Document");
                if (srcText) {
                    var doc = srcText.value;
                    data.text = { sourceText: doc.text || "", font: doc.font || "", fontSize: doc.fontSize || 0 };
                    try { data.text.fillColor = doc.fillColor; } catch (e) {}
                    try { data.text.tracking = doc.tracking; } catch (e) {}
                    try { data.text.leading = doc.leading; } catch (e) {}
                    try { data.text.justification = String(doc.justification); } catch (e) {}
                    if (srcText.expressionEnabled && srcText.expression)
                        data.text.sourceTextExpression = srcText.expression;
                }
            } catch (e) {}
        }

        // ══════════════════════════════════════════════════════
        // Walk ALL property groups recursively — one function for everything
        // ══════════════════════════════════════════════════════
        data.properties = {};

        var groups = [
            ["ADBE Transform Group", "transform"],
            ["ADBE Effect Parade", "effects"],
            ["ADBE Text Properties", "text_props"],
            ["ADBE Root Vectors Group", "shapes"],
            ["ADBE Mask Parade", "masks"],
            ["ADBE Material Options Group", "materialOptions"],
            ["ADBE Layer Styles", "layerStyles"],
            ["ADBE Audio Group", "audio"]
        ];

        for (var g = 0; g < groups.length; g++) {
            try {
                var grp = layer.property(groups[g][0]);
                if (grp) {
                    var walked = walkAny(grp, 0);
                    if (walked !== null) data.properties[groups[g][1]] = walked;
                }
            } catch (e) {}
        }

        return data;
    }

    // ═══════════════════════════════════════════════════════════════
    // Universal recursive walker — handles ANY AE property tree
    // No depth limits. No hardcoded property names.
    // ═══════════════════════════════════════════════════════════════

    function walkAny(node, depth) {
        if (!node) return null;
        // Safety: prevent infinite recursion on pathological trees
        if (depth > 20) return null;

        // Determine if this node is a group (has numProperties as a number)
        // or a leaf (numProperties is undefined)
        var numChildren;
        try { numChildren = node.numProperties; } catch (e) {}

        if (typeof numChildren !== "number") {
            // ── LEAF: extract value, keyframes, expression ──
            return extractLeaf(node);
        }

        if (numChildren === 0) {
            // Group with 0 children — try as leaf (some props report 0 but have values)
            var asLeaf = extractLeaf(node);
            if (asLeaf !== null) return asLeaf;
            return null;
        }

        // ── GROUP: recurse into children ──
        var children = [];
        for (var i = 1; i <= numChildren; i++) {
            try {
                var child = node.property(i);
                if (!child) continue;

                var childName = "";
                try { childName = child.name; } catch (e) {}
                if (!childName) childName = "prop_" + i;

                var childData = walkAny(child, depth + 1);
                if (childData !== null) {
                    children.push({ key: childName, data: childData });
                }
            } catch (e) {}
        }

        if (children.length === 0) return null;

        var result = {};
        for (var ci = 0; ci < children.length; ci++) {
            var ck = children[ci].key;
            // Deduplicate keys
            if (result[ck] !== undefined) ck = ck + "_" + (ci + 1);
            result[ck] = children[ci].data;
        }
        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    // Leaf property extractor — value, keyframes, expression
    // ═══════════════════════════════════════════════════════════════

    function extractLeaf(prop) {
        if (!prop) return null;
        var obj = {};

        // Try to get matchName for identification
        try { obj.matchName = prop.matchName; } catch (e) {}

        // Value — always try, catch silently
        var hasValue = false;
        try {
            var rawVal = prop.value;
            // Skip non-serializable types (TextDocument, Shape objects, etc.)
            var vtype = typeof rawVal;
            if (rawVal === null || rawVal === undefined) {
                obj.value = null;
            } else if (vtype === "number" || vtype === "boolean" || vtype === "string") {
                obj.value = rawVal;
                hasValue = true;
            } else if (rawVal instanceof Array) {
                obj.value = rawVal;
                hasValue = true;
            } else if (vtype === "object") {
                // Could be TextDocument, Shape, etc. — skip (captured separately)
                obj.value = null;
            } else {
                obj.value = null;
            }
        } catch (e) {
            obj.value = null;
        }

        // Expression — full text
        var hasExpr = false;
        try {
            var ex = prop.expression;
            if (ex && ex.length > 0) {
                obj.expression = ex;
                hasExpr = true;
                try { obj.expressionEnabled = prop.expressionEnabled; } catch (e) {}
            }
        } catch (e) {}

        // Keyframes — full detail
        var hasKeys = false;
        var nk = 0;
        try { nk = prop.numKeys; } catch (e) {}
        if (typeof nk === "number" && nk > 0) {
            obj.keyframes = [];
            hasKeys = true;
            for (var k = 1; k <= nk; k++) {
                var kf = {};
                try { kf.time = prop.keyTime(k); } catch (e) { continue; }
                try { kf.value = prop.keyValue(k); } catch (e) {}
                try {
                    kf.interpIn = interpName(prop.keyInInterpolationType(k));
                    kf.interpOut = interpName(prop.keyOutInterpolationType(k));
                } catch (e) {}
                try {
                    var eIn = prop.keyInTemporalEase(k);
                    var eOut = prop.keyOutTemporalEase(k);
                    kf.easeIn = []; kf.easeOut = [];
                    for (var d = 0; d < eIn.length; d++) {
                        kf.easeIn.push({ speed: eIn[d].speed, influence: eIn[d].influence });
                        kf.easeOut.push({ speed: eOut[d].speed, influence: eOut[d].influence });
                    }
                } catch (e) {}
                obj.keyframes.push(kf);
            }
        }

        // Must have at least something useful
        if (!hasValue && !hasExpr && !hasKeys) return null;

        // Clean empty fields
        if (!hasExpr) { delete obj.expression; delete obj.expressionEnabled; }
        if (!hasKeys) delete obj.keyframes;

        return obj;
    }

    // ═══════════════════════════════════════════════════════════════
    // Markers
    // ═══════════════════════════════════════════════════════════════

    function extractMarkers(mp) {
        var markers = [];
        for (var m = 1; m <= mp.numKeys; m++) {
            try {
                var mv = mp.keyValue(m);
                markers.push({
                    time: mp.keyTime(m),
                    comment: mv.comment || "",
                    duration: mv.duration || 0
                });
            } catch (e) {}
        }
        return markers;
    }

    // ═══════════════════════════════════════════════════════════════
    // Helpers
    // ═══════════════════════════════════════════════════════════════

    function getLayerType(layer) {
        if (layer instanceof TextLayer) return "text";
        if (layer instanceof ShapeLayer) return "shape";
        if (layer instanceof CameraLayer) return "camera";
        if (layer instanceof LightLayer) return "light";
        if (layer instanceof AVLayer) return "av";
        return "unknown";
    }

    function interpName(type) {
        switch (type) {
            case KeyframeInterpolationType.LINEAR: return "linear";
            case KeyframeInterpolationType.BEZIER: return "bezier";
            case KeyframeInterpolationType.HOLD: return "hold";
            default: return String(type);
        }
    }

    function blendModeName(bm) {
        var m = {};
        m[BlendingMode.NORMAL] = "normal"; m[BlendingMode.ADD] = "add";
        m[BlendingMode.MULTIPLY] = "multiply"; m[BlendingMode.SCREEN] = "screen";
        m[BlendingMode.OVERLAY] = "overlay"; m[BlendingMode.SOFT_LIGHT] = "softLight";
        m[BlendingMode.HARD_LIGHT] = "hardLight"; m[BlendingMode.DIFFERENCE] = "difference";
        return m[bm] || String(bm);
    }

    // ═══════════════════════════════════════════════════════════════
    // JSON serializer
    // ═══════════════════════════════════════════════════════════════

    function jsonStringify(obj, indent) {
        var pad = ""; for (var i = 0; i < indent; i++) pad += "  ";
        var pad1 = pad + "  ";
        if (obj === null || obj === undefined) return "null";
        if (typeof obj === "boolean") return obj ? "true" : "false";
        if (typeof obj === "number") {
            if (isNaN(obj) || !isFinite(obj)) return "null";
            return roundNum(obj);
        }
        if (typeof obj === "string") return '"' + escapeStr(obj) + '"';
        if (obj instanceof Array) {
            if (obj.length === 0) return "[]";
            if (obj.length <= 4 && allNumbers(obj)) {
                var nums = []; for (var a = 0; a < obj.length; a++) nums.push(roundNum(obj[a]));
                return "[" + nums.join(", ") + "]";
            }
            var items = [];
            for (var a = 0; a < obj.length; a++) items.push(pad1 + jsonStringify(obj[a], indent + 1));
            return "[\n" + items.join(",\n") + "\n" + pad + "]";
        }
        if (typeof obj === "object") {
            var keys = []; for (var k in obj) { if (obj.hasOwnProperty(k)) keys.push(k); }
            if (keys.length === 0) return "{}";
            var entries = [];
            for (var ki = 0; ki < keys.length; ki++) {
                var val = obj[keys[ki]]; if (val === undefined) continue;
                entries.push(pad1 + '"' + escapeStr(keys[ki]) + '": ' + jsonStringify(val, indent + 1));
            }
            return "{\n" + entries.join(",\n") + "\n" + pad + "}";
        }
        return String(obj);
    }

    function escapeStr(s) {
        return s.replace(/\\/g, "\\\\").replace(/"/g, '\\"')
                .replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t");
    }

    function roundNum(n) {
        if (n === Math.floor(n)) return String(n);
        return String(Math.round(n * 10000) / 10000);
    }

    function allNumbers(arr) {
        for (var i = 0; i < arr.length; i++) { if (typeof arr[i] !== "number") return false; }
        return true;
    }
})();
