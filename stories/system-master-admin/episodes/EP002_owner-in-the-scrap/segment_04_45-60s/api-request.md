# Segment 04 视频 API 请求

## 任务信息

- Story ID：system-master-admin
- Episode：EP002_owner-in-the-scrap
- Segment：segment_04_45-60s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：not_submitted

## 输入文件

- 首帧：`frames/first-frame.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`
- 参考图：顾沉 canonical、废核心 canonical、回收站 canonical

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

- 权限数字错误时改用终端语音表达；结尾人员脸过清时压暗前景并保持剪影。
