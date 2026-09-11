# kepu-001 科普短视频合集

## 概述

5 条抖音科普短视频，每条 ≤60 秒（4 段 × 15 秒），纯旁白+画面+字卡，无真人/数字人。

## 剧集清单

| 集 | 标题 | 风格 |
|---|---|---|
| ep01 | 火星日落是蓝色的 | AI 科幻大片 |
| ep02 | 宇宙95%看不见 | AI 科幻大片 |
| ep03 | 蜻蜓祖先有老鹰大 | 远古 2D 动漫 |
| ep04 | 银杏是恐龙的朋友 | 治愈系 2D 动漫 |
| ep05 | 弗莱明忘关窗 | 复古电影感 |

## 产线

首帧图(image_gen) → 图生视频(image_to_video, 15s/段) → 去水印(mediakit erase-video-subtitle-pro) → 4K/60fps增强(mediakit enhance-video professional) → 拼接(mediakit concat-video) → 音频淡入淡出(mediakit fade-video-audio) → 成片 MP4。
