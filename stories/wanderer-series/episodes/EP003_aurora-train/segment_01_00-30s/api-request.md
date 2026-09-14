# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-30s
- 时长：30
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：http-400
- 提交时间：2026-09-11T20:47:20+08:00
- 完成时间：
- Task ID：

## 输入文件

- Prompt：stories/wanderer-series/episodes/EP003_aurora-train/segment_01_00-30s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wanderer-series/episodes/EP003_aurora-train/frames/ref_01_train_interior.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wanderer-series/episodes/EP003_aurora-train/frames/ref_02_train_exterior.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/wanderer-series/episodes/EP003_aurora-train/frames/ref_03_train_bedroom.png
- 数字人资产（作为 image_url 提交）：
- 无
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：local_image / 车内一层生活场景
- API图片2：local_image / 列车外部与冰原雪景
- API图片3：local_image / 二层卧室仅锁定双层结构

数字人资产与场景素材统一计入提示词的 `参考图` 编号，编号与 API 图片输入顺序完全一致。

## 提示词参考图顺序

- 参考图1：车内一层生活场景
- 参考图2：列车外部与冰原雪景
- 参考图3：二层卧室仅锁定双层结构

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 30 |
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
