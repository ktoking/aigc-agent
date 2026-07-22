# Episode Production Contract

## Episode Layout

Create six episode-level files and four fixed segment directories. Each segment must contain `storyboard.md`, `first-frame.md`, `last-frame.md`, `prompt.md`, `director-promt.txt`, `api-request.md`, `frames/`, and `output/`.

Episode-level files:

- `episode.md`
- `overview-storyboard.md`
- `continuity.md`
- `image-manifest.md`
- `qa-checklist.md`
- `publish-package.md`

Fixed segment directories:

- `segment_01_00-15s`
- `segment_02_15-30s`
- `segment_03_30-45s`
- `segment_04_45-60s`

## Four-Segment Story Shape

| Segment | Job | Required result |
| --- | --- | --- |
| 01 | Hook and immediate problem | State the concrete shortage, threat, message, failure, or opportunity in the first five seconds |
| 02 | Limit and preparation | Show quantities, cost, route, energy, payload, tools, or rules |
| 03 | Main payoff or field test | Deliver the episode's strongest new image or useful capability |
| 04 | Result and consequence | Complete the resource/building task and reveal the next practical risk |

Do not make all four segments setup. Do not introduce an unrelated mystery only to manufacture a cliffhanger.

## Director Prompt Shot Format

Use exactly four shots unless the user explicitly changes the format. Title them `镜头一｜...` through `镜头四｜...` without per-shot timestamps. Every shot must include `景别`, `构图`, `运镜手法`, and `画面内容` in that order, followed by dialogue when needed.

Keep one continuous action chain per segment. Each shot must inherit the previous shot's object locations and completion state.

Every director prompt must also include numbered `参考图N：` descriptions, a `声音：` line, and a segment-specific `禁止：` line. Follow [director-prompt-and-assets.md](director-prompt-and-assets.md).

When a recurring character appears, wardrobe is part of continuity. Require the corresponding canonical outfit ID and the full visible garment description in the director prompt; digital-human face assets do not satisfy this requirement.

## Dialogue

- Require at least 4 useful lines and normally 45-80 spoken Chinese characters per segment; the validator rejects fewer than 4 lines, fewer than 45 characters, or more than 90 characters. Action-heavy shots should use one short line at most.
- Keep each spoken line natural and mostly within 10-22 Chinese characters.
- Treat a `角色名：` label as writing metadata, not as an API speaker-binding field. The video request has no structured `character_id -> line -> voice` mapping.
- Every in-video line must be preceded by a `说话者绑定：` sentence that names the speaker, their exact screen position, expression, and mouth state. Example: `说话者绑定：本镜头仅沈知夏开口。她坐在画面右侧后座，未戴口罩，正面中近景，先看见许砚手臂再说话；许砚只露侧背，不开口。`
- For any spoken line, show exactly one uncovered, readable mouth in frame. All non-speakers must be out of frame, back-facing, face-occluded, or remain silent with closed lips. Never ask a masked character to speak.
- Put dialogue only in a stable medium or close shot. Running, combat, loading, driving, closing a door, or injury-impact shots are silent action shots; move the line into the following reaction shot instead.
- Pass digital-human assets only for characters physically visible in the segment. Do not submit an absent character's asset solely because that character has an off-screen line.
- If a precise actor-to-voice match is mandatory, generate the action clip without dialogue and add a separately produced character voice in post. Seedance prompt labels alone cannot make this deterministic.
- Use dialogue to explain what, why, how much, and what happens next.
- Remove lines that merely repeat visible actions.
- Avoid clipped telegraph speech and abstract slogans.
- Before writing the four segments, give the episode a pressure chain: `goal -> obstacle -> choice -> consequence`. Each segment must move that chain; a segment that only explains tools, plans, or backstory must be merged into an action segment.
- Give every line one purpose only: verified fact, concrete cost, decision, changed plan, or professional judgment. Delete dialogue that merely lists equipment or describes the camera image.
- For rescue, battle, escape, and repair scenes, the middle must fail or worsen once after the plan starts. The resulting cost must have a visible cause and matter in the next segment.

## Resource Progression

Build episodes through dependencies:

```text
acquire resource -> install or settle it -> pay operating cost -> produce output -> expose a new weakness
```

Examples:

- chickens and ducks -> water/feed/cleaning -> eggs/manure -> smell/noise/disease
- drone -> battery/payload/route -> remote trade/survey -> noise and route exposure
- greenhouse -> water/heat/pollination -> vegetables -> pests and seasonal power load
- generator -> diesel/maintenance/noise -> stable electricity -> fuel shortage and attraction risk

Give a visible harvest or operational payoff every three to five episodes so building does not become endless preparation.
