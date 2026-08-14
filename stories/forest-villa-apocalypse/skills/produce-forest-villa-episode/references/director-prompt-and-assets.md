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
16:9横屏，15秒，720p，真人末日生存短剧质感。许砚使用固定数字人并穿 FVA_XU_YAN_OUTFIT_001：炭灰防水工装夹克、黑色肩部拼片、深灰内搭、黑灰工装裤、深棕高帮登山靴。白棠使用固定数字人并穿 FVA_BAI_TANG_OUTFIT_001：鼠尾草绿短款工装外套、浅灰内搭、深灰工装裤、黑色工作靴，发型严格沿用数字人资产。数字人只锁脸和身份，禁止沿用资产原始服装。

参考图1：[无人背景或资产名称]，只锁定[空间结构、色调、固定物位置]；图中没有人物，不锁人物动作。
参考图2：[无人道具或设备名称]，只锁定[外观、数量、连接方式]；图中没有人物，不改变参考图1的场地。

Segment 0N：[一句话说明本段发生什么]

同一[明确地点]，画面按“动作A、动作B、动作C、动作D”连续推进。[数量、时间、天气、物体状态]全段保持一致。
```

Use two or three reference images. Do not say only “参考某图”; explain each image's responsibility. Do not use a storyboard grid as a reference image.

## Wardrobe Lock

- Never treat a digital-human asset as a wardrobe reference. It locks identity, face, age, and body only.
- Repeat the full canonical base outfit in every segment. Writing only `同一套工装`, `延续上一段服装`, or an outfit ID without visible garment details is insufficient.
- Carry dirt, wetness, rolled sleeves, apron, gloves, mask, and tool-belt state across adjacent shots and segments.
- Task accessories layer over the canonical base outfit. They never replace its jacket, inner shirt, pants, or footwear unless the story explicitly records damage or a seasonal change.
- Add `数字人原始服装`, `人物随机换装`, and the likely accessory continuity error to the negative prompt.

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

All four fields are mandatory. A shot may omit dialogue when speech would damage rhythm; the segment as a whole requires at least 4 complete lines and normally 45-80 spoken Chinese characters, with no more than one short line per action-heavy shot.

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

## Performance And Dialogue Direction

Digital-human assets lock identity but do not direct a performance. For every close or medium-close face shot, write one short path:

```text
起点情绪：听到未知声音后的警觉。
微动作：手停在工具上，视线先移向电台再看同伴，短暂停顿后下颌收紧。
终点情绪：从犹豫变成决定。
```

Use one physical cue, not a pile of acting adjectives. Good cues include a held breath, delayed blink, eyes checking a route, a hand stopping mid-task, a jaw tightening, shoulders lowering after danger passes, or a glance that avoids an injury. Do not write only `紧张`、`愤怒`、`害怕`、`高冷`.

Use a face-only reaction shot when a character's changed expression is the story beat. Do not force dialogue into that shot. For example: `听到铁门外的刮擦声，白棠的视线停在监控屏上，手指离开开门键，脸上从疑惑变成警觉。`

For spoken lines, require all of the following:

- one visible speaker and one short sentence;
- the mouth is visible and the body is stationary or moving slowly;
- no line while the speaker drives, runs, fights, lifts, wears a mask, or turns away;
- radio/intercom dialogue is written as `画外音` or `通过设备`, while the image stays on an object, route, or listener reaction;
- cut to a reaction, an over-the-shoulder view, or a physical consequence when a line ends; do not keep one talking head speaking twice.

## Camera Motivation

The camera move must contribute one clear narrative function:

| Situation | Recommended move | Required finish state |
| --- | --- | --- |
| Decision or realization | Extremely slow push-in | Hold on the committed expression or the chosen object |
| Two-person tension | Long-lens over-the-shoulder | Both eye-lines and their physical distance remain readable |
| Unseen danger | Locked-off wide plus off-screen sound | Keep the threat outside the frame; show a reaction or object shift |
| Escape or rescue | Side follow-tracking | End with the character reaching the car, door, or cover |
| Information reveal | Rack focus or slow lateral reveal | The new object or figure becomes the final focus |

Use only one main move per shot. Preserve screen direction between cuts: a character exiting frame right must enter the next setup from frame left unless the edit explicitly re-establishes the geography.

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

Declare every digital human above `参考图1` in a separate identity-lock header. Each entry must contain the character name and full `asset-...` ID and must say that identities cannot be exchanged. Digital-human assets do not consume reference-image numbers.

Number only non-human references:

1. Every local `--image` in CLI order, including the preceding segment tail frame when it is actually submitted.
2. Every hosted `--image-url` in CLI order.

Within the non-human references, order by narrative importance:

1. Current location and construction state
2. Main equipment, prop, vehicle, animal, or route
3. Special state needed later in the segment

Use the same location anchor across adjacent segments when the action remains there. Do not mix modern and rustic versions, day and night states without instructions, or two incompatible wall/villa layouts.

For multi-person submission, use `--digital-human "角色名=asset://..."` and one `--image-label`/`--image-url-label` per non-human input. A missing or stale `参考图N` is a blocking error, not a warning. When two male digital humans occupy different spaces in one segment, explicitly isolate their permitted shots and locations; split the generation if identity accuracy is more important than a single 15-second render.

For a four-segment request, formal tasks are sequential: submit Segment01, wait for completion, inspect representative frames and audio, and record `output/video-qa.json` through `scripts/ark_video.py qa`. Submit Segment02 only after Segment01 is `passed`, and repeat through Segment04. Any `rejected` result stops the sequence; keep the failed output for diagnosis and do not regenerate or submit later segments without a new user instruction.

## Footer Template

```text
声音：[necessary ambience and action sounds]；人物说话时背景声压低，对白清楚。禁止字幕、水印、logo。
禁止：[format drift]、[character drift]、[continuity errors]、[object/count errors]、[unsafe or unwanted action]。
```

Negative constraints must be specific to the segment. Include likely failures such as objects moving by themselves, character face changes, count changes, prop teleportation, sudden location changes, game HUD, gore, or actions that exceed the available time.
