# Segment 视频 API 请求

## 任务信息

- Episode：EP023
- Segment：segment_03_30-45s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：succeeded，人工 QA passed
- 提交时间：2026-08-11T15:22:16+08:00
- 完成时间：2026-08-11T15:25:07+08:00
- Task ID：cgt-20260811152210-b2hjv

## 输入文件

- Prompt：stories/forest-villa-apocalypse/episodes/EP023_courtyard-trade-listening-device/segment_03_30-45s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/vehicles/references/mobile-convoy-merchant-cab-interior-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/references/wideband-radio-surveillance-console-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/references/auto-defense-turret-balcony-radar-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/villa-front-yard-trade-zone-open-gate-16x9.png
- 数字人资产（作为 image_url 提交）：
- 顾承泽：`asset://asset-20260720210545-pxk4m`
- 许砚：`asset://asset-20260320075237-29hdx`
- 沈知夏：`asset://asset-20260310030618-88hlb`
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：digital_human / 顾承泽
- API图片2：digital_human / 许砚
- API图片3：digital_human / 沈知夏
- API图片4：local_image / 顾承泽货车驾驶室
- API图片5：local_image / 控制室宽带无线电台
- API图片6：local_image / 六座自动炮台监控状态
- API图片7：local_image / 现代别墅前院

数字人资产与场景素材统一计入提示词的 `参考图` 编号，编号与 API 图片输入顺序完全一致。

## 提示词参考图顺序

- 参考图1：顾承泽
- 参考图2：许砚
- 参考图3：沈知夏
- 参考图4：顾承泽货车驾驶室
- 参考图5：控制室宽带无线电台
- 参考图6：六座自动炮台监控状态
- 参考图7：现代别墅前院

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

## 本次质量判定

- 任务 `cgt-20260811152210-b2hjv` 已完成并下载，视频规格为 864x496、15.104 秒、H.264 + AAC。
- 2fps 全片抽帧确认：镜头一和镜头四均为棕色微卷发、深绿色外套的顾承泽；镜头二和镜头三为黑色短发、灰色工装的许砚以及酒红工装的沈知夏，无人物互换、融合或额外人物。
- Whisper 识别出四句对白内容完整、顺序正确；结合画面检查，说话者依次为顾承泽、沈知夏、许砚、顾承泽。
- 本段人工 QA 已通过，记录见 `output/video-qa.json`。本次只提交 Segment03，未提交 Segment04。
