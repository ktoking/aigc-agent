# 《荒轨 / WASTELINE》EP001 生成记录

> 生成时间：2026-09-09
> 总时长：240s（8 段 × 30s）
> 画幅：16:9 横屏，1280×720，24fps
> 视频模型：Seedance 2.5（seedance_2.5，duration=30，ratio=16:9）
> 全片无对白、无旁白、无字幕

## 各段生成记录

| 段 | 时间 | 镜头 | 生成 URL | 去水印后本地路径 | 时长 | 水印验证 |
|---|---|---|---|---|---|---|
| Seg01 | 00:00–00:30 | L01-03 荒原开场 | https://aka.doubaocdn.com/s/RrFCpRUPtt | segment_01_00-30s/output/video.mp4 | 30.04s | OCR+抽帧通过 |
| Seg02 | 00:30–01:00 | L04-06 女主与目标 | https://aka.doubaocdn.com/s/GnQdbbB1KQ | segment_02_30-60s/output/video.mp4 | 30.04s | OCR+条带裁剪通过 |
| Seg03 | 01:00–01:30 | L07-09 敌人来临 | https://aka.doubaocdn.com/s/lPUco6vRae | segment_03_60-90s/output/video.mp4 | 30.04s | OCR+抽帧通过 |
| Seg04 | 01:30–02:00 | L10-12 第一波反击 | https://aka.doubaocdn.com/s/T4BBIIpDR8 | segment_04_90-120s/output/video.mp4 | 30.04s | OCR+抽帧通过 |
| Seg05 | 02:00–02:30 | L13-15 峡谷血战 | https://aka.doubaocdn.com/s/5HU8Ve8v7j | segment_05_120-150s/output/video.mp4 | 30.04s | 抽帧+条带复核通过 |
| Seg06 | 02:30–03:00 | L16-18 核心危机 | https://aka.doubaocdn.com/s/kyQNvazTQS | segment_06_150-180s/output/video.mp4 | 30.04s | 抽帧+条带复核通过 |
| Seg07 | 03:00–03:30 | L19-21 反杀与终点 | https://aka.doubaocdn.com/s/gOpYI8bS7A | segment_07_180-210s/output/video.mp4 | 30.04s | OCR+抽帧通过 |
| Seg08 | 03:30–04:00 | L22-24 牺牲与希望 | https://aka.doubaocdn.com/s/CYEBwtO6qx | segment_08_210-240s/output/video.mp4 | 30.04s | OCR+抽帧通过 |

## 去水印

- 工具：mediakit-cli `erase-video-subtitle-pro`（Text 模式，v5 算法）
- 擦除区域：顶部 0–16% + 底部 84–100% 条带（覆盖左上角与右下角"豆包AI生成"水印）
- 每段原带水印版备份为 `output/video_wm_original.mp4`
- 验证：mediakit `video-ocr`（Detailed 模式）+ 本地抽帧目检，全部通过，无水印残留

## 配乐（P5）

4 段式原创配乐，AI 合成单条 240s 音轨（`audio/soundtrack_240s.wav`）：

| 段 | 时间 | 风格 |
|---|---|---|
| A | 00:00–00:50 | 低频压迫、荒凉、末日感 |
| B | 00:50–01:50 | 鼓点进入，速度感上升 |
| C | 01:50–03:10 | 工业打击乐、强节奏、紧张推进 |
| D | 03:10–04:00 | 史诗悲壮 → 尾奏收束，留希望与苍凉 |

- 配乐源 URL：A `https://aka.doubaocdn.com/s/P6krwVfJY3` / B `https://aka.doubaocdn.com/s/BhoOl05Kqs` / C `https://aka.doubaocdn.com/s/PwyRqU3KyD` / D `https://aka.doubaocdn.com/s/KDMO5wc1JU`

## 合成（P6）

- 拼接：ffmpeg concat demuxer，8 段顺序拼接 → `EP001_concat.mp4`（240.35s）
- 混流：视频原音效（100%）+ 配乐（22% 音量），amix 混合
- 淡入淡出：音频 0.8s 淡入 + 最后 2s 淡出
- 最终成片：`EP001_wasteline_final.mp4`（240.27s，1280×720，24fps，H.264+AAC，106MB）

## 异常与处理

1. **额度不足**：Seg2/4/6/8 首次提交 seedance_2.5 时因账户额度不足被拦截；曾尝试 seedance_2.0 + 15s 回退，同样被拦截。额度恢复后全部以 seedance_2.5 + 30s 重新生成成功。
2. **OCR 网关超时**：Seg5 的 video-ocr 验证一次遇网关超时，改用本地抽帧 + 条带裁剪目检，结论一致。
3. **Seg8 OCR 误检**：检出 0.29s 右下角"难言"一处，抽帧目检确认为肩甲/布条金属纹理误判，无实际可读文字。

## 验收

- [x] 8 段全部生成，seedance_2.5 / 30s / 16:9
- [x] 全片无水印（OCR + 抽帧验证）
- [x] 全片无对白、无旁白、无字幕
- [x] 总时长 240s±1s（实际 240.27s）
- [x] 角色/道具跨段一致性（首帧参考图置首 + 资产设定卡锁定）
- [x] 4 段式配乐混流完成，淡入淡出
- [x] 最终成片 `EP001_wasteline_final.mp4` 已就位
