# EP041 Segment 4 视频交接

版本：2026-09-23-dialogue-rebuild-eight-shots
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：15秒；16:9；有声音；480p为当前草稿清晰度意图。
- 可沿用已有15秒分段方案；本次不调用API。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：2c0203a852bb0a47094674830599419750eedd41d90c434ea813d2e6405c0169。

## 具名数字人，按首次清晰出场排序
- 参考图1：叶凝霜=asset://asset-20260720212023-wwndz
- 参考图2：沈知夏=asset://asset-20260310030618-88hlb
- 参考图3：许砚=asset://asset-20260320075237-29hdx

仅画外音：白棠，不上传这些角色的脸。

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。当前所有非人物图均待新稿验收或待生图，不能把旧frames编号直接当API编号。

| 请求编号 | 用途 | 当前候选路径（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定叶凝霜本人脸和身份，服装按正文 | asset://asset-20260720212023-wwndz | user_registered_identity |
| 2 | 只绑定沈知夏本人脸和身份，服装按正文 | asset://asset-20260310030618-88hlb | user_registered_identity |
| 3 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 4 | 既定别墅冬季结构，只锁同一栋现代三层主楼、连续阳台、高围墙、黑门与院内空间；屋顶形状逐项服从原图，不按文字另造 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | candidate_needs_current_visual_review |
| 5 | 外门内外同一门柱、交易槽和门机位置；开闭按当镜状态 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-warm-gate-entry-16x9.png | candidate_needs_current_visual_review |
| 6 | 围墙完整、门外薄冰障被火烧融的状态 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 7 | 门柱对讲设备与手持终端，不增加广播大喇叭 | assets/props/references/outer-gate-trade-intercom-box-16x9.png | candidate_needs_current_visual_review |
| 8 | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-winter-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 9 | 沈知夏无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |

## 提交前门禁
- [ ] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [ ] 生成缺图，显式绑定路径与image-label；重排本地frames时另做清单，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
