# Unique Typography -- After Effects Animation Analysis

> Source: `Unique_scenes_animations.json` (40MB AE export)
> 30 scenes, 147 sub-compositions, 1920x1080 @ 30fps

---

## 1. Scene Classification

### Summary Table

| Scene | Duration | Text Comp | Layers | Nulls | AV | Edit Comps | Total Refs | Track Mattes | Null KFs | AV KFs | Effects |
|-------|----------|-----------|--------|-------|----|------------|------------|--------------|----------|--------|---------|
| 001 | 6.20s | Text 001 | 70 | 13 | 57 | 7 | 57 | 0 | Pos, Scale, ZRot | Scale, ZRot, Opacity | -- |
| 002 | 4.20s | Text 002 | 55 | 10 | 45 | 4 | 45 | 0 | Pos, XRot, YRot, ZRot, Scale | -- | -- |
| 003 | 3.50s | Text 003 | 101 | 11 | 90 | 3 | 90 | 0 | Pos, ZRot | -- | -- |
| 004 | 4.03s | Text 004 | 58 | 4 | 54 | 4 | 36 | 18 | Pos, ZRot, Scale, XRot, YRot | Pos | -- |
| 005 | 3.93s | Text 005 | 40 | 4 | 36 | 4 | 36 | 0 | Pos, ZRot, Scale | Pos | -- |
| 006 | 3.67s | Text 006 | 72 | 18 | 54 | 6 | 54 | 0 | Pos, ZRot, Scale | -- | -- |
| 007 | 3.30s | Text 007 | 53 | 7 | 46 | 4 | 37 | 0 | Pos, ZRot, Scale | Pos, Scale | -- |
| 008 | 4.03s | Text 008 | 50 | 5 | 45 | 4 | 45 | 0 | Pos, Scale, ZRot | -- | -- |
| 009 | 4.20s | Text 009 | 36 | 6 | 30 | 3 | 30 | 0 | Pos, ZRot, Scale | -- | -- |
| 010 | 3.47s | Text 010 | 45 | 9 | 36 | 4 | 36 | 0 | Pos, ZRot, Scale | -- | -- |
| 011 | 4.53s | Text 011 | 41 | 6 | 35 | 4 | 35 | 0 | Pos, ZRot, Scale | -- | -- |
| 012 | 3.43s | Text 012 | 48 | 12 | 36 | 4 | 36 | 0 | Pos, Scale, ZRot | -- | -- |
| 013 | 2.40s | Text 013 | 31 | 4 | 27 | 3 | 27 | 0 | Pos, ZRot, Scale | -- | -- |
| 014 | 3.17s | Text 014 | 131 | 14 | 117 | 3 | 117 | 0 | Pos, Scale, ZRot, XRot, YRot | -- | -- |
| 015 | 3.27s | Text 015 | 43 | 7 | 36 | 4 | 36 | 0 | Pos, ZRot, Scale | -- | -- |
| 016 | 1.97s | Text 016 | 41 | 5 | 36 | 4 | 36 | 0 | Pos, ZRot, Scale | -- | -- |
| 017 | 3.30s | Text 017 | 42 | 6 | 36 | 4 | 36 | 0 | Pos, Scale, ZRot | Pos, ZRot, Opacity | -- |
| 018 | 5.60s | Text 018 | 97 | 7 | 90 | 7 | 72 | 18 | Pos, ZRot, Scale | Pos, Scale, ZRot | -- |
| 019 | 3.57s | Text 019 | 32 | 5 | 27 | 3 | 27 | 0 | Pos, ZRot, Scale | -- | -- |
| 020 | 3.57s | Text 020 | 42 | 6 | 36 | 4 | 36 | 0 | Pos, YRot, ZRot | Opacity | -- |
| 021 | 4.03s | Text 021 | 46 | 9 | 37 | 4 | 36 | 0 | Pos, ZRot | Pos | -- |
| 022 | 3.23s | Text 022 | 62 | 8 | 54 | 6 | 54 | 0 | Pos, YRot, ZRot | -- | -- |
| 023 | 3.80s | Text 023 | 20 | 1 | 19 | 2 | 18 | 0 | -- | Pos, Scale, XRot, YRot, ZRot | -- |
| 024 | 3.27s | Text 024 | 30 | 3 | 27 | 3 | 27 | 0 | YRot, Pos | XRot | -- |
| 025 | 4.07s | Text 025 | 34 | 7 | 27 | 3 | 27 | 0 | ZRot, Pos, YRot | -- | -- |
| 026 | 3.63s | Text 026 | 30 | 3 | 27 | 3 | 27 | 0 | Pos, ZRot | -- | -- |
| 027 | 3.20s | Text 027 | 31 | 4 | 27 | 3 | 27 | 0 | Pos, Scale, ZRot | -- | -- |
| 028 | 3.17s | Text 028 | 49 | 4 | 45 | 3 | 45 | 0 | Pos, Scale, ZRot, YRot | Opacity | -- |
| 029 | 3.80s | *direct* | 46 | 7+ | -- | 4 | -- | 0 | Pos, ZRot, Scale | -- | -- |
| 030 | 3.47s | *direct* | 32 | 5+ | -- | 3 | -- | 0 | Pos, Scale, ZRot | -- | -- |

