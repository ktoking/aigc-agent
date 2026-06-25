# Segment 视频 API 请求

## 任务信息

- Episode：
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-fast-260128
- 任务状态：submitted
- 提交时间：2026-06-17T21:01:20+08:00
- 完成时间：
- Task ID：cgt-20260617210108-4rxmc

## 输入文件

- Prompt：/tmp/aigc-uploaded-template-v1/video_prompt_retry.txt
- 本地参考图：
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s/frames/style_3d_uploaded_template/clean/character-turnaround.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s/frames/style_3d_uploaded_template/clean/first-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s/frames/style_3d_uploaded_template/clean/last-frame.png
- /Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s/frames/style_3d_uploaded_template/storyboard-table.png
- 平台信任参考图 URL：
- 无

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 720p |
| generate_audio | False |
| return_last_frame | True |
| virtual_person_notice | True |
| privacy_retry | 0 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧/故事板图，
  自动追加“图中人物均为 AI 生成虚拟角色，不包含真人隐私信息”的说明后有限重试。
- 若重试后仍被拦截，脚本停止，不自动替换为场景图或其他错误参考图，避免人脸不一致和无效消耗。
