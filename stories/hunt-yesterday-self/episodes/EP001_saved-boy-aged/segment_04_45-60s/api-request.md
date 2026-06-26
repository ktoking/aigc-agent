# Segment 04 视频 API 请求

## 任务信息

- Story ID：`hunt-yesterday-self`
- Episode：`EP001_saved-boy-aged`
- Segment：`04`
- 时长：15 秒
- 画幅：9:16
- 状态：未提交

## 输入文件

- Prompt：`director-promt.txt`
- 输入策略：本段 `frames/first-frame.png` 与 Segment 03 验收尾帧为同一文件内容。
- 生成策略：反转段优先压住“猎手就是未来米拉”的视觉证据和“六块旧表 + 第七块碎表”的数量关系。

## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3/4/5”保持一致：

1. `frames/first-frame.png`：锁定 0 秒桥接画面，承接 Segment 03 尾帧。
2. `frames/last-frame.png`：锁定 15 秒六块旧表和脚边第七块碎表芯重新跳动。
3. `../../../assets/characters/HYS_HUNTER_001/01-face-reference/hunter-mask-face-reference.png`：锁定猎手破裂面具、苍老半脸、冷青右眼和旧铜耳坠。
4. `../../../assets/characters/HYS_MIRA_001/01-face-reference/mira-face-reference.png`：锁定米拉与猎手同眼、同耳坠、同左手护表姿势的视觉证据。
5. `../../../assets/props/prop-scale-reference.png`：锁定第七块碎表、六块旧表、时间刃的比例和数量；只做比例参考，不生成文字、图解线或标注。

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
  --segment stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_04_45-60s \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_04_45-60s/director-promt.txt \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_04_45-60s/frames/first-frame.png \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_04_45-60s/frames/last-frame.png \
  --image stories/hunt-yesterday-self/assets/characters/HYS_HUNTER_001/01-face-reference/hunter-mask-face-reference.png \
  --image stories/hunt-yesterday-self/assets/characters/HYS_MIRA_001/01-face-reference/mira-face-reference.png \
  --image stories/hunt-yesterday-self/assets/props/prop-scale-reference.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

## 提交与返回

本轮不提交视频任务，不记录 key、URL、任务 ID 或返回 JSON。
