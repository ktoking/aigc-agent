---
name: video-opening-title
description: Use when adding a premium opening title sequence to an existing video — Chinese title + English subtitle + decorative lines + fade in/out, magazine-cover style with Songti / Didot / Futura fonts. Works on any story package or standalone video file.
---

# 视频开幕标题

## 目的

给已有视频添加高端杂志风开幕标题序列：中文主标题 + 英文副标题 + 装饰细线 + 作者署名，白色字体，渐显→保持→渐隐。适用于 AI 漫剧 / 短剧 / MV 的片头。

## 必须遵守

- 不写死任何剧本的人名、设定或标题；所有文本通过参数传入。
- 原视频文件不覆盖，输出到用户指定的新路径。
- 音频流原样 copy，不重新编码。
- 标题 PNG 为透明背景，通过 ffmpeg `fade`（alpha 通道）+ `overlay` 实现渐显渐隐。
- 依赖：Python 3 + Pillow、ffmpeg（需支持 `overlay`、`fade`、`format` 滤镜）。
- 字体使用 macOS 系统字体；若在非 macOS 环境运行，需通过 `--font-cn` / `--font-en` / `--font-sub` 指定可用字体路径。

## 快速使用

```bash
python3 skills/video-opening-title/scripts/add_opening_title.py \
  --input  /path/to/input.mp4 \
  --output /path/to/output_opening.mp4 \
  --title-cn "荒轨" \
  --title-en "WASTELINE" \
  --subtitle "A POST-APOCALYPTIC TALE" \
  --author "西瓜终结者"
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `--input` | ✅ | — | 输入视频路径 |
| `--output` | ✅ | — | 输出视频路径 |
| `--title-cn` | ✅ | — | 中文主标题（宋体大号） |
| `--title-en` | ❌ | — | 英文主标题（Didot 衬线体，全大写+宽字间距） |
| `--subtitle` | ❌ | — | 英文副标题（Futura，全大写） |
| `--author` | ❌ | — | 作者名（显示为 "CREATED BY 作者名"） |
| `--show-duration` | ❌ | 6 | 标题总显示时长（秒） |
| `--fade-in` | ❌ | 1.2 | 渐显时长（秒） |
| `--fade-out` | ❌ | 1.2 | 渐隐时长（秒），从 `show-duration - fade-out` 处开始 |
| `--font-cn` | ❌ | 系统宋体 | 中文字体路径（.ttc/.ttf） |
| `--font-en` | ❌ | 系统 Didot | 英文主标题字体路径 |
| `--font-sub` | ❌ | 系统 Futura | 英文副标题字体路径 |
| `--title-size` | ❌ | 168 | 中文主标题字号 |
| `--en-size` | ❌ | 52 | 英文主标题字号 |
| `--tracking` | ❌ | 14 | 英文主标题字间距（px） |
| `--crf` | ❌ | 18 | 视频编码 CRF（越小画质越好文件越大） |
| `--preset` | ❌ | fast | x264 编码 preset |

## 布局规格（1280×720）

```
y=195  ── 顶部装饰线（120px宽，40%透明度）──
y=215  「中文主标题」宋体 168号 纯白
y=415  「ENGLISH TITLE」Didot 52号 85%白 宽字间距
y=500  ── 中间装饰线（200px宽，40%透明度）──
y=525  「SUBTITLE」Futura 20号 60%白
y=580  CREATED BY 「作者名」
```

其他分辨率按比例自适应（脚本以视频实际宽高计算居中位置）。

## 动画时序

```
0s          ─── 标题开始渐显
fade-in s   ─── 完全显示
(show - fade-out) s ─── 开始渐隐
show s      ─── 完全消失，后续正片不受影响
```

## 脚本内部流程

1. 读取输入视频分辨率。
2. 用 Pillow 生成同尺寸透明背景 PNG，按布局绘制文字和装饰线。
3. ffmpeg `-loop 1` 循环 PNG → `format=rgba` → `fade in/out`（仅 alpha 通道）→ `trim` 到显示时长 → `overlay` 叠加到原视频。
4. 音频 `-c:a copy` 原样保留。
5. 输出到 `--output`。

## 常见问题

- **ffmpeg 报 `No such filter: drawtext`**：本 skill 不使用 drawtext，文字由 Pillow 预渲染为 PNG，再用 overlay 叠加，因此不需要 libfreetype。
- **中文显示为方框**：指定的字体不包含中文字形，换用 `--font-cn` 指向宋体/苹方/黑体等中文字体。
- **输出文件很大**：调高 `--crf`（如 20/23）或换 `--preset medium`。
- **标题显示时间不对**：`--fade-out` 是从 `show-duration - fade-out` 开始渐隐，确保 `fade-in + fade-out < show-duration`。
