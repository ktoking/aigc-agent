# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-15s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-08-27T18:21:31+08:00
- 完成时间：
- Task ID：cgt-20260827182129-xbb8z

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP028_uninvited-guest-at-heat-drain/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/villa-control-room-first-snow-cold-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-metal-printer-installed-utilities-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-energy-shed-cooling-loop-16x9.png
- 数字人资产（作为 image_url 提交）：
- 许砚：`asset://asset-20260320075237-29hdx`
- 白棠：`asset://asset-20260320075131-k78qt`
- 沈知夏：`asset://asset-20260310030618-88hlb`
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：digital_human / 许砚
- API图片2：digital_human / 白棠
- API图片3：digital_human / 沈知夏
- API图片4：local_image / 冬季低温控制室
- API图片5：local_image / 工业打印仓
- API图片6：local_image / 冬季能源棚冷却回路

兼容旧剧集：数字人资产位于顶部身份锁，提示词 `参考图` 仅编号非人物素材。

## 提示词参考图顺序

- 参考图1：冬季低温控制室
- 参考图2：工业打印仓
- 参考图3：冬季能源棚冷却回路

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
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
