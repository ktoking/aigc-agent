# Segment 视频 API 请求

## 任务信息

- Episode：EP002_owner-in-the-scrap
- Segment：segment_02_15-30s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-08-05T12:13:42+08:00
- 完成时间：
- Task ID：cgt-20260805121339-fsgxt

## 输入文件

- Prompt：stories/system-master-admin/episodes/EP002_owner-in-the-scrap/segment_02_15-30s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/episodes/EP002_owner-in-the-scrap/segment_02_15-30s/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/characters/SMA_ZHAO_TIANLIN_001/canonical-turnaround.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/scenes/SCENE_AWAKENING_HALL_001/canonical-concept.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/episodes/EP002_owner-in-the-scrap/segment_02_15-30s/frames/last-frame.png
- 数字人资产（作为 image_url 提交）：
- 无
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 480p |
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
