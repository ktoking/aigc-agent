# EP047 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：719044327a33239f074e98ff34bd5351cff52451e5ff24c0c27a91478c965307
- 台词有效字数：92；按每秒4字仅粗估23.0秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 沈知夏 | asset://asset-20260310030618-88hlb | 只绑定沈知夏本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 独立能源棚外观 | assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-winter-energy-shed-cooling-loop-16x9.png | 原围墙内独立能源棚、密封发电模块外壳与外部供暖柜，生活区距离服从canonical；无人物 | existing_candidate_pending_new_shot_review |
| 4 | 外部供暖支路柜 | assets/production/ep044-050-seedance25/references/heatingBranch-16x9.png | 密封核能主机之外的独立供暖柜，源侧与回屋侧管路、外接阀件可区分；无人物，无主机内部 | generated_builtin_basic_visual_review |
| 5 | 外部执行件一次检查 | assets/production/ep044-050-seedance25/references/valveCheck-16x9.png | 同一外部传感器与两只小执行件，其中一只卡住；手持终端仅外观，不画内部电路；无人物 | generated_builtin_basic_visual_review |
| 6 | 现代客厅地暖空间 | assets/scenes/SCENE_FOREST_VILLA_001/references/villa-ground-floor-self-built-radiant-heating-16x9.png | 原现代客厅、稳定照明、地暖分水器、厚毯与暖桌；只锁空间，不靠图片断言温度 | existing_candidate_pending_new_shot_review |
| 7 | 旧件与最后一个备用件 | assets/production/ep044-050-seedance25/references/spareTray-16x9.png | 旧外接执行件、仅一只备用件与空格备件盒，分开摆放；换件后盒子为空，无人物 | generated_builtin_basic_visual_review |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 知夏暗酒红医护工装 | assets/characters/FVA_SHEN_ZHIXIA_001/references/shen-zhixia-medical-outfit-flatlay-16x9.png | 沈知夏无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
