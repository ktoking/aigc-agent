# API / 渲染记录

- 方式：本地 HyperFrames 动态漫合成
- 图片：内置 imagegen 生成 4 张真人分镜图，已复制到 `frames/shots/`
- TTS：豆包 `seed-tts-2.0`，男主 `zh_male_taocheng_uranus_bigtts`，女主 `ICL_uranus_zh_female_xingganmeihuo_tob`
- 规则：串行生成与渲染，失败自动重试，不并发请求
