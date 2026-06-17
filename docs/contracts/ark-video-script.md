# Ark 视频脚本使用说明

`scripts/ark_video.py` 用于把每个 segment 的 `prompt.md`、首帧、尾帧和故事板图提交给火山 Ark / Seedance，并在本地静默轮询、下载结果，避免 Codex 对话里出现大量轮询 JSON。

## 环境变量

不要把 key 写入仓库文件。运行前只在当前 shell 设置：

```bash
export ARK_API_KEY="你的火山 Ark key"
```

## 正式生成 15 秒视频

```bash
python scripts/ark_video.py submit \
  --segment stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s \
  --model doubao-seedance-2-0-fast-260128 \
  --duration 15 \
  --ratio 9:16 \
  --resolution 720p \
  --quiet
```

默认会自动读取：

- `prompt.md`
- `frames/first-frame.png`
- `frames/last-frame.png`
- `frames/storyboard-sheet.png` 或 `frames/storyboard.png`

输出会写入：

- `output/api-submit.json`
- `output/api-result.json`
- `output/task-id.txt`
- `output/video.mp4`
- `output/last-frame-generated.png`
- `api-request.md`

## 只提交不轮询

```bash
python scripts/ark_video.py submit \
  --segment stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s \
  --duration 15 \
  --no-poll
```

## 继续轮询已有任务

```bash
python scripts/ark_video.py poll \
  --segment stories/twin-dawn/episodes/EP001_rebirth-before-apocalypse/segment_01_00-15s \
  --quiet
```

如果没有传 `--task-id`，脚本会读取 `output/task-id.txt`。

## 成本建议

- 草稿验证：`--duration 5 --resolution 720p`
- 正式分段：`--duration 15 --resolution 720p`
- 无需声音时不要加 `--generate-audio`
- 需要段落衔接时保持默认 `--return-last-frame`

## 真人隐私审核拦截策略

正式生成默认开启 `--virtual-person-notice`，会在 prompt 末尾补充合规说明：

- 输入图中的人物均为 AI 生成虚拟角色。
- 不对应、不冒充、不还原任何真实人物。
- 不包含真人身份信息、真人肖像授权信息或个人隐私。
- 参考图只用于保持虚构短剧角色的脸型、发型、服装和镜头连续性。

如果火山返回 `InputImageSensitiveContentDetected.PrivacyInformation`，脚本会保留原首尾帧、故事板图和角色参考图，自动换更明确的虚拟人物说明重试，默认最多 `--privacy-retry 2` 次。

如果重试后仍被拦截，脚本会停止并输出 `submit_failed privacy_review_blocked`。不要自动改用场景图或其他不含正确人脸的图片继续生成，否则会导致角色脸不一致并浪费额度。
