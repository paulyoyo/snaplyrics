// Diagnostic: test what property access patterns work in this AE version
(function () {
    if (!app.project || !app.project.file) { alert("Save first"); return; }

    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) {
        if (app.project.item(i) instanceof CompItem && app.project.item(i).name === "Scene_01") {
            comp = app.project.item(i);
            break;
        }
    }
    if (!comp) { alert("Scene_01 not found"); return; }

    var log = [];
    var layer = comp.layer(2); // Rotation_02
    log.push("Layer: " + layer.name + " index=" + layer.index);

    // Test 1: Direct matchName access
    try {
        var xform = layer.property("ADBE Transform Group");
        log.push("Transform group: " + (xform ? "OK" : "null"));
        log.push("  matchName: " + xform.matchName);
        log.push("  numProperties: " + xform.numProperties);
        log.push("  propertyType: " + xform.propertyType);
    } catch (e) { log.push("Transform group FAILED: " + e.message); }

    // Test 2: Direct named child access
    try {
        var pos = xform.property("ADBE Position");
        log.push("Position (by matchName): " + (pos ? "OK" : "null"));
        log.push("  value: " + pos.value);
        log.push("  numKeys: " + pos.numKeys);
    } catch (e) { log.push("Position FAILED: " + e.message); }

    // Test 3: Index-based child access
    try {
        for (var i = 1; i <= xform.numProperties; i++) {
            var child = xform.property(i);
            var childName = "?", childMatch = "?", childType = "?", childNumProps = "?";
            try { childName = child.name; } catch (e) {}
            try { childMatch = child.matchName; } catch (e) {}
            try { childType = child.propertyType; } catch (e) {}
            try { childNumProps = child.numProperties; } catch (e) { childNumProps = "N/A (leaf)"; }

            var val = "?", nk = "?", expr = "?";
            try { val = String(child.value).substring(0, 50); } catch (e) { val = "ERR: " + e.message; }
            try { nk = child.numKeys; } catch (e) { nk = "ERR"; }
            try { expr = child.expression ? child.expression.substring(0, 40) : "(none)"; } catch (e) { expr = "ERR"; }

            log.push("  [" + i + "] " + childName + " (" + childMatch + ") type=" + childType +
                     " numProps=" + childNumProps + " val=" + val + " keys=" + nk + " expr=" + expr);
        }
    } catch (e) { log.push("Index iteration FAILED: " + e.message); }

    // Test 4: Effects group
    try {
        var efx = layer.property("ADBE Effect Parade");
        log.push("Effects: " + (efx ? "exists" : "null") + " numProps=" + efx.numProperties);
    } catch (e) { log.push("Effects FAILED: " + e.message); }

    // Test 5: Try layer 4 (Title_02) - text layer with expressions
    var tl = comp.layer(4);
    log.push("\nLayer: " + tl.name);
    try {
        var txform = tl.property("ADBE Transform Group");
        log.push("Transform numProperties: " + txform.numProperties);
        // Try Y Rotation specifically
        var yrot = txform.property("ADBE Rotate Y");
        log.push("Y Rotation: val=" + yrot.value + " keys=" + yrot.numKeys);
        if (yrot.numKeys > 0) {
            for (var k = 1; k <= yrot.numKeys; k++) {
                log.push("  key " + k + ": t=" + yrot.keyTime(k) + " v=" + yrot.keyValue(k));
            }
        }
        if (yrot.expression) {
            log.push("  expression: " + yrot.expression.substring(0, 100));
        }
    } catch (e) { log.push("Title_02 FAILED: " + e.message); }

    // Test 6: Opacity expression (backface culling)
    try {
        var opacity = tl.property("ADBE Transform Group").property("ADBE Opacity");
        log.push("Opacity: val=" + opacity.value + " keys=" + opacity.numKeys);
        log.push("  canSetExpression: " + opacity.canSetExpression);
        log.push("  expressionEnabled: " + opacity.expressionEnabled);
        if (opacity.expression) log.push("  expression: " + opacity.expression.substring(0, 100));
    } catch (e) { log.push("Opacity FAILED: " + e.message); }

    // Write results
    var outFile = new File(app.project.file.parent.fullName + "/ae_debug_log.txt");
    outFile.open("w");
    outFile.write(log.join("\n"));
    outFile.close();
    alert("Debug log saved:\n" + outFile.fullName + "\n\n" + log.length + " lines");
})();
