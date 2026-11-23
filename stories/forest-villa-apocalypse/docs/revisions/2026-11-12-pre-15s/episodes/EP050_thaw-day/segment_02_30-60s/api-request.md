# EP050 Segment 2 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：b7ba8ee2fd19ccadb4a5320147cdace1a49a75d3a08bdac83607cd2fef853a66
- 台词有效字数：85；按每秒4字仅粗估21.3秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 沈知夏 | asset://asset-20260310030618-88hlb | 只绑定沈知夏本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只绑定叶凝霜本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 4 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物 | existing_candidate_pending_new_shot_review |
| 5 | 原双门人工交易槽 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-gate-transfer-hatch-16x9.png | 原黑门上的双门交易槽、托盘与内外门关系，主门关闭，箱子需人手推动；无人物 | existing_candidate_pending_new_shot_review |
| 6 | 原料包装与合格试件 | assets/production/ep044-050-seedance25/references/feedstockCheck-16x9.png | 匹配本机包装的一小袋原料、同批小试件、旧机型标签并列，有限数量；无人物，无制造参数 | generated_builtin_basic_visual_review |
| 7 | 同一旧泵修后试水 | assets/production/ep044-050-seedance25/references/repairedPump-16x9.png | 同一旧泵装上新外部支架，防溅台上试转、管口回到同一水桶；电气部分不浸水，无人物 | generated_builtin_basic_visual_review |
| 8 | 现代别墅暖色餐区 | assets/production/ep044-050-seedance25/references/dining-16x9.png | canonical现代别墅暖色餐区、普通碗筷、窗外冬雪；四把椅子可见但没有人物，不画四人合照 | generated_builtin_basic_visual_review |
| 9 | 青菜鸡蛋面 | assets/production/ep044-050-seedance25/references/noodles-16x9.png | 普通陶瓷碗中的青菜鸡蛋面，少量真实热气，现代餐桌，无火锅、宴席、人物和文字 | generated_builtin_basic_visual_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