**Notes:**
- All scenes are 1920x1080 @ 30fps
- Scenes 001-028 use the `Scene NNN -> Text NNN` sub-comp pattern
- Scenes 029-030 have animation directly in the scene comp (no intermediate Text sub-comp)
- All layers are 3D throughout
- Max parent chain depth is consistently 1 (AV layers parent to Null, Null to Null, one root Null)
- Edit Text duplication: each Edit Text comp is referenced 9x (for 3D depth), some comps have one copy at 25% opacity for depth shadow

---

## 2. Distinct Animation Patterns

### Pattern A: "Null-Chain Spin-In / Fly-Out" (MOST COMMON)
**Scenes:** 001, 002, 003, 006, 008, 009, 010, 011, 012, 013, 014, 015, 016, 019, 022, 025, 026, 027

**Structure:**
- Root Null 1 [idx 1]: EXPR-only (Scale from Control slider, XYZ Rotation from Control)
- Entrance Null [idx ~6]: KF Position (offscreen -> onscreen) + KF Z Rotation (360 spin -> 0) + bounce expression
- Hold phase: no animation
- Exit Null [idx ~2]: KF Position (onscreen -> offscreen/depth), KF Z Rotation (0 -> random spin), sometimes KF Scale (100% -> 0%)
- AV layers: static transforms, parented to a null, offset in Z for depth (z=0,2,4,6,8...)

**Timing Pattern:**
- Entrance: 0.0-0.8s to 0.6-1.6s (entrance complete)
- Hold: 1-2s visible
- Exit: starts 1-2s before end, flies out

**Key Data (Text 009 representative):**
```
Null exit [idx 2]: t=3.23 pos=[50,50,0] -> t=4.7 pos=[50,1110,0], ZRot t=3.23 v=0 -> t=4.7 v=141
Null entrance [idx 6]: t=0 pos=[0,-1155,0] -> t=0.67 pos=[50,15,0] + bounce expr
                        t=0 ZRot=255 -> t=0.67 ZRot=0 + bounce expr
```

### Pattern B: "Track-Matte Wipe Reveal" 
**Scenes:** 004, 018

**Structure:**
- Same null chain as Pattern A
- AV layers have `trackMatteType: alphaInverted` 
- AV layers are ANIMATED in Position (slide to reveal through matte)
- 18 layers use track mattes (groups of Edit Text comps slide in/out)

**Key Data (Text 004):**
```
AV Edit Text 018 [idx 2]: trackMatte=alphaInverted, parent=Null 1
  KF Position: t=2 v=[325.14,1427.80,0] -> t=2.33 v=[-72.86,1427.80,0]
  (slides horizontally to reveal text through alpha matte)
```

### Pattern C: "Slide-In Text with Null Group"
**Scenes:** 005, 007, 017, 021

**Structure:**
- Null chain controls group entrance/exit
- Individual AV (Edit Text) layers also have KF Position (slide from off-screen)
- Text enters from opposing directions (one from top, one from bottom)
- Sometimes AV layers have opacity/ZRot keyframes too

