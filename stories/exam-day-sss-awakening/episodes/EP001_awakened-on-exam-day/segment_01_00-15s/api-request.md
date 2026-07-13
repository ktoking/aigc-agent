# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-07-02T18:30:37+08:00
- 完成时间：
- Task ID：cgt-20260702183028-w76h4

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/exam-day-sss-awakening/episodes/EP001_awakened-on-exam-day/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/exam-day-sss-awakening/episodes/EP001_awakened-on-exam-day/segment_01_00-15s/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/exam-day-sss-awakening/episodes/EP001_awakened-on-exam-day/segment_01_00-15s/frames/last-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/exam-day-sss-awakening/assets/characters/EX_SHEN_JIN_001/character-reference.png
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 720p |
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
