# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_02_15-30s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-260128
- 任务状态：submitted
- 提交时间：2026-06-18T22:12:35+08:00
- 完成时间：
- Task ID：cgt-20260618221234-hn8h5

## 输入文件

- Prompt：stories/last-mile-robot/episodes/SF001_last-delivery/segment_02_15-30s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/last-mile-robot/assets/characters/LMR_COURIER_BOT_001/01-locked-reference/main-reference.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/last-mile-robot/episodes/SF001_last-delivery/segment_02_15-30s/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/last-mile-robot/assets/scenes/SCENE_RUINED_DELIVERY_CITY/01-locked-reference/main-reference.png
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15 |
| resolution | 720p |
| generate_audio | True |
| return_last_frame | True |
| virtual_person_notice | True |
| privacy_retry | 0 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧/故事板图，
  自动追加“图中人物均为 AI 生成虚拟角色，不包含真人隐私信息”的说明后有限重试。
- 若重试后仍被拦截，脚本停止，不自动替换为场景图或其他错误参考图，避免人脸不一致和无效消耗。
