# Segment 04 视频 API 请求

## 任务信息

- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_04_45-60s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9
- 模型/平台：未选择
- 任务状态：未提交
- Task ID：无

## 输入文件

- Prompt：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_04_45-60s/director-promt.txt`
- 参考图1：`frames/first-frame.png`，穿过凝固箭雨
- 参考图2：`frames/shot-02.png`，反噬血线、落箭和韩枭跪姿
- 参考图3：`frames/last-frame.png`，阿璃正常人脸与妖王雾影
- 角色锚点：沈烬 `DPE_SHEN_JIN_001`、阿璃 `DPE_A_LI_001`、韩枭 `DPE_HAN_XIAO_001`

## 推荐参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15；若对白未说完则以完整语音时长为准 |
| resolution | 480p draft |
| generate_audio | True |
| return_last_frame | True |
| motion_strength | low-medium |
| virtual_person_notice | True |

## 提交记录

- 本轮明确不提交视频任务。
- 未产生请求 payload、任务 ID、返回 URL 或费用。

## 失败原因与重试策略

- 牵手变形时减少手部运动，用遮挡切到已握住状态。
- 落箭必须落在安全通道两侧或沿原方向飞过，禁止追踪人物。
- 阿璃本人若被妖化，强化 `normal human face`，妖王只作为山谷雾影。
