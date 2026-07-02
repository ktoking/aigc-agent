# Segment 00 视频 API 请求

## 任务信息

- Story ID：`apocalypse-supermarket`
- Episode：EP001_open-store-after-apocalypse
- Segment：segment_00_prologue_00-15s
- 时长：15
- 画幅：16:9
- 分辨率：720p
- 模型/平台：Seedance 2.0-mini 草稿
- 是否生成音频：是，提交时必须加 `--generate-audio`
- 任务状态：未提交

## 参考图上传计划

1. `frames/first-frame.png`：锁定灰雨街道和城市失序。
2. `frames/last-frame.png`：锁定林乔准备开门、超市暖灯亮起。
3. `assets/characters/AS_LIN_QIAO_001/turnaround.png`：锁定林乔服装和发型。
4. `assets/scenes/SCENE_FORTIFIED_SUPERMARKET/scene-reference.png`：锁定超市空间。

不上传：故事板表格图、带箭头标注图、任何可读文字图。

## Dry-run 命令

```bash
python3 scripts/ark_video.py submit \
  --segment stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_00_prologue_00-15s \
  --duration 15 \
  --ratio 16:9 \
  --resolution 720p \
  --prompt-file stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_00_prologue_00-15s/director-promt.txt \
  --image stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_00_prologue_00-15s/frames/first-frame.png \
  --image stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_00_prologue_00-15s/frames/last-frame.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

