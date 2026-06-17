# Story 包契约

## 目的

Story 包是一个剧本项目的最小生产单元。每个 story 必须能独立回答三个问题：

- 这是什么故事，观众为什么继续看。
- 角色、场景、道具、风格如何保持一致。
- 每一集如何拆成可交给视频 API 的短段。

根目录只提供通用能力；具体剧本的创作规则都写入 story 包。

## 必需目录

```text
stories/<story-id>/
  README.md
  AGENTS.md
  docs/
    story-memory.md
    production-rules.md
    workflow.md
    season-arc.md
    audience-strategy.md
  assets/
    characters/
    scenes/
    props/
    style/
  episodes/
```

## 必需文件职责

| 文件 | 职责 | 必须包含 |
| --- | --- | --- |
| `README.md` | 给人看的 story 入口 | 标题、题材、目标受众、单集规格、关键文件 |
| `AGENTS.md` | 给 Codex 的 story 规则 | 必读顺序、角色锁、剧集格式、禁忌 |
| `docs/story-memory.md` | 故事圣经 | 世界观、人物、关系、时间线、长期伏笔、关键对白 |
| `docs/production-rules.md` | 生产约束 | 人脸锁、风格锁、镜头禁忌、负面提示词、视频模型风险 |
| `docs/workflow.md` | 本 story 流程 | 生成顺序、资产引用、每集目录、质检规则 |
| `docs/season-arc.md` | 季度/长线规划 | 阶段目标、每阶段爽点、反派升级、关键钩子 |
| `docs/audience-strategy.md` | 短视频策略 | 目标观众、情绪卖点、开头钩子、标题封面方向 |

## 资产命名

角色、场景、道具必须使用稳定 ID，避免后续 prompt 漂移。

- 角色：`CHARACTER_NAME_001`，例如 `LIN_WAN_001`
- 场景：`SCENE_LOCATION_NAME`
- 道具：`PROP_OBJECT_NAME`
- 特效：`VFX_EFFECT_NAME`

资产卡必须写清：

- 可见特征
- 变化范围
- 禁止变化
- prompt 关键词
- 负面提示词
- 参考图路径，如果存在

## 默认剧集规格

除非用户明确要求，所有 story 使用统一短剧规格：

- 一集 60 秒。
- 一集 4 段。
- 每段 15 秒以内。
- 9:16 竖屏。
- 每段包含 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`。
- 每段可独立交给视频 API 生成。
- 首尾帧必须能连续剪辑。

## Episode 目录契约

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
  segment_03_30-45s/
  segment_04_45-60s/
```

其中 `api-request.md`、`qa-checklist.md`、`publish-package.md` 是推荐增强文件。已有旧剧集可以不补齐，但新剧集应优先生成。

## 生成前检查

- Story 包是否存在 `AGENTS.md`。
- Story 包是否存在故事记忆和生产规则。
- 是否能定位上一集。
- 是否能定位本集需要的角色、场景、道具、风格文件。
- 是否有明确观众情绪卖点和结尾钩子。
- 是否能把一集拆成四个 15 秒以内的视频任务。

## 禁止事项

- 不要把 story A 的角色设定写进 story B。
- 不要在根模板中写死具体故事名或人名。
- 不要只写剧情不写首尾帧。
- 不要只写 prompt 不写连续性。
- 不要生成无法给视频 API 拆段执行的长段落。
