# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_04_45-60s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-07-31T20:40:17+08:00
- 完成时间：
- Task ID：仅保留于已忽略的 `output/task-id.txt`，不提交仓库

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/episodes/EP001_no-system-clean-the-stage/segment_04_45-60s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/episodes/EP001_no-system-clean-the-stage/segment_03_30-45s/output/last-frame-generated.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/characters/SMA_ZHAO_TIANLIN_001/canonical-turnaround.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/assets/scenes/SCENE_SYSTEM_WORLD_MONTAGE_001/canonical-concept.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/system-master-admin/episodes/EP001_no-system-clean-the-stage/segment_04_45-60s/frames/last-frame.png
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
| privacy_retry | 1 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧/故事板图，
  自动追加“图中人物均为 AI 生成虚拟角色，不包含真人隐私信息”的说明后有限重试。
- 若重试后仍被拦截，脚本停止，不自动替换为场景图或其他错误参考图，避免人脸不一致和无效消耗。
