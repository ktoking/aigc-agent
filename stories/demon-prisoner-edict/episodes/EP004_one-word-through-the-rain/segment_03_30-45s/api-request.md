# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_03_30-45s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-08-21T15:12:31+08:00
- 完成时间：
- Task ID：cgt-20260821151227-pj86n

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP004_one-word-through-the-rain/segment_03_30-45s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP004_one-word-through-the-rain/segment_03_30-45s/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP004_one-word-through-the-rain/segment_03_30-45s/frames/shot-02.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP004_one-word-through-the-rain/segment_03_30-45s/frames/last-frame.png
- 数字人资产（作为 image_url 提交）：
- 无
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：local_image / first-frame
- API图片2：local_image / shot-02
- API图片3：local_image / last-frame

数字人资产与场景素材统一计入提示词的 `参考图` 编号，编号与 API 图片输入顺序完全一致。

## 提示词参考图顺序

- 参考图1：first-frame
- 参考图2：shot-02
- 参考图3：last-frame

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
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
