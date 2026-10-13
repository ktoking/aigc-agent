# Segment 03 视频 API 请求

## 任务信息

- Story ID：the-locked-study
- Episode：EP001_the-locked-study
- Segment：segment_03_60-90s
- 时长：30 秒
- 画幅：16:9
- 模型/平台：seedance_2.5（image_to_video）
- 任务状态：待确认（未提交）
- 提交时间：-
- 完成时间：-

## 输入文件

- Prompt：`director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词，逐字直投）
- 参考图（按 API 输入顺序）：
  1. `frames/first-frame.png`：锁定 0 秒桥接画面（落地钟敲响，房间静止）。
  2. `frames/last-frame.png`：锁定 30 秒收束画面（Hale 停在书房门口，众人跟随）与 Seg4 衔接。
  3. `assets/characters/EDWARD_HALE/edward-hale-reference.png`：锁定侦探外观。
  4. `assets/characters/ARTHUR_VALE/arthur-vale-reference.png`：锁定关键嫌疑人外观（微笑裂纹）。
  5. `assets/characters/CLARA_VALE/clara-vale-reference.png`：锁定 Clara 外观（本段紧张行为）。
- 不上传：storyboard 表格图。

## 请求参数

| 参数 | 值 |
| --- | --- |
| model_version | seedance_2.5 |
| task_type | 图生视频（r2v） |
| duration | 30 |
| ratio | 16:9 |
| prompt | director-promt.txt（原文透传） |
| image_reference_url_list | [first-frame.png, last-frame.png, edward-hale-reference.png, arthur-vale-reference.png, clara-vale-reference.png] |

## 提交记录

```json
{}
```

## 返回记录

```json
{}
```

## 失败原因与重试策略

- 前置门禁：Segment 02 的 `output/video-qa.json` 必须为 passed 才允许提交本段。
- 额度不足 / ModelNotOpen：停止并报告，不自动重试、不换模型。
- 隐私审核拦截：停止，不换错图、不自动重试。
- 生成失败：同参数重试 1 次；连续 2 次失败再调整参考图组合。
- 人脸漂移：强化角色参考图，重新提交。
- 完成：下载 → 抽帧检查 → `qa --status passed|rejected`，通过后才允许提交 Segment 04。