**Key Data (Text 017):**
```
Null exit [idx 3]: t=3 pos=[50,50,0] -> t=3.17 pos=[121,50,0] -> t=3.8 pos=[-329,50,0]
                   t=3 scale=[100,100,100] -> t=3.17 scale=[107,107,107] -> t=3.8 scale=[0,0,0]
                   t=3 ZRot=0 -> t=3.17 ZRot=-12.2 -> t=3.8 ZRot=90

AV Edit Text 069 [idx 4]: KF Position t=2 v=[36,1812,0] -> t=3 v=[36,50,0] (slides up)
AV Edit Text 068 [idx 5]: KF Position t=2 v=[52,-1553,0] -> t=3 v=[52,50,0] (slides down)
```

### Pattern D: "Y-Rotation Card Flip"
**Scenes:** 020, 024, 028

**Structure:**
- Null chain with Y Rotation keyframes (0 -> 90 to flip away)
- AV layers may have X Rotation with bounce expression
- Creates a 3D card-flip exit effect

**Key Data (Text 024):**
```
Null [idx 2]: KF Y Rotation t=2 v=0 -> t=3.33 v=90 (ease: influence=90)
Null [idx 3]: KF Y Rotation t=0 v=-90 -> t=1 v=0 (entrance flip)
```

**Key Data (Text 028):**
```
Null [idx 3]: KF Y Rotation t=0 v=90 -> t=0.7 v=0 + bounce expr (entrance flip)
              KF Position t=0 v=[50,50,-1460] -> t=0.7 v=[50,50,0] + bounce expr
Null [idx 4]: KF Scale t=1.5 v=[100,100,100] -> t=2.5 v=[0,0,0]
              KF Y Rotation t=1.5 v=0 -> t=2.5 v=270
AV layers: KF Opacity flash (0->100->100->0 over ~0.5s) for strobe entrance
```

### Pattern E: "AV-Driven 3D Tumble" (unique)
**Scenes:** 023

**Structure:**
- Only 1 Null (root control null, no KFs)
- ALL animation is on the AV layers directly
- Each AV layer has KF Position, Scale, X/Y/Z Rotation
- Creates a per-word 3D tumble effect

**Key Data (Text 023):**
```
AV layers have individual Position, Scale, XRot, YRot, ZRot keyframes
Root Null: only EXPR links to Control layer (Scale/Rotation sliders)
19 AV layers + 1 Null = 20 total (smallest comp)
```

### Pattern F: "Z-Depth Fly-Through"
**Scenes:** 006, 022

**Structure:**
- Many nulls (18 in Scene 006, 8 in 022)
- Exit null uses Z Position deep travel (e.g., [50,50,0] -> [50,50,-4320])
- Word groups stagger at different times
- Creates a dramatic depth fly-through exit

**Key Data (Text 006):**
```
Null exit [idx 2]: KF Position t=2.67 v=[50,50,0] -> t=4.33 v=[50,50,-4320]
Null [idx 3]: KF ZRot t=1.27 v=0 -> t=1.57 v=-7.5 -> t=2.37 v=0 (subtle wobble)
6 word groups, each with its own entrance null
```

### Pattern G: "Direct Scene Animation" (no sub-comp)
**Scenes:** 029, 030

**Structure:**
- Animation lives directly in Scene comp (no Text sub-comp)
- Null chain + Edit Text layers as direct children
- Same expression system (bounce, Control layer links)
- Scene 029 has a "Control" layer (named, not "Null 1") that controls the group

**Key Data (Scene 029):**
```
Control [idx 2]: KF Position t=3.13 v=[50,50,0] -> t=4.13 v=[50,50,-4370]
                 KF ZRot t=0.3 v=90 -> t=1 v=0 -> t=3.13 v=0 -> t=4.13 v=153 + bounce
Null [idx 13]: KF Position t=0.17 v=[-3397.57,21,0] -> t=0.83 v=[42.43,21,0] + bounce
```

**Key Data (Scene 030):**
```
Null exit [idx 2]: t=2.67 pos=[50,50,0] -> t=2.9 pos=[50,257,0] -> t=3.9 pos=[50,-1532,0]
                   t=2.67 scale=[100,100,100] -> t=2.9 scale=[126,126,126] -> t=3.9 scale=[37,37,37]
Null entrance [idx 3]: t=1.67 pos=[1380,50,0] -> t=2.67 pos=[50,50,0]
```

