# EP001 生成与合成记录 — 《黑龙远征 / Dragon Quest》

- Story：dragon-quest《黑龙远征 / Dragon Quest》
- Episode：EP001（2 分钟无对白荷马史诗式奇幻微电影）
- 画幅：16:9 / 1280×720 / 24fps / H.264 + AAC 44100Hz 立体声
- 流程：P3 生成 → 去水印 → P4 拼接 → P5 配乐 → P6 合成交付
- 完成时间：2026-09-10

## 1. 四段视频生成（P3，seedance_2.5 / image_to_video / 30s / 16:9）

| 段 | 剧情 | 原片生成 URL | 去水印后本地产物 | 时长 |
|---|---|---|---|---|
| segment_01_00-30s | 王国出发·森林遇妖 | https://aka.doubaocdn.com/s/SjMYNaQHIm | `segment_01_00-30s/output/video.mp4` | 30.042s |
| segment_02_30-60s | 瀑布·沼泽·沙漠 | https://aka.doubaocdn.com/s/lxuZWIeUjN | `segment_02_30-60s/output/video.mp4` | 30.042s |
| segment_03_60-90s | 攀山·龙穴·对峙 | https://aka.doubaocdn.com/s/rUV5pejUDE | `segment_03_60-90s/output/video.mp4` | 30.042s |
| segment_04_90-120s | 决战·坠崖·尾声 | https://aka.doubaocdn.com/s/KUIXhFUFpP | `segment_04_90-120s/output/video.mp4` | 30.042s |

- 去水印：mediakit-cli `erase-video-subtitle-pro`（Text v5，顶部 0-16% + 底部 84-100% 条带）
- 质量验证：4 段均通过抽帧目检 + video-ocr Detailed 校验，无「豆包AI生成」水印残留、无任何字幕文字

## 2. P4 拼接

- 输入：上表 4 段去水印成片（各 30.042s）
- 命令：`ffmpeg -i seg1 -i seg2 -i seg3 -i seg4 -filter_complex`
  - 视频：`xfade=transition=fade:duration=0.5`（3 次，offset 29.541667 / 59.083334 / 88.625）
  - 音频：`acrossfade=d=0.5`（3 次，与视频过渡对齐）
  - 编码：`libx264 crf 18 / preset medium / yuv420p` + `aac 192k / 44100Hz`
- 输出：`EP001_dragon-quest_concat.mp4`
- 结果：118.667s / 1280×720 / 24fps / AAC 立体声

## 3. P5 配乐（BGM）

- 工具：text_to_audio_plus（T2A）
- 时长：120s（工具上限；比成片 118.67s 略长，结尾在合成时做 4s 淡出）
- 风格：荷马史诗式中世纪欧洲奇幻管弦乐（指环王/权游式），纯器乐、无歌词、无演唱，允许无词合唱哼鸣
- 情绪谱（严格对应 4 段）：
  - 00:00-00:30 王国出发→森林遇狼：低沉圆号→弦乐渐强→英雄主题→紧张鼓点
  - 00:30-01:00 瀑布→沼泽蛇战→沙漠：宏大管弦→急促打击乐+铜管→孤独弦乐+微弱希望
  - 01:00-01:30 攀山→龙穴→对峙：渐强定音鼓→低沉管风琴+合唱哼鸣→寂静后爆发
  - 01:30-02:00 激战→坠崖→河流尾声：全编制+合唱最高潮→弦乐拉长+钟声→钢琴独奏+微弱弦乐留悬念，结尾淡出
- 生成 URL：https://aka.doubaocdn.com/s/2UNbhMGquV
- 本地产物：`audio/EP001_BGM_epic_fantasy.wav`（120.000s / PCM s16le / 40000Hz / 立体声）

## 4. P6 合成

- 输入：`EP001_dragon-quest_concat.mp4` + `audio/EP001_BGM_epic_fantasy.wav`
- 命令：`ffmpeg -i concat.mp4 -i bgm.wav -filter_complex`
  - BGM：`aresample=44100, volume=0.85, afade=t=out:st=114.5:d=4`
  - 原环境声（视频原音轨）：`volume=0.15`
  - 混合：`amix=inputs=2:duration=first:dropout_transition=0:normalize=0`
  - 视频流 `-c:v copy`（不重编码），音频 `aac 192k / 44100Hz`，`-movflags +faststart`
- 输出：`EP001_dragon-quest_MV_final.mp4`

## 5. 最终成片验证

| 检查项 | 结果 |
|---|---|
| 时长 | 118.667s（约 120s，4 段 120.17s − 3×0.5s 过渡）✅ |
| 分辨率 | 1280×720（16:9 横屏）✅ |
| 帧率 / 编码 | 24fps / H.264 ✅ |
| 音轨 | AAC 44100Hz 立体声（BGM 0.85 + 环境声 0.15，结尾淡出）✅ |
| 内容约束 | 无对白、无字幕、无歌词（提示词全程锁定）✅ |

## 6. 交付物清单

| 产物 | 路径 |
|---|---|
| 最终成片 | `episodes/EP001_dragon-quest/EP001_dragon-quest_MV_final.mp4` |
| 拼接稿 | `episodes/EP001_dragon-quest/EP001_dragon-quest_concat.mp4` |
| BGM | `audio/EP001_BGM_epic_fantasy.wav` |
| 4 段去水印成片 | 各 `segment_0X/output/video.mp4` |
