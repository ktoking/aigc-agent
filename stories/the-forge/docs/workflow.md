# 工作流（Workflow）

## P0 骨架（当前阶段）
- 建 `stories/the-forge/` 全套目录、AGENTS.md、README、docs、assets 骨架。
- 4 段 segment 框架（storyboard / first-frame / last-frame / prompt / api-request / frames / output）就绪。
- 验收：目录完整，12 镜头已映射到 4 段。

## P1 核心资产定锚
- 产出（3 张设定图，16:9）：
  1. `assets/characters/BLACKSMITH/` 女铁匠半身+全身设定图（含面部细节、肌肉疤痕、皮革围裙）
  2. `assets/props/LEGENDARY_SWORD/` 圣剑成品设定图（含剑身符文、剑格、柄首）
  3. `assets/scenes/VOLCANO_FORGE/` 火山熔炉全景设定图（含熔炉、铁砧、淬火槽、磨石、石中剑石台）
- 方法：image_gen（文生图），每条 prompt = 设定卡描述 + 总控前缀 + 负面约束。
- 验收：与设定卡逐项核对；无 AI 伪影；风格统一。

## P2 首尾帧（每段 2 张：首帧+尾帧）
- 方法：image_gen 基于核心资产图延展（保持角色/道具一致性）。
- 首帧 = 段内首个镜头起始画面；尾帧 = 段内末个镜头结束画面。
- 验收：与上一段尾帧/下一段首帧衔接成立。

## P3 视频生成（4 段 × 30s）
- 模型：Seedance 2.5（seedance_2.5），duration=30，ratio=16:9。
- 方法：图生视频，参考图 = 本段首帧 + 核心资产图。
- 提示词 = 总控前缀 + 段内 3 镜头连续叙事 + 负面约束（按 production-rules）。
- 提交记录 → `api-request.md`；结果 → `output/`。
- 验收：角色一致、镜头顺序对、无字幕水印（水印留待 P4 去）。

## P4 后处理
- 去水印：mediakit erase-video-subtitle-pro（顶部/底部条带）→ `output/segXX_nowatermark.mp4`
- 动态转场：ffmpeg xfade（dissolve/fadeblack/slide/wipe）按 BGM 节奏拼接
- 拼接：4 段顺序拼接 → 全片（120s）
- 淡入淡出：fade-video-audio（片头 0.5s / 片尾 1.5s）
- 验收：抽帧 OCR 无水印；时长 120s±1s；转场自然卡点。

## P5 配乐（4 段式原创）
| 段 | 时间 | 风格 |
|---|---|---|
| A | 00:00–00:30 | 低频鼓点+金属敲击，庄严仪式感，火山熔炉氛围 |
| B | 00:30–01:00 | 节奏加快，史诗弦乐进入，锤击鼓点加速，闪回画面 |
| C | 01:00–01:30 | 全乐队高潮，重金属+史诗弦乐，圣剑诞生金光爆发 |
| D | 01:30–02:00 | 庄严收束，弦乐+合唱氛围，石中剑与晨光，希望与苍凉 |
- 生成方式：AI 配乐合成单条 120s 音轨（4 段间加交叉淡化过渡）；验收：各幕情绪衔接、不压关键音效（锤击/淬火）。

## P6 合成交付
- 画面 + 配乐混流（保留画面内音效）→ `episodes/EP001_the-forge/EP001_the-forge_final.mp4`
- present_files 交付；更新 README 进度。

## 风险与回退
- 额度不足：分段生成，先 1-2 段后 3-4 段。
- 一致性漂移：回到 P1 核心资产，改用 image_edit 重出首尾帧再生成。
- 单段失败：重试该段（同 api-request 参数），连续 2 次失败换描述措辞。
- 闪回画面与现实混淆：闪回必须用柔光/慢动作/剪影处理，与现实硬光实焦区分。