---

## 3. Detailed Keyframe Data for Representative Scenes

### 3a. Text 001 (Pattern A - 7 words, 6.2s, 70 layers)

**Null Chain:**
```
[1] "Null 1" ROOT - parent=none, in=0, out=6.2
    EXPR Scale: temp = comp("Main Composition").layer("Control").effect("Scale")("Slider"); [temp,temp,temp]
    EXPR X Rotation: comp("Main Composition").layer("Control").effect("Rotation X")("Slider")
    EXPR Y Rotation: comp("Main Composition").layer("Control").effect("Rotation Y")("Slider")
    EXPR Z Rotation: comp("Main Composition").layer("Control").effect("Rotation Z")("Slider")

[2] "Null 1" EXIT - parent=Null1[1], in=4.5, out=6.2
    KF Position: {t:4.5, v:[80,62,0]} {t:5.5, v:[60,47,0]} {t:5.67, v:[60,47,0]} {t:5.83, v:[116,47,0]} {t:6.27, v:[-1941,47,0]}
    KF Scale: {t:4.5, v:[100,100,100]} {t:5.5, v:[30,30,30]}
    KF Z Rotation: {t:4.5, v:0} {t:5.5, v:450} {t:5.67, v:450} {t:5.83, v:438} {t:6.27, v:530}

[3] "Null 1" TRANSITION - parent=Null1[1], in=3.17, out=6.2
    KF Position: {t:3.17, v:[20,38,0]} {t:3.83, v:[20,-19,0]} + bounce(amp=8, freq=1, decay=4)
    KF Scale: {t:3.17, v:[100,100,100]} {t:3.83, v:[60,60,60]} + bounce

[4] "Null 1" ROTATION - parent=Null1[1], in=3.17, out=6.2
    KF Z Rotation: {t:3.17, v:0} {t:3.83, v:360} + bounce

[5] "Null 1" ENTRANCE GROUP - parent=Null1[1], in=2, out=6.2
    KF Position: (entrance values with bounce)
    KF Z Rotation: t=2 v=-120 -> t=2.5 v=0 + bounce(amp=8)

[6-13] More entrance/transition nulls for word groups 2-7
```

**AV Layer Pattern (9 copies per Edit Text, offset in Z):**
```
Edit Text 001 copies: parent=Null1, positions offset in Z (0, 2, 4, 6, 8...)
  Opacity EXPR: if(comp("Main Comp").layer("Control").effect("3D Text")("Checkbox")==1) 100 else 0
  Fill Color EXPR: comp("Main Comp").layer("Control").effect("Color Side 01")("Color")
  One copy at 25% opacity (3D depth shadow)
```

### 3b. Text 004 (Pattern B - Track Matte, 4.03s, 58 layers)

**Null Chain:**
```
[3] "Null 1" ROOT - parent=none, in=0, out=4.03
    EXPR Scale/XRot/YRot/ZRot: linked to Control layer

[55] "Null 1" - parent=Null1[3], in=0, out=4.03
    KF Position: {t:0, v:[50,-1222,0]} -> {t:0.67, v:[50,-176.7,0]}
    (entrance from off-screen top)

[57] "Null 1" EXIT - parent=Null1[3]
    KF Position + ZRot for exit
```

**Track Matte AV Layers:**
```
[2] "Edit Text 018" parent=Null1, in=2.17, out=4.03, trackMatte=alphaInverted
    KF Position: {t:2, v:[325.14,1427.80,0]} -> {t:2.33, v=[-72.86,1427.80,0]}
    Easing: eIn=speed:0/influence:16.67, eOut=speed:0/influence:75 (slow start, fast end)

[4] "Edit Text 017" parent=Null1, trackMatte=alphaInverted  
    Similar horizontal wipe pattern
```

### 3c. Text 006 (Pattern F - Z-Depth, 3.67s, 72 layers, 18 nulls)

