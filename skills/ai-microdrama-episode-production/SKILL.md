---
name: ai-microdrama-episode-production
description: 生成、更新、排查和交付 AI 短剧 / AI 漫剧的结构化 story 与 episode 包。适用于创建新 story、分析新剧本、继续生成下一集、生成 episode.md/continuity.md/overview-storyboard.md/segment 文件、生成或整理首尾帧图片、从 Codex 会话记录找回已生成图片、把 first-frame.png/last-frame.png 放入各 segment 的 frames/、校验最终图片完整性、保持角色资产和视频 API prompt 格式一致。
---

# AI 短剧剧集生产

## 目的

这是仓库通用短剧制作 skill，必须适用于 `stories/<story-id>/` 下的任意剧本，而不是只服务某一个故事。

默认输出语言为中文。文件名和目录名可以使用英文 slug，但剧集说明、故事板、首尾帧提示词、连续性检查、视频 prompt 主体都应使用中文。

## 工作原则

- 先读真实项目结构和 story 规则，再写内容或移动资产。
- 不要把某个 story 的人物、世界观、脸部参考、视觉锁带到另一个 story。
- 不要重复生成已经存在的图片；先查项目目录、临时目录、会话 JSONL、manifest，再决定是否缺图。
- 图片、视频和脚本执行不接入 Skynet 统计流程；不要运行 `skynet gen`、`skynet fast`、`skynet test-code-gen`。
- 任何“已完成”都必须有落地文件和校验结果支撑。

## 必须识别 Story Root

生产内容前，先确认目标 story 根目录。

优先级：

1. 用户明确给出 story 路径或 story id 时，使用用户指定值。
2. 用户只给出集数，且 `stories/` 下只有一个 story 时，使用该 story。
3. `stories/` 下有多个 story 且用户没有指定时，先询问使用哪个 story。

Story 根目录结构：

```text
stories/<story-id>/
  README.md
  AGENTS.md
  docs/story-memory.md
  docs/production-rules.md
  docs/workflow.md
  assets/
  episodes/
  templates/              # 可选
```

## 必读上下文与资源

生成剧集前必须读取：

1. 根目录 `docs/workflow.md`
2. 根目录 `docs/contracts/story-package-contract.md`
3. 根目录 `docs/contracts/video-api-handoff.md`
4. 根目录 `docs/methods/douyin-short-drama-method.md`
5. 根目录 `docs/methods/story-analysis-method.md`
6. 根目录 `docs/checklists/episode-quality-checklist.md`
7. 根目录 `templates/`
8. 根目录 `skills/ai-microdrama-episode-production/references/episode-format.md`
9. Story `AGENTS.md`
10. Story `docs/story-memory.md`
11. Story `docs/production-rules.md`
12. Story `docs/audience-strategy.md`，如果存在
13. Story `docs/season-arc.md`，如果存在
14. Story `docs/workflow.md`，如果存在
15. 如果是连续剧，读取上一集的 `episode.md`、`continuity.md`、`overview-storyboard.md`
16. 相关角色卡：story `assets/characters/*/00-character-card.md`
17. 相关场景卡：story `assets/scenes/*/scene-card.md`
18. 相关道具/特效卡：story `assets/props/*/prop-card.md`
19. 相关风格文件：story `assets/style/`
20. Story `templates/`，如果存在；story-local templates 优先级高于根模板

如果任务涉及首尾帧、图片已经生成但位置不明、图片落位、视频 API handoff 或最终交付校验，必须读取：

- `references/frame-asset-workflow.md`
- `references/production-playbook.md`

不要把一个 story 的人物、人脸锁、世界观或剧情设定带到另一个 story。

## 默认剧集规格

除非用户或 story 规则明确要求改格式，默认按仓库标准生成：

- 一集 60 秒。
- 一集拆成 4 段。
- 每段 15 秒以内。
- 默认 9:16 竖屏短剧 / AI 漫剧。
- 每段必须包含 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`、`director-promt.txt`。
- `prompt.md` 是可读的完整视频提示词；`director-promt.txt` 是给视频 API / 图生视频工具直接使用的纯文本导演提示词。
- `director-promt.txt` 沿用项目既有文件名拼写，必须包含规格、参考图用途、角色锁、逐秒动作因果、运镜、声音和负面约束。
- 每段可独立生成，但首尾帧要能连续剪辑。
- 每段推荐生成 `api-request.md`，用于记录视频 API 参数、提交返回和重试策略；其中 Prompt 默认指向 `director-promt.txt`。
- 每集推荐生成 `qa-checklist.md` 和 `publish-package.md`，用于质检和发布包装。

如果 story 明确要求样片、横屏或长集，可以扩展为更多 segment，例如 10 段、150 秒、16:9 横屏样片。扩展时仍然必须保持每段有 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`、`director-promt.txt`、`api-request.md`、`frames/`、`output/`，并按真实时间段命名。

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
    director-promt.txt
    api-request.md
    frames/
    output/
  segment_02_15-30s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    director-promt.txt
    frames/
    output/
  segment_03_30-45s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    director-promt.txt
    frames/
    output/
  segment_04_45-60s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    director-promt.txt
    frames/
    output/
```

扩展剧集目录示例：

```text
episodes/SF001_slug/
  segment_01_00-15s/
  segment_02_15-30s/
  ...
  segment_10_135-150s/
