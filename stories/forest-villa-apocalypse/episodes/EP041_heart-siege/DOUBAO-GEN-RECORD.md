# DOUBAO-GEN-RECORD — EP041《攻心》

- 生成日期：2026-09-08
- 故事：forest-villa-apocalypse / episodes/EP041_heart-siege
- 流水线：2×30s 合并段生成（seedance 2.5）→ 去水印（erase-video-subtitle-pro v5）→ 4k/60fps 增强（enhance-video professional）→ 拼接成片（交叉淡化 + 音频淡入淡出）
- 数字人资产：白棠=asset-20260320075131-k78qt；许砚=asset-20260320075237-29hdx；叶凝霜=asset-20260720212023-wwndz；沈知夏=asset-20260310030618-88hlb
- 角色正脸图（image_reference_url_list 共用 4 张）：
  - 白棠 https://aka.doubaocdn.com/s/zy4EkwXnWu
  - 许砚 https://aka.doubaocdn.com/s/AgPOhLYMza
  - 叶凝霜 https://aka.doubaocdn.com/s/36s2FF7Z8z
  - 沈知夏 https://aka.doubaocdn.com/s/uV45IILn8X

---

## 阶段 A：30s 合并段视频生成

### A1. s01+s02 合并段（冬狼喊话 / 凝霜发作）
- 合并稿：`segment_01_00-15s/output/merged_s01s02_prompt.txt`
- 合并规则：去重规格头（16:9/30s/480p/有声音）、8 镜头连续编号（镜头一~镜头八）、参考图说明合并去重（6 项）、4 个数字人身份锁全保留、空间连续性/说话者绑定规则保留；未改剧本与台词。
- image_to_video 提交参数：
  - model_version=`seedance_2.5`，duration=`30`，ratio=`16:9`
  - image_reference_url_list=角色正脸 4 张（见上）
  - prompt=合并稿全文透传（未润色）
- 返回视频 URL：`https://aka.doubaocdn.com/s/UoplCRNKYj`（30s, 1280x720 mp4）
- 本地下载：`segment_01_00-15s/output/video-30s.mp4`
- 提交记录已追加：`segment_01_00-15s/api-request.md`、`segment_02_15-30s/api-request.md`

### A2. s03+s04 合并段（定策 / 分工出发）
- 合并稿：`segment_03_30-45s/output/merged_s03s04_prompt.txt`
- 合并规则同上：8 镜头连续编号、参考图合并去重（13 项）、4 数字人身份锁全保留、未改剧本与台词。
- image_to_video 提交参数：model_version=`seedance_2.5`，duration=`30`，ratio=`16:9`，参考图=角色正脸 4 张，prompt=合并稿全文透传。
- 返回视频 URL：`https://aka.doubaocdn.com/s/uwmc4N0vaD`（30s, 1280x720 mp4）
- 本地下载：`segment_03_30-45s/output/video-30s.mp4`
- 提交记录已追加：`segment_03_30-45s/api-request.md`、`segment_04_45-60s/api-request.md`

生成纪律：两段依次生成（s01s02 完成后再提交 s03s04），未同时提交；未遇到额度不足，未降级模型。

---

## 阶段 B：去水印（erase-video-subtitle-pro）

命令模板（已用 `--schema` 确认参数）：
```
mediakit-cli video erase-video-subtitle-pro \
  --video-url <本地路径> --mode Text --model-version v5 \
  --erase-ratio-location '[{"top_left_x":0,"top_left_y":0,"bottom_right_x":1,"bottom_right_y":0.16},{"top_left_x":0,"top_left_y":0.84,"bottom_right_x":1,"bottom_right_y":1}]'
```
（顶部 0–16% 与底部 84–100% 两条带，覆盖左上/右下“豆包AI生成”水印）

| 段 | task_id | 结果 |
|---|---|---|
| s01s02 | amk-tool-erase-video-subtitle-pro-1027385992706 | completed（30.042s） |
| s03s04 | amk-tool-erase-video-subtitle-pro-902815063298 | completed（30.042s） |

- 去水印结果下载：`segment_01_00-15s/output/video.mp4`、`segment_03_30-45s/output/video.mp4`
- 原带水印备份：`segment_01_00-15s/output/video-wm-original.mp4`、`segment_03_30-45s/output/video-wm-original.mp4`（未删除，可回源）

