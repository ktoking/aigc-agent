# 第 01 段《门缝》视频 API 请求

| 参数 | 规划值 |
| --- | --- |
| Story / Episode | spore-sea / EP001_floor-47 |
| Segment | segment_01_00-15s |
| 草稿模型 | `doubao-seedance-2-0-mini-260615` |
| duration / ratio / resolution | 15s / 9:16 / 720p |
| prompt / include_storyboard | `director-promt.txt` / false |
| generate_audio | false，另做配音与音效 |
| 状态 | 未提交，待生成参考图 |

## 输入图顺序

1. `frames/first-frame.png`，标签「首帧」，本段开场与站位。
2. `frames/last-frame.png`，标签「尾帧」，本段收束与接点。
3. `assets/characters/BRANCHBOUND_001/reference.png`（相对 story 根目录），标签「枝甲人」。只限定一只枝甲人的灰袖、三根木指和腕部剪影。

## Dry-run

从仓库根目录运行，需先按图像计划准备三个已选定的输入文件。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_floor-47/segment_01_00-15s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model doubao-seedance-2-0-mini-260615 --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/BRANCHBOUND_001/reference.png' --image-label '枝甲人' --dry-run
```

## 回执与重试

提交和完成时间待填写。回执按工具实际输出写入本段 `output/`。
若钩子不清楚，重做门与腕枝镜头，固定门缝方向和三根木指。若塔群不够可读，先补外景镜头再回切同一走廊，不挪动闸门。
