# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_ballroom-reversal
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-07-02T17:35:39+08:00
- 完成时间：
- Task ID：cgt-20260702173529-kjhwt

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rich-family-revenge-heiress/experiments/EP001_heirship-reveal/segment_01_ballroom-reversal/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rich-family-revenge-heiress/experiments/EP001_heirship-reveal/segment_01_ballroom-reversal/frames/heroine-reference.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rich-family-revenge-heiress/experiments/EP001_heirship-reveal/segment_01_ballroom-reversal/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rich-family-revenge-heiress/experiments/EP001_heirship-reveal/segment_01_ballroom-reversal/frames/last-frame.png
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 720p |
| generate_audio | False |
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
