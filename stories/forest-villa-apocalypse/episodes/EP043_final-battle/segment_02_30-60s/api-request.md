# EP043 Segment 2 视频交接

版本：2026-10-08-human-dialogue
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：30秒；16:9；有声音；480p为当前草稿清晰度意图。
- 保留现有30秒分段，不擅自恢复成四段；本次未核实任何服务是否支持30秒、480p与指定模型的组合，提交前必须核对实际端点。不声称Seedance 2.0-mini或旧文档中的Seedance 2.5必然支持。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：8b9e0b4f9b6a73b7b84b5df91a9716709888224b2b4d1e135800f2d1bf8efcc4。

## 具名数字人，按首次清晰出场排序
- 参考图1：白棠=asset://asset-20260320075131-k78qt
- 参考图2：许砚=asset://asset-20260320075237-29hdx
- 参考图3：沈知夏=asset://asset-20260310030618-88hlb

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。六项非人物图已按新稿核对并落盘；仅上传下表编号4-9，不自动扫描旧frames根目录。

| 请求编号 | 用途 | 已验收输入（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定白棠本人脸和身份，服装按正文 | asset://asset-20260320075131-k78qt | user_registered_identity |
| 2 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 3 | 只绑定沈知夏本人脸和身份，服装按正文 | asset://asset-20260310030618-88hlb | user_registered_identity |
| 4 | 只锁现代车库独立维修区、唯一打印仓及接线；门外已改冬季雪林 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | generated_reviewed_16x9 |
| 5 | 手机投影三选一：短时防护外骨骼、便携观察镜、未知卡 | assets/production/ep042-044-reference-refresh/references/exoskeleton-three-choice-cards-16x9.png | generated_reviewed_16x9 |
| 6 | 一件暗灰工业防护外骨骼与人工扣合结构 | assets/production/ep042-044-reference-refresh/references/industrial-protective-exoskeleton-16x9.png | generated_reviewed_16x9 |
| 7 | 外骨骼人工卸下后挂回的充电支架 | assets/production/ep042-044-reference-refresh/references/exoskeleton-charge-stand-night-16x9.png | generated_reviewed_16x9 |
| 8 | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | reviewed_existing_16x9 |
| 9 | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | reviewed_existing_16x9 |

## 提交前门禁
- [x] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [x] 生成缺图，显式绑定路径与image-label；新图在frames/current-references，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
