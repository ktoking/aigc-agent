# 本段执行记录

- 平台：本地 Hypit 0.3.1 与 FFmpeg。
- 视频生成 API：不适用，没有提交，不存在 API 任务 ID。
- 图片来源：GPT 内置 imagegen，来源与提示词保存在 generated-sources.json。
- 本地构建 Run：`production/hypit/episode.svrun`。
- 状态：全片本地构建完成；Build `bld_20261016T093949297Z_DECD58C7C4`，本段帧区间见 output/render-record.json。
- 重试：保留既有图片；失败只修复本地编排或环境，再提交新的本地 Build，不重复生图。
