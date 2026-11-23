# MiniMax 配音接入

## 默认参数

- 模型：`speech-2.8-turbo`。
- 音色：`Chinese_calm_streamer_nv1`。
- 语速：1.0；MP3，32 kHz，128 kbps，单声道。
- `subtitle_enable=false`，不生成独立 SRT/VTT。
- 官方同步接口：`https://api.minimax.cn/v1/t2a_v2`。
- [官方接口文档](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http)。

## 凭据

脚本先读取 `MINIMAX_API_KEY`，再读取 macOS Keychain service `codex-minimax-api-key`。不要把 Key 写入脚本、文本文件、生产文档或 API 记录。

## 调用

```bash
python3 scripts/minimax_tts.py \
  --text-file stories/<story-id>/episodes/<episode>/segment_01_00-15s/narration.txt \
  --output stories/<story-id>/episodes/<episode>/segment_01_00-15s/output/narration.mp3
```

也可用 `--text '试听文本'`。`--preset`选择场景，`--emotion/--speed/--vol/--pitch`覆盖表演参数；还支持发音词典、效果器及WAV/FLAC。`--dry-run`只查看请求，不取密钥、不调用API；`--list-presets`查看11个预设。

完整参数范围、模型限制、场景预设、创作提示词和时间线策略统一维护在[skill场景配音指南](../../skills/story-film-workflow/references/minimax-tts.md)。实现随skill分发，仓库脚本是同一实现的入口。

实际生成会调用付费语音API，失败不自动重试，已有输出不覆盖。响应记录只保存所需元数据与不含凭据的参数，不落地原始响应或请求头。

## 后续视频流程

2026-10-22 起，本仓库后续新制内容默认使用 MiniMax 配音，以实际音频时长安排画面，不再默认交付独立字幕文件。用户明确要求字幕或静音时按当次要求执行。已有成片和字幕不回溯修改。

配音后用 ffprobe 检查时长及音频流，再用 ffmpeg 完整解码；音色自然度、情绪和念字效果通过试听判断。使用逐句或逐镜配音时保护词头词尾，不能为了固定段长直接截断音频。

旧 `skills/story-film-workflow/scripts/story_video.py` 仍是静音/独立字幕工具，不能直接当作带配音渲染器。后续制作时先生成配音，再在具体故事工程中接入音轨、对齐镜头；以最终 MP4 的音频流和实际播放验收为准。
