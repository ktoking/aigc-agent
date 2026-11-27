# 第 03 段《29层的清层队》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_03_30-45s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-red-band-relocation.png`，标签「段内关键帧」。段内约4秒。锁定《抱着铺盖等安置的人》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/scenes/tower4-vertical-reference.png`，标签「楼层竖轴」。锁定农场下方服务井、下层安置走廊和 29 层驻地。
5. `assets/characters/jiang-jin-unmasked-reference.png`，标签「江烬素脸」。锁定江烬黑短发、稍瘦脸形、右眉微断与石墨服。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_03_30-45s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-red-band-relocation.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/scenes/tower4-vertical-reference.png' --image-label '楼层竖轴' \
  --image 'stories/spore-sea/assets/characters/jiang-jin-unmasked-reference.png' --image-label '江烬素脸' --dry-run
```

实际回执随后记入本段 `output/`。若镜位停不住，降到 29 层暗梁后再减速，给男主脸至少一段稳定近景。
