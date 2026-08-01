# Segment 02 视频 API 请求

## 任务信息

- Story ID：system-master-admin
- Episode：EP003_the-wine-paid-by-patients
- Segment：segment_02_15-30s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：not_submitted

## 输入文件

- 首帧：`frames/first-frame.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`
- 参考图：顾沉 canonical、酒箱 canonical、宴会后勤走廊 canonical

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 480p |
| generate_audio | True |
| return_last_frame | True |

## 提交与返回

```json
{}
```

## 重试策略

- 酒箱落地时缩短保安动作并强化全程抱持；场景跳到宴会厅时提高后勤走廊参考权重。
