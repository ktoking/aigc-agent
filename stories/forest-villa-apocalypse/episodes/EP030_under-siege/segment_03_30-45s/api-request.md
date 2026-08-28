# Segment 视频 API 请求

## 任务信息

- Episode：EP030
- Segment：segment_03_30-45s
- 时长：15
- 画幅：16:9
- 模型/平台：doubao-seedance-2-0-mini-260615
- 任务状态：pending
- 提交时间：
- 完成时间：
- Task ID：

## 输入文件

- Prompt：director-promt.txt
- 数字人资产（作为 image_url 提交）：
  - 许砚：`asset://asset-20260320075237-29hdx`
  - 白棠：`asset://asset-20260320075131-k78qt`
  - 沈知夏：`asset://asset-20260310030618-88hlb`
- 本地参考图：待提交前确认场景/道具参考图路径

## 请求参数

| 参数 | 值 |
| --- | --- |
| ratio | 16:9 |
| duration | 15 |
| resolution | 480p |
| generate_audio | True |
| return_last_frame | True |
| virtual_person_notice | True |
| privacy_retry | 0 |

## 提交记录

详见 `output/api-submit.json`。

## 返回记录

详见 `output/api-result.json`。

## 失败原因与重试策略

- 若火山返回隐私拦截，脚本保留原参考图，追加虚拟角色说明后有限重试。
- 若重试后仍被拦截，停止，不自动替换参考图。
