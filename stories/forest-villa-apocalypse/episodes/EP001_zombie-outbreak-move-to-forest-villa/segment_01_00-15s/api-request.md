# Segment 视频 API 请求

## 任务信息

- Episode：EP001_zombie-outbreak-move-to-forest-villa
- Segment：segment_01_00-15s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-260128
- 任务状态：submitted
- 提交时间：2026-07-09T11:27:21+08:00
- 完成时间：
- Task ID：cgt-20260709112716-9gcvj

## 输入文件

- Prompt：stories/forest-villa-apocalypse/episodes/EP001_zombie-outbreak-move-to-forest-villa/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/production/city-outbreak-street.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/interiors/references/xu-yan-city-apartment-evacuation.png
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
