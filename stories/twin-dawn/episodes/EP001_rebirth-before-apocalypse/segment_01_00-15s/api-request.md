# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-fast-260128
- 任务状态：submitted
- 提交时间：2026-06-17T15:45:09+08:00
- 完成时间：
- Task ID：cgt-20260617154508-zklxx

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s/prompt.md
- 参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/assets/scenes/SCENE_APOCALYPSE_STREET/apocalypse-street-night.png

## 版本判定

- 本次 `video-scene-ref-15s.mp4` 使用场景图绕过输入图片隐私审核，未使用本段首帧、尾帧和故事板人物图。
- 因角色脸部一致性不可靠，本视频只保留为接口连通性技术测试，不作为 EP001 Segment 01 正片或可发布素材。
- 正片生成必须优先使用 `frames/first-frame.png`、`frames/last-frame.png`、`frames/storyboard.png`，并在 prompt 中声明图中人物均为 AI 生成虚拟角色、不包含真人隐私信息。

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 720p |
| generate_audio | False |
| return_last_frame | True |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，保留原首尾帧/故事板图，在 prompt 中补充“人物均为 AI 生成虚拟角色，不包含真人隐私信息，不需要真人隐私校验”等说明后有限重试。
- 若重试后仍被拦截，停止生成，不自动替换为场景图或其他错误人物参考图。
