# Segment 01 视频 API 请求

## 任务信息

- Episode：`EP001_a-word-stops-the-arrows`
- Segment：`segment_01_00-15s`
- 时长：约 15 秒，以完整台词为准
- 画幅：16:9
- 模型/平台：未选择
- 任务状态：未提交
- Task ID：无

## 输入文件

- Prompt：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_01_00-15s/director-promt.txt`
- 参考图1：`frames/first-frame.png`，雾谷囚车外景
- 参考图2：`frames/shot-02.png`，囚车内部与两人服装
- 参考图3：`frames/last-frame.png`，沈烬睁眼与门帘人影
- 角色锚点：沈烬 `DPE_SHEN_JIN_001`、阿璃 `DPE_A_LI_001`

## 推荐参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15；若对白未说完则以完整语音时长为准 |
| resolution | 720p draft |
| generate_audio | True |
| return_last_frame | True |
| motion_strength | low |
| virtual_person_notice | True |

## 提交记录

- 未产生请求 payload、任务 ID、返回 URL 或计费记录。

## 失败原因与重试策略

- 若虚构人物被隐私规则拦截，只追加“原创成年半写实 3D 动画角色，不对应现实人物”，有限重试一次。
- 若人脸漂移，只重试人物近景并同时引用定妆图与三视图。
- 若门帘人影出现清晰五官，强化 `silhouette behind curtain only`。
