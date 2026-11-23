# 云端执行包 v2：连续叙述，取消等待

本版取代旧的固定60秒/四段各15秒提示词。正文、人物、画风和故事图计划保留，改为默认5.0字/秒、逐句0帧空档，让镜头跟着正文节奏走。配音由用户后期生成和控制倍速，本包不生成配音、不烧录字幕。

## 使用

上传本包并解压。将`CLOUD-CODEX-PROMPT-v2.md`全文发给云端Codex，或在文件可读取时发送：

> 请读取CLOUD-CODEX-PROMPT-v2.md全文，按v2流程直接执行。使用scripts-and-shots.json中的八集原文，先运行retime_text.py生成按5字/秒连续排时的字幕和时间线，再据此制作图片与剪辑视频。句间、段间、集间0帧空档，取消凑满60秒/15秒的等待。你不生成语音；交付无音轨视频和独立SRT，并标明字幕尚未与我后期生成的语音对齐。不要只改字幕而继续用旧视频。

## 文件

- `CLOUD-CODEX-PROMPT-v2.md`：完整独立提示词，含八集正文、67张故事图清单和新验收规范。
- `scripts-and-shots.json`：正文、镜头计划及v2时间策略，无旧60秒执行时间线。
- `retime_text.py`：仅用Python标准库，生成连续SRT/VTT、逐集正文和唯一帧时间线。
- `estimated-timing/`：已生成八集估算字幕、合集字幕、正文与时间线；不是新成片，不要直接套回旧视频。
- `references/`：4张画风、人物、场景参考及hash清单；许棠参考只取外观，不继承开门背景。
- `analysis/comparison-report.md`：与用户抖音版本的具体对照及验证边界。
- `analysis/reference-cue-observations.json`：参考字幕5fps抽样区间；不是音轨时间戳。
- `analysis/reference-contact-sheet.jpg`：参考视频每秒画面拼图。

重算：

```bash
python3 retime_text.py --source scripts-and-shots.json --cps 5.0 --fps 30 --out estimated-timing
```

默认第一集38.4秒、八集合计343.6秒，均为完整正文的文字估算。字幕文件名中`text-estimate`明确标记其性质。云端生图/渲染能力仍需实际预检；本轮只更新执行流程及时间稿，未生成v2视频或配音。

