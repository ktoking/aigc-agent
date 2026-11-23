# 本地渲染记录

- 平台：本地 HyperFrames 0.8.170 + FFmpeg。
- 外部视频 API：NOT_RUN，本片为确定性矢量动画，无需调用。
- 状态：已完成；15 秒本地成片与首尾帧已验证。外部 API 未调用。
- 源工程：production/inner-noise/index.html。
- 结果：output/video.mp4。
- 重试：修改局部时间线后重渲染，不替换原始参考。