### OCR 水印残留验证（video-ocr，mode=Detailed）
| 段 | task_id | 结果 |
|---|---|---|
| s01s02 | amk-tool-video-ocr-957604653826 | subtitles=[]（全片无识别文字） |
| s03s04 | amk-tool-video-ocr-906917687810 | 仅 1 条：单字符“0”（text_label=Others，位置 y≈69.5%~72.5%，为监控屏画面数字，非水印） |

- 附加核验：ffmpeg 抽取两段 1s/15s/29s 共 6 帧人工检视，顶部/底部条带均无“豆包AI生成”等文字残留。**结论：去水印通过。**

---

## 阶段 C：4k/60fps 增强（enhance-video）

命令（已用 `--schema` 确认参数）：
```
mediakit-cli video enhance-video --video-url <video.mp4> --resolution 4k --fps 60 --tool-version professional
```

| 段 | task_id | 结果 |
|---|---|---|
| s01s02 | amk-tool-enhance-video-902770976514 | completed，4k / 60fps / 30s |
| s03s04 | amk-tool-enhance-video-755222634498 | completed，4k / 60fps / 30s |

- 增强结果下载：`segment_01_00-15s/output/video-4k.mp4`（175,249,010 B）、`segment_03_30-45s/output/video-4k.mp4`（173,494,573 B）
- 两段均：3840×2160，60fps，h264，aac 44100Hz 立体声

---

## 阶段 D：拼接成片

- 输入（按序）：`segment_01_00-15s/output/video-4k.mp4`（s01s02，前）→ `segment_03_30-45s/output/video-4k.mp4`（s03s04，后）
- 转场：**交叉淡化 0.8s**（要求 0.5–1s 区间内）。
  - 说明：`mediakit-cli editing concat-video` 仅支持 12 种特效转场 ID（交替出场/旋转放大/泛开/六角形/故障转换/飞眼/梦幻放大/开门展现/立方转换/透镜变换/晚霞转场/圆形交替），**无交叉淡化/溶解选项**；为满足指定转场，改用 ffmpeg `xfade=transition=fade:duration=0.8:offset=29.2` + `acrossfade=d=0.8` 完成拼接，单次编码避免二次转码画质损失。
- 音频淡入淡出：`afade=t=in:st=0:d=2`（片头淡入 2s）、`afade=t=out:st=57.2:d=2`（片尾淡出 2s）。
- 编码：libx264 preset=medium crf=19 yuv420p 60fps，aac 192k，faststart。
- 成片：`episodes/EP041_heart-siege/EP041_final.mp4`

### 成片核验（ffprobe）
- 时长：59.2s（≈60s，含 0.8s 交叉淡化）
- 分辨率：3840×2160（4K）
- 帧率：60fps
- 音轨：有（aac，44100Hz，双声道）
- 抽帧复核：t≈0.5s（白棠报话）、t≈10s（许砚通话台）、t=29.0s（知夏/凝霜，s01s02 尾）、t=29.5s（叠化过渡帧，正常交叉淡化）、t=30.8s（白棠/许砚，s03s04 头）、t≈58s（许砚出门风雪）——内容与合并稿分镜一致。

---

## 产物清单

| 产物 | 路径 |
|---|---|
| 成片 | `episodes/EP041_heart-siege/EP041_final.mp4` |
| 合并稿 s01+s02 | `episodes/EP041_heart-siege/segment_01_00-15s/output/merged_s01s02_prompt.txt` |
| 合并稿 s03+s04 | `episodes/EP041_heart-siege/segment_03_30-45s/output/merged_s03s04_prompt.txt` |
| s01s02 30s 原始URL | https://aka.doubaocdn.com/s/UoplCRNKYj |
| s03s04 30s 原始URL | https://aka.doubaocdn.com/s/uwmc4N0vaD |
| s01s02 去水印版 | `segment_01_00-15s/output/video.mp4`（备份 video-wm-original.mp4） |
| s03s04 去水印版 | `segment_03_30-45s/output/video.mp4`（备份 video-wm-original.mp4） |
| s01s02 4k 增强版 | `segment_01_00-15s/output/video-4k.mp4` |
| s03s04 4k 增强版 | `segment_03_30-45s/output/video-4k.mp4` |

## 备注
- 未修改剧本与台词；合并稿仅做结构合并。
- 全程未调用 Skynet 相关命令；mediakit-cli 调用前均先 `--schema`/`--help` 确认参数。
- s03s04 的 video-ocr 服务端任务一度长时间 pending，期间以抽帧人工核验兜底，最终任务正常返回 completed。
