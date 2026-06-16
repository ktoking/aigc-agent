# AI 漫剧生产仓库

本项目用于生产 AI 短剧 / AI 漫剧《末日重生：双生曙光》。仓库不是普通文本大纲，而是一套可持续迭代的“角色资产 + 场景资产 + 剧集分镜 + 视频提示词 + 制作规范”工作台。核心目标是让每一集都能按固定格式拆成 4 个 15 秒以内的竖屏视频段，并保持角色、人脸、场景、首尾帧连续。

## 项目定位

- 类型：末日重生、双女主、异能、囤货、基地建设、复仇反派线。
- 画幅：9:16 竖屏短剧。
- 单集时长：60 秒。
- 单集结构：4 段，每段 15 秒以内。
- 核心生产链路：故事记忆 -> 资产库 -> 剧集大纲 -> 连续性表 -> 分段故事板 -> 首尾帧 -> 图生视频 -> 剪辑交付。

## 核心故事

林晚是重生者和 SSS 级空间异能者，前世末日中为保护沈清雪而死。她重生回病毒爆发前 30 天，带着前世记忆开始囤货、验证空间能力、寻找沈清雪，并逐步揭开顾景辰和病毒计划的真相。沈清雪是 SSS 级精神系异能者，是林晚未来并肩建立幸存者基地的关键伙伴。

完整设定记忆见 [docs/story-memory.md](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/docs/story-memory.md)。

## 目录结构

```text
.
├── assets/
│   ├── characters/      # 角色卡、定妆图、表情、服装、动作姿势
│   ├── scenes/          # 场景卡和场景参考图
│   ├── props/           # 道具、异能特效、关键剧情物件
│   ├── enemies/         # 感染者、尸王等敌方资产
│   └── style/           # 全局风格、镜头语言、负面提示词
├── docs/
│   ├── story-memory.md  # 故事圣经、人设、视觉锚点、剧情规则
│   └── workflow.md      # AI 漫剧生产流程
├── episodes/
│   ├── EP001_rebirth-before-apocalypse/
│   └── EP002_awakening-and-stockpiling/
├── templates/           # 剧集、连续性、故事板模板
└── skills/              # 项目专属 Codex skill
```

## 资产库

### 角色

- `LIN_WAN_001`：林晚，重生者，SSS 级空间异能者。最高优先级参考图为 `assets/characters/double-hero-final-reference.png` 左侧人物。
- `SHEN_QINGXUE_001`：沈清雪，SSS 级精神系异能者。最高优先级参考图为 `assets/characters/double-hero-final-reference.png` 右侧人物。
- `GU_JINGCHEN_001`：顾景辰，科技集团继承人，前男友，病毒计划幕后参与者。

### 场景

- `SCENE_MODERN_APARTMENT`：林晚重生醒来的现代公寓。
- `SCENE_INDUSTRIAL_WAREHOUSE`：囤货爽点场景。
- `SCENE_SPACE_BASE`：林晚空间异能内部基地。
- `SCENE_APOCALYPSE_STREET`：前世末日废弃街道。
- `SCENE_SURVIVOR_BASE`：中后期幸存者基地。
- `SCENE_BASE_WALL`：最终尸潮攻防场景。

### 风格

所有生成必须遵守：

- [assets/style/global-style.md](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/assets/style/global-style.md)
- [assets/style/camera-language.md](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/assets/style/camera-language.md)
- [assets/style/negative-prompts.md](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/assets/style/negative-prompts.md)

## 剧集格式

每集目录固定包含：

```text
episodes/EPXXX_slug/
  episode.md
  continuity.md
  overview-storyboard.md
  segment_01_00-15s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    frames/
    output/
  segment_02_15-30s/
  segment_03_30-45s/
  segment_04_45-60s/
```

每集必须满足：

- 开头 5 秒有视觉钩子或情绪钩子。
- 每集至少一个反转、揭示或爽点释放。
- 结尾必须留下下一集悬念。
- 每段首帧继承上一段尾帧，除非使用明确转场。
- 双女主人脸优先级高于所有文字设定。
- 不生成完整长视频，先生成首尾帧，再做图生视频。

## 已有剧集

### EP001 重生前夜

林晚和沈清雪在末日街道被尸潮围困。林晚牺牲自己释放最后的空间异能，随后重生回末日前 30 天。钩子是手机日期显示 `2030年10月15日`。

目录：[episodes/EP001_rebirth-before-apocalypse](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/episodes/EP001_rebirth-before-apocalypse)

### EP002 觉醒囤货

林晚从重生震惊中恢复，验证空间异能仍在，立刻取消与顾景辰的晚宴并租下大型工业仓库开始囤货。顾景辰察觉异常，反派线首次进入现代时间线。

目录：[episodes/EP002_awakening-and-stockpiling](/Users/kaiyi.wang/IdeaProjects/ktoking/aigc-agent/episodes/EP002_awakening-and-stockpiling)

## 如何继续生成新剧集

后续生成 EP003、EP004 时，优先使用项目 skill：

```text
使用 skills/ai-microdrama-episode-production 生成 EP003，承接 EP002，保持现有格式。
```

生成前必须读取：

1. `docs/story-memory.md`
2. `docs/workflow.md`
3. 上一集的 `episode.md`、`continuity.md`、`overview-storyboard.md`
4. `assets/characters/*/00-character-card.md`
5. 本集会用到的场景卡、道具卡、风格文件
6. `templates/` 中对应模板

## 视频平台建议

本项目的文本和首尾帧结构适合接入即梦、可灵、豆包、Seedance、LiblibAI 等工具。建议生产顺序：

1. 用角色参考图生成本集关键首尾帧。
2. 每段使用 `first-frame.md` + `last-frame.md` + `prompt.md` 做图生视频。
3. 输出结果放入对应 `segment_xx/output/`。
4. 失败时只重做偏差段，不重做整集。

## 质量检查

- 林晚是否始终匹配参考图左侧人物。
- 沈清雪是否始终匹配参考图右侧人物。
- 林晚左眼下淡痣是否保留。
- 沈清雪是否保持短发和白色服装方向。
- 顾景辰是否保持表面温和、眼神隐藏控制欲。
- 本集是否有明确爽点、情绪点和结尾钩子。
- 四段视频首尾帧是否能自然衔接。
- 是否避免动漫、游戏 UI、AI 脸、过度血腥和低成本 cosplay 感。
