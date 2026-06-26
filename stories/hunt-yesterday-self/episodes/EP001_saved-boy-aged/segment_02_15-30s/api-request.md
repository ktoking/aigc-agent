# Segment 02 视频 API 请求

## 任务信息

- Story ID：`hunt-yesterday-self`
- Episode：`EP001_saved-boy-aged`
- Segment：`02`
- 时长：15 秒
- 画幅：9:16
- 状态：未提交

## 输入文件

- Prompt：`director-promt.txt`
- 输入策略：本段 `frames/first-frame.png` 与 Segment 01 验收尾帧为同一文件内容。
- 生成策略：优先保持上一段成片末尾连续性，重点压住“残余连接不是持续吸寿”。

## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3/4”保持一致：

1. `frames/first-frame.png`：锁定 0 秒桥接画面，承接 Segment 01 尾帧。
2. `frames/last-frame.png`：锁定 15 秒猎手切断残余寿命连接、米拉半蹲护表护少年。
3. `../../../assets/characters/HYS_BOY_001/02-age-progression/boy-age-progression.png`：锁定少年第一次按表后的白发/皱纹状态，不让本段继续老化或恢复年轻。
4. `../../../assets/props/prop-scale-reference.png`：锁定第七块怀表、时间刃、红围巾和手部比例；只做比例参考，不生成文字、图解线或标注。

不上传：`frames/storyboard-sheet.png`。故事板表格只做人类审阅，避免文字/表格污染和静态拉图。

## 请求参数

| 参数 | 值 |
| --- | --- |
| aspect_ratio | 9:16 |
| duration | 15 |
| resolution | 720p |
| prompt | director-promt.txt |
| auto_images | 首帧 + 尾帧 |
| include_storyboard | false |

## 推荐 dry-run 命令

```bash
python3 scripts/ark_video.py submit \
  --segment stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_02_15-30s \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_02_15-30s/director-promt.txt \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_02_15-30s/frames/first-frame.png \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_02_15-30s/frames/last-frame.png \
  --image stories/hunt-yesterday-self/assets/characters/HYS_BOY_001/02-age-progression/boy-age-progression.png \
  --image stories/hunt-yesterday-self/assets/props/prop-scale-reference.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

## 提交与返回

本轮不提交视频任务，不记录 key、URL、任务 ID 或返回 JSON。
