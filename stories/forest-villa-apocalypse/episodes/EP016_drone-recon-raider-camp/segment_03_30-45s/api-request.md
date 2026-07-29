# Segment 视频 API 请求

## 任务信息

- Episode：EP016
- Segment：segment_03_30-45s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-07-27T18:34:28+08:00
- 完成时间：
- Task ID：cgt-20260727183419-ffdld

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP016_drone-recon-raider-camp/segment_03_30-45s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP016_drone-recon-raider-camp/segment_02_15-30s/output/last-frame-generated.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/rainy-energy-shed-micro-reactor-complete-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/backup-battery-system-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/props/references/auto-defense-turret-balcony-radar-16x9.png
- 数字人资产（作为 image_url 提交）：
- `asset://asset-20260320075237-29hdx`
- `asset://asset-20260320075131-k78qt`
- `asset://asset-20260310030618-88hlb`
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
