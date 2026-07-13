# Story 工作流

1. 先读取 `docs/story-memory.md` 和 `docs/production-rules.md`。
2. 每集默认 60 秒，拆成 4 段，每段 15 秒以内。
3. 每段必须有 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`、`director-promt.txt`、`api-request.md`。
4. 视频参考图顺序默认：首帧、尾帧、角色/道具参考。
5. 故事板图只做人类审阅，不默认上传视频 API。
6. 生成视频时默认使用 Seedance 2.0-mini 草稿，剧情样片加 `--generate-audio`。
