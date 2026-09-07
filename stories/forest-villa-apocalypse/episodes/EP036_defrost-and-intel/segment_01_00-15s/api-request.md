# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-15s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：submitted
- 提交时间：2026-09-03T16:33:11+08:00
- 完成时间：
- Task ID：cgt-20260903163304-lcgff

## 输入文件

- Prompt：/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP036_defrost-and-intel/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/production/ep036-defrost-and-intel/references/modern-winter-intel-control-room-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-winter-outfit-flatlay-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png
- 数字人资产（作为 image_url 提交）：
- 沈知夏：`asset://asset-20260310030618-88hlb`
- 叶凝霜：`asset://asset-20260720212023-wwndz`
- 白棠：`asset://asset-20260320075131-k78qt`
- 许砚：`asset://asset-20260320075237-29hdx`
- 平台信任参考图 URL：
- 无

## 实际 API 图片输入顺序

- API图片1：digital_human / 沈知夏
- API图片2：digital_human / 叶凝霜
- API图片3：digital_human / 白棠
- API图片4：digital_human / 许砚
- API图片5：local_image / EP036_CONTROL_ROOM_INTEL_001
- API图片6：local_image / FVA_YE_NINGSHUANG_OUTFIT_FLATLAY_001
- API图片7：local_image / FVA_XU_YAN_OUTFIT_FLATLAY_001
- API图片8：local_image / FVA_BAI_TANG_OUTFIT_FLATLAY_001
- API图片9：local_image / FVA_SHEN_ZHIXIA_OUTFIT_FLATLAY_001

兼容旧剧集：数字人资产位于顶部身份锁，提示词 `参考图` 仅编号非人物素材。

## 提示词参考图顺序

- 参考图1：EP036_CONTROL_ROOM_INTEL_001
- 参考图2：FVA_YE_NINGSHUANG_OUTFIT_FLATLAY_001
- 参考图3：FVA_XU_YAN_OUTFIT_FLATLAY_001
- 参考图4：FVA_BAI_TANG_OUTFIT_FLATLAY_001
- 参考图5：FVA_SHEN_ZHIXIA_OUTFIT_FLATLAY_001

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15 |
| resolution | 480p |
| generate_audio | True |
| return_last_frame | False |
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
