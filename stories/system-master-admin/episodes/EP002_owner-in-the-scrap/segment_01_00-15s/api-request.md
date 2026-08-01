# Segment 01 视频 API 请求

## 任务信息

- Story ID：system-master-admin
- Episode：EP002_owner-in-the-scrap
- Segment：segment_01_00-15s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：not_submitted
- 提交时间：
- 完成时间：

## 输入文件

- 首帧：`frames/first-frame.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`
- 参考图：顾小满 canonical、顾沉 canonical、低权限病房 canonical、回收站 canonical

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 9:16 |
| duration | 15 |
| resolution | 480p |
| generate_audio | True |
| return_last_frame | True |

## 提交记录

```json
{}
```

## 返回记录

```json
{}
```

## 重试策略

- 黑发妹妹漂移时增强顾小满 canonical 权重；病房跳变时仅保留首尾帧、病房和回收站两张场景图。
