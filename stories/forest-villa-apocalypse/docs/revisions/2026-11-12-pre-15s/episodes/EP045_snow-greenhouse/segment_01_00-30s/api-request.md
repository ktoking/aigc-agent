# EP045 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：21c72bf8abd9e7194fc9f73bc74e47d0acb16a4a03fbf40299ca461c6daf23df
- 台词有效字数：78；按每秒4字仅粗估19.5秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物 | existing_candidate_pending_new_shot_review |
| 4 | 旧锁板变形 | assets/production/ep042-044-reference-refresh/references/black-gate-center-latch-strain-16x9.png | 门内旧锁板歪斜、中央锁舌错位，门本体没有被打穿；无人物 | existing_candidate_pending_new_shot_review |
| 5 | 新锁板装回原门 | assets/production/ep045-rebuild-reference-refresh/references/black-gate-replaced-center-latch-16x9.png | 同一黑门装回一块新锁板的局部，旧划痕保留，不新增外侧护板；无人物 | existing_candidate_pending_new_shot_review |
| 6 | 打印仓单块锁板成品 | assets/production/ep045-rebuild-reference-refresh/references/industrial-printer-single-gate-latch-plate-16x9.png | 原打印仓输出托盘里的一块新锁板与旁边旧件，有限材料，人工安装；无人物 | existing_candidate_pending_new_shot_review |
| 7 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 本段物件收束局部 | assets/production/ep045-rebuild-reference-refresh/references/courtyard-greenhouse-old-film-leak-16x9.png | 院内同一现代温室旧膜一处接缝掀起，下面两盘苗落雪，黑色棚架完整；无人物 | existing_candidate_pending_new_shot_review |

## 下一步
本地候选图齐全；提交前须逐图确认新镜头的建筑、服装、状态和机位，再核对实际请求映射。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
