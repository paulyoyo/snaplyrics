# Isokinetic Typography — Complete Scene Analysis

Exported from: Isokinetic
Scenes: 8 | Sub-compositions: 10

Generated for JSX rebuild. All expressions, keyframes, effect values included verbatim.

---

## Scene_01
Duration: 20.0534s | 1920x1080 | 29.97fps | Layers: 12

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Center Point:
        Point (ADBE Point Control-0001): [960,484]
      [Effect] Wiggle:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Title_01:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_03:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_04:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_05:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_06:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Rotation_02" — type=av, enabled=false, parent="none", in=0, out=20.0534, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,484,0]
        EXPR: ```
        x=thisComp.layer("Control").effect("Center Point")("ADBE Point Control-0001")[0];
        y=thisComp.layer("Control").effect("Center Point")("ADBE Point Control-0001")[1];
        z=0;
        [x,y,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [298.0843,3.5944,43.685]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=5 else x=0;
        wiggle(0.5,x)
        ```
      X Rotation (ADBE Rotate X): -180
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=0, v=180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-490.4182,"influence":16.6667}]
          t=0.367, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":-490.4182,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=10.01, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-490.4182,"influence":16.6667}]
          t=10.377, v=-180, interpIn=linear, interpOut=linear, easeIn=[{"speed":-490.4182,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_01" — type=text, enabled=true, parent="Rotation_02", in=0, out=10.1101, 3D=true, collapse=true
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "ISO", font=Montserrat-Black, size=400, color=[1,1,1], tracking=0, leading=480, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [5.6016,-140,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,0,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_02" — type=text, enabled=true, parent="Rotation_02", in=0.1001, out=10.2102, 3D=true, collapse=true
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "pack", font=Montserrat-Black, size=112, color=[1,1,1], tracking=0, leading=134.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [3.7526,-83.104,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [373.7977,0,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_01"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_01").transform.position[0]; 
        y=thisComp.layer("Title_01").transform.position[1]; 
        z=thisComp.layer("Title_01").transform.position[2]; 
        [x+sizex/2+20,y,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,137.1084,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -59
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=0.1001, v=-180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":449.55,"influence":16.6667}]
          t=0.3003, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":449.55,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=10.01, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":154.845,"influence":16.6667}]
          t=10.2102, v=-59, interpIn=linear, interpOut=linear, easeIn=[{"speed":154.845,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Z Rotation (ADBE Rotate Z): -90
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Title_03" — type=text, enabled=true, parent="Rotation_02", in=0.1001, out=10.2102, 3D=true, collapse=true
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "kenetic", font=Montserrat-Black, size=175.1, color=[1,1,1], tracking=0, leading=210.12, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [4.2033,-143.7571,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,166.4,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_01"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_01").transform.position[0]; 
        y=thisComp.layer("Title_01").transform.position[1]; 
        z=thisComp.layer("Title_01").transform.position[2]; 
        [x,y+sizey/2+20,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=0.2336, v=180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-449.55,"influence":16.6667}]
          t=0.4338, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":-449.55,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=10.01, v=90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":33.3333}]
          t=10.4771, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":-385.3286,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Rotation_01" — type=av, enabled=false, parent="none", in=10.1101, out=20.0534, 3D=true, startTime=10.01
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,484,0]
        EXPR: ```
        x=thisComp.layer("Control").effect("Center Point")("ADBE Point Control-0001")[0];
        y=thisComp.layer("Control").effect("Center Point")("ADBE Point Control-0001")[1];
        z=0;
        [x,y,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [298.0843,3.5944,43.685]
        EXPR: ```
        thisComp.layer("Rotation_02").transform.orientation
        ```
      X Rotation (ADBE Rotate X): 0
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=10.01, v=180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-490.4182,"influence":16.6667}]
          t=10.377, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":-490.4182,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=19.653, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-490.4182,"influence":16.6667}]
          t=20.02, v=-180, interpIn=linear, interpOut=linear, easeIn=[{"speed":-490.4182,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Title_04" — type=text, enabled=true, parent="Rotation_01", in=10.1101, out=20.0534, 3D=true, collapse=true, startTime=10.01
   Markers: [{"time":11.5115,"comment":"Change text","duration":0}]
   Text: "20+", font=Montserrat-Black, size=400, color=[1,1,1], tracking=0, leading=480, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-13.599,-140,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,0,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "Title_05" — type=text, enabled=true, parent="Rotation_01", in=10.1101, out=19.9867, 3D=true, collapse=true, startTime=10.01
   Markers: [{"time":11.5115,"comment":"Change text","duration":0}]
   Text: "titles", font=Montserrat-Black, size=92, color=[1,1,1], tracking=0, leading=110.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-0.8274,-75.532,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [395.5945,0,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_04"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_04").transform.position[0]; 
        y=thisComp.layer("Title_04").transform.position[1]; 
        z=thisComp.layer("Title_04").transform.position[2]; 
        [x+sizex/2+20,y,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,128.4084,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=10.1101, v=-180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":449.55,"influence":16.6667}]
          t=10.3103, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":449.55,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=19.653, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":154.845,"influence":16.6667}]
          t=19.8532, v=-59, interpIn=linear, interpOut=linear, easeIn=[{"speed":154.845,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Z Rotation (ADBE Rotate Z): -90
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

9. "Title_06" — type=text, enabled=true, parent="Rotation_01", in=10.1101, out=19.9867, 3D=true, collapse=true, startTime=10.01
   Markers: [{"time":11.5115,"comment":"Change text","duration":0}]
   Text: "typography", font=Montserrat-Black, size=120.3, color=[1,1,1], tracking=0, leading=144.36, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [0.9024,-89.2626,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,166.4,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_04"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_04").transform.position[0]; 
        y=thisComp.layer("Title_04").transform.position[1]; 
        z=thisComp.layer("Title_04").transform.position[2]; 
        [x,y+sizey/2+20,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 90
        EXPR: ```
        amp = 0.1;
        freq = 2;
        decay = 3;
        n = 0;
        if (numKeys > 0){
        n = nearestKey(time).index;
        if (key(n).time > time){
        n--;
        }
        }
        if (n == 0){
        t = 0;
        }else{
        t = time - key(n).time;
        }
        
        if (n > 0){
        v = velocityAtTime(key(n).time - thisComp.frameDuration/10);
        value + v*amp*Math.sin(freq*t*2*Math.PI)/Math.exp(decay*t);
        }else{
        value;
        }
        ```
        Keyframes [4]:
          t=10.2436, v=180, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-449.55,"influence":16.6667}]
          t=10.4438, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":-449.55,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
          t=19.653, v=90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":33.3333}]
          t=20.1201, v=-90, interpIn=linear, interpOut=linear, easeIn=[{"speed":-385.3286,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

10. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=20.0534, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

11. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

12. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_02
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 10

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Wiggle:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Titles:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_01:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_03:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_04:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_05:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_06:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Rotation_02" — type=av, enabled=false, parent="none", in=0, out=20.0534, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,540,0]
        Keyframes [2]:
          t=0, v=[960,664,0], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":0,"influence":90.4252}]
          t=2.0687, v=[960,540,0], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":87.9506}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Titles")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [25.9755,326.8069,352.1916]
        Keyframes [2]:
          t=0, v=[0,0,0], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":0,"influence":90.4252}]
          t=2.0687, v=[25.9755,326.8069,352.1916], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":87.9506}], easeOut=[{"speed":0,"influence":16.6667}]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_01" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "new project new project new project ", font=Montserrat-Black, size=181, color=[1,1,1], tracking=0, leading=217.2, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-22.3517,2.896,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,-371.4881,64.9482]
        EXPR: ```
        textLayer = thisComp.layer("Title_02"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_02").transform.position[0]; 
        y=thisComp.layer("Title_02").transform.position[1]; 
        z=thisComp.layer("Title_02").transform.position[2]; 
        [value[0],y,z+sizey]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [88.87,88.87,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.3003, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -11.13
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_02" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "special for videohive  special for videohive  special for videohive", font=Montserrat-Black, size=100, color=[1,1,1], tracking=0, leading=120, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-1.0494,1.6,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,-371.4881,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_03"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_03").transform.position[0]; 
        y=thisComp.layer("Title_03").transform.position[1]; 
        z=thisComp.layer("Title_03").transform.position[2]; 
        [value[0],y-sizey,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [88.727,88.727,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.1335, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -11.273
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Title_03" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "LOOK LOOK LOOK", font=Montserrat-Black, size=502, color=[1,1,1], tracking=0, leading=602.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [20.5821,8.032,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,0,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [101.0951,101.0951,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.0667, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.367, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 1.0951
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Title_04" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "different angle different angle different angle", font=Montserrat-Black, size=200, color=[1,1,1], tracking=0, leading=240, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [2.3012,-143.2,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,0,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_03"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_03").transform.position[0]; 
        y=thisComp.layer("Title_03").transform.position[1]; 
        z=thisComp.layer("Title_03").transform.position[2]; 
        [value[0],y,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [104.6903,104.6903,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.2336, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.5339, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 4.6903
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Title_05" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "envato envato envato", font=Montserrat-Black, size=348, color=[1,1,1], tracking=0, leading=417.6, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [4.8735,-249.168,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,0,-153.2666]
        EXPR: ```
        textLayer = thisComp.layer("Title_04"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_04").transform.position[0]; 
        y=thisComp.layer("Title_04").transform.position[1]; 
        z=thisComp.layer("Title_04").transform.position[2]; 
        [value[0],y,z-sizey]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [113.4119,113.4119,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.1335, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 13.4119
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "Title_06" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":2.0687,"comment":"Change text","duration":0}]
   Text: "expression expression expression expression", font=Montserrat-Black, size=330, color=[1,1,1], tracking=0, leading=396, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [0.0023,-236.28,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [0,288.9009,-153.2666]
        EXPR: ```
        textLayer = thisComp.layer("Title_05"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_05").transform.position[0]; 
        y=thisComp.layer("Title_05").transform.position[1]; 
        z=thisComp.layer("Title_05").transform.position[2]; 
        [value[0],y+sizey,z]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [112.1026,112.1026,100]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=effect("Wiggle")("ADBE Slider Control-0001") else x=0;
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1+x, temp2+x, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.3337, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.634, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 12.1026
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

9. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

10. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_08
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 14

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Wiggle:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Title_01:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_03:
        Slider (ADBE Slider Control-0001): 50
      [Effect] Size - Title_04:
        Slider (ADBE Slider Control-0001): 50
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_01" — type=text, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "IT", font=Montserrat-Black, size=152, color=[1,1,1], tracking=0, leading=182.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [4.0286,-53.2,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_02" — type=text, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "IS", font=Montserrat-Black, size=152, color=[1,1,1], tracking=0, leading=182.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [3.3442,-53.2,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [1149.755,536.392,190.0222]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_03" — type=text, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Markers: [{"time":3.37,"comment":"Change text","duration":0}]
   Text: "MAGIC", font=Montserrat-Black, size=152, color=[1,1,1], tracking=0, leading=182.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [4.028,-53.2,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [959.7328,536.392,380.0445]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [50,50,50]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [0,270,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Title_04" — type=text, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Markers: [{"time":3.37,"comment":"Change text","duration":0}]
   Text: "CUBE", font=Montserrat-Black, size=152, color=[1,1,1], tracking=0, leading=182.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-0.3792,-53.2,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [769.7105,536.392,190.0222]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [50,50,50]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Cube_01" — type=av, enabled=true, parent="none", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,190]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
        EXPR: ```
        if(thisComp.layer("Control").effect("Wiggle")("ADBE Checkbox Control-0001")==1) x=5 else x=0;
        wiggle(0.5,x)
        ```
      X Rotation (ADBE Rotate X): 25
      Y Rotation (ADBE Rotate Y): 998.7896
        Keyframes [2]:
          t=0, v=45, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":54.0361,"influence":16.6667}]
          t=19.9867, v=1125, interpIn=linear, interpOut=linear, easeIn=[{"speed":54.0361,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Cube_02" — type=av, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,0]
      Position (ADBE Position): [769.7105,536.392,190.0222]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "Cube_03" — type=av, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,0]
      Position (ADBE Position): [1149.755,536.392,190.0222]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

9. "Cube_04" — type=av, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,0]
      Position (ADBE Position): [959.7328,726.4143,190.0223]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

10. "Cube_05" — type=av, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,0]
      Position (ADBE Position): [959.7327,346.3697,190.0223]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

11. "Cube_06" — type=av, enabled=true, parent="Cube_01", in=0, out=20.02, 3D=true, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [959.7327,536.392,0]
      Position (ADBE Position): [959.7328,536.392,380.0445]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,270,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
        EXPR: ```
        toCompVec([0, 0, 1])[2] > 0 ? value : 0
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Stroke:
        Path (ADBE Stroke-0001): 1
        All Masks (ADBE Stroke-0010): 0
        Stroke Sequentially (ADBE Stroke-0011): 1
        Color (ADBE Stroke-0002): [1,1,1,1]
        Brush Size (ADBE Stroke-0003): 7.4
        Brush Hardness (ADBE Stroke-0004): 0.75
        Opacity (ADBE Stroke-0005): 1
        Start (ADBE Stroke-0008): 0
        End (ADBE Stroke-0009): 100
        Spacing (ADBE Stroke-0006): 15
        Paint Style (ADBE Stroke-0007): 3
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

12. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=20.02, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

13. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

14. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_10
Duration: 10.0434s | 1920x1080 | 29.97fps | Layers: 7

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=10.0434
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Substrate:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Title:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - echo:
        Slider (ADBE Slider Control-0001): -0.048
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_01" — type=av, enabled=true, parent="none", in=0, out=10.0434, collapse=true
   Markers: [{"time":1.7017,"comment":"Open and change text","duration":0}]
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [-100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title")("ADBE Slider Control-0001")-100;
        [-temp1, temp2]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
      [Effect] CC Cylinder:
        Radius (%) (CC Cylinder-0002): 100
        Position X (CC Cylinder-0004): 0
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[0]-960
          ```
        Position Y (CC Cylinder-0005): 50.6667
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[1]-540
          ```
        Position Z (CC Cylinder-0006): -1900
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[2]
          ```
        Rotation X (CC Cylinder-0009): -62
          Keyframes [2]:
            t=0, v=-165.4, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":19.1879}]
            t=3.003, v=-62, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":13.5513}], easeOut=[{"speed":0,"influence":33.3333}]
        Rotation Y (CC Cylinder-0010): -102
          Keyframes [2]:
            t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-33.966,"influence":16.6667}]
            t=3.003, v=-102, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":33.3333}]
        Rotation Z (CC Cylinder-0011): 0
        Rotation Order (CC Cylinder-0027): 3
        Render (CC Cylinder-0013): 1
        Light Intensity (CC Cylinder-0015): 300
        Light Color (CC Cylinder-0016): [1,1,1,1]
        Light Height (CC Cylinder-0017): 100
        Light Direction (CC Cylinder-0018): 0
        Ambient (CC Cylinder-0021): 55
        Diffuse (CC Cylinder-0022): 54
        Specular (CC Cylinder-0023): 99
        Roughness (CC Cylinder-0024): 0.075
        Metal (CC Cylinder-0025): 100
      [Effect] Echo:
        Echo Time (seconds) (ADBE Echo-0001): -0.168
          EXPR: ```
          thisComp.layer("Control").effect("Size - echo")("ADBE Slider Control-0001")-0.12
          ```
        Number Of Echoes (ADBE Echo-0002): 25
        Starting Intensity (ADBE Echo-0003): 1
        Decay (ADBE Echo-0004): 1
        Echo Operator (ADBE Echo-0005): 6
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_02" — type=av, enabled=false, parent="none", in=0, out=20.02, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [-200,200,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title")("ADBE Slider Control-0001")-100;
        [-temp1, temp2]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] CC Cylinder:
        Radius (%) (CC Cylinder-0002): 100
        Position X (CC Cylinder-0004): 0
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[0]-960
          ```
        Position Y (CC Cylinder-0005): 50.6667
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[1]-540
          ```
        Position Z (CC Cylinder-0006): -1900
          EXPR: ```
          thisComp.layer("Rotation_01").transform.position[2]
          ```
        Rotation X (CC Cylinder-0009): -62
          Keyframes [2]:
            t=0, v=-165.4, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":19.1879}]
            t=3.003, v=-62, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":13.5513}], easeOut=[{"speed":0,"influence":33.3333}]
        Rotation Y (CC Cylinder-0010): -102
          Keyframes [2]:
            t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-33.966,"influence":16.6667}]
            t=3.003, v=-102, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":33.3333}]
        Rotation Z (CC Cylinder-0011): 0
        Rotation Order (CC Cylinder-0027): 3
        Render (CC Cylinder-0013): 1
        Light Intensity (CC Cylinder-0015): 238
        Light Color (CC Cylinder-0016): [1,1,1,1]
        Light Height (CC Cylinder-0017): 100
        Light Direction (CC Cylinder-0018): 0
        Ambient (CC Cylinder-0021): 55
        Diffuse (CC Cylinder-0022): 54
        Specular (CC Cylinder-0023): 99
        Roughness (CC Cylinder-0024): 0.075
        Metal (CC Cylinder-0025): 100
      [Effect] Echo:
        Echo Time (seconds) (ADBE Echo-0001): -0.168
          EXPR: ```
          thisComp.layer("Control").effect("Size - echo")("ADBE Slider Control-0001")-0.12
          ```
        Number Of Echoes (ADBE Echo-0002): 25
        Starting Intensity (ADBE Echo-0003): 1
        Decay (ADBE Echo-0004): 1
        Echo Operator (ADBE Echo-0005): 6
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Rotation_01" — type=av, enabled=true, parent="none", in=0, out=10.0434, 3D=true
   Markers: [{"time":3.003,"comment":"","duration":0}]
   Transform:
      Anchor Point (ADBE Anchor Point): [50,50,0]
      Position (ADBE Position): [960,590.6667,-1900]
        Keyframes [2]:
          t=0, v=[966.6693,1897.3777,2464.3779], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":1666.7687,"influence":16.6667}]
          t=3.003, v=[960,590.6667,-1900], interpIn=linear, interpOut=linear, easeIn=[{"speed":1666.7687,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=10.0434, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 0
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Background" — type=av, enabled=true, parent="none", in=0, out=10.0434
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Background" — type=av, enabled=true, parent="none", in=0, out=10.0434
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_12
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 9

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Wiggle:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Substrate:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_01" — type=av, enabled=true, parent="none", in=0, out=20.02, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [947.6297,133.7533,499.3331]
        Keyframes [2]:
          t=0, v=[960,540,967], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=[947.6297,133.7533,499.3331], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [30,0,0]
        Keyframes [2]:
          t=0, v=[0,0,0], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":36.1197}]
          t=1.7017, v=[30,0,0], interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -45
        Keyframes [2]:
          t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=-45, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_01_x1" — type=av, enabled=true, parent="Title_01", in=0, out=20.02, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [289.1759,95,0]
      Position (ADBE Position): [289.1759,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 90
        Keyframes [2]:
          t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
          Keyframes [2]:
            t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
            t=1.7017, v=-50, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_01_x2" — type=av, enabled=true, parent="Title_01_x1", in=0, out=20.02, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [760.0892,95.0111,0]
      Position (ADBE Position): [760.0892,95.0111,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
        Keyframes [2]:
          t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=-90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Title_01_x3" — type=av, enabled=true, parent="Title_01_x2", in=0, out=20.02, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [979.5099,95.0111,0]
      Position (ADBE Position): [979.5099,95.0111,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 90
        Keyframes [2]:
          t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
          Keyframes [2]:
            t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
            t=1.7017, v=-50, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Title_01_x4" — type=av, enabled=true, parent="Title_01_x3", in=0, out=20.02, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [1541.8264,95.0333,0]
      Position (ADBE Position): [1541.8264,95.0333,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): -90
        Keyframes [2]:
          t=0, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":33.3333}], easeOut=[{"speed":0,"influence":80.4954}]
          t=1.7017, v=-90, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":91.6409}], easeOut=[{"speed":0,"influence":33.3333}]
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=20.0534, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

9. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_15
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 11

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Titles:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_01:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_03:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_04:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_05:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_06:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Rotation_02" — type=av, enabled=false, parent="none", in=0, out=20.0534, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = thisComp.layer("Control").effect("Size - Titles")("ADBE Slider Control-0001");
        [temp, temp, temp]
        ```
      Orientation (ADBE Orientation): [19.9755,40.8069,8.1916]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 0
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_01" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "VIDEOHIVE VIDEOHIVE VIDEOHIVE", font=Montserrat-Black, size=185, color=[1,1,1], tracking=0, leading=222, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-4.9015,2.96,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [148.5309,-354.288,150.06]
        EXPR: ```
        textLayer = thisComp.layer("Title_02"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_02").transform.position[0]; 
        y=thisComp.layer("Title_02").transform.position[1]; 
        z=thisComp.layer("Title_02").transform.position[2]; 
        [value[0],y,z+sizey]
        ```
        Keyframes [2]:
          t=0, v=[0,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":28.7192,"influence":16.6667}]
          t=19.9867, v=[574,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":28.7192,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.3003, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -2.0003
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_02" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "videohive videohive videohive videohive videohive videohive", font=Montserrat-Black, size=205, color=[1,1,1], tracking=0, leading=246, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-5.4314,3.28,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [31.8282,-354.288,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_03"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_03").transform.position[0]; 
        y=thisComp.layer("Title_03").transform.position[1]; 
        z=thisComp.layer("Title_03").transform.position[2]; 
        [value[0],y-sizey,z]
        ```
        Keyframes [2]:
          t=0, v=[0,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":6.1541,"influence":16.6667}]
          t=19.9867, v=[123,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":6.1541,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.0667, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.367, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 3.0945
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Title_03" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.0667
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "videohive videohive videohive videohive", font=Montserrat-Black, size=484, color=[1,1,1], tracking=0, leading=580.8, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-12.8233,7.744,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [107.6461,0,0]
        Keyframes [2]:
          t=0, v=[0,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":20.8139,"influence":16.6667}]
          t=19.9867, v=[416,0,0], interpIn=linear, interpOut=linear, easeIn=[{"speed":20.8139,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_03")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.1335, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -7.5007
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Title_04" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "videohive videohive videohive videohive videohive videohive videohive videohive videohive videohive videohive videohive", font=Montserrat-Black, size=64, color=[1,1,1], tracking=0, leading=76.8, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-1.6956,-45.824,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [169.2333,0,0]
        EXPR: ```
        textLayer = thisComp.layer("Title_03"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_03").transform.position[0]; 
        y=thisComp.layer("Title_03").transform.position[1]; 
        z=thisComp.layer("Title_03").transform.position[2]; 
        [value[0],y,z]
        ```
        Keyframes [2]:
          t=0, v=[0,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":32.7218,"influence":16.6667}]
          t=19.9867, v=[654,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":32.7218,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_04")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.2002, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.5005, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -17.5654
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Title_05" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "videohive videohive videohive videohive", font=Montserrat-Black, size=220, color=[1,1,1], tracking=0, leading=264, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-5.8288,-157.52,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [147.7546,0,-46.848]
        EXPR: ```
        textLayer = thisComp.layer("Title_04"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_04").transform.position[0]; 
        y=thisComp.layer("Title_04").transform.position[1]; 
        z=thisComp.layer("Title_04").transform.position[2]; 
        [value[0],y,z-sizey]
        ```
        Keyframes [2]:
          t=0, v=[0,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":28.5691,"influence":16.6667}]
          t=19.9867, v=[571,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":28.5691,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_05")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.2669, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.5672, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): -7.4392
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "Title_06" — type=text, enabled=true, parent="Rotation_02", in=0, out=20.02, 3D=true, collapse=true, startTime=-0.367
   Markers: [{"time":1.7017,"comment":"Change text","duration":0}]
   Text: "videohive videohive videohive videohive videohive", font=Montserrat-Black, size=752, color=[1,1,1], tracking=0, leading=902.4, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [-19.9239,-538.432,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        ```
      Position (ADBE Position): [124.207,161.04,-46.848]
        EXPR: ```
        textLayer = thisComp.layer("Title_05"); 
        bbox = textLayer.sourceRectAtTime(time,true); 
        sizex=bbox.width*textLayer.scale[0]/100; 
        sizey=bbox.height*textLayer.scale[1]/100; 
        x=thisComp.layer("Title_05").transform.position[0]; 
        y=thisComp.layer("Title_05").transform.position[1]; 
        z=thisComp.layer("Title_05").transform.position[2]; 
        [value[0],y+sizey,z]
        ```
        Keyframes [2]:
          t=0, v=[0,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":24.016,"influence":16.6667}]
          t=19.9867, v=[480,-0.6625,-115.1483], interpIn=linear, interpOut=linear, easeIn=[{"speed":24.016,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp1 = transform.scale[0]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp2 = transform.scale[1]+thisComp.layer("Control").effect("Size - Title_06")("ADBE Slider Control-0001")-100;
        temp3 = transform.scale[2];
        [temp1, temp2, temp3]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0.3337, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":333,"influence":16.6667}]
          t=0.634, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":16.6667}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -50
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
      [Effect] Wiggle:
        Slider (ADBE Slider Control-0001): 16.1639
          EXPR: ```
          wiggle(0.5,30)
          ```
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

9. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=60.0601, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

10. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

11. "Background" — type=av, enabled=true, parent="none", in=0, out=20.0534
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_17
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 7

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] High quality:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Titles:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Substrate:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Titles:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_01" — type=av, enabled=false, parent="none", in=0, out=20.02
   Markers: [{"time":1.7017,"comment":"Open and change text","duration":0}]
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Pre-comp-title_17" — type=av, enabled=true, parent="none", in=0, out=20.02, collapse=true, startTime=-1.001
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Time Displacement:
        Time Displacement Layer (ADBE Time Displacement-0001): 7
        Max Displacement Time [sec] (ADBE Time Displacement-0002): 0.7
        Time Resolution [fps] (ADBE Time Displacement-0003): 350
          EXPR: ```
          if(thisComp.layer("Control").effect("High quality")("ADBE Checkbox Control-0001")==1) 350 else 100
          ```
        If Layer Sizes Differ (ADBE Time Displacement-0004): 1
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Titles")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=20.0534, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "GRADIENT_01" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Scene_18
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 8

### Layer Hierarchy

1. "Control" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] High quality:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Noise BG:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Alpha BG:
        Checkbox (ADBE Checkbox Control-0001): 0
      [Effect] Subtext:
        Checkbox (ADBE Checkbox Control-0001): 1
      [Effect] Color - BG 1:
        Color (ADBE Color Control-0001): [0.1451,0.1451,0.1451,1]
      [Effect] Color - BG 2:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Title_01:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Substrate_01:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Title_02:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Color - Substrate_02:
        Color (ADBE Color Control-0001): [0,0,0,1]
      [Effect] Color - Subtext:
        Color (ADBE Color Control-0001): [1,1,1,1]
      [Effect] Size - Title_01:
        Slider (ADBE Slider Control-0001): 100
      [Effect] Size - Title_02:
        Slider (ADBE Slider Control-0001): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_01" — type=av, enabled=false, parent="none", in=0, out=20.02
   Markers: [{"time":1.7017,"comment":"Open and change text","duration":0}]
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Title_01")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate_01")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_02" — type=av, enabled=false, parent="none", in=0, out=20.02
   Markers: [{"time":1.7017,"comment":"Open and change text","duration":0}]
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Title_01")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate_01")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Pre-comp-title_18" — type=av, enabled=true, parent="none", in=0, out=20.02, collapse=true, startTime=-1.001
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Title_01")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Substrate_01")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Element_01" — type=shape, enabled=true, parent="none", in=0, out=20.0534, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [836.2499,-448.125,0]
      Position (ADBE Position): [1770,100,0]
        EXPR: ```
        [1920,0]+[-150,100]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [57.3334,57.3334,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":230.5385,"influence":16.6667}]
          t=0.4338, v=100, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
        Keyframes [2]:
          t=0, v=90, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-207.4846,"influence":16.6667}]
          t=0.4338, v=0, interpIn=bezier, interpOut=bezier, easeIn=[{"speed":0,"influence":100}], easeOut=[{"speed":0,"influence":33.3333}]
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [1,1,1,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - Subtext")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
      [Effect] Transform:
        Anchor Point (ADBE Geometry2-0001): [960,540]
        Position (ADBE Geometry2-0002): [960,540]
        Uniform Scale (ADBE Geometry2-0011): 1
        Scale Height (ADBE Geometry2-0003): 100
        Scale Width (ADBE Geometry2-0004): 100
        Skew (ADBE Geometry2-0005): 0
        Skew Axis (ADBE Geometry2-0006): 0
        Rotation (ADBE Geometry2-0007): 0
        Opacity (ADBE Geometry2-0008): 100
          EXPR: ```
          if(thisComp.layer("Control").effect("Subtext")("ADBE Checkbox Control-0001")==1) 100 else 0
          ```
        Use Composition’s Shutter Angle (ADBE Geometry2-0009): 1
        Shutter Angle (ADBE Geometry2-0010): 0
        Sampling (ADBE Geometry2-0012): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

6. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [960,540]
        Start Color (ADBE Ramp-0002): [0.1451,0.1451,0.1451,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 1")("ADBE Color Control-0001")
          ```
        End of Ramp (ADBE Ramp-0003): [1943.7862,1089.6214]
        End Color (ADBE Ramp-0004): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Ramp Shape (ADBE Ramp-0005): 2
        Ramp Scatter (ADBE Ramp-0006): 80
        Blend With Original (ADBE Ramp-0007): 0
      [Effect] Noise Alpha:
        Noise (ADBE Noise Alpha2-0001): 1
        Amount (ADBE Noise Alpha2-0002): 40
          EXPR: ```
          if(thisComp.layer("Control").effect("Noise BG")("ADBE Checkbox Control-0001")==1) 40 else 0;
          ```
        Original Alpha (ADBE Noise Alpha2-0003): 2
        Overflow (ADBE Noise Alpha2-0004): 2
        Contextual Control (ADBE Noise Alpha2-0005): 0
        Cycle Noise (ADBE Noise Alpha2-0007): 0
        Cycle (in Revolutions) (ADBE Noise Alpha2-0008): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

7. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
        EXPR: ```
        if(thisComp.layer("Control").effect("Alpha BG")("ADBE Checkbox Control-0001")==1) 0 else 100;
        ```
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
          EXPR: ```
          thisComp.layer("Control").effect("Color - BG 2")("ADBE Color Control-0001")
          ```
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

8. "GRADIENT_02" — type=av, enabled=false, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

# Sub-Compositions

---

## Textholder_10
Duration: 20.02s | 1920x190 | 29.97fps | Layers: 2

### Layer Hierarchy

1. " VIDEOHIVE VIDEOHIVE" — type=text, enabled=true, parent="none", in=0, out=20.02, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: " VIDEOHIVE VIDEOHIVE", font=Montserrat-Black, size=151.5, color=[0,0,0], tracking=0, leading=181.8, justify=7415
   Transform:
      Anchor Point (ADBE Anchor Point): [18.7102,-53.025,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        
        ```
      Position (ADBE Position): [960,95,0]
        EXPR: ```
        [(thisComp.width/2), (thisComp.height/2)]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Shape Layer 1" — type=shape, enabled=true, parent="none", in=0, out=20.02, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Textholder_12
Duration: 20.02s | 1920x190 | 29.97fps | Layers: 2

### Layer Hierarchy

1. "travel through space" — type=text, enabled=true, parent="none", in=0, out=20.02, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "travel through space", font=Montserrat-Black, size=133.4, color=[0,0,0], tracking=0, leading=160.08, justify=7414
   Transform:
      Anchor Point (ADBE Anchor Point): [-922.1184,-46.69,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        
        ```
      Position (ADBE Position): [960,95,0]
        EXPR: ```
        [(thisComp.width/2), (thisComp.height/2)]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Shape Layer 1" — type=shape, enabled=true, parent="none", in=0, out=20.02, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Textholder_17
Duration: 22.022s | 1920x190 | 29.97fps | Layers: 2

### Layer Hierarchy

1. "Envato Envato Envato" — type=text, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "Envato Envato Envato", font=Montserrat-Black, size=133.4, color=[0,0,0], tracking=0, leading=160.08, justify=7414
   Transform:
      Anchor Point (ADBE Anchor Point): [-932.7928,-46.69,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        
        ```
      Position (ADBE Position): [960,95,0]
        EXPR: ```
        [(thisComp.width/2), (thisComp.height/2)]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = comp("Scene_17").layer("Control").effect("Size - Titles")("ADBE Slider Control-0001");
        [temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Shape Layer 1" — type=shape, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Pre-comp-title_17
Duration: 22.022s | 1920x1080 | 29.97fps | Layers: 5

### Layer Hierarchy

1. "Title_x4" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,50,95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [270,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -39.1667
          EXPR: ```
          loopOut("cycle")
          ```
          Keyframes [4]:
            t=2.002, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-74.925,"influence":16.6667}]
            t=3.003, v=-75, interpIn=linear, interpOut=linear, easeIn=[{"speed":-74.925,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=5.005, v=-25, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=6.006, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_x3" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,145,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -64.1667
          EXPR: ```
          loopOut("cycle")
          ```
          Keyframes [4]:
            t=3.003, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-74.925,"influence":16.6667}]
            t=4.004, v=-75, interpIn=linear, interpOut=linear, easeIn=[{"speed":-74.925,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=6.006, v=-25, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=7.007, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_x2" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,-45,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -14.1667
          EXPR: ```
          loopOut("cycle")
          ```
          Keyframes [4]:
            t=1.001, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-74.925,"influence":16.6667}]
            t=2.002, v=-75, interpIn=linear, interpOut=linear, easeIn=[{"speed":-74.925,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=4.004, v=-25, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=5.005, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_x1" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,50,-95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Brightness & Contrast:
        Brightness (ADBE Brightness & Contrast 2-0001): -32.5
          EXPR: ```
          loopOut("cycle")
          ```
          Keyframes [4]:
            t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":-74.925,"influence":16.6667}]
            t=1.001, v=-75, interpIn=linear, interpOut=linear, easeIn=[{"speed":-74.925,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=3.003, v=-25, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":24.975,"influence":16.6667}]
            t=4.004, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":24.975,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
        Contrast (ADBE Brightness & Contrast 2-0002): 0
        Use Legacy (supports HDR) (ADBE Brightness & Contrast 2-0003): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Rotation_01" — type=av, enabled=true, parent="none", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [50,50,0]
      Position (ADBE Position): [960,540,95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 1119
        EXPR: ```
        loopOut("continue")
        ```
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":89.91,"influence":16.6667}]
          t=4.004, v=360, interpIn=linear, interpOut=linear, easeIn=[{"speed":89.91,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## GRADIENT_01
Duration: 22.022s | 1920x1080 | 29.97fps | Layers: 1

### Layer Hierarchy

1. "Background" — type=av, enabled=true, parent="none", in=0, out=22.022
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [0,540]
        Start Color (ADBE Ramp-0002): [0,0,0,1]
        End of Ramp (ADBE Ramp-0003): [1920,540]
        End Color (ADBE Ramp-0004): [1,1,1,1]
        Ramp Shape (ADBE Ramp-0005): 1
        Ramp Scatter (ADBE Ramp-0006): 0
        Blend With Original (ADBE Ramp-0007): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Textholder_18_1
Duration: 22.022s | 1920x190 | 29.97fps | Layers: 2

### Layer Hierarchy

1. "Envato Envato Envato" — type=text, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "Envato Envato Envato", font=Montserrat-Black, size=133.4, color=[0,0,0], tracking=0, leading=160.08, justify=7414
   Transform:
      Anchor Point (ADBE Anchor Point): [-932.7928,-46.69,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        
        ```
      Position (ADBE Position): [960,95,0]
        EXPR: ```
        [(thisComp.width/2), (thisComp.height/2)]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = comp("Scene_18").layer("Control").effect("Size - Title_01")("ADBE Slider Control-0001");
        [temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Shape Layer 1" — type=shape, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Textholder_18_2
Duration: 22.022s | 1920x190 | 29.97fps | Layers: 2

### Layer Hierarchy

1. "MARKET MARKET MARKET" — type=text, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Markers: [{"time":0,"comment":"Change text","duration":0}]
   Text: "MARKET MARKET MARKET", font=Montserrat-Black, size=129.3, color=[0,0,0], tracking=0, leading=155.16, justify=7414
   Transform:
      Anchor Point (ADBE Anchor Point): [-926.9439,-45.255,0]
        EXPR: ```
        tempx = thisLayer.sourceRectAtTime(time,false).width/2 + thisLayer.sourceRectAtTime(time,false).left; 
        tempy = thisLayer.sourceRectAtTime(time,false).height/2 + thisLayer.sourceRectAtTime(time,false).top; 
        [tempx,tempy]
        
        ```
      Position (ADBE Position): [960,95,0]
        EXPR: ```
        [(thisComp.width/2), (thisComp.height/2)]
        ```
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
        EXPR: ```
        temp = comp("Scene_18").layer("Control").effect("Size - Title_02")("ADBE Slider Control-0001");
        [temp, temp]
        ```
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Fill:
        Fill Mask (ADBE Fill-0001): 0
        All Masks (ADBE Fill-0007): 0
        Color (ADBE Fill-0002): [0,0,0,1]
        Invert (ADBE Fill-0006): 0
        Horizontal Feather (ADBE Fill-0003): 0
        Vertical Feather (ADBE Fill-0004): 0
        Opacity (ADBE Fill-0005): 1
   Text Properties:
      Path Options:
        Path (ADBE Text Path): 0
        Reverse Path (ADBE Text Reverse Path): 0
        Perpendicular To Path (ADBE Text Perpendicular To Path): 1
        Force Alignment (ADBE Text Force Align Path): 0
        First Margin (ADBE Text First Margin): 0
        Last Margin (ADBE Text Last Margin): 0
      More Options:
        Anchor Point Grouping (ADBE Text Anchor Point Option): 1
        Grouping Alignment (ADBE Text Anchor Point Align): [0,0]
        Fill & Stroke (ADBE Text Render Order): 1
        Inter-Character Blending (ADBE Text Character Blend Mode): 1
        Variable Font Spacing (ADBE Text Variable Font Spacing): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Shape Layer 1" — type=shape, enabled=true, parent="none", in=0, out=22.022, collapse=true
   Transform:
      Anchor Point (ADBE Anchor Point): [0,0,0]
      Position (ADBE Position): [960,95,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Pre-pre-comp-title_18
Duration: 22.022s | 1920x1080 | 29.97fps | Layers: 5

### Layer Hierarchy

1. "Title_x4" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,50,95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [270,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Title_01")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Substrate_01")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "Title_x3" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,145,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [1,1,1,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Title_02")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [0,0,0,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Substrate_02")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

3. "Title_x2" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,-45,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): -90
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [1,1,1,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Title_02")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [0,0,0,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Substrate_02")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

4. "Title_x1" — type=av, enabled=true, parent="Rotation_01", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [960,95,0]
      Position (ADBE Position): [50,50,-95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100.5,100.5,100.5]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Effects:
      [Effect] Motion Tile:
        Tile Center (ADBE Tile-0001): [960,95]
        Tile Width (ADBE Tile-0002): 100
        Tile Height (ADBE Tile-0003): 100
        Output Width (ADBE Tile-0004): 110
        Output Height (ADBE Tile-0005): 100
        Mirror Edges (ADBE Tile-0006): 0
        Phase (ADBE Tile-0007): 0
        Horizontal Phase Shift (ADBE Tile-0008): 0
      [Effect] Tint:
        Map Black To (ADBE Tint-0001): [0,0,0,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Title_01")("ADBE Color Control-0001")
          ```
        Map White To (ADBE Tint-0002): [1,1,1,1]
          EXPR: ```
          comp("Scene_18").layer("Control").effect("Color - Substrate_01")("ADBE Color Control-0001")
          ```
        Amount to Tint (ADBE Tint-0003): 100
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

5. "Rotation_01" — type=av, enabled=true, parent="none", in=0, out=22.022, 3D=true
   Transform:
      Anchor Point (ADBE Anchor Point): [50,50,0]
      Position (ADBE Position): [960,327.2909,95]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,-100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 429
        EXPR: ```
        loopOut("continue")
        ```
        Keyframes [2]:
          t=0, v=0, interpIn=linear, interpOut=linear, easeIn=[{"speed":0,"influence":16.6667}], easeOut=[{"speed":89.91,"influence":16.6667}]
          t=4.004, v=360, interpIn=linear, interpOut=linear, easeIn=[{"speed":89.91,"influence":16.6667}], easeOut=[{"speed":0,"influence":16.6667}]
      Y Rotation (ADBE Rotate Y): 0
      Z Rotation (ADBE Rotate Z): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## Pre-comp-title_18
Duration: 22.022s | 1920x1080 | 29.97fps | Layers: 2

### Layer Hierarchy

1. "Pre-pre-comp-title_18" — type=av, enabled=true, parent="none", in=0, out=22.022
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Time Displacement:
        Time Displacement Layer (ADBE Time Displacement-0001): 2
        Max Displacement Time [sec] (ADBE Time Displacement-0002): 1
        Time Resolution [fps] (ADBE Time Displacement-0003): 350
          EXPR: ```
          if(comp("Scene_18").layer("Control").effect("High quality")("ADBE Checkbox Control-0001")==1) 350 else 100
          ```
        If Layer Sizes Differ (ADBE Time Displacement-0004): 1
      [Effect] CC Sphere:
        Rotation X (CC Sphere-0002): 90
        Rotation Y (CC Sphere-0003): 0
        Rotation Z (CC Sphere-0004): 0
        Rotation Order (CC Sphere-0026): 1
        Radius (CC Sphere-0006): 320
        Offset (CC Sphere-0007): [960,540]
        Render (CC Sphere-0008): 1
        Light Intensity (CC Sphere-0010): 100
        Light Color (CC Sphere-0011): [1,1,1,1]
        Light Height (CC Sphere-0012): 40
        Light Direction (CC Sphere-0013): -85
        Ambient (CC Sphere-0016): 90
        Diffuse (CC Sphere-0017): 100
        Specular (CC Sphere-0018): 10
        Roughness (CC Sphere-0019): 0.05
        Metal (CC Sphere-0020): 100
        Reflective (CC Sphere-0021): 0
        Reflection Map (CC Sphere-0022): 1
        Internal Shadows (CC Sphere-0023): 0
        Transparency Falloff (CC Sphere-0024): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

2. "GRADIENT_01" — type=av, enabled=false, parent="none", in=0, out=22.022
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1

---

## GRADIENT_02
Duration: 20.02s | 1920x1080 | 29.97fps | Layers: 1

### Layer Hierarchy

1. "Background" — type=av, enabled=true, parent="none", in=0, out=20.02
   Transform:
      Anchor Point (ADBE Anchor Point): [960,540,0]
      Position (ADBE Position): [960,540,0]
      X Position (ADBE Position_0): 0
      Y Position (ADBE Position_1): 0
      Z Position (ADBE Position_2): 0
      Scale (ADBE Scale): [100,100,100]
      Orientation (ADBE Orientation): [0,0,0]
      X Rotation (ADBE Rotate X): 0
      Y Rotation (ADBE Rotate Y): 0
      Opacity (ADBE Opacity): 100
      Appears in Reflections (ADBE Envir Appear in Reflect): 1
      Rotation (ADBE Rotate Z): 0
   Effects:
      [Effect] Gradient Ramp:
        Start of Ramp (ADBE Ramp-0001): [596,540]
        Start Color (ADBE Ramp-0002): [0,0,0,1]
        End of Ramp (ADBE Ramp-0003): [1296,540]
        End Color (ADBE Ramp-0004): [1,1,1,1]
        Ramp Shape (ADBE Ramp-0005): 1
        Ramp Scatter (ADBE Ramp-0006): 0
        Blend With Original (ADBE Ramp-0007): 0
   Material Options:
      Casts Shadows: 0
      Light Transmission: 0
      Accepts Shadows: 1
      Accepts Lights: 1
      Shadow Color: [0,0,0,1]
      Appears in Reflections: 1
      Ambient: 100
      Diffuse: 50
      Specular Intensity: 50
      Specular Shininess: 5
      Metal: 100
      Reflection Intensity: 0
      Reflection Sharpness: 100
      Reflection Rolloff: 0
      Transparency: 0
      Transparency Rolloff: 0
      Index of Refraction: 1
