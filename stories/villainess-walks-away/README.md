# 当恶毒女配决定不爱了

Story ID：villainess-walks-away。豪门穿书／退婚／追妻／系统悬疑；第一季12集，每集约2分钟。

距离原著中的死亡只剩21天。系统要苏晚棠攻略四个男人，她先摘下订婚戒指，准备带着自己的钱离开。

## 当前执行规格

用户2026-10-29指定：**4段×30秒，每段10张参考图**。共24镜；不再采用八段15秒与五图输入。文字时长仍为估排；尚未制作配音或视频。

| 段 | 时段 | 内容 | 参考图 |
| --- | --- | --- | --- |
| 01 | 00—30秒 | 死亡任务与拒绝攻略 | 10张 |
| 02 | 30—60秒 | 准备离开与带协议赴约 | 10张 |
| 03 | 60—90秒 | 退婚谈判与承担过错 | 10张 |
| 04 | 90—120秒 | 签字与反常追问 | 10张 |

## 当前入口

- production/segments-30s-v1/README.md：四段提示词与十图入口。
- production/segments-30s-v1/gallery.md：每段十图总览。
- production/segments-30s-v1/index.html：离线图库，点击放大。
- production/segments-30s-v1/manifest.json：四段、时长、十图顺序及hash。
- episodes/EP001_no-more-chasing/episode.md：第一集剧本。
- 同集novel.md：小说正文；storyboard.md：24镜分镜。

每个当前segment的frames/内恰有10张真实PNG，按reference-manifest.json的inputs1—10对应director-promt.txt；不需要从其他目录临时找图。每段还有references.md，可逐张查看职责。

## 素材与历史

assets-v1共31张新图：8张人物/服装参考、4张场景、3张道具/系统、16张事件画面；另保留用户风格原图。当前打包复用这些素材，四段首尾共8张，其余8张事件画面作为段内关键帧。人物、场景与道具可跨段引用。

旧八段15秒目录已完整归档到episodes/EP001_no-more-chasing/archive/segments-15s/。production/assets-v1/gallery.md保留最初素材全集，图片链接已修复到实际归档位置。剧情与台词未改，未重复生图。
