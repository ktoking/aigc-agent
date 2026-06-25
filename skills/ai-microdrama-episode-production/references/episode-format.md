# 剧集格式参考

## 必须创建的文件

默认每集创建这些叙事文件。除非 story 规则明确要求扩展，否则使用 4 段；如果扩展为样片或长集，按同一文件结构复制到所有 segment。

- `episode.md`
- `continuity.md`
- `overview-storyboard.md`
- `image-manifest.md`，推荐用于跟踪图片和视频 API 任务
- `qa-checklist.md`，推荐用于交付质检
- `publish-package.md`，推荐用于标题、封面、评论和标签
- `segment_01_00-15s/storyboard.md`
- `segment_01_00-15s/first-frame.md`
- `segment_01_00-15s/last-frame.md`
- `segment_01_00-15s/prompt.md`
- `segment_01_00-15s/api-request.md`，推荐用于视频 API 任务记录
- `segment_02_15-30s/storyboard.md`
- `segment_02_15-30s/first-frame.md`
- `segment_02_15-30s/last-frame.md`
- `segment_02_15-30s/prompt.md`
- `segment_02_15-30s/api-request.md`
- `segment_03_30-45s/storyboard.md`
- `segment_03_30-45s/first-frame.md`
- `segment_03_30-45s/last-frame.md`
- `segment_03_30-45s/prompt.md`
- `segment_03_30-45s/api-request.md`
- `segment_04_45-60s/storyboard.md`
- `segment_04_45-60s/first-frame.md`
- `segment_04_45-60s/last-frame.md`
- `segment_04_45-60s/prompt.md`
- `segment_04_45-60s/api-request.md`

每个 segment 目录还应包含：

- `frames/`：首帧、尾帧、故事板图等图片产物。
- `output/`：视频 API 任务提交、返回结果、生成视频等产物。

最终首尾帧标准命名：

- `frames/first-frame.png`
- `frames/last-frame.png`

不要把未确认归属的候选图直接放成最终名。候选图可暂存到 `frames/archive/`、`output/` 或临时目录。

## `episode.md`

使用这些章节：

- 标题：`# EPXXX 标题`
- `## 基本信息`
- `## 必读故事资料`
- `## 出场角色`
- `## 剧情梗概`
- `## 情绪曲线`
- `## 分段概览`
- `## 关键对白`
- `## 发布标题候选`
- `## 备注`

## `continuity.md`

使用这些章节：

- 标题：`# EPXXX 连续性表`
- `## 上一集承接`
- `## 本集固定状态`
- `## 人物连续性`
- `## 场景与道具连续性`
- `## 分段桥接`
- `## 禁止偏差`

如果 story 有固定参考图、人脸锁或风格锁，必须写入连续性表。

## `overview-storyboard.md`

使用这些章节：

- 标题：`# EPXXX 60秒概述故事板`
- `## 本集一句话`
- `## 总体节奏`
- `## 总览表`
- `## 本集关键画面`
- `## 本集关键对白`
- `## 本集生成总提示词`
- `## 检查清单`

## Segment `storyboard.md`

使用这些章节：

- 标题：`# Segment XX 故事板`
- `## 分段信息`
- 镜头表字段：`镜头 | 时间 | 画面内容 | 运镜方式 | 台词 | 音效`
- `## 首帧要求`
- `## 尾帧要求`
- `## 优化后视频提示词`
- `## 连续性检查`

## Segment `first-frame.md`

按这个顺序写：

1. 所属 story、集数、分段。
2. 首帧画面精确描述。
3. 角色锁定和可见状态。
4. 场景、道具、特效、光线、构图、镜头。
5. 与上一段尾帧的继承关系。
6. 负面提示词。

## Segment `last-frame.md`

按这个顺序写：

1. 所属 story、集数、分段。
2. 尾帧画面精确描述。
3. 角色锁定和可见状态。
4. 场景、道具、特效、光线、构图、镜头。
5. 给下一段首帧继承的画面状态。
6. 负面提示词。

## Segment `prompt.md`

按这个顺序写，方便后续视频 API / 图生视频工具使用：

1. 视频规格：9:16、时长 15 秒以内、风格、清晰度、运动质量。
2. 角色锁定和 story 参考。
3. 叙事动作和运镜。
4. 台词。
5. 音效。
6. 负面提示词。

## Segment `api-request.md`

使用这些章节：

- 标题：`# Segment XX 视频 API 请求`
- `## 任务信息`
- `## 输入文件`
- `## 请求参数`
- `## 提交记录`
- `## 返回记录`
- `## 失败原因与重试策略`

## `qa-checklist.md`

必须检查：

- 剧情与留存。
- 四段结构。
- 首尾帧连续性。
- 视频 API 可提交性。
- story 资产引用。
- 发布包装。

## `publish-package.md`

必须包含：

- 3 个标题候选。
- 封面画面建议。
- 封面大字。
- 抖音简介。
- 评论区引导。
- 标签方向。
- 适合二次切片的瞬间。

## 命名

- 新 episode 目录使用 `EPXXX_short-english-slug`。
- 默认 60 秒 4 段时，segment 目录固定：
  - `segment_01_00-15s`
  - `segment_02_15-30s`
  - `segment_03_30-45s`
  - `segment_04_45-60s`
- 如果 story 明确要求 2-3 分钟样片或长集，可以继续递增，例如：
  - `segment_05_60-75s`
  - `segment_06_75-90s`
  - `segment_07_90-105s`
  - `segment_08_105-120s`
  - `segment_09_120-135s`
  - `segment_10_135-150s`

## 导演检查清单

- 开头是否承接上一集钩子或剧本开场。
- 前 5 秒是否有压力、情绪或好奇点。
- 本集是否有清晰爽点、揭示、反转或情绪爆发。
- 最后一个镜头是否强迫观众想看下一集。
- 是否明确引用 story 的角色锁、场景锁、道具锁。
- 每段是否都有故事板、首帧、尾帧和视频 prompt。
- 每段是否能独立交给视频 API 生成。
- 是否有 API 任务记录位置。
- 是否有标题、封面、评论引导和标签。
- 首尾帧是否能连续剪辑。
- 负面提示词是否足够防止人脸漂移、风格漂移和视频伪影。
- 最终图片是否已运行 `scripts/verify_episode_frames.py`。
- 是否打开最终 contact sheet 做视觉检查。
