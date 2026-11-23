# EP046 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：60a9885b773b1f075a74067a90d268ab5a969bd35992a1ed90471dcc95ddbe68
- 台词有效字数：86；按每秒4字仅粗估21.5秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只绑定叶凝霜本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 4 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物 | existing_candidate_pending_new_shot_review |
| 5 | 原禽舍饮水器冻住 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-empty-modern-16x9.png | 原院内现代金属禽舍结构、旧饮水器出水口冻住的局部，少量鸡，不出现陌生房屋或人 | existing_candidate_pending_new_shot_review |
| 6 | 原鱼池局部保温罩 | assets/production/ep044-050-seedance25/references/pondCover-16x9.png | 原循环鱼池边缘薄冰，局部透明保温罩留通气与检修口，过滤桶仍在旧位置；无人物 | generated_builtin_basic_visual_review |
| 7 | 有限膜材分配与旧架 | assets/production/ep044-050-seedance25/references/shelterBuild-16x9.png | 同一院内原禽舍单侧挡风膜与相邻鱼池罩，有限膜材在旧架上，通风口留出；无人物 | generated_builtin_basic_visual_review |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
