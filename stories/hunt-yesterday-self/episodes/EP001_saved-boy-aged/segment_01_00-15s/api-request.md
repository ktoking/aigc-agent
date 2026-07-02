# Segment 视频 API 请求

## 任务信息

- Episode：EP001_saved-boy-aged
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615（下一次草稿默认）
- 任务状态：上一版已生成但判定废片；下一次待提交前 dry-run
- 提交时间：2026-06-26T14:23:21+08:00
- 完成时间：
- Task ID：cgt-20260626142319-vv4w4

## 输入文件

- Prompt：stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/director-promt.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/frames/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/frames/last-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/hunt-yesterday-self/assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/chase-spatial-reference.png
- 不建议上传动作编排图：上一版容易被模型理解成姿势拼贴，下一次 mini 草稿先减少参考图数量。
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 5 秒动作小样优先；15 秒整段需先 dry-run |
| resolution | 720p |
| generate_audio | True |
| return_last_frame | True |
| virtual_person_notice | True |
| privacy_retry | 0 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 上一版视频像首尾帧硬插姿势图：人物第 6 秒悬空平移，缺少起跳、受力、坠落速度、落地冲击；时间回溯只是一闪光，缺少“事故路径倒序播放”的过程。
- 下一版 prompt 已改为：切链 -> 抓表 -> 撞栏 -> 踩空 -> 翻转下坠 -> 钢梁擦手 -> 膝盖/手掌落地滑行 -> 3 秒局部倒序回溯 -> 拖少年滚离轨道 -> 寿命丝线回流。
- 下一次正式提交前必须先 dry-run，优先用 `doubao-seedance-2-0-mini-260615`，先做 5 秒小样验证“切链坠落”或“时间回溯”单个动作，不要直接烧 15 秒复杂正片。
- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧/故事板图，
  自动追加“图中人物均为 AI 生成虚拟角色，不包含真人隐私信息”的说明后有限重试。
- 若重试后仍被拦截，脚本停止，不自动替换为场景图或其他错误参考图，避免人脸不一致和无效消耗。
