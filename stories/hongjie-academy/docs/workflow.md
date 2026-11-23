# 工作流

从剧集目录读取 `episode-plan.json`、`dialogue-v1.md` 和 `连续性.md`。各段的 `storyboard.md` 用于分镜审阅，`director-promt.txt` 用于复制投喂，`reference-plan.json` 记录首帧、转折帧、尾帧的三图顺序。按连续动作演出，依据实际片段验收动作是否发生。

生成后把每个 MP4 放入对应的 `output/video.mp4`，保留各轮原结果和任务记录，按逐句实听修订估时。先完成三个单段的口型、对白和画面验收，再按节目顺序硬切成合集。
