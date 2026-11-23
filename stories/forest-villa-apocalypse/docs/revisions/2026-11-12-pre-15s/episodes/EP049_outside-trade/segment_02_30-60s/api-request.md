# EP049 Segment 2 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：059d6def6cd5cb3fba386cde2890f992949e58ddc3b372a9410d9d2a6a4d6778
- 台词有效字数：88；按每秒4字仅粗估22.0秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 原现代工作间 | assets/production/ep042-044-reference-refresh/references/industrial-metal-printer-winter-workshop-16x9.png | 原现代灰白工作间、打印仓和金属台面，窗外冬雪；只锁空间与机器，不锁台上新道具 | existing_candidate_pending_new_shot_review |
| 4 | 旧泵变形支架 | assets/production/ep044-050-seedance25/references/brokenPump-16x9.png | 一台小型旧水泵、明显歪斜的外部安装支架，保留完整原外壳；无人物，不拆复杂内部 | generated_builtin_basic_visual_review |
| 5 | 待验原料包装照片 | assets/production/ep044-050-seedance25/references/feedstockLabel-16x9.png | 手机上的旧仓库原料包装照片，与本机原包装标签并列；只锁包装外观，不把照片变为已收到实物；无人物 | generated_builtin_basic_visual_review |
| 6 | 收到的盐包储位 | assets/production/ep044-050-seedance25/references/saltShelf-16x9.png | 现代干燥储架里刚收好的一包盐，自用食品储位保留，不出现无限物资；无人物 | generated_builtin_basic_visual_review |
| 7 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 8 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 本段物件收束局部 | assets/production/ep044-050-seedance25/references/ep049-s2-detail-16x9.png | 原工作间独立待修架上仅同一故障泵、旧件与有限工具，旁边盐包已收好；无人物 | generated_builtin_basic_visual_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
