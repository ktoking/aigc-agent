# Segment 01 视频 API 请求

## 任务信息

- Story ID：the-locked-study
- Episode：EP001_the-locked-study
- Segment：segment_01_00-30s
- 时长：30 秒
- 画幅：16:9
- 模型/平台：seedance_2.5（image_to_video）
- 任务状态：待确认（未提交）
- 提交时间：-
- 完成时间：-

## 输入文件

- Prompt：`director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词，逐字直投）
- 参考图（按 API 输入顺序）：
  1. `frames/first-frame.png`：锁定 0 秒桥接画面（庄园门口，Hale 跺雪登场）。
  2. `frames/last-frame.png`：锁定 30 秒收束画面（众人目光汇聚 Hale）与 Seg2 衔接。
  3. `assets/characters/EDWARD_HALE/edward-hale-reference.png`：锁定侦探人脸与服装。
  4. `assets/characters/LADY_ELEANOR/lady-eleanor-reference.png`：锁定贵妇外观。
  5. `assets/characters/ARTHUR_VALE/arthur-vale-reference.png`：锁定关键嫌疑人外观。
- 不上传：storyboard 表格图（避免文字/表格污染）。

## 请求参数

| 参数 | 值 |
| --- | --- |
| model_version | seedance_2.5 |
| task_type | 图生视频（r2v） |
| duration | 30 |
| ratio | 16:9 |
| prompt | director-promt.txt（原文透传） |
| image_reference_url_list | [first-frame.png, last-frame.png, edward-hale-reference.png, lady-eleanor-reference.png, arthur-vale-reference.png] |

## 提交记录

```json
{}
```

## 返回记录

```json
{}
```

## 失败原因与重试策略

- 额度不足 / ModelNotOpen：停止并报告，不自动重试、不换模型。
- 隐私审核拦截：停止，不换错图、不自动重试。
- 生成失败：同参数重试 1 次；连续 2 次失败再调整参考图组合。
- 人脸漂移：强化角色参考图，重新提交。
- 台词口型差：原生音频以环境声为主，关键台词后期配音。
- 完成后：下载视频 → 抽帧检查 → `qa --status passed|rejected` 写入 `output/video-qa.json`，通过后才允许提交 Segment 02。
