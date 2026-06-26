# Segment 03 视频 API 请求

## 任务信息

- Story ID：`hunt-yesterday-self`
- Episode：`EP001_saved-boy-aged`
- Segment：`03`
- 时长：15 秒
- 画幅：9:16
- 状态：未提交

## 输入文件

- Prompt：`director-promt.txt`
- 输入策略：本段 `frames/first-frame.png` 与 Segment 02 验收尾帧为同一文件内容。
- 生成策略：这段是动作与规则最复杂的一段，参考图数量提高到 5 张，用于压住“护表反制、击飞怀表、少年二次跃迁、猎手动作克制”。

## 参考图上传计划

按以下顺序传给 API，并与 `director-promt.txt` 内“参考图1/2/3/4/5”保持一致：

1. `frames/first-frame.png`：锁定 0 秒桥接画面，承接 Segment 02 尾帧。
2. `frames/last-frame.png`：锁定 15 秒猎手面具右侧破裂、同眼同耳坠的身份线索。
3. `../../../assets/action-choreography/choreo-ep001-02-watch-defense.png`：锁定米拉护表、猎手击飞怀表、双方身体方向；只做动作调度参考，不生成分格漫画。
4. `../../../assets/characters/HYS_HUNTER_001/05-action-poses/hunter-action-poses.png`：锁定猎手克制、精准、刀锋避开身体的动作语汇。
5. `../../../assets/characters/HYS_BOY_001/02-age-progression/boy-age-progression.png`：锁定第二次按表瞬间少年从白发状态跃迁为佝偻老人，不能提前持续老化。

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
  --segment stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_03_30-45s \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --prompt-file stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_03_30-45s/director-promt.txt \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_03_30-45s/frames/first-frame.png \
  --image stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_03_30-45s/frames/last-frame.png \
  --image stories/hunt-yesterday-self/assets/action-choreography/choreo-ep001-02-watch-defense.png \
  --image stories/hunt-yesterday-self/assets/characters/HYS_HUNTER_001/05-action-poses/hunter-action-poses.png \
  --image stories/hunt-yesterday-self/assets/characters/HYS_BOY_001/02-age-progression/boy-age-progression.png \
  --generate-audio \
  --privacy-retry 0 \
  --dry-run
```

## 提交与返回

本轮不提交视频任务，不记录 key、URL、任务 ID 或返回 JSON。
