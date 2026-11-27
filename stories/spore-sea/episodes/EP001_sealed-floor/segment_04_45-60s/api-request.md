# 第 04 段《失守在往上走》视频 API 交接

| 参数 | 制作计划 |
| --- | --- |
| Story / Episode / Segment | spore-sea / EP001_sealed-floor / segment_04_45-60s |
| 模型 / 时长 / 画幅 / 清晰度 | `doubao-seedance-2-0-mini-260615` / 15 秒 / 9:16 / 720p |
| Prompt | `director-promt.txt` |
| 声音 | 静音样片，配音、动作和环境声后期对齐 |
| 状态 | 未提交，所有参考图待生成 |

## 参考输入顺序

`frames/` 相对本段目录，`assets/` 相对故事根目录。依次传入，图像计划未包含带字分镜表。

1. `frames/first-frame.png`，标签「首帧」。段内约0秒。锁定起始状态和机位。
2. `frames/keyframe-infected-on-monitor.png`，标签「段内关键帧」。段内约9秒。锁定《值班屏里带菌者往上爬》。
3. `frames/last-frame.png`，标签「尾帧」。段内约14.8秒。锁定结束状态和承接。
4. `assets/characters/jiang-jin-unmasked-reference.png`，标签「江烬素脸」。锁定同一侧眉、发型与服装，右腕蓝带未扣。
5. `assets/scenes/f29-status-desk-reference.png`，标签「29层值班台」。锁定铺位旁执勤板、回放屏和独立未锁的楼层牌槽位置。

## Dry-run

从仓库根目录运行。准备好上述已选定的参考图后核对请求，再按生产安排提交。

```zsh
spore_segment='stories/spore-sea/episodes/EP001_sealed-floor/segment_04_45-60s'
python3 scripts/ark_video.py submit \
  --segment "$spore_segment" --prompt-file "$spore_segment/director-promt.txt" \
  --model 'doubao-seedance-2-0-mini-260615' --duration 15 --ratio 9:16 --resolution 720p \
  --no-auto-images --require-images \
  --image "$spore_segment/frames/first-frame.png" --image-label '首帧' \
  --image "$spore_segment/frames/keyframe-infected-on-monitor.png" --image-label '段内关键帧' \
  --image "$spore_segment/frames/last-frame.png" --image-label '尾帧' \
  --image 'stories/spore-sea/assets/characters/jiang-jin-unmasked-reference.png' --image-label '江烬素脸' \
  --image 'stories/spore-sea/assets/scenes/f29-status-desk-reference.png' --image-label '29层值班台' --dry-run
```

实际回执随后记入本段 `output/`。若监控人物跑进真实驻地，补拍小屏画面和边框。真实空间、录制位置和楼层字贴分开。
