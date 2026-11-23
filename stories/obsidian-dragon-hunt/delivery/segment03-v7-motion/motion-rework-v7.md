# Segment03对抗重做｜v7

可以参考《英雄联盟》电影短片的动作设计：预备、启动、接触、失衡、反制和恢复，由对手的行动触发下一动作。此处没有取得或调用官方骨骼/动作捕捉文件，也未将作品名当作可执行动作数据。

本次保留原segment03的30秒、三头龙、6人身份、同一谷地、4+2弹药和既有破甲链。重写的是龙与队员持续争主动权的动作。

- 原片完整抽帧与定点密集序列：output/review-v7/。
- 原片问题与来源：../../../production/v7/segment03-rework/source-review.json。
- 新30秒导演提示：director-promt.txt；新版分镜：storyboard.md。
- 新动作首帧：frames/motion-v7/first-frame.png。
- 新输入：共5图，图1动作预备、图2龙结构、图3机器人、图4精灵、图5刺客；旧10张站姿图仍保留但不批量喂作时间目标。
- 原片已判不通过，下一次生成另存take-v7-motion.mp4，完整检查后才能替换当前video.mp4。

动作参考入口：[Riot 2019赛季／Awaken](https://na.leagueoflegends.com/en/featured/events/season-start-2019)、[Riot Warriors CG资料](https://www.leagueoflegends.com/en-us/news/community/warriors-cinematic-season-2020-asset-pack/)。以上只标识参考作品；本次对原片的判断来自本地视频抽帧，未声称已逐帧分析这两部官方短片。
