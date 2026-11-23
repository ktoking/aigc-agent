# EP044 Segment 2 视频交接

版本：2026-10-08-human-dialogue
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：30秒；16:9；有声音；480p为当前草稿清晰度意图。
- 保留现有30秒分段，不擅自恢复成四段；本次未核实任何服务是否支持30秒、480p与指定模型的组合，提交前必须核对实际端点。不声称Seedance 2.0-mini或旧文档中的Seedance 2.5必然支持。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：7175224e7821e079d853c706c9a59af67df204e494e60b96bd8388cfff641c2e。本轮仅扩写导演稿的非对白执行细节；已有prompt.md对白与导演稿不完全一致，不得混用或覆盖。

## 具名数字人，按首次清晰出场排序
- 参考图1：冬狼=asset://asset-20260720205729-l4dfh
- 参考图2：叶凝霜=asset://asset-20260720212023-wwndz
- 参考图3：许砚=asset://asset-20260320075237-29hdx

仅画外音：白棠，不上传这些角色的脸。

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。六项非人物图已按新稿核对并落盘；仅上传下表编号4-9，不自动扫描旧frames根目录。

| 请求编号 | 用途 | 已验收输入（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定冬狼本人脸和身份，服装按正文 | asset://asset-20260720205729-l4dfh | user_registered_identity |
| 2 | 只绑定叶凝霜本人脸和身份，服装按正文 | asset://asset-20260720212023-wwndz | user_registered_identity |
| 3 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 4 | 既定别墅冬季结构，只锁同一栋现代三层主楼、连续阳台、高围墙、黑门与院内空间；屋顶形状逐项服从原图，不按文字另造 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | reviewed_existing_16x9 |
| 5 | 只锁正确别墅原有黑色双扇铁门、灰墙和门柱；开闭按镜头变化，别墅全貌只服从参考图4 | assets/production/ep042-044-reference-refresh/references/canonical-gate-closed-winter-16x9.png | generated_reviewed_16x9 |
| 6 | 只锁门外单个冰封物倒地的冰层质感；冬狼身份与服装仍服从数字人和参考图8 | assets/production/ep042-044-reference-refresh/references/ice-covered-faceless-silhouette-snow-16x9.png | generated_reviewed_16x9 |
| 7 | 只锁外骨骼过热关节和熄灭状态灯，不锁背景或新增装备 | assets/production/ep042-044-reference-refresh/references/exoskeleton-overheat-joint-16x9.png | generated_reviewed_16x9 |
| 8 | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | generated_reviewed_16x9 |
| 9 | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | generated_reviewed_16x9 |

## 提交前门禁
- [x] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [x] 生成缺图，显式绑定路径与image-label；新图在frames/current-references，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
