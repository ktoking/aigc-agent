# 第06段视频输入包

图片状态为IMAGES_READY。视频提交状态为NOT_SUBMITTED。规划15秒、16:9，director-promt.txt是当前视频提示词。图片采用多图参考的段内锚点，顺序如下。

参考图1＝frames/keyframe-06-a-v1.png，段内约6.7秒关键状态《刚想苟住，又来一位尊者》，锁定该时段构图、人物动作和场景关系。
参考图2＝frames/keyframe-06-b-v1.png，段内约14.4秒关键状态《唯一山门，被白璃挡住》，锁定该时段构图、人物动作和场景关系。
参考图3＝frames/C01-xie-wujiu-new-cast-turnaround-v1.png，谢无咎新人物三视图，锁脸、发型、服装与道具位置。
参考图4＝frames/C02-shen-zhaoyue-new-cast-turnaround-v1.png，沈照月新人物三视图，锁脸、发型、服装与道具位置。
参考图5＝frames/C04-xuanheng-new-cast-turnaround-v1.png，玄衡新人物三视图，锁脸、发型、服装与道具位置。
参考图6＝frames/C05-lu-qing-new-cast-turnaround-v1.png，陆青新人物三视图，锁脸、发型、服装与道具位置。
参考图7＝frames/C06-driver-and-loader-new-cast-turnaround-v1.png，外门车夫与搬货弟子新人物三视图，锁脸、发型、服装与道具位置。
参考图8＝frames/C03-bai-li-new-cast-turnaround-v1.png，白璃新人物三视图，锁脸、发型、服装与道具位置。

本段输入为两张关键帧和实际出场人物三视图，文件均在frames。first-frame.md和last-frame.md记录两张图的段内锚点。正式任务提交时核验模型支持、输入数与实测配音时长，返回记录保存到output。
