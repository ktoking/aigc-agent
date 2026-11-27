# 第 06 段《小满的纸百合》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_06_75-90s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-paper-lily-question.png`，标签「段内关键帧」。段内约9秒。锁定《真正的花和折纸花》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/characters/xiao-man-reference.png`，标签「小满」。锁定发夹、外套、左腕锈红带和白纸花尺寸。
5. `assets/characters/jiang-jin-unmasked-reference.png`，标签「江烬素脸」。锁定江烬素脸及左臂臂章的附着位置。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_06_75-90s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-paper-lily-question.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/xiao-man-reference.png' --image-label '小满' \
  --image 'stories/spore-sea/assets/characters/jiang-jin-unmasked-reference.png' --image-label '江烬素脸' --dry-run
```

实际回执随后记入本段 `output/`。孩子脸和手花漂移时先补受保护的双人近景。湿痕只留在门边，花最终插在江烬左臂。
