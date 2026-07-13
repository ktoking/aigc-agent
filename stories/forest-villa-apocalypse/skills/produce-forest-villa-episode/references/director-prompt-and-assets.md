# Director Prompt And Asset Contract

Use this contract for every `director-promt.txt`. It replaces loose cinematic prose with a fixed, model-readable production prompt.

## Prompt Order

Write sections in this exact order:

1. Output format and character locks
2. Numbered reference-image responsibilities
3. Segment title
4. One-sentence continuous action chain
5. Four shots
6. Sound direction
7. Negative constraints

## Header Template

```text
16:9横屏，15秒，720p，真人末日生存短剧质感。使用许砚数字人 asset://asset-20260320075237-29hdx 和白棠数字人 asset://asset-20260320075131-k78qt，锁定脸、年龄、体型和本段服装。

参考图1：[无人背景或资产名称]，只锁定[空间结构、色调、固定物位置]；图中没有人物，不锁人物动作。
参考图2：[无人道具或设备名称]，只锁定[外观、数量、连接方式]；图中没有人物，不改变参考图1的场地。

Segment 0N：[一句话说明本段发生什么]

同一[明确地点]，画面按“动作A、动作B、动作C、动作D”连续推进。[数量、时间、天气、物体状态]全段保持一致。
```

Use two or three reference images. Do not say only “参考某图”; explain each image's responsibility. Do not use a storyboard grid as a reference image.

## Shot Template

```text
镜头一｜具体动作标题
景别：[大全景/全景/中景/中近景/近景/特写/第一视角等]。
构图：[主体位置、前中后景关系、关键物体位置]。
运镜手法：[固定、轻推、横移、跟随、抬升等一个清楚动作]。
画面内容：[谁做什么，物体如何变化，镜头结束时留下什么状态；写明禁止出现的歧义]。
白棠：
“正常、具体、能说完的话。”
许砚：
“直接解释原因或下一步。”
```

All four fields are mandatory. A shot may omit dialogue only when speech would damage rhythm; the segment as a whole requires 6-8 complete lines and normally 70-110 spoken Chinese characters.

## Shot Design Rules

- `景别` decides how much the viewer sees. Use a wide shot for geography, medium shots for actions, and close-ups for one decisive detail.
- `构图` records stable screen geography. Name left/right/center and foreground/background when continuity matters.
- `运镜手法` describes one executable camera move. Avoid combining pan, orbit, zoom, whip, handheld, and drone movement in one shot.
- `画面内容` describes visible causality, not mood. Write the starting state, action, result, exact quantity, and continuity prohibition when needed.
- Each shot performs one main action. Do not ask one 3-4 second shot to establish a location, introduce equipment, perform an exchange, explain rules, and reveal zombies.
- Prefer continuous physical transitions. A box does not move by itself; show a person pushing it, a drone lifting it, or cut after the action is complete.
- Do not switch to an unexplained monitor, intercom, phone, or first-person view. Establish the device before showing its feed.
- Do not assign dialogue to a speaker who is absent unless marked `画外音` or transmitted through a clearly established radio/intercom.
- Never add individual shot seconds. The segment runtime is fixed at 15 seconds.

## Dialogue Test

Read the whole segment aloud once. Rewrite when any line:

- sounds like a slogan, riddle, trailer copy, or clipped telegram;
- repeats exactly what the viewer already sees;
- answers a question nobody asked or predicts an outsider's need before contact;
- uses an unclear pronoun such as “它”“这个”“那边” without a visible referent;
- contains production language a character would not naturally say;
- cannot be spoken clearly within the segment alongside the required action.

Good dialogue names the object and reason: `井水接上以后，生活用水就不用再省了。`

Bad dialogue hides the meaning: `先有棚，才养得住。`

## Asset Generation Template

Generate each missing background or object as a separate photoreal image:

```text
Photorealistic natural live-action film still, 16:9 AI video reference image, [one exact location or asset].
Purpose: lock [one main responsibility].
Architecture/style: modern three-story forest villa, cool white, pale gray and charcoal palette when the villa is present; match the canonical villa three-view.
Objects and counts: [exact list and exact counts].
Composition: clean readable large shapes, practical camera height, unobstructed subject, enough negative space for later digital-human insertion.
Continuity: [current construction, season, weather, time of day, wear state].
Absolutely no people, no hands, no body parts, no faces, no silhouettes, no clothing.
No text, subtitles, logos, watermark, anime, illustration, game CG, rustic styling, retro interior, excessive sharpening, fish-scale grids, or cluttered micro-detail.
```

For exact counts, state the count in both the object list and negative constraints. Inspect the image at full size. Correct count, architecture drift, human presence, unreadable objects, or wrong aspect ratio before referencing it.

## Reference Selection And Ordering

Order references by narrative importance:

1. Current location and construction state
2. Main equipment, prop, vehicle, animal, or route
3. Special state needed later in the segment

Use the same location anchor across adjacent segments when the action remains there. Do not mix modern and rustic versions, day and night states without instructions, or two incompatible wall/villa layouts.

## Footer Template

```text
声音：[necessary ambience and action sounds]；人物说话时背景声压低，对白清楚。禁止字幕、水印、logo。
禁止：[format drift]、[character drift]、[continuity errors]、[object/count errors]、[unsafe or unwanted action]。
```

Negative constraints must be specific to the segment. Include likely failures such as objects moving by themselves, character face changes, count changes, prop teleportation, sudden location changes, game HUD, gore, or actions that exceed the available time.
