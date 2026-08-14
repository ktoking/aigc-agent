# Segment 视频 API 请求

## 任务信息

- Episode：EP023
- Segment：segment_01_00-15s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：generated-legacy-format
- 提交时间：2026-08-07T18:39:32+08:00
- 完成时间：
- Task ID：cgt-20260807183926-xkftl

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP023_courtyard-trade-listening-device/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP022_mobile-supply-convoy-trade-test/segment_04_45-60s/output/last-frame-generated.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/villa-front-yard-trade-zone-open-gate-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-structure-three-view-perimeter-electric-v2-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/references/ep023-antibiotic-trade-case-hidden-compartment-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/references/ep023-listening-device-shield-box-16x9.png
- 数字人资产（作为 image_url 提交）：
- `asset://asset-20260320075237-29hdx`
- `asset://asset-20260310030618-88hlb`
- `asset://asset-20260720210545-pxk4m`
- 平台信任参考图 URL：
- 无

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

## 质量判定

- 原任务沿用 EP022 的分层格式：数字人作为独立资产输入，场景与道具图片单独编号。后续继续保留这种格式。
- 抽帧确认本段许砚与顾承泽能够区分；保留原 Task ID、请求记录和视频。

## 下次提交门禁

- 数字人顺序固定为：许砚、沈知夏、顾承泽。
- 本地图顺序固定为：EP022尾帧、别墅前院交易区、别墅三视图、抗生素物资箱、窃听器与屏蔽盒。
- 每个数字人使用 `角色名=asset://...` 并在提示词顶部写身份锁；本地图提供同序 `--image-label`，只校验 `参考图1..5`。
- 本段生成完成后先抽帧和听音验收；只有写入 `output/video-qa.json` 且状态为 `passed`，才允许提交 Segment02。
