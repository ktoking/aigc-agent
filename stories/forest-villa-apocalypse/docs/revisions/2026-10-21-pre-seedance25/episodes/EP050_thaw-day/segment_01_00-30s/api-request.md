# EP050 Segment 1 视频交接

版本：2026-10-08-human-dialogue
状态：新版剧本文本完成；未提交新版视频。旧output及视频均为历史版本，未改动。

## 参数意图
- 时长：30秒；16:9；有声音；480p为当前草稿清晰度意图。
- 保留现有30秒分段，不擅自恢复成四段；本次未核实任何服务是否支持30秒、480p与指定模型的组合，提交前必须核对实际端点。不声称Seedance 2.0-mini或旧文档中的Seedance 2.5必然支持。
- 无首尾帧；禁止auto-images；禁止自动重生成。
- Prompt：director-promt.txt，SHA256：152ebbca7b4c6d8db846eebe3bccb3a75806d7c30ca671f9f2a4c5ee66ce1a4b。

## 具名数字人，按首次清晰出场排序
- 参考图1：白棠=asset://asset-20260320075131-k78qt
- 参考图2：叶凝霜=asset://asset-20260720212023-wwndz

## 参考图上传计划
九项规划见reference-assets.json，数字人计入九项。当前所有非人物图均待新稿验收或待生图，不能把旧frames编号直接当API编号。

| 请求编号 | 用途 | 当前候选路径（相对story root） | 状态 |
| --- | --- | --- | --- |
| 1 | 只绑定白棠本人脸和身份，服装按正文 | asset://asset-20260320075131-k78qt | user_registered_identity |
| 2 | 只绑定叶凝霜本人脸和身份，服装按正文 | asset://asset-20260720212023-wwndz | user_registered_identity |
| 3 | 一层工作中的育苗灯架、育苗盘与已有滴灌 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 4 | 单盘叶菜由苗到成熟，旁边其他盘不变 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 5 | 当晚自用一篮菜、一枚蛋、另留的少量交易菜 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 6 | 完成挡风改造的原禽舍，饮水器恢复出水 | 尚无可确认的新稿对应图 | needs_generation_for_new_script |
| 7 | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 8 | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-winter-outfit-flatlay-16x9.png | candidate_needs_current_visual_review |
| 9 | 无脸头模的银白长发颜色、长度和层次，不生成人脸或头模 | assets/characters/FVA_ICE_WOMAN_001/references/ye-ningshuang-silver-white-hair-reference-16x9.png | candidate_needs_current_visual_review |

## 提交前门禁
- [ ] 逐图人工确认人物、服装、建筑、时段和道具状态。旧蓝西装炎魁、古风冬狼、旧黑丝袜凝霜图不得控制新稿服装。
- [ ] 生成缺图，显式绑定路径与image-label；重排本地frames时另做清单，不改旧任务证据。
- [ ] 确认真实模型、时长、清晰度支持；正式请求与本段9项规划一致。
- [ ] dry-run回读asset ID、标签、顺序、数量与prompt哈希。
- [ ] 试听实际合成对白与动作空间，不拿字数检查替代音画验收。

本次提交记录：无。任务ID：无。既有任务历史仍在output，不代表本轮提示词已生成。
