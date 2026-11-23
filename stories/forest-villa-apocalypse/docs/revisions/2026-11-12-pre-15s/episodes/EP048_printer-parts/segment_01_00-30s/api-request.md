# EP048 Segment 1 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：f2ec8113f26973a3156700697ebd856dfb5fe79e0d1dda278d3207b283820599
- 台词有效字数：88；按每秒4字仅粗估22.0秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 白棠 | asset://asset-20260320075131-k78qt | 只绑定白棠本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 原工业打印仓 | assets/props/FVA_INDUSTRIAL_METAL_PRINTER_001/references/industrial-metal-printer-installed-utilities-16x9.png | 既有单台炭灰封闭工业金属打印仓、原料盒、输出托盘与工作间；不锁时间或人物 | existing_candidate_pending_new_shot_review |
| 4 | 有限机械小件与护板 | assets/production/ep044-050-seedance25/references/mechanicalParts-16x9.png | 少量机械支架、单块外门防撞护板与有限原料并列，电子封装件单独放；无人物 | generated_builtin_basic_visual_review |
| 5 | 外门新增外侧防撞板 | assets/production/ep044-050-seedance25/references/gateRepair-single-plate-v2-16x9.png | 沿用EP045已修好的黑门内锁板，新增外侧同色防撞护板；灰墙、电网、屋顶不变，无人物 | generated_builtin_basic_visual_review |
| 6 | 有限种子与空育苗盘 | assets/production/ep044-050-seedance25/references/seedTray-16x9.png | 原工作间旧架、空育苗盘与有限种子袋，接近窗口光照不均；无人物，不画成熟蔬菜 | generated_builtin_basic_visual_review |
| 7 | 白棠鼠尾草绿工装 | assets/characters/FVA_BAI_TANG_001/references/bai-tang-survival-outfit-flatlay-16x9.png | 白棠无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 8 | 许砚炭灰工装 | assets/characters/FVA_XU_YAN_001/references/xu-yan-winter-work-outfit-flatlay-16x9.png | 许砚无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 本段物件收束局部 | assets/production/ep044-050-seedance25/references/ep048-s1-detail-16x9.png | 原打印仓有限剩余料、已分格机械备件与单独旧电子件，不把电子件打印出来；无人物 | generated_builtin_basic_visual_review |

## 下一步
本地图已补齐；新图已做基础目视检查，旧候选图仍须按镜头复核。只按reference-assets.json显式取图，不扫描旧frames，不传首尾帧。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
