# Segment XX 视频 API 请求

## 任务信息

- Story ID：
- Episode：
- Segment：
- 时长：
- 画幅：9:16
- 模型/平台：
- 任务状态：未提交
- 提交时间：
- 完成时间：

## 输入文件

- Prompt：`director-promt.txt`

## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3”保持一致：

1. `frames/first-frame.png`：锁定 0 秒桥接画面和人物站位。
2. `frames/last-frame.png`：锁定 15 秒收束画面和下一段衔接。
3. `STORY_ASSET_REFERENCE_PATH`：锁定本段最容易漂移的角色、动作、场景路线或关键道具。

不上传：`frames/storyboard-sheet.png`。故事板表格只做人类审阅，避免文字/表格污染和静态拉图。

## 请求参数

| 参数 | 值 |
| --- | --- |
| aspect_ratio | 9:16 |
| duration |  |
| resolution |  |
| seed |  |
| guidance |  |
| motion_strength |  |
| camera_motion |  |
| prompt | director-promt.txt |
| include_storyboard | false |

## 推荐 dry-run 命令

```bash
python3 scripts/ark_video.py submit \
  --segment STORY_SEGMENT_PATH \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file STORY_SEGMENT_PATH/director-promt.txt \
  --image STORY_SEGMENT_PATH/frames/first-frame.png \
  --image STORY_SEGMENT_PATH/frames/last-frame.png \
  --image STORY_ASSET_REFERENCE_PATH \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

## 提交记录

```json
{}
```

## 返回记录

```json
{}
```

## 失败原因与重试策略

-
