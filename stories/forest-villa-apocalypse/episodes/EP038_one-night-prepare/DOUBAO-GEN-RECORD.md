# EP038 豆包通道视频生成记录

- 生成时间：2026-09-07
- 通道：豆包视频生成（工作套餐额度），非火山引擎 API
- 模型：seedance_2.0
- 规格：15 秒 / 16:9 / 1280x720 / 带音频
- 角色锁定图：许砚三视图（用户生成）+ 叶凝霜正脸肖像 + 沈知夏正脸肖像 + 白棠成片抽帧（EP033 同一数字人）

| 段 | 输出文件 | 生成 URL |
|---|---|---|
| segment_01_00-15s | output/video.mp4 | https://aka.doubaocdn.com/s/fuxnaJGYjc |
| segment_02_15-30s | output/video.mp4 | https://aka.doubaocdn.com/s/J6CYdz4WDz |
| segment_03_30-45s | output/video.mp4 | https://aka.doubaocdn.com/s/RH7Hg7oyLH |
| segment_04_45-60s | output/video.mp4 | https://aka.doubaocdn.com/s/UO2zvdoxjX |

说明：画面右上角带「豆包AI生成」平台水印；s01 台词提到白棠，抽查帧中出现白棠侧影（模型自动带入，轻微瑕疵）。

## 2026-09-08 去水印处理

- 工具：mediakit-cli video erase-video-subtitle-pro（v5，Text 模式，限定顶部 16% + 底部 16% 条带）
- 处理结果：8 段全片 OCR 复核无任何文字残留
- 文件：`output/video.mp4` 为去水印版；原带水印版备份为 `output/video-wm-original.mp4`
- 输出规格保持 15s / 1280x720 / 带音频（Quality 编码，体积增大属正常）
