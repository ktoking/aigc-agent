# 第 01 段《灰雨之后》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_01_00-15s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-rooftop-islands.png`，标签「段内关键帧」。段内约7.5秒。锁定《荧光孢海刚淹到屋檐》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/scenes/gray-rain-street-reference.png`，标签「灰雨旧城」。锁定同一条旧街断开高架、外露折梯和消防屋顶相对位置。
5. `assets/scenes/seven-towers-reference.png`，标签「七塔外景」。锁定四号塔及其他六座塔的层次、廊桥与五百层高度感。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_01_00-15s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-rooftop-islands.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/scenes/gray-rain-street-reference.png' --image-label '灰雨旧城' \
  --image 'stories/spore-sea/assets/scenes/seven-towers-reference.png' --image-label '七塔外景' --dry-run
```

实际回执随后记入本段 `output/`。若追扑抢掉撤离动线，保留街柱与楼梯脚的远处接触，让镜头跟幸存者向上。近云遮满画面时完成十七年的过渡，保留原视轴和升势。检查七座塔都有独立冠部。
