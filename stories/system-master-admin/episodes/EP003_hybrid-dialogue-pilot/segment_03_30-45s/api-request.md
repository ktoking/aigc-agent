# Segment 03 视频 API 请求（文本试验版）

## 任务信息

- Story ID：`system-master-admin`
- Episode：`EP003_hybrid-dialogue-pilot`
- Segment：`03`
- 时长：15 秒
- 画幅：9:16
- 模型/平台：Seedance 2.0 mini / Ark（后续提交）
- 分辨率：480p 草稿
- 声音：需要，顾沉内心对白后续独立 TTS 优先
- 任务状态：未提交

## 参考图上传计划

1. `frames/first-frame.png`：承接掌纹读取和管理员背影。
2. `frames/last-frame.png`：锁定签发节点入眼、终端恢复和顾沉离场。
3. `../../../assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png`：锁定顾沉。
4. `../../../assets/scenes/SCENE_AWAKENING_HALL_001/canonical-concept.png`：锁定礼堂后台。

终端和管理员只按道具卡、背影和文字提示生成；不上传未确认的人脸或大段文字截图。不上传分镜表格图。

## 请求参数

| 参数 | 值 |
| --- | --- |
| model | `doubao-seedance-2-0-mini-260615` |
| aspect_ratio | `9:16` |
| duration | `15` |
| resolution | `480p` |
| generate_audio | `true` |
| prompt | `director-promt.txt` |

## 提交记录

文本试验阶段未提交。
