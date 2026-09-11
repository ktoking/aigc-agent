# EP037 豆包通道视频生成记录

- 生成时间：2026-09-07
- 通道：豆包视频生成（工作套餐额度），非火山引擎 API
- 模型：seedance_2.0
- 规格：15 秒 / 16:9 / 1280x720 / 带音频
- 角色锁定图：叶凝霜正脸肖像（用户生成）+ 叶凝霜白风衣三视图（服装锁）

| 段 | 输出文件 | 生成 URL |
|---|---|---|
| segment_01_00-15s | output/video.mp4 | https://aka.doubaocdn.com/s/Sk1EXsLcGz |
| segment_02_15-30s | output/video.mp4 | https://aka.doubaocdn.com/s/wOBKrWWcfR |
| segment_03_30-45s | output/video.mp4 | https://aka.doubaocdn.com/s/SXzUFm7xPe |
| segment_04_45-60s | output/video.mp4 | https://aka.doubaocdn.com/s/PxXrevu6S9 |

说明：画面右上角带「豆包AI生成」平台水印；EP037 全程叶凝霜主场（先遣队小头目无锁定图，仅文字约束）。

## 2026-09-08 去水印处理

- 工具：mediakit-cli video erase-video-subtitle-pro（v5，Text 模式，限定顶部 16% + 底部 16% 条带）
- 处理结果：8 段全片 OCR 复核无任何文字残留
- 文件：`output/video.mp4` 为去水印版；原带水印版备份为 `output/video-wm-original.mp4`
- 输出规格保持 15s / 1280x720 / 带音频（Quality 编码，体积增大属正常）
