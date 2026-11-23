# EP044 Segment 2 视频交接

版本：2026-10-21-seedance25-story-rebuild

状态：提示词已重写；本轮未提交视频。旧output为历史记录。

## 参数
- 模型：Seedance 2.5，doubao-seedance-2-5-260628。依据2026-10-21官方教程；账户权限未调用测试。
- duration=30，ratio=16:9，resolution=480p，generate_audio=true。
- 参考生视频；无首尾帧；auto_images=false。
- 唯一提交提示词：director-promt.txt；prompt.md为逐字副本。
- SHA256：23d006e7222489f08ad4f54dafc1f5278c5d06fc3484f5db0ad997c3cecc678b
- 台词有效字数：68；按每秒4字仅粗估17.0秒，不等于音频实测；画外音可覆盖动作，口型镜头留反应时间。

## 精确输入顺序
数字人先按首次清晰露脸排序，然后是场景道具；所有图片内容块统一1–9编号。身份段与场景段分开展示，编号不重新从1开始。

| 图片序号 | 标签 | 来源（相对story根目录） | 职责 | 当前状态 |
| --- | --- | --- | --- | --- |
| 1 | 冬狼 | asset://asset-20260720205729-l4dfh | 只绑定冬狼本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 2 | 叶凝霜 | asset://asset-20260720212023-wwndz | 只绑定叶凝霜本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 3 | 许砚 | asset://asset-20260320075237-29hdx | 只绑定许砚本人脸与身份；服装和表演以正文为准 | user_registered_identity |
| 4 | 正确别墅冬季总景 | assets/production/ep036-defrost-and-intel/references/canonical-villa-overcast-snow-16x9.png | 正确冬日别墅总景，只锁建筑、围墙、外门与院内位置，屋顶服从原图；图中没有人物 | existing_candidate_pending_new_shot_review |
| 5 | 同一关闭黑门 | assets/production/ep042-044-reference-refresh/references/canonical-gate-closed-winter-16x9.png | 原黑门门柱、内外侧与关闭状态，不改变canonical建筑；冻结发生墙外 | existing_candidate_pending_new_shot_review |
| 6 | 墙外冰封倒地轮廓 | assets/production/ep042-044-reference-refresh/references/ice-covered-faceless-silhouette-snow-16x9.png | 墙外单个无脸冰封轮廓与倒地冰层质感；不锁新面孔，不出现碎尸 | existing_candidate_pending_new_shot_review |
| 7 | 外骨骼过热停用 | assets/production/ep042-044-reference-refresh/references/exoskeleton-overheat-joint-16x9.png | 外骨骼同款关节、过热警示与停用状态；不锁新人物或新装甲 | existing_candidate_pending_new_shot_review |
| 8 | 冬狼现代黑色冬装 | assets/production/ep042-044-reference-refresh/references/wolf-winter-long-coat-flatlay-16x9.png | 冬狼无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |
| 9 | 凝霜白色冬装 | assets/production/ep042-044-reference-refresh/references/ye-winter-long-coat-flatlay-16x9.png | 叶凝霜无脸服装参考，服装必须与本段完整文字一致；不据此生成其他人脸 | existing_candidate_pending_new_shot_review |

## 下一步
本地候选图齐全；提交前须逐图确认新镜头的建筑、服装、状态和机位，再核对实际请求映射。

不自动上传旧frames、人物三视图或旧output；不自动重生成。正式生成后检查身份、服装、人数、动作、声音与切镜，不能用文本检查替代看片。

提交记录：无。任务ID：无。
