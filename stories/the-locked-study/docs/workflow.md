# 工作流（Workflow）— THE LOCKED STUDY

## P0 骨架 ✅
`stories/the-locked-study/` 全套目录、AGENTS.md、README、docs、assets 骨架。4 段 segment 框架就绪。

## P1 核心资产定锚 ✅
6 位角色设定图（16:9，真人电影质感）：EDWARD_HALE / LADY_ELEANOR / CLARA_VALE / ARTHUR_VALE / MORRIS / OWEN；另含 Hale 室内无大衣版、室内戴手套版、全员参考表，以及庄园外景 / 大客厅 / 书房 3 张场景锚点。

## P2 关键帧 ✅
4 段 × 10 张 = 40 张关键帧，全部生成并落盘各段 `frames/`；每段首尾仍固定为 `frames/first-frame.png` / `frames/last-frame.png`，中间 8 张按叙事节拍编号。

## P3 视频生成（待用户确认后执行）
- 模型：Seedance 2.5（seedance_2.5），duration=30，ratio=16:9。
- 方法：图生视频，参考图 = 本段首帧 + 本段尾帧 + 2-3 张关键角色参考图。
- 提示词：`director-promt.txt`（用户原文，逐字透传）。
- 顺序：四段串行（Seg1 → QA passed → Seg2 → QA passed → Seg3 → QA passed → Seg4）。
- 每段完成后 `scripts/ark_video.py qa --status passed|rejected` 写入 `output/video-qa.json`。

## P4 后处理（待执行）
- 去水印：byted-mediakit `erase-video-subtitle-pro`（顶部 0-16% + 底部 84-100% 条带）。
- 拼接：ffmpeg xfade（fade 0.5s）+ acrossfade 对齐 → 全片（约 119s）。

## P5 配乐与合成（待执行）
- 配乐：text_to_audio_plus，4 段式英式悬疑配乐（风雪氛围 → 紧张弦乐 → 猜疑推高 → 揭示定格）。
- 合成：画面 + 配乐混流 → `EP001_the-locked-study_final.mp4`，present_files 交付。

## 风险与回退

| 风险 | 处理 |
|---|---|
| 多角色口型/台词漂移 | 原生音频只做环境声；台词后期配音叠加 |
| 人脸漂移 | 强化角色参考图 + 首帧锚定 |
| 场景跳变 | 首尾帧继承 + 场景卡锚定 |
| 表演过度/夸张 | 提示词强调克制、静止、微表情 |
| 额度不足 | 停止并报告，不自动重试、不换模型 |
| 隐私拦截 | 停止，不换错图 |

## 交付口径

- 每段：`output/video.mp4`（或 take-N），`output/task-id.txt`，`output/api-submit.json`，`output/api-result.json`，`output/video-qa.json`。
- 全片：`EP001_the-locked-study_final.mp4`。
- 不做 Skynet 统计；git commit/push 一律 `--no-verify`。