**Null Chain (6 word groups):**
```
[1] "Null 1" ROOT - EXPR Scale/Rotation from Control
[2] "Null 1" EXIT - in=2.67, KF Position {t:2.67, v:[50,50,0]} -> {t:4.33, v:[50,50,-4320]} (deep Z exit)
[3] "Null 1" WOBBLE - in=1.27, KF ZRot {t:1.27, v:0} -> {t:1.57, v:-7.5} -> {t:2.37, v:0}
[4-18] Word group nulls with staggered entrance times
  Typical: KF ZRot from 360 -> 0 + bounce, KF Scale from [100,100,100] -> smaller
```

**6 Edit Text comps x 9 copies each = 54 AV layers**
```
Edit Text 023-028, one per word group
Each with Z-offset depth copies (z=0,2,4,6,8,10,12,14,16)
Opacity conditional on "3D Text" checkbox
Fill linked to "Color Side 01" or "Color Side 02"
```

### 3d. Text 017 (Pattern C - Slide-In, 3.73s, 42 layers)

**Null Chain:**
```
[1] "Null 1" ROOT - EXPR Scale/Rotation from Control
[2] "Null 1" EMPTY - parent=Null1, in=0, out=3.73 (no KFs, grouping null)
[3] "Null 1" EXIT - parent=Null1, in=3, out=3.73
    KF Position: {t:3, v:[50,50,0]} -> {t:3.17, v:[121,50,0]} -> {t:3.8, v:[-329,50,0]}
    KF Scale: {t:3, v:[100,100,100]} -> {t:3.17, v:[107,107,107]} -> {t:3.8, v:[0,0,0]}
    KF Z Rotation: {t:3, v:0} -> {t:3.17, v:-12.2} -> {t:3.8, v:90}
    (3-keyframe "hesitate then fly out" pattern)

[6] "Null 1" ENTRANCE - parent=Null1, in=2, out=3.73
    KF Position: {t:2, v:[50.1,50,0]} -> {t:3, v:[49.9,58.6,0]}
    KF Scale: {t:2, v:[100,100,100]} -> {t:3, v:[smaller]}
```

**Slide-In AV Layers:**
```
[4] "Edit Text 069" parent=Null1[3], in=2, out=3.73, trackMatte=alphaInverted
    KF Position: {t:2, v:[36,1812,0]} -> {t:3, v:[36,50,0]} (slides UP from below)
    EXPR Position: bounce(amp=12, freq=1, decay=4)
    Scale: [259.71, 259.71, 259.71] (static, large)
    Anchor: [1200,75,0]

[5] "Edit Text 068" parent=Null1[3], in=2, out=3.73, trackMatte=alphaInverted
    KF Position: {t:2, v:[52,-1553,0]} -> {t:3, v=[52,50,0]} (slides DOWN from above)
    EXPR Position: bounce(amp=12)
    Anchor: [0,75,0]
```

**Z-Depth Copies (8 per word):**
```
Edit Text 066 x9: parent=idx10, positions=[601.5,75,z] where z=0,2,4,...,16
Edit Text 067 x9: parent=idx8, positions=[604.7,75,z]
Edit Text 068 x9: parent=idx5, positions=[0,75,z]
Edit Text 069 x9: parent=idx4, positions=[1199.6,75,z]
```

### 3e. Text 023 (Pattern E - AV-Driven, 3.8s, 20 layers)

**Minimal Null Chain:**
```
[1] "Null 1" ROOT - only EXPR Scale/Rotation from Control (no KFs at all)
```

**AV Layers Drive All Animation:**
```
Each of 19 AV layers has its own KF Position, Scale, X/Y/Z Rotation
  EXPR Opacity: if(3D Text checkbox==1) 100 else 0
  EXPR Fill Color: linked to Color Side 01 or 02
  Fill effect present
```

### 3f. Text 028 (Pattern D - Y-Rotation Flip, 3.17s, 49 layers)

**Null Chain:**
```
[3] "Null 1" ROOT parent=none, in=0, out=3.17
    EXPR Scale/Rotation from Control

[4] "Null 1" EXIT parent=Null1[3], in=0, out=3.17
    KF Scale: {t:1.5, v:[100,100,100]} -> {t:2.5, v:[0,0,0]}  
    KF Y Rotation: {t:1.5, v:0} -> {t:2.5, v:270} (3/4 turn card flip)
    KF Position: {t:1.5, v:[50,50,0]} -> {t:2.5, v:[50,50,-1460]}
    Static: Scale=[67,67,67], Position=[50,50,244]
```

