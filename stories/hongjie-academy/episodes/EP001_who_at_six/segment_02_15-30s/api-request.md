# 橘日奈｜视频生成记录

| 字段 | 计划 |
| --- | --- |
| 版本 | galgame-v4，导演稿和三张锚点就绪 |
| 模型 | Ark Seedance 2.0 Mini 草稿入口，`doubao-seedance-2-0-mini-260615` |
| 画幅 / 时长 / 分辨率 | 9:16 / 15 秒 / 720p 草稿 |
| 声音 | 原生普通话对白及轻环境声，时点为表演估时 |
| 图 1 · 开场首帧 | [人物、开场和机位](frames/first-frame.png) |
| 图 2 · 表演转折 | [中段躯干动作](frames/mid-frame.png) |
| 图 3 · 终态尾帧 | [末段动作与表情](frames/last-frame.png) |
| 导入位置 | `output/video.mp4` |
| 任务 ID、实际时长 | 待生成后记录 |

## 三图本地预检

三张图按上述顺序传。图 2 和图 3 是动作锚点，实际时点以动态结果验收为准。在仓库根执行。

```bash
SEG=stories/hongjie-academy/episodes/EP001_who_at_six/segment_02_15-30s
python3 scripts/ark_video.py submit --segment "$SEG" --model doubao-seedance-2-0-mini-260615 --no-auto-images \
  --prompt-file "$SEG/director-promt.txt" \
  --image "$SEG/frames/first-frame.png" --image-label "开场首帧" \
  --image "$SEG/frames/mid-frame.png" --image-label "表演转折" \
  --image "$SEG/frames/last-frame.png" --image-label "终态尾帧" \
  --require-images --duration 15 --ratio 9:16 --resolution 720p --generate-audio --return-last-frame --dry-run
```

## 验收和补跑

从始至终使用日奈左手，位置在画面右下。上臂留在肩下，肘的弯伸带动手。撤回时手掌在腰带上方、衣服前面；再递时手掌逐渐转朝上，手腕与袖口连续可见。与男主不接触。另一手留在画外。
以固定背景为参照，看 1 倍速播放时肩线、腰线和画面落点是否真的变化，确认起势、到位和收尾连贯。核对完整台词与闭唇反应。交接上一轮结果时记录实际时长、剪辑入出点和任务 ID，只补偏差段。
