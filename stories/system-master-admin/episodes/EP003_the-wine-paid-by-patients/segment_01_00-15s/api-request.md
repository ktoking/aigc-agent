# Segment 01 视频 API 请求

## 任务信息

- Story ID：system-master-admin
- Episode：EP003_the-wine-paid-by-patients
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：not_submitted

## 输入文件

- 首帧：`frames/first-frame.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`
- 参考图：顾沉 canonical、赵天麟 canonical、酒箱 canonical、回收站 canonical

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

- 赵天麟若被生成实体，强化“只在卡中半身通讯影像”；倒计时乱码时只保留圆环与数字20。
