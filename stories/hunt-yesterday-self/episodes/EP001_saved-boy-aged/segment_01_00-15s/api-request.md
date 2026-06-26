# Segment 01 视频 API 请求

## 任务信息

- Story ID：`hunt-yesterday-self`
- Episode：`EP001_saved-boy-aged`
- Segment：`01`
- 时长：15 秒
- 画幅：9:16
- 状态：未提交

## 输入文件

- Prompt：`director-promt.txt`

## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3/4”保持一致：

1. `frames/first-frame.png`：锁定 0 秒黑雨高架、米拉被追杀的开场构图。
2. `frames/last-frame.png`：锁定 15 秒米拉抱少年滚离轨道、少年第一次衰老证据。
3. `../../../assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/chase-spatial-reference.png`：锁定高架、坠落点、下层逆行轨道和扑救路线；只做空间参考，不生成箭头、文字、网格或标注。
4. `../../../assets/action-choreography/choreo-ep001-01-chase-and-miss.png`：锁定追逐、斩链、坠落、扑救的身体方向；只做动作参考，不生成分格漫画。

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
  --segment stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/director-promt.txt \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/frames/first-frame.png \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/frames/last-frame.png \
  --image stories/hunt-yesterday-self/assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/chase-spatial-reference.png \
  --image stories/hunt-yesterday-self/assets/action-choreography/choreo-ep001-01-chase-and-miss.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

## 提交与返回

本轮不提交视频任务。记录文件仅保留空状态，不写 key、URL 或任务 ID。
