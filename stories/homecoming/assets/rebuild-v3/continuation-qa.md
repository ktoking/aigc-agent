# 缺图续生成检查

- 本轮补充19张原先缺失的关键帧；怪人主参考沿用本次v3新图，五张原始男主参考保持不变。
- `segment_01` 的 `keyframe_07_monster_claw_wall.png` 仍缺失。原构图以及无伤害静态手部特写均被内置图片服务输出审核拒绝（moderation_blocked / violence）。没有用旧图或其他镜头冒充。
- `segment_02/keyframe_01_speed_attack.png` 改为交手前怪人蹲在公交车顶蓄势；`keyframe_02_one_hand_blast.png` 改为动作后男主抬左手、空店铺落尘。两张是前后状态参考，不是实际接触瞬间；视频导演稿未改动。
- 已针对无人超市多余怪人、云端肩部错误菜篮、云端人物比例、巨拳张手等问题进行局部修正，修正提示词与图同名保存。
- 图片为生成的构图及身份参考，不等于视频动作连续性已验证。巨人近景与远景的精确600m比例、左右手跨镜衔接仍需视频阶段核对；单张透视图不能证明精确尺寸。
- 每段 `frames/reference-manifest.json` 列出本段实际文件。按镜头选择引用；不能将全部参考不加区分一次提交。
- 原始男主参考文件实际编码为JPEG。各段副本使用 `ref-male-protagonist-three-view.jpg` 并记录 `image/jpeg`，内容哈希与原始男主文件完全相同；assets中的原图未改名、未转码。
