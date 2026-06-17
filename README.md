# AI 短剧 / AI 漫剧生产框架

本仓库是一套通用 AI 短剧生产工作台，用来把不同剧本整理成可持续生产的“故事记忆 + 资产库 + 剧集分镜 + 首尾帧 + 视频 API 提示词”结构。

根目录只放通用能力；每个具体剧本都放进独立的 `stories/<story-id>/` 文件夹。这样当前剧本、后续新剧本、不同题材项目都可以共用同一套生产流程，但各自保留自己的角色设定、视觉锁定、对白、世界观和禁忌规则。

## 根目录放什么

- `docs/`：通用生产流程和架构说明。
- `templates/`：通用中文模板，默认按 `twin-dawn` 的剧集格式输出。
- `skills/`：通用 Codex skill，用于分析剧本、创建故事包、生成剧集生产文件。
- `stories/`：每个剧本一个独立 story 文件夹。

根目录不要写死某个剧本的人名、剧情、人脸锁、世界观或具体剧集产物。

## Story 文件夹约定

每个剧本放在 `stories/<story-id>/`：

```text
stories/<story-id>/
  README.md
  AGENTS.md
  docs/
    story-memory.md          # 故事圣经、人物、世界观、剧情阶段、对白记忆
    workflow.md              # 本剧本自己的生产流程补充
    production-rules.md      # 本剧本自己的视觉锁、禁忌、风格规则
    season-arc.md            # 长线剧情阶段和前 10 集规划
    audience-strategy.md     # 抖音短剧受众、钩子、标题封面策略
  assets/
    characters/
    scenes/
    props/
    enemies/
    style/
  episodes/
    EP001_slug/
  templates/                 # 可选：本剧本专属模板覆盖
```

## 默认剧集格式

后续所有新 story 的 episodes 默认按照当前 `twin-dawn` 格式生成：

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

固定要求：

- 一集 60 秒。
- 一集拆成 4 段。
- 每段 15 秒以内。
- 每段必须有 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`。
- `prompt.md` 要能直接服务后续视频 API / 图生视频工具。
- `first-frame.md` 和 `last-frame.md` 要明确首尾帧画面，方便连续生成。
- `segment_02` 首帧继承 `segment_01` 尾帧，依次类推。
- 推荐每集生成 `qa-checklist.md` 和 `publish-package.md`。
- 推荐每段生成 `api-request.md`，记录视频 API 参数、提交结果和重试策略。

## 通用能力地图

- [通用生产工作流](docs/workflow.md)
- [Story 包契约](docs/contracts/story-package-contract.md)
- [视频 API 交付规范](docs/contracts/video-api-handoff.md)
- [新剧本分析方法](docs/methods/story-analysis-method.md)
- [抖音短剧方法论](docs/methods/douyin-short-drama-method.md)
- [剧集质量检查清单](docs/checklists/episode-quality-checklist.md)

## 当前故事包

- [stories/twin-dawn](stories/twin-dawn/README.md)：《末日重生：双生曙光 / 末日降临：我和闺蜜觉醒双SSS异能》。

## 新增剧本流程

1. 创建 `stories/<story-id>/`。
2. 写入 `README.md`、`AGENTS.md`、`docs/story-memory.md`、`docs/production-rules.md`。
3. 补齐 `docs/season-arc.md` 和 `docs/audience-strategy.md`。
4. 把角色、场景、道具、风格资产放入 `assets/`。
5. 如果剧本需要特殊字段，再添加 `stories/<story-id>/templates/`；否则使用根目录中文通用模板。
6. 使用 `skills/ai-microdrama-episode-production/` 生成剧集。

示例：

```text
使用 stories/twin-dawn，承接 EP004，生成 EP005。
```
