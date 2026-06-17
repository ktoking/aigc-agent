# 通用 AI 短剧生产工作流

## 目标

本框架把任意剧本整理成可重复生产的 AI 短剧资产：

```text
故事圣经 -> 资产库 -> 单集设计 -> 连续性表 -> 分段故事板 -> 首尾帧 -> 视频 API 提示词 -> 剪辑交付
```

框架本身保持通用；具体人物、人脸锁、剧情事实、世界观、风格禁忌都放在 `stories/<story-id>/`。

## Story 输入

每个 story 至少应提供：

- `docs/story-memory.md`：故事圣经、人物、世界观、时间线、剧情阶段、关键对白、长期记忆。
- `docs/production-rules.md`：本剧本的视觉锁定、风格规则、禁忌、参考图、模型提示词习惯。
- `docs/season-arc.md`：长线剧情阶段、前 10 集规划、阶段爽点和阶段钩子。
- `docs/audience-strategy.md`：目标观众、情绪卖点、开头钩子、标题封面策略。
- `assets/characters/`：角色卡、定妆图、表情、服装、动作姿势。
- `assets/scenes/`：场景卡和场景参考。
- `assets/props/`：道具、特效、符号、武器、车辆等复用资产。
- `assets/style/`：本剧本的风格、镜头语言、光线、负面提示词。
- `episodes/`：生成后的剧集目录。
- `templates/`：可选，只有剧本需要覆盖通用模板时使用。

## 默认单集规格

所有新 story 默认沿用 `twin-dawn` 的剧集生产规格：

- 一集 60 秒。
- 一集拆成 4 段。
- 每段 15 秒以内。
- 竖屏短剧 / AI 漫剧优先，默认 9:16。
- 每段先写首尾帧，再写视频 prompt，方便后续视频 API 或图生视频工具调用。

默认目录：

```text
episodes/EPXXX_slug/
  episode.md
  continuity.md
  overview-storyboard.md
  image-manifest.md
  qa-checklist.md
  publish-package.md
  segment_01_00-15s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    api-request.md
    frames/
    output/
  segment_02_15-30s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    frames/
    output/
  segment_03_30-45s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    frames/
    output/
  segment_04_45-60s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    frames/
    output/
```

## 每集必须包含

- `episode.md`：本集目标、冲突、爽点/揭示、情绪点、结尾钩子、分段概览、关键对白。
- `overview-storyboard.md`：60 秒总览故事板，汇总 4 个视频段落的背景叙事、分镜描述、首帧、尾帧、桥接关系。
- `continuity.md`：承接上一集、固定状态、人物/场景/道具连续性、分段桥接、禁止偏差。
- 4 个 `storyboard.md`：每段镜头表，说明画面、运镜、台词、音效、首尾帧要求。
- 4 个 `first-frame.md`：每段首帧图提示词。
- 4 个 `last-frame.md`：每段尾帧图提示词。
- 4 个 `prompt.md`：可交给视频 API / 图生视频工具的完整视频提示词。
- 4 个 `api-request.md`：推荐生成，记录视频 API 参数、提交记录、返回记录和重试策略。
- `image-manifest.md`：可选但推荐，用于跟踪首尾帧、故事板图、封面、视频任务等生成产物。
- `qa-checklist.md`：推荐生成，用于检查剧情、留存、连续性、视频 API 和发布项。
- `publish-package.md`：推荐生成，用于标题、封面、简介、评论引导和标签。

## 默认四段节奏

- Segment 01：承接上一集或剧本开场，5 秒内制造视觉钩子或情绪钩子。
- Segment 02：推进选择、压力、误会、危机、计划或信息揭示。
- Segment 03：释放爽点、反转、能力展示、情绪爆发或关键发现。
- Segment 04：展示后果，并留下下一集钩子。

每段只承担一个清晰戏剧功能，方便视频 API 按 15 秒短段生成。

## 首尾帧连续性

- `segment_02` 首帧继承 `segment_01` 尾帧。
- `segment_03` 首帧继承 `segment_02` 尾帧。
- `segment_04` 首帧继承 `segment_03` 尾帧。
- 如果时间、空间、服装、伤口、光线、道具、站位发生变化，必须在上一段尾帧、下一段首帧或转场说明中解释。
- 所有角色、场景、道具、特效优先使用 story 自己的资产编号。

## 生产顺序

1. 读取 story 包和上一集上下文。
2. 读取受众策略和长线规划，明确本集在连续剧情中的任务。
3. 按抖音短剧方法论设计前 5 秒钩子、四段留存任务和结尾钩子。
4. 选择本集角色、场景、道具、特效、风格文件。
5. 编写 `episode.md`。
6. 编写 `overview-storyboard.md`，先确认 60 秒整体节奏。
7. 编写 `continuity.md`。
8. 编写 4 段 `storyboard.md`。
9. 编写 4 段 `first-frame.md` 和 `last-frame.md`。
10. 编写 4 段 `prompt.md`，服务视频 API / 图生视频工具。
11. 编写 4 段 `api-request.md`，预留 API 参数和提交记录。
12. 编写 `qa-checklist.md` 和 `publish-package.md`。
13. 做连续性和提示词质量检查。
14. 外部生成图片和视频后，把产物放入对应 segment 的 `frames/` 和 `output/`。

## 质量检查

- 开头 5 秒是否有钩子。
- 本集是否有明确冲突、情绪推进、爽点/揭示和结尾钩子。
- 四段是否各自能独立交给视频 API 生成。
- 每段是否都有故事板、首帧、尾帧、视频 prompt。
- 首尾帧是否能自然桥接。
- 角色、服装、发型、伤口、道具、光线、场景是否遵循 story 规则。
- 负面提示词是否针对本剧本和视频模型的真实风险。
