# 虹阶学院

EP01《今晚六点，你陪谁？》是原创日系 3D Galgame 式约会事件。45 秒，9:16，同一男主第一视角。三位女主都喜欢男主，分别用直说前的犹豫、主动伸手和临场改约表达。

| 段落 | 表演轨迹 | 可投喂导演稿 | 表演转折帧 |
| --- | --- | --- | --- |
| 01 雨宫六花 | 捏领叫住 → 腰肩转向窗边 → 转回来直视 | [最新版导演稿](episodes/EP001_who_at_six/segment_01_00-15s/director-promt.txt) | [被问中后装镇定](episodes/EP001_who_at_six/segment_01_00-15s/frames/mid-frame.png) |
| 02 橘日奈 | 先伸手 → 俯身收手 → 起身再递 | [最新版导演稿](episodes/EP001_who_at_six/segment_02_15-30s/director-promt.txt) | [手收回了，话还是说出口](episodes/EP001_who_at_six/segment_02_15-30s/frames/mid-frame.png) |
| 03 白峰澪 | 合掌请求 → 跨半步、侧身让路 → 转回合掌偷笑 | [最新版导演稿](episodes/EP001_who_at_six/segment_03_30-45s/director-promt.txt) | [改约现在](episodes/EP001_who_at_six/segment_03_30-45s/frames/mid-frame.png) |

[九张图的输入顺序](episodes/EP001_who_at_six/image-manifest.md) · [附件台词留存](episodes/EP001_who_at_six/dialogue-v1.md) · [逐拍时间线](episodes/EP001_who_at_six/episode-plan.json) · [质检](episodes/EP001_who_at_six/qa-checklist.md)

## 交接

每段优先使用首帧、表演转折、尾帧三张输入。图库对齐的是同一人物三个动作状态，影片持续演出。各段 `api-request.md` 提供三图本地预检命令。手动生成的 MP4 放在对应分段的 `output/video.mp4`。原生声轨先逐句核对音色、口型和尾字，再根据实听调整字幕时间。
