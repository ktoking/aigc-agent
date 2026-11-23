# EP046 Segment 2 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：df268b02660715205ce12f48146735320ec69d104d49667e80f43323c4ee4c80
- 台词有效字数：74；按每秒4字仅粗估18.5秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只绑定叶凝霜本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 4 | 禽舍修后通风与饮水 | assets/production/ep044-050-seedance25/references/coopWarm-16x9.png | 同一现代禽舍完成单侧挡风、原饮水器解冻后有水，保留通风口；无人物 | generated_builtin_basic_visual_review |
| 5 | 窝箱单枚鸡蛋 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-poultry-pen-first-egg-16x9.png | 同一禽舍窝箱内仅一枚蛋与垫草的近景，不锁背景建筑或人物 | existing_candidate_pending_new_shot_review |
| 6 | 保温罩内循环水和鱼影 | assets/production/ep044-050-seedance25/references/pondWarm-16x9.png | 同一透明罩下鱼影、气泡与正常循环水，鱼大小不被异能放大；无人物 | generated_builtin_basic_visual_review |
| 7 | 山谷旧泵房炊烟 | assets/production/ep044-050-seedance25/references/pumpHouseSmoke-16x9.png | 南侧山谷旧泵房远景，一缕炊烟，树林遮挡；没有人物脸、尸潮、可读坐标或新别墅 | generated_builtin_basic_visual_review |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 凝霜白色冬装 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
