# EP041 Segment 2 视频交接

版本：2026-09-23-dialogue-rebuild-eight-shots
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：15秒；16:9；有声音；480p为当前草稿清晰度意图。
- 可沿用已有15秒分段方案；本次不调用API。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：0843e9cff5a3587ee6b9e25362e8b5569f956ad677888d3c72a63f5721275863。

## 具名数字人，按首次清晰出场排序
- 参考图1：叶凝霜=asset://asset-20260720212023-wwndz
- 参考图2：沈知夏=asset://asset-20260310030618-88hlb

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。当前所有非人物图均待新稿验收或待生图，不能把旧frames编号直接当API编号。

| 请求编号 | 用途 | 当前候选路径（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定叶凝霜本人脸和身份，服装按正文 | asset://asset-20260720212023-wwndz | user_registered_identity |
| 2 | 只绑定沈知夏本人脸和身份，服装按正文 | asset://asset-20260310030618-88hlb | user_registered_identity |
| 3 | 现代控制室的监控台、座位与空间，不沿用旧屏幕剧情 | assets/production/ep039-041-reference-completion/references/controlClean-16x9.png | candidate_needs_current_visual_review |
| 4 | 控制室相邻的休整椅与医疗观察位置 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 5 | 叶凝霜旧印记边缘的少量残留微光 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 6 | 现有医疗工作台与急救包外观，不生成隔离剧情 | assets/scenes/SCENE_FOREST_VILLA_001/references/garage-quarantine-medical-bay-16x9.png | candidate_needs_current_visual_review |
| 7 | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-winter-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 8 | 沈知夏无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 9 | 无脸头模的银白长发颜色、长度和层次，不生成人脸或头模 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-silver-white-hair-reference-16x9.png | candidate_needs_current_visual_review |

## 提交前门禁
- [ ] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [ ] 生成缺图，显式绑定路径与image-label；重排本地frames时另做清单，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
