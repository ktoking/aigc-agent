# EP041 Segment 1 视频交接

版本：2026-09-23-dialogue-rebuild-eight-shots
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：15秒；16:9；有声音；480p为当前草稿清晰度意图。
- 可沿用已有15秒分段方案；本次不调用API。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：4e9933f7ea191daee114ad0982642575825a57252a0d8ad1b31240504dde525f。

## 具名数字人，按首次清晰出场排序
- 参考图1：许砚=asset://asset-20260320075237-29hdx
- 参考图2：白棠=asset://asset-20260320075131-k78qt

仅画外音：冬狼，不上传这些角色的脸。

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。当前所有非人物图均待新稿验收或待生图，不能把旧frames编号直接当API编号。

| 请求编号 | 用途 | 当前候选路径（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定许砚本人脸和身份，服装按正文 | asset://asset-20260320075237-29hdx | user_registered_identity |
| 2 | 只绑定白棠本人脸和身份，服装按正文 | asset://asset-20260320075131-k78qt | user_registered_identity |
| 3 | 现代控制室的监控台、座位与空间，不沿用旧屏幕剧情 | assets/production/ep039-041-reference-completion/references/controlClean-16x9.png | candidate_needs_current_visual_review |
| 4 | 既定别墅冬季结构，只锁同一栋现代三层主楼、连续阳台、高围墙、黑门与院内空间；屋顶形状逐项服从原图，不按文字另造 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | candidate_needs_current_visual_review |
| 5 | 冬狼车载扩音器外壳，不锁乘员或车辆完好程度 | assets/production/ep039-041-reference-completion/references/loudspeaker-16x9.png | candidate_needs_current_visual_review |
| 6 | 围墙完整、门外薄冰障被火烧融的状态 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 7 | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 8 | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 9 | 本段「对方开出条件」的无人物局部机位，锁同一空间材质、光向与物件比例 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |

## 提交前门禁
- [ ] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [ ] 生成缺图，显式绑定路径与image-label；重排本地frames时另做清单，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
