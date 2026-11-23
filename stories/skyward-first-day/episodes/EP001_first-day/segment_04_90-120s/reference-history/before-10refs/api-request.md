# Segment 04 生成交接单｜v2

状态：NOT_SUBMITTED；剧本：skyward-first-day/EP001_first-day；本导演段全片90—120秒，目标30秒/900帧，16:9。用户本轮明确指定30秒分段，覆盖通用15秒导演段格式。

| 项目 | 计划 |
| --- | --- |
| 生成提示词 | director-promt.txt，完整30秒导演段 |
| 草稿风格/清晰度 | 非真人3D动漫，720p |
| 仓库草稿默认模型 | doubao-seedance-2-0-mini-260615 |
| 当前平台单任务30秒能力 | 未验证；此处只记录导演段目标，不伪称已支持 |
| 提交时间/任务ID/费用/返回 | 无；未调用API |

本轮仅交文字。后续以真实平台支持的单任务时长落地；若平台需要拆任务，则按本30秒导演段内部镜头边界生成后拼回30秒，导演段仍保留用户指定的4×30秒结构。seed、guidance、motion_strength未指定，不虚构平台字段。

## 拟参考图顺序

| 顺序 | 路径 | 职责 | 状态 |
| --- | --- | --- | --- |
| 1 | frames/first-frame.png | 仅锁本段0秒起始构图、人物位置与道具初始状态 | missing |
| 2 | frames/last-frame.png | 仅锁本段30秒收束状态、空间与下段接点，不能用首尾直接变形省掉中间事件 | missing |
| 3 | frames/ref-classroom-cast.png | 只锁回现实后的林桃、许星、顾岩和旧机；历史模型中不加入这些现实角色实体 | missing |
| 4 | frames/ref-history-world.png | 锁远古环门、核心、研究台、城市指令链与重建沙盘的统一3D形态 | missing |
| 5 | frames/ref-classroom-layout.png | 锁真实教室第二排、过道、教学罩和电源台，确保女主末尾正常步行到台前 | missing |

真实图片尚缺；将正确图复制进本段frames后才可使用带图请求。不得上传带文字的故事板表格。图号与实际API输入顺序要一致，参考卡标注不进成片。不能把计划路径当现成图片。

## 验收与重试

先检查身份、关键接触动作、空间路径与首尾状态；只返工偏差镜头或段。30秒内每个子节拍的时间见storyboard.md和production-plan.json，不能截断教师句尾、用快放赶动作或用形变代替剪切。真实请求和返回以后存output/api-submit.json与api-result.json，不写密钥或签名访问链接。
