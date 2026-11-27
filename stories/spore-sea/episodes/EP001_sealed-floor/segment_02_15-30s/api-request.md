# 第 02 段《往上，就是身份》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_02_15-30s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-upper-white-band.png`，标签「段内关键帧」。段内约7.5秒。锁定《白腕带过门、锈红腕带改道》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/scenes/top-greenhouse-reference.png`，标签「云顶花园」。锁定 500 层穹顶、真百合、茶桌、画右竖柱及墙牌空面。
5. `assets/scenes/tower4-vertical-reference.png`，标签「楼层竖轴」。锁定四号塔右柱、楼板截面、320 层电梯区、210 层农场顺序。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_02_15-30s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-upper-white-band.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/scenes/top-greenhouse-reference.png' --image-label '云顶花园' \
  --image 'stories/spore-sea/assets/scenes/tower4-vertical-reference.png' --image-label '楼层竖轴' --dry-run
```

实际回执随后记入本段 `output/`。若楼板形状变化，按同一柱子和下降速度检查两处遮挡。分别固定金、白、蓝腕带颜色，保留桌、门、农架同层位置。
