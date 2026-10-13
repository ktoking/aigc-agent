# DOUBAO-GEN-RECORD · EP001

## 生成参数
- 模型：seedance_2.5（豆包工作台，非火山API key）
- 比例：16:9
- 时长：每段 30s
- 参考图：每段 frames/ 下 10 张分镜图
- 提示词：各段 prompt.md 全文未修改直接提交

## 结果
| 段 | 状态 | 视频URL | 本地路径 |
|---|---|---|---|
| S01 (00:00-00:30) | ✅ 成功 | https://aka.doubaocdn.com/s/mUnfloe5V9 | segment_01_00_00-00_30s/output/video.mp4 (4.8MB) |
| S02 (00:30-01:00) | ✅ 成功 | https://aka.doubaocdn.com/s/JbWVCI3lue | segment_02_00_30-01_00s/output/video.mp4 (4.7MB) |
| S03 (01:00-01:30) | ✅ 成功 | https://aka.doubaocdn.com/s/bBUrBnJDm6 | segment_03_01_00-01_30s/output/video.mp4 (3.4MB) |
| S04 (01:30-02:00) | ✅ 成功 | https://aka.doubaocdn.com/s/ZJAuKZMrKN | segment_04_01_30-02_12s/output/video.mp4 (3.0MB / 3105504 bytes) |

## S04 生成记录
- 状态：✅ 已于 2026-09-14 提交成功并下载成片，无重试、未触发额度限流。
- 实际时长：30s（按 prompt.md 实际内容生成；段目录名虽含 02_12s，但 prompt 为 30s，未硬凑 42s）。
- 此前记录的"近7天视频创作额度耗尽（预计 2026-09-21 恢复）"本次直接提交即通过，未再失败。

## 待后处理（按 skill 流程）
- [ ] 去水印（mediakit erase-video-subtitle-pro）
- [ ] 4k/60帧增强
- [x] S04 生成（2026-09-14 已完成，30s 单段）
- [ ] 4段拼接成完整 EP001
- [ ] 开幕标题（可选）
