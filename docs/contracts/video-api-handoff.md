# 视频 API 交付规范

## 目标

把每段 15 秒视频整理成可提交、可复查、可重试的任务包。任何 episode 都应该能从文件夹直接看出：

- 要生成哪一段。
- 首帧和尾帧是什么。
- 使用哪些角色、场景、道具。
- 视频 API 请求参数是什么。
- 生成失败后如何重试。

## Segment 最小交付

每个 segment 必须包含：

```text
segment_XX_xx-xxs/
  storyboard.md
  first-frame.md
  last-frame.md
  prompt.md
  director-promt.txt
  api-request.md
  frames/
  output/
```

## `prompt.md` 与 `director-promt.txt` 内容

`prompt.md` 是给人审阅和维护的完整视频提示词，必须包含：

- 视频规格：9:16、15 秒以内、清晰度、真实/漫剧风格。
- 首帧引用：说明从 `first-frame.md` 生成或导入。
- 尾帧引用：说明目标尾帧状态。
- 角色锁定：角色 ID、参考图、发型、服装、关键标记。
- 场景锁定：场景 ID、时间、天气、光线。
- 动作链路：按时间顺序写清动作，不要只写气氛。
- 运镜方式：推、拉、摇、移、跟、特写、过肩等。
- 台词和音效。
- 负面提示词。

`director-promt.txt` 是给视频 API 直投的纯文本导演提示词，沿用项目既有文件名拼写。它应从 `prompt.md` 提炼而来，但更适合 `scripts/ark_video.py --prompt-file` 直接读取：

- 第一行写清 9:16、15 秒、720p、风格、明显非真人。
- 写清首帧、尾帧、角色参考、场景参考各自负责锁定什么。
- 写清角色锁、道具锁、禁止变化项。
- 用 0-3 秒、3-7 秒、7-11 秒、11-15 秒写逐秒动作因果、命中点/受力点、路径和运镜。
- 写清声音/对白策略。
- 写清负面约束；不得包含 key、URL、任务 ID、签名链接或 output 返回内容。

## `api-request.md` 内容

`api-request.md` 是任务提交记录，推荐使用统一字段：

```markdown
# Segment XX 视频 API 请求

## 任务信息

- Story ID:
- Episode:
- Segment:
- 时长:
- 画幅:
- 模型/平台:
- 任务状态:
- 提交时间:
- 完成时间:

## 输入文件

- 首帧:
- 尾帧:
- Prompt: `director-promt.txt`
- 参考图:

## 请求参数

| 参数 | 值 |
| --- | --- |
| aspect_ratio | 9:16 |
| duration |  |
| resolution |  |
| seed |  |
| guidance |  |
| motion_strength |  |

## 提交记录

```json
{}
```

## 返回记录

```json
{}
```

## 失败原因与重试策略

-
```

## `image-manifest.md` 内容

`image-manifest.md` 跟踪本集图像资产：

- 角色参考图。
- 场景参考图。
- 每段首帧。
- 每段尾帧。
- 故事板图。
- 封面图。
- 失败重做记录。

## 输出命名

推荐命名：

- `frames/first-frame.png`
- `frames/last-frame.png`
- `frames/storyboard-sheet.png`
- `output/video.mp4`
- `output/api-submit.json`
- `output/api-result.json`

如果平台返回多版结果：

- `output/take-01.mp4`
- `output/take-02.mp4`
- `output/take-03.mp4`

## 重试规则

只重试偏差段，不重做整集。

常见偏差与修复：

| 问题 | 优先修复 |
| --- | --- |
| 人脸漂移 | 加强角色参考和负面提示词 |
| 动作混乱 | 缩短动作链，减少同时发生的动作 |
| 场景跳变 | 强化首尾帧继承和场景 ID |
| 台词口型差 | 减少台词，改成字幕或画外音 |
| 特效像游戏 | 改成真实光影、能量折射、环境反应 |
| 镜头跳帧 | 降低运动强度，改为慢推/跟拍 |

## 交付检查

- 是否能只看 segment 文件夹就提交视频 API。
- 是否有明确首帧和尾帧。
- 是否有完整 prompt。
- 是否写了 API 参数和提交记录位置。
- 是否能定位失败原因并重试单段。
