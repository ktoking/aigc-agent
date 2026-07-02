# Segment 01 视频 API 请求

## 任务信息

- Story ID：`apocalypse-supermarket`
- Episode：EP001_open-store-after-apocalypse
- Segment：segment_01_00-15s
- 时长：15
- 画幅：16:9
- 分辨率：720p
- 模型/平台：Seedance 2.0-mini 草稿
- 是否生成音频：是，提交时必须加 `--generate-audio`
- 任务状态：已提交，running
- Task ID：`cgt-20260628145456-n6pxn`
- 提交响应：`output/api-submit-codex-v2.json`
- 首次查询：`output/api-poll-codex-v2-once.json`

## 参考图上传计划

1. `frames/first-frame.png`：锁定本段 0 秒桥接画面和人物站位。
2. `frames/last-frame.png`：锁定本段 15 秒收束画面和下一段衔接。
3. 按本段风险追加 1-2 张资产图：角色三视图、横屏超市场景图、补货特效图或会员卡道具图。

不上传：`frames/storyboard-sheet.png` 或任何带表格、箭头、文字标注的故事板图。

本次实际提交使用压缩后的 Codex Image 新风格参考图：

1. `output/submit-assets-codex-v2/first-frame-1280.jpg`
2. `output/submit-assets-codex-v2/last-frame-1280.jpg`
3. `output/submit-assets-codex-v2/scene-reference-1280.jpg`

## Dry-run 命令

```bash
python3 scripts/ark_video.py submit \
  --segment stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_01_00-15s \
  --duration 15 \
  --ratio 16:9 \
  --resolution 720p \
  --prompt-file stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_01_00-15s/director-promt.txt \
  --image stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_01_00-15s/frames/first-frame.png \
  --image stories/apocalypse-supermarket/episodes/EP001_open-store-after-apocalypse/segment_01_00-15s/frames/last-frame.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```
