# Segment 03 视频 API 请求

## 任务信息

- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_03_30-45s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9
- 模型/平台：未选择
- 任务状态：未提交
- Task ID：无

## 输入文件

- Prompt：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_03_30-45s/director-promt.txt`
- 参考图1：`frames/first-frame.png`，刀锋与三人轴线
- 参考图2：`frames/shot-02.png`，放箭方向与沈烬抬眼
- 参考图3：`frames/last-frame.png`，箭、雨、刀同时凝固
- 角色锚点：沈烬 `DPE_SHEN_JIN_001`、阿璃 `DPE_A_LI_001`、韩枭 `DPE_HAN_XIAO_001`

## 推荐验证参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 先做 5 秒无付费动作验证候选；正式段以完整语音为准 |
| resolution | 480p draft |
| generate_audio | True |
| return_last_frame | True |
| motion_strength | medium |
| virtual_person_notice | True |

## 提交记录

- 本轮明确不提交视频任务。
- 未产生请求 payload、任务 ID、返回 URL 或费用。

## 失败原因与重试策略

- 箭向错误时固定箭从后方右侧进入，禁止箭逆向。
- 凝固不同步时删去次要动作，只保留“放箭—说停—刀箭雨同时停”。
- 若特效像游戏，移除粒子，只保留雨滴、透明折射和瞳内微光。
