# Segment 01｜30秒、十图任务包

状态：图片已备齐，视频未提交。

- duration目标：30秒。
- ratio：9:16；resolution目标：720p。
- prompt：director-promt.txt。
- 参考图：严格按frames/reference-manifest.json的inputs1—10。
- 当前仓库草稿默认模型：doubao-seedance-2-0-mini-260615；本轮没有验证其当时30秒与十图输入能力。实际提交前核对接口参数，不假定本地任务包等于平台接受。
- 输出：output/；本轮无任务ID、计费或视频返回。

参考图1：frames/first-frame.png。用途：0秒首帧状态，只定义段首。
参考图2：frames/last-frame.png。用途：30秒目标尾帧状态，不得提前出现尾段动作。
参考图3：frames/keyframe_before-15s.png。用途：约15秒前的内部关键状态，按对应镜头使用。
参考图4：frames/keyframe_after-15s.png。用途：约15秒后的内部关键状态，作为中段节拍参考。
参考图5：frames/ref-su-sleep.png。用途：只锁苏晚棠脸、长发、耳钉与卧室米白睡衣；参考板多视图不复制到成片。
参考图6：frames/ref-su-gown.png。用途：只锁10—15秒原书记忆中的同一女主与黑礼服；不把礼服带回卧室。
参考图7：frames/ref-bedroom.png。用途：卧室布局、自然光、床和镜子。
参考图8：frames/ref-fire-hall.png。用途：仅10—15秒生日宴记忆的空间与火烟，其他时间不得出现火烟。
参考图9：frames/ref-ring.png。用途：一枚银色钻戒与一只深蓝戒盒，控制摘下、装盒、闭盒顺序；道具多视图只作形态参考。
参考图10：frames/ref-system.png。用途：系统二维提示与四档案卡的视觉；头像、数值和文字留后期，仅女主感知。
