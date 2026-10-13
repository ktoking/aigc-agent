# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：l07
- 时长：5
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：http-403
- 提交时间：2026-09-17T18:36:09+08:00
- 完成时间：
- Task ID：

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rift-breakers/episodes/OP00_opening/segment_01_00-30s/promt_dir/prompt_l07.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/rift-breakers/episodes/OP00_opening/segment_01_00-30s/frame/07_l07_akaji-leap.png
- 数字人资产（作为 image_url 提交）：
- 无
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：local_image / 07_l07_akaji-leap

数字人资产与场景素材统一计入提示词的 `参考图` 编号，编号与 API 图片输入顺序完全一致。

## 提示词参考图顺序

- 参考图1：07_l07_akaji-leap

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 5 |
| resolution | 720p |
| generate_audio | False |
| return_last_frame | True |
| virtual_person_notice | True |
| privacy_retry | 2 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧/故事板图，
  自动追加“图中人物均为 AI 生成虚拟角色，不包含真人隐私信息”的说明后有限重试。
- 若重试后仍被拦截，脚本停止，不自动替换为场景图或其他错误参考图，避免人脸不一致和无效消耗。
