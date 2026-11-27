# 第 07 段《23层警报》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_07_90-105s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-mask-latch.png`，标签「段内关键帧」。段内约9.5秒。锁定《江烬合罩，眉眼留在光下》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/characters/jiang-jin-masked-reference.png`，标签「江烬带罩」。只锁面罩、右眉和同人眉眼。
5. `assets/characters/a-gui-masked-reference.png`，标签「阿鬼带罩」。锁定深蓝灰身形和右上护目片细斜划痕。
6. `assets/scenes/f23-gate-reference.png`，标签「23层闸口」。固定楼梯、临时开启的闸和高低侧。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_07_90-105s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-mask-latch.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/jiang-jin-masked-reference.png' --image-label '江烬带罩' \
  --image 'stories/spore-sea/assets/characters/a-gui-masked-reference.png' --image-label '阿鬼带罩' \
  --image 'stories/spore-sea/assets/scenes/f23-gate-reference.png' --image-label '23层闸口' --dry-run
```

实际回执随后记入本段 `output/`。先验证戴罩动作前后眼睛位置对得上。警灯只扫墙不取代所有环境光，腕带显示交给后期。
