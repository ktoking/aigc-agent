# EP039《森林公路伏击》后期流水线记录（DOUBAO-GEN-RECORD）

- 集数：EP039_forest-road-ambush
- 流水线：去水印 → OCR 验证 → 4K/60fps 增强 → 拼接（交叉淡化）→ 音频淡入淡出 → 成片
- 完成时间：2026-09-08
- 说明：本集未生成新视频，仅对既有 30s 合并素材执行后期处理。

---

## 1. 素材与备份

| 段 | 原始合并视频 URL | 本地原文件 | 带水印备份 |
|---|---|---|---|
| s01+s02 | https://aka.doubaocdn.com/s/L9Sfe689Ux | `segment_01_00-15s/output/video-30s.mp4` | `segment_01_00-15s/output/video-wm-original.mp4` |
| s03+s04 | https://aka.doubaocdn.com/s/NeHlCDX50D | `segment_03_30-45s/output/video-30s.mp4` | `segment_03_30-45s/output/video-wm-original.mp4` |

原始规格：1280×720 @24fps，30.04s，H.264 + AAC。

> 备份通过 `cp` 复制保留，原 `video-30s.mp4` 未删除。

## 2. 去水印（erase-video-subtitle-pro）

> 历史：初批任务（`...946883867138`、`...957589751042`）运行超过 30 分钟无终态，判定卡住后由上级重新提交；旧任务 ID 废弃，不再追踪。

| 段 | 去水印 task_id | 结果 URL | 下载产物 |
|---|---|---|---|
| s01+s02 | `amk-tool-erase-video-subtitle-pro-957604278530` | https://2130825428-amk-2130605177-default-534849.vod.cn-north-1.volcvideo.com/3501191614f74bf2a488315fb6b8644f?preview=1&auth_key=1788957517-r0-u0-97b5ab44ddb44ad650d4ec00f559559e | `segment_01_00-15s/output/video.mp4`（27.1MB） |
| s03+s04 | `amk-tool-erase-video-subtitle-pro-946884098050` | https://2130825428-amk-2130605177-default-534849.vod.cn-north-1.volcvideo.com/ebd3f60b9768485ca4fbc0ff9b417cf0?preview=1&auth_key=1788957737-r0-u0-2ef93f423fa4ece607fd0f921ad60a97 | `segment_03_30-45s/output/video.mp4`（29.8MB） |

两任务均 `status=completed`，`duration=30.042s`。

## 3. OCR 验证（video-ocr，Detailed 模式）

| 段 | OCR task_id | 结果 |
|---|---|---|
| s01+s02 | `amk-tool-video-ocr-902815129602` | 仅检出画面中部内容文本：“送”(y395–434)、“我”(y403–450)，位于 55%–62% 高度；顶部 0–16%（y<115）与底部 84–100%（y>605）无水印文字残留 |
| s03+s04 | `amk-tool-video-ocr-755222328834` | 检出文本均位于画面中部（y335–446）及左上场景区；顶部左侧 "m"（y42–186，x0–67）经 17.5s/26.3s 帧目视复核为雪地围栏场景误检（图像 OCR 无文本），非水印 |

**帧级交叉验证**（ffmpeg 抽帧对比原版与去水印版）：
- s03 17.5s / 26.3s：原版右下角“豆包AI生成”水印（y≈88%–95%）在去水印版中已完全清除。
- s01 20.2s：右下水印区干净（画面底部中央小标识为屏显内容，原版/去水印版均存在）。

**结论：两段顶部 0–16% 与底部 84–100% 区域均无水印文字残留，验证通过，无需重新提交。**

## 4. 4K/60fps 增强（enhance-video，professional）

参数：`--resolution 4k --fps 60 --tool-version professional`

| 段 | 增强 task_id | 结果 URL | 下载产物 |
|---|---|---|---|
| s01+s02 | `amk-tool-enhance-video-902815321346`（首次提交响应缺 task_id，重试后成功） | https://2130825428-amk-2130605177-default-534849.vod.cn-north-1.volcvideo.com/9a935c04cd2c41a288e98cd21b25bdba?preview=1&auth_key=1788962264-r0-u0-8754f4c0951dac77b86c911961572b87 | `segment_01_00-15s/output/video-4k.mp4`（164MB） |
| s03+s04 | `amk-tool-enhance-video-902815320066` | https://2130825428-amk-2130605177-default-534849.vod.cn-north-1.volcvideo.com/91fad87f74534a03b38b7d04c6f6f5f9?preview=1&auth_key=1788962009-r0-u0-5cd2a66e56541b7f826ebf193df10223 | `segment_03_30-45s/output/video-4k.mp4`（176MB） |

增强结果：3840×2160 @60fps，30.0s，H.264 + AAC（两段均 `status=completed`，`resolution=4k`，`fps=60`）。

## 5. 拼接（转场）

- 工具说明：`mediakit-cli editing concat-video` 的转场仅支持预设特效 ID（交替出场/旋转放大/泛开等 12 种），**不含淡入淡出/交叉淡化选项**，无法满足“淡入淡出或交叉淡化 0.5–1s”的要求，故改用 ffmpeg 实现真正的交叉淡化。
- 命令：`ffmpeg -i s01_4k.mp4 -i s03_4k.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.75:offset=29.25[v];[0:a][1:a]acrossfade=d=0.75[a]"`（H.264 videotoolbox，4K 40Mbps，AAC 192k）
- 转场类型：**交叉淡化（fade crossfade），时长 0.75s**（视频 xfade + 音频 acrossfade 同步）。
- 顺序：s01+s02（前）→ s03+s04（后）。
- 中间产物：`EP039_forest-road-ambush/concat-59.25s.mp4`（59.25s，4K，248MB）。

## 6. 音频淡入淡出（fade-video-audio）

- 工具：`mediakit-cli editing fade-video-audio`
- 参数：`--fade-in-duration 2 --fade-out-duration 2`
- task_id：`amk-tool-fade-video-audio-957605093122`（`status=completed`，`duration=59.274`，`resolution=4k`）
- 结果 URL：https://2130825428-amk-2130605177-default-534849.vod.cn-north-1.volcvideo.com/1d167f157b57410b88b1a917f15d52e1.mp4?preview=1&auth_key=1788963326-r0-u0-f3c607706cbc15cf721c73ab0c3672ae

## 7. 最终成片

- 路径：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP039_forest-road-ambush/EP039_final.mp4`
- 时长：**59.25s**（30 + 30 − 0.75 交叉淡化）
- 分辨率：**3840×2160（4K）**
- 帧率：60fps
- 编码：H.264 + AAC（44100Hz，立体声）
- 大小：64.5MB

### ffprobe 验证结果
```
stream 0: video h264 3840x2160 60fps
stream 1: audio aac 44100Hz 2ch
duration=59.250000s
```
时长约 60 秒 ✓ / 4K 分辨率 ✓ / 含音轨 ✓

---

## 附：过程中的异常与处理

| 异常 | 处理 |
|---|---|
| 首批去水印任务（946883867138 / 957589751042）>30min 无终态 | 上级重新提交新任务（957604278530 / 946884098050），改为轮询新任务 |
| s01 增强首次提交返回“异步任务提交成功响应缺少 task_id” | 按纪律重试一次，成功获取 `amk-tool-enhance-video-902815321346` |
| concat-video 无淡入淡出转场 | 改用 ffmpeg xfade/acrossfade 交叉淡化 0.75s，并在此记录偏差 |
