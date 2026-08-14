# Segment 01 视频 API 请求

## 任务信息

- Story ID：`demon-prisoner-edict`
- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_01_00-15s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9 横屏
- 模型/平台：未选择
- 任务状态：未提交

## 输入文件

- 首帧：`frames/first-frame.png`
- 中间参考：`frames/shot-02.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`

## 推荐参数

| 参数 | 值 |
| --- | --- |
| aspect_ratio | 16:9 |
| duration | 15 |
| resolution | 720p draft |
| motion_strength | low |

## 提交与返回

- 未产生请求 payload。
- 未产生任务 ID、返回 URL 或计费记录。

## 重试策略

- 人脸漂移：只重试镜头二或三，加强角色锚点。
- 人影被画清：降低门帘后景清晰度，强调 silhouette only。
- 运镜过大：改为固定机位加 2.5D 轻推。
