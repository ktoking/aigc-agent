# Segment 03 视频 API 请求

## 任务信息

- Story ID：`demon-prisoner-edict`
- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_03_30-45s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9 横屏
- 模型/平台：未选择
- 任务状态：未提交

## 输入文件

- 首帧：`frames/first-frame.png`
- 中间参考：`frames/shot-02.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`

## 推荐验证参数

| 参数 | 值 |
| --- | --- |
| aspect_ratio | 16:9 |
| duration | 5-second action test before any full render |
| resolution | 720p draft |
| motion_strength | medium |

## 提交与返回

- 本轮明确不提交视频任务。
- 未产生请求 payload、任务 ID、返回 URL 或费用。

## 重试策略

- 箭向错误：固定箭从后方右侧进入。
- 凝固不同步：删去次要动作，只保留刀、箭、雨同时停。
- 特效像游戏：移除粒子，只保留雨滴、折射和瞳内微光。
