# Segment 02 视频 API 请求

## 任务信息

- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_02_15-30s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9
- 模型/平台：未选择
- 任务状态：未提交
- Task ID：无

## 输入文件

- Prompt：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_02_15-30s/director-promt.txt`
- 参考图1：`frames/first-frame.png`，骨针与腕锁
- 参考图2：`frames/shot-02.png`，帘缝祭坛山道
- 参考图3：`frames/last-frame.png`，韩枭拔刀与三人站位
- 角色锚点：沈烬 `DPE_SHEN_JIN_001`、阿璃 `DPE_A_LI_001`、韩枭 `DPE_HAN_XIAO_001`

## 推荐参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15；若对白未说完则以完整语音时长为准 |
| resolution | 720p draft |
| generate_audio | True |
| return_last_frame | True |
| motion_strength | low-medium |
| virtual_person_notice | True |

## 提交记录

- 未产生请求 payload、任务 ID、返回 URL 或计费记录。

## 失败原因与重试策略

- 若骨针手指变形，缩短开锁动作并采用微距静帧加局部旋转。
- 若人物翻轴，重新固定沈烬中央、阿璃左后、韩枭门口。
- 若真人隐私规则拦截，明确三人为原创成年半写实 3D 角色后有限重试一次。