**AV Opacity Strobe (unique to 028):**
```
[1] "Edit Text 117" parent=Null1, in=1.47, out=12.07
    KF Opacity: {t:1.73, v:0} -> {t:2.03, v:100} -> {t:2.1, v:100} -> {t:2.23, v:0}
    Easing: linear (speed:333.33 / influence:16.67)
    Creates rapid flash/strobe reveal

[2] "Edit Text 117" copy with different timing - staggered strobe
```

---

## 4. Scene-Level Effects

### Layer Structure (ALL 30 scenes identical)

Every scene (001-028) has exactly 6 layers referencing the same Text sub-comp:

| Layer | Blend Mode | Opacity | Purpose |
|-------|-----------|---------|---------|
| Text NNN | normal | 100 | Main text animation |
| Drop Shadow | normal | 0 | Drop shadow (disabled by default) |
| Glow 02 | normal | 0 | Second glow pass (disabled) |
| Glow 01 | normal | 0 | First glow pass (disabled) |
| Shadow | normal | 0 | Floor shadow (disabled) |
| Long Shadow | normal | 0 | Extruded shadow (disabled) |

**Key Finding:** All effect layers (Drop Shadow, Glow 01/02, Shadow, Long Shadow) have **opacity 0** by default. They are disabled templates meant to be toggled on by the user. The animation itself is entirely self-contained in the Text sub-comp.

**Layer order varies** between scenes:
- Scenes 001-006, 018-030: Text on top, Drop Shadow second
- Scenes 007-017: Text on top, Long Shadow second

**Scenes 029-030** do NOT follow this pattern -- they have nulls and Edit Text layers directly in the scene comp.

---

## 5. Edit Text Sub-Comps

### Structure (consistent across all 117 comps)

Each Edit Text comp contains:
- **1 text layer** (the actual editable text)
- **Comp size:** 500x150 (most) or variable
- **Duration:** 10.03s (default) or 6.03-6.2s (later comps)

### Sample Data

| Comp | Text Content | Position | Anchor | Scale |
|------|-------------|----------|--------|-------|
| Edit Text 001 | "hey 2" | [248.21, 75, 0] | [0.19, -16.47, 0] | [100,100,100] |
| Edit Text 002 | "friend" | [11.89, 75.25, 0] | [1.88, -26.25, 0] | [100,100,100] |
| Edit Text 003 | "you" | [489, 75, 0] | -- | -- |
| Edit Text 008 | "Just" | [250, 75, 0] | [0.10, -34.25, 0] | [100,100,100] |
| Edit Text 009 | "add" | [249.28, 110, 0] | [0.09, -31.80, 0] | [100,100,100] |

### Properties
- All have `Variable Font Spacing: 1`
- No animations inside Edit Text comps (static text only)
- Position is center-aligned (x ~ 250 for centered text, varies for left/right aligned)
- Anchor point is near text baseline origin
- No effects on the text layers themselves

### "Pre Edit Text" Comps (2 found)
- `Pre Edit Text 044` and `Pre Edit Text 045`: 14 layers each, 9.5s
- Contain 14 Null layers (no source) -- these appear to be animation pre-compositions for more complex word-by-word reveals

---

## 6. Common Expression Templates

### Bounce Expression (used on Position, Scale, Z Rotation)
```javascript
amp = 8       // amplitude (varies: 8, 12, 40)
freq = 1      // frequency (always 1)
decay = 4     // decay rate (varies: 2, 4)
n = 0;
if (numKeys > 0) {
  n = nearestKey(time).index;
  if (key(n).time > time) { n--; }
}
if (n == 0) { t = 0; } 
else { t = time - key(n).time; }
if (n > 0) {
  v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
  value + (v/100) * amp * Math.sin(freq * t * 2 * Math.PI) / Math.exp(decay * t);
} else {
  value;
}
```

**Variants by amplitude:**
- `amp=8, decay=4`: standard bounce (most nulls)
- `amp=12, decay=4`: stronger bounce (entrance nulls, Scene 017/029)
- `amp=40, decay=2`: heavy bounce (Scene 024 X Rotation)

