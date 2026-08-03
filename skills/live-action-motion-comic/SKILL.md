---
name: live-action-motion-comic
description: 制作真人静帧动态漫短剧段落：生成 3-4 张真人镜头图、第一人称内心独白与角色对白、豆包情绪配音、气泡字幕、音效和 HyperFrames 竖屏 MP4。用户提到真人动态漫、静帧动态漫、图切镜、HyperFrames 短剧、豆包配音或需要低成本替代整段图生视频时使用。
---

# 真人静帧动态漫

## 目标

用 3-4 张 9:16 真人镜头图完成一个 15 秒段落。HyperFrames 负责切镜、慢推、轻微漂移、字幕、气泡、音效和混音；不要默认把一对首尾帧提交给视频 API。

## 开始前

1. 读取仓库和目标 story 的 `AGENTS.md`、`docs/production-rules.md`、`docs/story-memory.md`、相关角色卡、目标 segment 的 `shot-list.md` 与 `storyboard.md`。
2. 读取目标 HyperFrames 项目的 `DESIGN.md` 后再编辑 HTML。
3. 复用已存在的角色、场景和镜头图；只有缺图才生成。每个新图都使用真人角色定妆图作参考。
4. 角色 voice_type 以 story 的 `production-rules.md` 为唯一来源。不要因情绪切换音色。

## 段落结构

- 每段 15 秒、9:16、3-4 个镜头；每 3-5 秒改变一次画面或信息。
- 生产文档以“分镜 01 / 02 / 03 / 04”组织，不在 `storyboard.md`、`shot-list.md`、`prompt.md`、`director-promt.txt` 写秒数或时间区间。几个镜头图就写几个分镜；每个分镜下面依次写画面、运镜、旁白、角色对白、音效。
- 渲染 HTML 可以保留内部 `data-start` / `data-duration`，它只服务于合成，不应反向污染创作提示词或分镜文档。
- `first-frame.png` / `last-frame.png` 只作相邻段连续性锚点，实际播放读取 `frames/shots/shot_*.png`。
- 内心独白使用男主第一人称“我”，不是全知第三人称旁白；对白采用短句，避免在动作镜头要求口型。
- 先试听全部角色分轨，再把音频按真实 `ffprobe` 时长回填到时间线。自然语速总时长超过 15 秒时，先精简台词或谨慎加速，绝不把对白重叠。

## 图像与动态

每个镜头只使用一种主运镜：明显推近、明显拉远、横移或轻微漂移。静帧动态漫的位移要让观众能感知镜头在动，但不得裁掉人物主体或制造空黑边；以独立镜头图实现表情变化，不做真人脸部扭曲；用气泡、字幕和反应镜头承接台词。

保留真人电影感、清晰人物轮廓和干净大形；避免动漫线稿、游戏 UI、红圈锁定框、镜头编号/时间码水印、霓虹网格、满屏微纹理、过量特效和换脸换装。

## 豆包语音

- 使用豆包语音合成 2.0：`X-Api-Resource-Id: seed-tts-2.0`。
- API Key 只能从 macOS Keychain 读取，绝不写入仓库、提示词、日志或成片元数据。
- 每句单独生成 MP3，并在 `context_texts` 中使用以 `#` 开头的情绪指令；指令应说明身份、情绪、节奏、停顿和禁止项。
- 同一角色全季固定 voice_type；通过语音指令改变压抑、惊慌、克制或命令感。

## HyperFrames 合成与验收

1. 在 root 直接挂载 `<audio>` 分轨；图片镜头使用不重叠的 `.clip` 与 `data-start` / `data-duration`。
2. 构建一个暂停的 GSAP timeline，并注册到 `window.__timelines[compositionId]`。
3. 对每次镜头切换使用短淡入，字幕和气泡按对应音频起点入场；最后一个命令/钩子预留音效落点。
4. 运行 `npx hyperframes check --json`，修复错误；再运行 draft render。
5. 用 `ffprobe` 校验输出存在、时长约 15 秒且含 AAC 音频流。将 MP4 放到该 composition 的 `output/`，并在 segment 的 `output/` 留可追溯链接或副本。

## 最低交付

- `shot-list.md` 与 3-4 张 `frames/shots/` 图片。
- 已锁定的台词、voice_type、情绪指令和分轨音频。
- 可复查的 HyperFrames `index.html`、`DESIGN.md`、`VOICEOVER.md`。
- 含声音的 15 秒 MP4，且报告真实文件路径、时长与大小。
