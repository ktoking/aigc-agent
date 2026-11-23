# 第01段视频输入包

图片状态为IMAGES_READY。视频提交状态为NOT_SUBMITTED。规划15秒、16:9，director-promt.txt是当前视频提示词。图片采用多图参考的段内锚点，顺序如下。

参考图1＝frames/keyframe-01-a-v1.png，段内约2秒关键状态《袖内试法，手里空空》，锁定该时段构图、人物动作和场景关系。
参考图2＝frames/keyframe-01-b-v1.png，段内约11.8秒关键状态《尊者请登云》，锁定该时段构图、人物动作和场景关系。
参考图3＝frames/C01-xie-wujiu-new-cast-turnaround-v1.png，谢无咎新人物三视图，锁脸、发型、服装与道具位置。
参考图4＝frames/C04-xuanheng-new-cast-turnaround-v1.png，玄衡新人物三视图，锁脸、发型、服装与道具位置。
参考图5＝frames/C05-lu-qing-new-cast-turnaround-v1.png，陆青新人物三视图，锁脸、发型、服装与道具位置。

本段输入为两张关键帧和实际出场人物三视图，文件均在frames。first-frame.md和last-frame.md记录两张图的段内锚点。正式任务提交时核验模型支持、输入数与实测配音时长，返回记录保存到output。
