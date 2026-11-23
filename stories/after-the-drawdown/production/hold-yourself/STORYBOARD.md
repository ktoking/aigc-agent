---
compositionId: hold-yourself
duration_s: 60.0
canvas: { w: 1920, h: 1080, fps: 60 }
style:
  font: "EB Garamond / Inter / JetBrains Mono"
  palette: ["#FAF9F5", "#141413", "#CC785C", "#181715"]
assets: "Original GPT morning illustration and existing user confirmed soundtrack"
build_notes: ["project Chinese art direction in ART-DIRECTION.md", "one paused timeline per frame", "root owns captions and music"]
avoid: ["slideshow", "branch lines", "single still for whole film", "tiny-object theatre"]
---

## Frame 1 — 01-pressure

- src: compositions/frames/01-pressure.html
- duration: 16.533s
- span_sec: [0.0, 16.533]
- pacing: beat_cut
- mood: [dark, tense, cinematic]
- feel: opening rolls accumulate, strong energy at 6s, density drops at8s and surges at11s

### Groups

- **pressure** — free_design
  - span_sec: [0.0, 8.057]
  - free_design: { dominant_system: "oversized phone and descending market planes", primitives: ["kinetic-letter-in", "mask-reveal", "dolly-zoom"], density_topology: "accumulate then release" }
  - anchors: [1.649, 3.808, 5.921, 6.455, 8.057]
  - copy: ["跌怕了吗", "反复下跌", "示意画面"]
  - direction: 开场就是一个巨大的倾斜手机屏幕，右侧占半屏，下跌方块/蜡烛随拍子在空间中落下，左侧“跌怕了吗”两行特大字。3.808视角推进屏幕，视觉压力增大；5.921–6.455画面变为情绪质问“我是不是错了？”，不要真假账户金额。不能只做入场后漂浮。下一组在8.057强拍切换成全景文字空间。
- **identity** — free_design
  - span_sec: [8.057, 16.533]
  - free_design: { dominant_system: "compressed typographic space opens into clarity", primitives: ["mask-reveal", "staggered-exit", "negative-space-hold"], density_topology: "compress then clear" }
  - anchors: [8.057, 10.194, 12.307, 14.443, 16.533]
  - copy: ["计划", "家人", "明天", "生活", "亏损 ≠ 你"]
  - direction: 与第一组构图彻底不同。四个半透明纵向巨幅面板从两侧挤近，中间出现未来生活的字片。12.307四片退开，形成宽阔空间，中心出现大字“亏损 ≠ 你”，不等号逐拍完成，14.443把等号的一横变为一张大纸页的边缘，为下一幕纸页做视觉衔接。留出底字幕区域。

## Frame 2 — 02-perspective

- src: compositions/frames/02-perspective.html
- duration: 19.156s
- span_sec: [16.533, 35.689]
- pacing: beat_cut
- mood: [elegant, cinematic, warm]
- feel: medium rhythmic bed grows into high-energy22–26s, roll26.3–28.7 resolves before29.327

### Groups

- **history** — free_design
  - span_sec: [16.533, 29.327]
  - free_design: { dominant_system: "large archival paper spreads flip across time", primitives: ["3d-card-flip", "mask-reveal", "staggered-reveal"], density_topology: "reveal then reconsider" }
  - anchors: [16.533, 18.692, 20.828, 22.941, 25.078, 27.191, 29.327]
  - copy: ["2008–2009", "2020", "−57%", "−34%", "后来", "新的起点", "当时", "谁也不知道底在哪里"]
  - direction: 暖白纸面大跨页占满画面，两个年份在两页的上部。数据必须标清“标普500 峰谷跌幅，约数”，下方来源26px“来源：Charles Schwab · Bull vs. Bear (2024)”。2007–2009完整熊市峰谷约57%，2020约34%。16.533起先左页，18.692右页翻开；20.828纸张翻转为暖金的“后来”，22.941“新的起点”占横屏。25.078画面空间反向抽离/翻回未写满的纸面，出现“当时 / 谁也不知道底在哪里”。小注“历史指数表现，不代表个股或未来保证”。不能编造股价折线，不要分支线。信息层级清晰，数据画面要让人读得完。
- **affirmation** — free_design
  - span_sec: [29.327, 35.689]
  - free_design: { dominant_system: "expansive typographic release", primitives: ["kinetic-letter-in", "mask-reveal", "negative-space-hold"], density_topology: "one thought expands" }
  - anchors: [29.327, 31.44, 33.576, 35.689]
  - copy: ["不必完美", "也值得被肯定", "认真生活的人", "辛苦了"]
  - direction: 纸面依次展开，29.327用巨大“完美”轮廓字组成框，31.44纸框向边缘打开，显出“也值得被肯定”。33.576转成一张横向手写感卡片“认真生活的人 / 辛苦了”，大尺度而非小卡片UI。这一场情绪安静但图形仍在呼吸式打开，不用无意义的旋转。底部字幕由根接续。

## Frame 3 — 03-life

- src: compositions/frames/03-life.html
- duration: 24.311s
- span_sec: [35.689, 60.0]
- pacing: beat_cut
- mood: [warm, cinematic]
- feel: sustained fill35.9–40.38; hold and next fill43–45; brief accent49–51; energy drops52 and56

### Groups

- **agency** — free_design
  - span_sec: [35.689, 52.175]
  - free_design: { dominant_system: "three full-height panels unfold into personal agency", primitives: ["3d-card-flip", "staggered-reveal", "mask-reveal"], density_topology: "open one by one then unite" }
  - anchors: [35.689, 37.825, 39.938, 42.075, 44.188, 46.324, 48.46, 50.573, 52.175]
  - copy: ["有依据的坚持", "理由", "还成立吗", "时间", "这笔钱能等吗", "风险", "扛得住吗", "调整，也是一种坚持", "把生活留在手里"]
  - direction: 深墨蓝底，35.689一张大计划纸展开；37.825–44.188三扇高而宽的立体面板依次转正点亮，分别对应理由/时间/风险，面板上同时保留问题。不要像三张网页小卡片，形成全屏建筑性空间。46.324三面板像书页一样收束，金色标题“调整，也是一种坚持”横向展开；48.46强化保留余地，50.573三片向左右打开为窗景做准备。不要结尾台阶或回升行情。
- **life** — free_design
  - span_sec: [52.175, 60.0]
  - free_design: { dominant_system: "window opens onto warm everyday life", primitives: ["mask-reveal", "negative-space-hold"], density_topology: "expand then breathe" }
  - anchors: [52.175, 54.799, 56.935, 59.002]
  - copy: ["账户之外", "还有生活", "你的人生", "还很长"]
  - direction: 52.175暖光从右侧向左推开，assets/morning.png充满画面且人物在右，大字在左干净暗墙。使用无滤镜原画面，做干净矩形开窗遮罩和温柔推镜，独立光影几何片轻移。54.799主字替换“你的人生 / 还很长”，56.935最后强调落稳，59.002收束，不黑屏。生成插画只出现在最后8秒，不能取代前面动态图形。结尾字幕保持足够对比度。
