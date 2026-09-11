# DOUBAO-GEN-RECORD — EP040_snow-plain-siege

- 生成时间：2026-09-08 19:55 ~ 2026-09-09 01:35（本地）
- 最终交付：`EP040_final.mp4`
- 说明：未改动剧本与台词；两个合并稿仅做结构合并（去重规格头、8镜头连续编号），内容逐字沿用 director-promt.txt。

---

## 一、合并段视频生成（image_to_video）

### 合并段1（s01+s02）《别为了省子弹跑出去，这只比前面的更难挡》
- 合并稿：`/tmp/ep040_s01s02_merged30s.txt`（全文透传，未润色）
- 提交参数：`model_version=seedance_2.5`，`duration=30`，`ratio=16:9`
- 参考图（image_reference_url_list，3张角色正脸）：
  - 白棠 `https://aka.doubaocdn.com/s/zy4EkwXnWu`
  - 许砚 `https://aka.doubaocdn.com/s/AgPOhLYMza`
  - 叶凝霜 `https://aka.doubaocdn.com/s/36s2FF7Z8z`
- 返回URL：`https://aka.doubaocdn.com/s/aVSkOSa9qN`
- 下载：`segment_01_00-15s/output/video-30s.mp4`（1280x720@24fps，30.04s，2.8MB）
- api-request.md 追加记录：segment_01 / segment_02

### 合并段2（s03+s04）《奖励来了，人还没撤，他和凝霜一样被控制了》
- 合并稿：`segment_03_30-45s/output/merged_s03s04_prompt.txt`（s03 镜头一~四 + s04 镜头一~四 → 连续编号镜头一~镜头八）
- 提交参数：`model_version=seedance_2.5`，`duration=30`，`ratio=16:9`
- 参考图（image_reference_url_list，3张角色正脸）：同上
- 返回URL：`https://aka.doubaocdn.com/s/EsY8TRGsGV`
- 下载：`segment_03_30-45s/output/video-30s.mp4`（1280x720@24fps，30.04s，1.9MB）
- api-request.md 追加记录：segment_03 / segment_04

---

## 二、去水印（erase-video-subtitle-pro）

参数（--schema 确认）：`--mode Text --model-version v5 --erase-ratio-location` 两个擦除框（顶部 0-16%、底部 84-100%）。

| 段 | task_id | 状态 | 结果时长 | 结果文件 |
|---|---|---|---|---|
| 段1（s01+s02） | `amk-tool-erase-video-subtitle-pro-902830116866` | completed | 30.042s | `segment_01_00-15s/output/video.mp4`（35MB） |
| 段2（s03+s04） | `amk-tool-erase-video-subtitle-pro-906902281474` | completed | 30.042s | `segment_03_30-45s/output/video.mp4`（25.5MB） |

- 原带水印版备份：两个段均保留 `output/video-wm-original.mp4`（即 video-30s.mp4 副本），未覆盖用户素材。
- 去水印结果均为 1280x720@24fps、30.04s、含 AAC 音轨。

### video-ocr 验证（--mode Detailed，含 text_location）

| 段 | task_id | 检测文本位置（y，画面 720p） | 结论 |
|---|---|---|---|
| 段1 | `amk-tool-video-ocr-755222634754` | 318~502px（画面中部） | 顶部 0-16%（0-115px）与底部 84-100%（605-720px）无水印文字残留 ✓ |
| 段2 | `amk-tool-video-ocr-1161633434626` | 131~462px（画面中部） | 顶部 0-16% 与底部 84-100% 无水印文字残留 ✓ |

> 段2 OCR 前两次提交遇“异步任务提交成功响应缺少 task_id”瞬时错误，重试后成功。

---

## 三、4k 增强（mediakit 异常 → ffmpeg 兜底）

### mediakit enhance-video 异常记录
参数（--schema 确认）：`--resolution 4k --fps 60 --tool-version professional`。共提交 4 个任务：

| 任务 | 提交方式 | 状态 |
|---|---|---|
| `amk-tool-enhance-video-1170465187586`（段1） | 本地路径 | 运行超 2 小时仍 running，放弃 |
| `amk-tool-enhance-video-902801871362`（段2） | 本地路径 | 运行超 2 小时仍 running，放弃 |
| `amk-tool-enhance-video-906903217922`（段1） | 去水印结果 URL | 运行超 1 小时仍 running，放弃 |
| `amk-tool-enhance-video-957591158786`（段2） | 去水印结果 URL | 运行超 1 小时仍 running，放弃 |

> **结论：mediakit enhance-video 服务对 EP040 视频持续异常（4 个任务均卡在 running 超 1 小时），放弃 mediakit 增强。**

### ffmpeg 兜底方案
- 命令：`ffmpeg -i input.mp4 -vf "scale=3840:2160:flags=lanczos,minterpolate=fps=60:mi_mode=blend" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 128k output`
- 说明：先尝试 `mi_mode=mci`，4k 分辨率下过慢（30分钟未完成），改用 `mi_mode=blend` 完成。
- 结果：
  - 段1：`segment_01_00-15s/output/video-4k.mp4`（3840x2160@60fps，29.97s，h264+AAC，86MB）
  - 段2：`segment_03_30-45s/output/video-4k.mp4`（3840x2160@60fps，29.97s，h264+AAC，60MB）

---

## 四、拼接与音频处理

- 方法：ffmpeg `xfade` 交叉淡化 + `acrossfade` + `afade`
  - 视频：`xfade=transition=fade:duration=0.8:offset=29.17`
  - 音频：`acrossfade=d=0.8:c1=tri:c2=tri`（交叉段），`afade=t=in:st=0:d=2`（淡入2s）+ `afade=t=out:st=57.13:d=2`（淡出2s）
- 编码：`libx264 -preset fast -crf 18`，`aac -b:a 128k`
- 拼接顺序：段1（s01s02）在前，段2（s03s04）在后
- 输出：`EP040_final.mp4`

---

## 五、最终成片信息

- 路径：`/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/stories/forest-villa-apocalypse/episodes/EP040_snow-plain-siege/EP040_final.mp4`
- 时长：59.15s（≈60s）
- 分辨率：3840x2160（4K）
- 帧率：60fps
- 视频编码：H.264
- 音轨：AAC 双声道 44.1kHz
- 文件大小：153.8MB

---

## 六、原始 30s 视频 URL（备查）

- 合并段1（s01+s02）：`https://aka.doubaocdn.com/s/aVSkOSa9qN`
- 合并段2（s03+s04）：`https://aka.doubaocdn.com/s/EsY8TRGsGV`

## 七、异常与处置备注

1. `image_to_video` 两次提交均一次成功，未遇额度不足。
2. video-ocr 提交出现 2 次瞬时错误（缺 task_id），重试成功。
3. mediakit `enhance-video` 对 EP040 持续异常（4 任务卡 running >1h），已改用 ffmpeg lanczos 升频 + minterpolate blend 插帧完成 4k/60fps。
4. 原带水印视频均保留备份（`video-wm-original.mp4`），未覆盖任何用户素材。
