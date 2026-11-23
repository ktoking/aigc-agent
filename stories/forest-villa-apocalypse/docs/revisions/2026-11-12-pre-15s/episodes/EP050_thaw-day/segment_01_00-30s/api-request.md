# EP050 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：a7bb496f829c001941f7ad20a6971af1bddae2a7a2777e3ab79836d27bbee1dd
- 台词有效字数：85；按每秒4字仅粗估21.3秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 原现代工作间 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | 原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具 | existing_candidate_pending_new_shot_review |
| 4 | 旧泵变形支架 | assets/production/ep044-050-seedance25/references/brokenPump-16x9.png | 一台小型旧水泵、明显歪斜的外部安装支架，保留完整原外壳；无人物，不拆复杂内部 | generated_builtin_basic_visual_review |
| 5 | 同一旧泵修后试水 | assets/production/ep044-050-seedance25/references/repairedPump-16x9.png | 同一旧泵装上新外部支架，防溅台上试转、管口回到同一水桶；电气部分不浸水，无人物 | generated_builtin_basic_visual_review |
| 6 | 一层育苗灯架 | assets/production/ep044-050-seedance25/references/seedlingRack-16x9.png | 原工作间一层旧金属架安装有限育苗灯、控制组件与一盘刚播种的苗盘；无人物，不生成多层工厂 | generated_builtin_basic_visual_review |
| 7 | 单盘叶菜与邻盘幼苗 | assets/production/ep044-050-seedance25/references/growthTray-16x9.png | 温室中一盘接近采收的叶菜与邻盘刚播小苗，前者展开到成熟、后者不变；仅提供作物状态，不锁人物 | generated_builtin_basic_visual_review |
| 8 | 自用与交换的有限收成 | assets/production/ep044-050-seedance25/references/eggAndGreens-16x9.png | 当晚自用碗与少量交换菜分别放，库存鸡蛋和有限青菜，不虚构满仓收获；无人物 | generated_builtin_basic_visual_review |
| 9 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
