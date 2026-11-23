# EP049 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：059849c9083ff4c9ada73a12eeacd772d100a0c5069d82082671afd0139bc5d4
- 台词有效字数：93；按每秒4字仅粗估23.3秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物 | existing_candidate_pending_new_shot_review |
| 4 | 原双门人工交易槽 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-gate-transfer-hatch-16x9.png | 原黑门上的双门交易槽、托盘与内外门关系，主门关闭，箱子需人手推动；无人物 | existing_candidate_pending_new_shot_review |
| 5 | 盐包与有限菜蛋 | assets/production/ep044-050-seedance25/references/saltTrade-16x9.png | 封口盐包、小筐青菜与两枚垫好的鸡蛋分开放，交易量有限；无人物，无药品交易 | generated_builtin_basic_visual_review |
| 6 | 旧泵变形支架 | assets/production/ep044-050-seedance25/references/brokenPump-16x9.png | 一台小型旧水泵、明显歪斜的外部安装支架，保留完整原外壳；无人物，不拆复杂内部 | generated_builtin_basic_visual_review |
| 7 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 本段物件收束局部 | assets/production/ep044-050-seedance25/references/ep049-s1-detail-16x9.png | 原门外对讲与小物资箱的位置关系，关闭主门、双门交易托盘，不画人或自动推出的箱子 | generated_builtin_basic_visual_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
