# 《您已安全》

## 当前制作优先级 · 2026-10-21 六分钟原版重做

- 用户明确指定恢复六分钟原版：`production/photoreal-6min-v1`、`episodes/SF004_6min-photoreal-original`，360秒、12段、96镜。`source/director-design-v2.md`为只读情节来源，旧两分钟版本归档，不再是本次制作目标。
- 16:9真人写实，正常干燥清爽日光；不要阴雨、湿地或脏旧灰暗摄影。洪水/海岸保留剧情水体，矿井仅必要岩尘，不删除相关剧情。
- 全程陈默第一人称转述，无音轨MP4＋独立SRT/VTT，不烧录字幕。7.5个非标点字/秒为文字估时；镜头按原版3/4秒时点，剩余为留白，母亲消失后第80镜完整3秒无字幕。
- 96张正式图片重新生成。内置imagegen＋本地FFmpeg固定图片流程，叠化精确0.1秒（30fps下3帧），占后镜原有时间。不接视频API、不使用zoompan、不宣称连续肢体动画。
- 原稿的二维竖屏和多声对白设计被上述用户指令覆盖；下文旧版本说明仅作历史记录，不覆盖本节。完整保留洪水、矿井、战区、隔离、拒食、全球求助、母亲消失、归零、砸手机、海边与座机结尾。
- 任何完成状态以本轮文件及QA为准，不沿用两分钟版本的播放记录。沿用本仓库不使用Skynet及hooks的规则。

当前已交付：[六分钟原版真人横屏](output/photoreal-6min-v1/)，360秒、96张新图、95条独立字幕、无音轨。整片解码、0.1秒转场采样与1倍速完整播放已核验。提示词、图片、时间线及QA见[当前制作项目](production/photoreal-6min-v1/)。


当前交付为用户选定的 **R2冷暖电影真人写实、16:9横屏图片叙事视频v1**。

## 直接查看

- [成片MP4](output/photoreal-v1/you-are-safe-photoreal-v1.mp4)
- [独立SRT](output/photoreal-v1/you-are-safe.zh-CN.srt) / [VTT](output/photoreal-v1/you-are-safe.zh-CN.vtt)
- [第一人称配音文案](output/photoreal-v1/narration.txt)
- [本地外挂字幕播放器](output/photoreal-v1/index.html)

1920×1080输出、30fps、112.8秒/3384帧，20张独立事件图，固定构图和4帧短叠化。全程陈默第一人称文字，无音轨、无烧录字幕；由用户自行配音。786个非标点字以7.5字/秒估计104.8秒，另有8秒关键情绪留白。字幕为文字估时，尚未对齐真实配音。

源图实际1672×941，交付放大至1080p。图片事件状态与短叠化不等于连续角色动画。

## 可编辑制作源

- production/photoreal-v1/BRIEF.md：当前确认要求。
- production/photoreal-v1/timeline.json：帧时间线、文案、留白与图片绑定。
- production/photoreal-v1/image-prompts.json、image-manifest.json：提示词、来源、尺寸、hash及重做。
- production/photoreal-v1/scripts/：字幕、固定镜头渲染、播放器和检查脚本。
- [技术检查](production/photoreal-v1/qa/technical-report.json)、[观看边界](production/photoreal-v1/qa/visual-review.md)、[实际编码画面总览](production/photoreal-v1/qa/encoded-overview.png)。
- episodes/SF003_photoreal-first-person/：四段实际区间的故事板、制作单与编码首尾帧。

已完成结构、完整解码、字幕文字/帧时间检查；正常1倍速播放到ended=true，并抽看关键画面。未发布或上传外部平台。

## 设计历史

- [六分钟原稿](source/director-design-v2.md)与episodes/SF001_6min-source：归档未改。
- [两分钟详细导演稿v2](docs/two-minute-detailed-director-prompts-v2.md)与episodes/SF002_2min-adaptation：历史二维、多声角色拍摄方案，当前以真人第一人称制作要求覆盖。
- [导演重写记录](docs/two-minute-director-rewrite-review.md)、[原稿设计检查](docs/design-review.md)。
- assets/style/photoreal-auditions-20261021/：R1/R2/R3摄影参考，用户选R2；漫画试镜与竖屏试图仅归档。

## 本地复现

从仓库根运行：

```bash
python3 stories/you-are-safe/production/photoreal-v1/scripts/write_subtitles.py
python3 stories/you-are-safe/production/photoreal-v1/scripts/render_film.py
python3 stories/you-are-safe/production/photoreal-v1/scripts/package_player.py
python3 stories/you-are-safe/production/photoreal-v1/scripts/verify_delivery.py
```

播放器需通过本地HTTP服务打开，文件本身也可直接导入剪辑软件。
