# Segment 02 视频 API 请求

## 任务信息

- Story ID：system-master-admin
- Episode：EP002_owner-in-the-scrap
- Segment：segment_02_15-30s
- 时长：15
- 画幅：9:16
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：not_submitted

## 输入文件

- 首帧：`frames/first-frame.png`
- 尾帧：`frames/last-frame.png`
- Prompt：`director-promt.txt`
- 参考图：顾沉 canonical、回收站 canonical、废核心 canonical

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

- 主管脸抢戏时裁掉头部；核心比例漂移时提高道具图权重并删除多余环境参考。
