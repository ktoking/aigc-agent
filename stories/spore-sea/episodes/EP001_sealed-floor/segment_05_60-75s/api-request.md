# 第 05 段《蓝腕带与下行货梯》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_05_60-75s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-blue-band-egg.png`，标签「段内关键帧」。段内约4.5秒。锁定《蓝腕带和留给小满家的蛋》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/characters/jiang-jin-unmasked-reference.png`，标签「江烬素脸」。锁定江烬的右眉、作业服和右腕蓝带。
5. `assets/characters/a-gui-unmasked-reference.png`，标签「阿鬼素脸」。锁定寸头、宽颧、深蓝灰作业服及面罩挂的位置。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_05_60-75s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-blue-band-egg.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/jiang-jin-unmasked-reference.png' --image-label '江烬素脸' \
  --image 'stories/spore-sea/assets/characters/a-gui-unmasked-reference.png' --image-label '阿鬼素脸' --dry-run
```

实际回执随后记入本段 `output/`。蓝带对应旧红痕的镜头用独立手部参考。电梯门与人物位置保持画面同侧，不旋转梯厢。