```

## 生产规则

- 保持每段一个清晰戏剧功能。
- 保持 story 自己的人设、人脸锁、视觉参考、题材气质、负面提示词。
- 优先使用 story 中定义的角色、场景、道具、特效资产编号。
- 对白短、狠、可演，不写冗长解释。
- 一集尽量控制在 2-3 个实用场景内，减少视频生成漂移。
- 按抖音短剧逻辑设计：前 5 秒钩子、每 3-5 秒信息变化、每段一个留存任务、最后 3 秒抛出具体问题。
- 同步生成标题、封面、评论区引导和标签方向。
- 保持首尾帧连续：
  - Segment 02 首帧继承 Segment 01 尾帧。
  - Segment 03 首帧继承 Segment 02 尾帧。
  - Segment 04 首帧继承 Segment 03 尾帧。
  - 扩展到更多 segment 时，按编号持续继承。
  - 如果必须跳切，必须写清楚可见转场。

## 剧集设计模式

1. **承接钩子**：从上一集最后画面、未解决问题或剧本开场切入。
2. **确定本集任务**：本集只解决一个核心戏剧任务。
3. **选择资产**：角色、场景、道具/特效、风格文件、负面约束。
4. **设计短视频留存**：开头 5 秒钩子、四段留存任务、结尾 3 秒钩子、标题封面卖点。
5. **设计四段节奏**：
   - Segment 01：钩子和即时冲突。
   - Segment 02：选择、压力、计划、误会或危机升级。
   - Segment 03：爽点、反转、揭示、能力展示或情绪爆发。
   - Segment 04：后果和下一集钩子。
6. **写入文件**：
   - `episode.md`
   - `continuity.md`
   - `overview-storyboard.md`
   - `image-manifest.md`，推荐生成
   - `qa-checklist.md`，推荐生成
   - `publish-package.md`，推荐生成
   - 四段 `storyboard.md`
   - 四段 `first-frame.md`
   - 四段 `last-frame.md`
   - 四段 `prompt.md`
   - 四段 `director-promt.txt`
   - 四段 `api-request.md`，推荐生成
7. **首尾帧生产与落位**：
   - 先写清每段 `first-frame.md` 和 `last-frame.md`，再生成或整理图片。
   - 每张图必须引用 story 的角色锁、场景锁、道具锁、风格锁和负面提示词。
   - 已生成图片优先找回和归档，不要重复生成。
   - 标准落位为 `segment_XX_*/frames/first-frame.png` 和 `segment_XX_*/frames/last-frame.png`。
   - 若有修正版，使用最新明确修正版覆盖旧版，并在 manifest 或工作记录里保留来源。
8. **最终自检**：
   - 是否引用 story 资料。
   - 是否明确角色和资产锁定。
   - 每段是否都有故事板、首帧、尾帧、视频 prompt。
   - `prompt.md` 是否包含画幅、时长、风格、角色锁、动作、运镜、对白、音效、负面提示词。
   - `director-promt.txt` 是否能直接作为 `scripts/ark_video.py --prompt-file` 输入，且比 `prompt.md` 更少 Markdown 结构和解释性文字。
   - 是否生成视频 API 任务记录位置。
   - 是否生成发布包装。
   - 结尾钩子是否自然推动下一集。
   - 是否运行首尾帧校验脚本并查看最终拼图或缩略图预览。

## 新剧本分析模式

当用户提供新剧本或故事概念，而不是已有 story 目录时：

1. 生成一个合适的 story id。
2. 创建 `stories/<story-id>/`。
3. 把故事圣经整理到 `stories/<story-id>/docs/story-memory.md`。
4. 把本剧本专属规则整理到 `stories/<story-id>/docs/production-rules.md`。
5. 把受众策略整理到 `stories/<story-id>/docs/audience-strategy.md`。
6. 把长线规划整理到 `stories/<story-id>/docs/season-arc.md`。
7. 创建 `stories/<story-id>/README.md` 和 `AGENTS.md`。
8. 草拟角色、场景、道具/特效、风格资产卡。
9. 后续 episodes 默认按一集四段、每段 15 秒、每段首尾帧 + 故事板 + prompt 的格式生成。

通用流程写在根目录；具体剧本创意决策写在 story 目录。

## 输出质量底线

缺少以下任意内容时，不要声称剧集可交付：

- 4 段故事板。
- 4 段首帧。
- 4 段尾帧。
- 4 段视频 prompt。
- 4 段 API 直投导演提示词 `director-promt.txt`。
- 每段首尾帧连续性说明。
- story 资产引用。
- 负面提示词。
- 至少 3 个发布标题候选。
- 视频 API 任务记录位置。
- 首尾帧图片落在对应 `frames/` 目录。
- 最终图片校验结果，包括数量、尺寸、hash 和视觉预览。

## 题材通用原则

- 竖屏短剧每段只承载一个清晰情绪点或信息点。
- AI 漫剧生产应保持资产优先：角色 -> 场景 -> 故事板 -> 首尾帧 -> 视频。
- 题材规则属于 story 包，不要在根 skill 中写死末日、恋爱、玄幻、喜剧等特定类型。

## 可用脚本

- `scripts/extract_session_images.py`：从 Codex JSONL 会话记录中解包 `image_generation_end` 的 base64 图片，按 revised prompt 推断 segment 和 first/last 类型。
- `scripts/verify_episode_frames.py`：检查 episode 下每个 segment 是否有 `frames/first-frame.png` 和 `frames/last-frame.png`，输出尺寸、hash、缺失项，并可生成 contact sheet。

输出格式见 `references/episode-format.md`。首尾帧资产流程见 `references/frame-asset-workflow.md`。制作方法论见 `references/production-playbook.md`。
