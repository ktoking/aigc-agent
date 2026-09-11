# 荒轨 / WASTELINE

> 末日废土世界里，一名女狙击手护送一枚净水核心穿越死亡铁路，逃离铁王庭的疯狂追杀，把最后的希望送往地下净水站。
> 无台词 · 4 分钟 · 16:9 横屏 · Seedance 2.5 · 24 镜头 · 8 段 × 30s

## 视觉气质

真人电影质感 · Mad Max 式狂暴追逐（原创世界观）· 灰黑雷暴荒原 · 铁锈色机械 · 白色盐湖 · 黑色峡谷 · 少量橙色火焰 · 冷蓝色净水核心为唯一希望色 · 高对比低饱和 · 强风沙尘烟雾火花闪电。

## 目录导航

- `AGENTS.md`：剧本专属硬规则
- `assets/style/`：全片统一风格（总控前缀 / 负面约束 / 镜头语言）
- `assets/characters/`：女主、巨汉设定卡
- `assets/enemies/`：铁王庭设定卡
- `assets/props/`：净水核心、装甲火车设定卡
- `assets/scenes/`：荒原、峡谷桥、净水站场景卡
- `docs/`：story-memory / production-rules / workflow / season-arc / audience-strategy
- `episodes/EP001_wasteline/`：8 段生成工作区（segment_01~08）

## 当前进度

**EP001 全流程完成（P0–P6）**，成片已交付。

- P0 骨架 ✅
- P1 核心资产定锚 ✅（女主/巨汉/装甲火车/净水核心/峡谷桥/净水站/净化室设定图）
- P2 首尾帧 ✅（8 段 × 首帧+尾帧，16:9）
- P3 视频生成 ✅（8 段 × seedance_2.5 / 30s / 16:9，图生视频，首帧参考置首）
- P4 去水印+拼接 ✅（mediakit erase-video-subtitle-pro v5，顶部/底部条带；ffmpeg concat 8 段 → 240s）
- P5 配乐 ✅（4 段式情绪谱 240s 原创音轨，低频压迫→鼓点加速→工业打击→史诗悲壮）
- P6 合成交付 ✅（原音效+配乐混流，0.8s 淡入/2s 淡出，`EP001_wasteline_final.mp4`，1280×720，24fps，106MB）

成片路径：`episodes/EP001_wasteline/EP001_wasteline_final.mp4`
生成记录：`episodes/EP001_wasteline/DOUBAO-GEN-RECORD.md`
