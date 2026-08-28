# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_02_15-30s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-08-25T18:58:55+08:00
- 完成时间：
- Task ID：cgt-20260825185849-cm2fx

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP027_evolved-draw-heat-signature-concealment/segment_02_15-30s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/villa-overnight-defense-control-room-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/FVA_EVOLVED_DRAW_SYSTEM_001/references/evolved-daily-draw-three-choice-phone-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/villa-thermal-signature-reactor-printer-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/rainy-energy-shed-micro-reactor-complete-16x9.png
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
- API图片4：local_image / 控制室
- API图片5：local_image / 三选一抽卡手机
- API图片6：local_image / 改造前热成像
- API图片7：local_image / 雨后能源棚

数字人资产与场景素材统一计入提示词的 `参考图` 编号，编号与 API 图片输入顺序完全一致。

## 提示词参考图顺序

- 参考图1：许砚
- 参考图2：白棠
- 参考图3：沈知夏
- 参考图4：控制室
- 参考图5：三选一抽卡手机
- 参考图6：改造前热成像
- 参考图7：雨后能源棚

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
