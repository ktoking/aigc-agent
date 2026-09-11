# 工作流（Workflow）

## P0 骨架（当前已完成）
- 建 `stories/wasteline/` 全套目录、AGENTS.md、README、docs、assets 骨架。
- 8 段 segment 框架（storyboard / first-frame / last-frame / prompt / api-request / frames / output）就绪。
- 验收：目录完整，24 镜头已映射到 8 段。

## P1 核心资产定锚
- 产出（7 张设定图，16:9）：
  1. `assets/characters/LEAD_SNIPER/` 女主半身+全身设定图（含面部细节）
  2. `assets/characters/GIANT_BRUTE/` 巨汉全身设定图
  3. `assets/props/ARMORED_TRAIN/` 装甲火车车头+侧面设定图
  4. `assets/props/WATER_CORE/` 净水核心特写设定图
  5. `assets/enemies/IRON_COURT/` 铁王庭战车/摩托+破旗设定图
  6. `assets/scenes/CANYON_BRIDGE/` 黑色峡谷高桥氛围设定图
  7. `assets/scenes/WASTELAND/` 灰黑雷暴荒原氛围设定图
- 方法：image_gen（文生图），每条 prompt = 设定卡描述 + 总控前缀 + 负面约束。
- 验收：与设定卡逐项核对；无 AI 伪影；风格统一。

## P2 首尾帧（每段 2 张：首帧+尾帧）
- 方法：image_edit 基于核心资产图延展（保持角色/道具一致性）。
- 首帧 = 段内首个镜头起始画面；尾帧 = 段内末个镜头结束画面。
- 验收：与上一段尾帧/下一段首帧衔接成立。

## P3 视频生成（8 段 × 30s）
- 模型：Seedance 2.5（seedance_2.5），duration=30，ratio=16:9。
- 方法：图生视频，参考图 = 本段首帧 + 关键资产图。
- 提示词 = 总控前缀 + 段内 3 镜头连续叙事 + 负面约束（按 production-rules）。
- 提交记录 → `api-request.md`；结果 → `output/`。
- 验收：角色一致、镜头顺序对、无字幕水印（水印留待 P4 去）。

## P4 后处理
- 去水印：mediakit erase-video-subtitle-pro（顶部/底部条带）→ `output/segXX_nowatermark.mp4`
- 拼接：mediakit concat-video 按段序 → 全片（240s）
- 淡入淡出：fade-video-audio（片头 0.5s / 片尾 1.5s）
- 验收：抽帧 OCR 无水印；时长 240s±1s。

## P5 配乐（4 段式原创）
| 段 | 时间 | 风格 |
|---|---|---|
| A | 00:00-00:50 | 低频压迫、荒凉、末日感 |
| B | 00:50-01:50 | 鼓点进入，速度感上升 |
| C | 01:50-03:10 | 工业打击乐、强节奏、紧张推进 |
| D | 03:10-04:00 | 史诗悲壮 → 尾奏收束，留希望与苍凉 |
- 生成方式：AI 配乐合成单条 240s 音轨；验收：各幕情绪衔接、不压关键音效。

## P6 合成交付
- 画面 + 配乐混流（保留画面内音效）→ `episodes/EP001_wasteline/EP001_wasteline_final.mp4`
- present_files 交付；更新 README 进度。

## 风险与回退
- 额度不足：分段生成，先 1-4 段后 5-8 段。
- 一致性漂移：回到 P1 核心资产，改用 image_edit 重出首尾帧再生成。
- 单段失败：重试该段（同 api-request 参数），连续 2 次失败换描述措辞。
