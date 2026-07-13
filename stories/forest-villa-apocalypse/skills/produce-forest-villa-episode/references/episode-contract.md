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

## Dialogue

- Require 6-8 useful lines and normally 70-110 spoken Chinese characters per segment; the validator rejects fewer than 6 lines, fewer than 70 characters, or more than 120 characters.
- Keep each spoken line natural and mostly within 10-22 Chinese characters.
- Use one main visible speaker per shot when possible.
- Use dialogue to explain what, why, how much, and what happens next.
- Remove lines that merely repeat visible actions.
- Avoid clipped telegraph speech and abstract slogans.

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
