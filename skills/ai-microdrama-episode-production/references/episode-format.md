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
- `segment_01_00-15s/director-promt.txt`
- `segment_01_00-15s/api-request.md`，推荐用于视频 API 任务记录
- `segment_02_15-30s/storyboard.md`
- `segment_02_15-30s/first-frame.md`
- `segment_02_15-30s/last-frame.md`
- `segment_02_15-30s/prompt.md`
- `segment_02_15-30s/director-promt.txt`
- `segment_02_15-30s/api-request.md`
- `segment_03_30-45s/storyboard.md`
- `segment_03_30-45s/first-frame.md`
- `segment_03_30-45s/last-frame.md`
- `segment_03_30-45s/prompt.md`
- `segment_03_30-45s/director-promt.txt`
- `segment_03_30-45s/api-request.md`
- `segment_04_45-60s/storyboard.md`
- `segment_04_45-60s/first-frame.md`
- `segment_04_45-60s/last-frame.md`
- `segment_04_45-60s/prompt.md`
- `segment_04_45-60s/director-promt.txt`
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

## Segment `director-promt.txt`

这是视频 API 直投提示词，沿用项目既有文件名拼写 `director-promt.txt`。内容应是纯文本导演执行指令，不要写成 Markdown 报告，也不要包含 key、URL、任务 ID 或 output 产物信息。

按这个顺序写：

1. 全局规格：9:16、15 秒、720p、风格、明显非真人、是否生成声音。
2. 参考图用途：按 API 输入顺序写“参考图1/参考图2/参考图3”，首帧锁什么、尾帧锁什么、角色/场景/动作/道具参考锁什么；不要笼统写“参考所有图片”，不要把故事板表格拉成视频。
3. 角色锁定：角色 ID 或角色名、发型、服装、关键标记、禁止变化项。
4. 本段戏剧任务：本 15 秒要让观众看懂的一个核心问题。
5. 逐秒动作因果：0-3 秒、3-7 秒、7-11 秒、11-15 秒，每块写清动作、命中点/受力点、路径和运镜。
6. 声音：无对白/有对白、环境声、动作声、台词落点。
7. 禁止项：字幕、水印、logo、静态拉图、角色漂移、场景跳变、故事专属禁忌和画质负面词。

## Segment `api-request.md`

使用这些章节：

- 标题：`# Segment XX 视频 API 请求`
- `## 任务信息`
- `## 输入文件`
- `## 参考图上传计划`：按 API 输入顺序列出 3-5 张图；默认首帧、尾帧，加本段最容易漂移的角色/动作/场景/道具图；明确 `frames/storyboard-sheet.png` 默认不上传。
- `## 请求参数`
- `## 推荐 dry-run 命令`：显式列出 `--image` 或 `--image-url`，不要依赖读者猜测。
- `## 提交记录`
- `## 返回记录`
- `## 失败原因与重试策略`

参考图上传计划写法：

```markdown
## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3”保持一致：

1. `frames/first-frame.png`：锁定 0 秒桥接画面。
2. `frames/last-frame.png`：锁定 15 秒收束画面。
3. `<story-assets-path>`：锁定本段最容易漂移的角色、动作、场景路线或关键道具。

不上传：`frames/storyboard-sheet.png`。故事板表格只做人类审阅，避免文字/表格污染和静态拉图。
```

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