### Control Layer Expressions
```javascript
// Scale -- linked to Scale slider
temp = comp("Main Composition").layer("Control").effect("Scale")("Slider");
[temp, temp, temp]

// Rotation -- linked to individual axis sliders
comp("Main Composition").layer("Control").effect("Rotation X")("Slider")
comp("Main Composition").layer("Control").effect("Rotation Y")("Slider")
comp("Main Composition").layer("Control").effect("Rotation Z")("Slider")
```

### 3D Text Visibility
```javascript
// Toggle 3D depth copies
if (comp("Main Composition").layer("Control").effect("3D Text")("Checkbox") == 1) 100 else 0;
// Shadow copies use 25 instead of 100
```

### Fill Color Expression
```javascript
comp("Main Composition").layer("Control").effect("Color Side 01")("Color")
comp("Main Composition").layer("Control").effect("Color Side 02")("Color")
```

---

## 7. Easing Reference

### Common Easing Patterns

**Entrance (overshoot/bounce):**
```
easeIn:  {speed: 0, influence: 75}      // slow departure from start
easeOut: {speed: 0, influence: 75}      // slow arrival
+ bounce expression applied on top
```

**Exit (smooth acceleration):**
```
easeIn:  {speed: 0, influence: 16.6667}  // quick departure
easeOut: {speed: 0, influence: 16.6667}  // linear arrival
```

**Hold-to-exit (3KF hesitate pattern):**
```
KF1 (hold):    influence: 16.67 / 16.67
KF2 (hesitate): influence: varies (builds up)
KF3 (fly out):  influence: 16.67 / 16.67
```

---

## 8. Implementation Guide

### Architecture
Each scene follows this hierarchy:
```
Scene Comp (1920x1080)
  ├── Text NNN (main animation sub-comp, same size)
  │     ├── Null 1 [ROOT] -- EXPR links to Control layer
  │     ├── Null 1 [EXIT] -- KF Position/Scale/ZRot for exit
  │     ├── Null 1 [ENTRANCE] -- KF Position/ZRot + bounce for entrance
  │     ├── ...more nulls for transitions/groups...
  │     ├── Edit Text 0XX (x9, Z-depth copies, parent=Null)
  │     │     └── Text layer ("word")
  │     ├── Edit Text 0YY (x9, parent=Null)
  │     └── ...
  ├── Drop Shadow (opacity 0, disabled)
  ├── Glow 01 (opacity 0)
  ├── Glow 02 (opacity 0)
  ├── Shadow (opacity 0)
  └── Long Shadow (opacity 0)
```

### Key Implementation Details

1. **3D Depth Copies:** Each Edit Text comp is instantiated 9 times with Z offsets (0,2,4,6,...,16). One copy at 25% opacity acts as depth shadow. The "3D Text" checkbox toggles these.

2. **Two Color Sides:** AV layers alternate between `Color Side 01` and `Color Side 02` fill expressions. Front-facing copies use one color, depth copies use the other.

3. **Bounce Expression:** Post-keyframe physics simulation. Apply after the last keyframe on any property. Use velocity at keyframe time to determine initial bounce amplitude.

4. **Null Purpose Detection:** 
   - `in=0` with only EXPR: Root null (Control link)
   - `in` near comp end + exit KFs: Exit null
   - `in` near start + entrance KFs: Entrance null
   - Middle timing: Transition null

5. **Track Matte Scenes (004, 018):** Alpha-inverted matte creates a wipe reveal. The AV layer slides horizontally while masked, revealing text progressively.

6. **Scene 023 Exception:** No null animation chain. Each AV layer animates independently with full 3D transforms. Simplest to implement but hardest to generalize.

### Duration Ranges
- Shortest: Scene 016 (1.97s)
- Longest: Scene 001 (6.20s)
- Average: ~3.6s
- Most scenes: 3.0-4.2s

### Word Count per Scene
- 2 words: Scenes 023, 024 (2 Edit Text comps)
- 3 words: Scenes 003, 009, 013, 014, 019, 025, 026, 027, 028, 029, 030
- 4 words: Scenes 002, 004, 005, 007, 008, 010, 011, 012, 015, 016, 017, 020, 021
- 6 words: Scenes 006, 022
- 7 words: Scene 001
- 7 words: Scene 018
