# 第 08 段《上行与藤蔓者》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_08_105-120s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-vineframe.png`，标签「段内关键帧」。段内约10秒。锁定《格栅被顶弯，肩袖露出》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/characters/vineform-reference.png`，标签「藤蔓者」。锁定人体比例、两三根藤和灰蓝衣袖。
5. `assets/scenes/f23-gate-reference.png`，标签「23层闸口」。锁定格栅、上行短梯、扫描侧与闸门横梁。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_08_105-120s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-vineframe.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/vineform-reference.png' --image-label '藤蔓者' \
  --image 'stories/spore-sea/assets/scenes/f23-gate-reference.png' --image-label '23层闸口' --dry-run
```

实际回执随后记入本段 `output/`。怪物或住户数漂移时拆受力格栅和撤离出口镜头，保留走廊同一动线和手部接触。
