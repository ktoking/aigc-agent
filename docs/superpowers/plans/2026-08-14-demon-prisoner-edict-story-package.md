# Demon Prisoner Edict Story Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `stories/demon-prisoner-edict/` 创建《镇妖囚徒》原创半写实 3D 东方玄幻 story 包、EP001 四段 60 秒完整提示词，以及可直接用于后续动态漫制作的角色、场景、道具和 12 张关键分镜资产。

**Architecture:** 参考 `stories/forest-villa-apocalypse/` 的 story-local 文档、资产卡、剧集根文件和 segment 交付结构，但内容完全独立。先固定人物、场景、道具和视觉规范，再编写 EP001 的动作链与连续性，最后用内置图像生成按“角色锚点 → 场景锚点 → 连续分镜”的顺序生成并验收资产。

**Tech Stack:** Markdown story package、内置 image generation、仓库现有 episode validator、`rg`/`find`/ImageMagick 或 `sips` 图像元数据检查。

## Global Constraints

- 新内容只能写入 `stories/demon-prisoner-edict/`，设计与计划文档除外。
- 9:16，60 秒，4 个不超过 15 秒的 segment，目录名固定为 `segment_01_00-15s` 至 `segment_04_45-60s`。
- 风格固定为半写实 3D 东方玄幻动画电影；冷灰蓝低饱和、体积雾、空气透视、浅景深、自然皮肤与布料。
- 不复制参考作品角色、对白、专有设定或逐镜构图；只采用通用电影镜头方法。
- 避免过度锐化、鱼鳞状网格、蜡像皮肤、满屏微纹理、七彩霓虹、游戏 UI、文字、水印和红圈标记。
- 每段使用 3 张主要关键分镜图，共 12 张；首尾帧从对应分镜资产中选用。
- 本计划不提交任何付费视频 API 任务。
- 保留工作区现有无关修改，不批量暂存或提交其他 story 的文件。

---

### Task 1: 创建 Story 骨架与本地生产规则

**Files:**
- Create: `stories/demon-prisoner-edict/AGENTS.md`
- Create: `stories/demon-prisoner-edict/README.md`
- Create: `stories/demon-prisoner-edict/docs/story-memory.md`
- Create: `stories/demon-prisoner-edict/docs/production-rules.md`
- Create: `stories/demon-prisoner-edict/docs/workflow.md`
- Create: `stories/demon-prisoner-edict/docs/season-arc.md`
- Create: `stories/demon-prisoner-edict/docs/audience-strategy.md`
- Create: `stories/demon-prisoner-edict/assets/style/global-style.md`
- Create: `stories/demon-prisoner-edict/assets/style/camera-language.md`
- Create: `stories/demon-prisoner-edict/assets/style/negative-prompts.md`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-08-14-demon-prisoner-edict-story-design.md` and repository-level `AGENTS.md`.
- Produces: Story ID、角色/场景/道具 ID、视觉前缀、负面提示词和连续性规则，供 Task 2–5 使用。

- [ ] **Step 1: 从参考包提取结构字段**

Run:

```bash
sed -n '1,220p' stories/forest-villa-apocalypse/docs/production-rules.md
sed -n '1,180p' stories/forest-villa-apocalypse/docs/workflow.md
```

Expected: 只提取文件职责、ID 锁定、上一集继承、生成和 QA 字段，不复制末日剧情规则。

- [ ] **Step 2: 写入 story-local 文档和风格规范**

要求明确以下固定 ID：`DPE_SHEN_JIN_001`、`DPE_A_LI_001`、`DPE_HAN_XIAO_001`、`DPE_FOG_VALLEY_CART_001`、`DPE_CART_INTERIOR_001`、`DPE_ALTAR_ROAD_001`、`DPE_BONE_NEEDLE_001`、`DPE_RUNE_SHACKLE_001`、`DPE_DEMON_BLADE_001`。

- [ ] **Step 3: 验证骨架内容**

Run:

```bash
find stories/demon-prisoner-edict -maxdepth 3 -type f | sort
rg -n "DPE_SHEN_JIN_001|半写实 3D|红圈|游戏 UI" stories/demon-prisoner-edict
```

Expected: 10 个基础文档存在，角色 ID 和视觉禁用项均可检索。

- [ ] **Step 4: 独立提交 Story 骨架**

```bash
git add stories/demon-prisoner-edict/AGENTS.md stories/demon-prisoner-edict/README.md stories/demon-prisoner-edict/docs stories/demon-prisoner-edict/assets/style
git commit --no-verify -m "feat: scaffold demon prisoner story"
```

### Task 2: 创建角色、场景与道具资产卡

**Files:**
- Create: `stories/demon-prisoner-edict/assets/characters/DPE_SHEN_JIN_001/character-card.md`
- Create: `stories/demon-prisoner-edict/assets/characters/DPE_A_LI_001/character-card.md`
- Create: `stories/demon-prisoner-edict/assets/characters/DPE_HAN_XIAO_001/character-card.md`
- Create: `stories/demon-prisoner-edict/assets/scenes/DPE_FOG_VALLEY_CART_001/scene-card.md`
- Create: `stories/demon-prisoner-edict/assets/scenes/DPE_CART_INTERIOR_001/scene-card.md`
- Create: `stories/demon-prisoner-edict/assets/scenes/DPE_ALTAR_ROAD_001/scene-card.md`
- Create: `stories/demon-prisoner-edict/assets/props/DPE_BONE_NEEDLE_001/prop-card.md`
- Create: `stories/demon-prisoner-edict/assets/props/DPE_RUNE_SHACKLE_001/prop-card.md`
- Create: `stories/demon-prisoner-edict/assets/props/DPE_DEMON_BLADE_001/prop-card.md`
- Create: `stories/demon-prisoner-edict/assets/image-generation-prompts.md`

**Interfaces:**
- Consumes: Task 1 固定 ID、视觉前缀和负面提示词。
- Produces: 所有图像生成调用共用的角色身份描述、场景空间关系、道具比例和逐资产最终提示词。

- [ ] **Step 1: 写入三张角色卡**

每张角色卡必须包含年龄、脸型、五官、发型、服装、伤势或标记、姿态、表情范围、禁止漂移项和参考图清单。

- [ ] **Step 2: 写入三张场景卡与三张道具卡**

场景卡必须固定光线、天气、空间方向和可见锚点；道具卡必须固定材质、颜色、比例、持有关系及禁止变形项。

- [ ] **Step 3: 汇总图像生成提示词**

`image-generation-prompts.md` 必须按生成顺序列出：3 张角色锚点、3 张场景锚点、3 张道具锚点、12 张 EP001 分镜图和 1 张封面，共 22 个独立提示词；所有图禁止文字和水印。

- [ ] **Step 4: 验证资产卡不存在占位内容**

Run:

```bash
rg -n "TBD|TODO|待补|占位" stories/demon-prisoner-edict/assets
```

Expected: no matches.

- [ ] **Step 5: 独立提交资产卡**

```bash
git add stories/demon-prisoner-edict/assets
git commit --no-verify -m "feat: define demon prisoner visual assets"
```

### Task 3: 编写 EP001 剧集根文件

**Files:**
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/episode.md`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/overview-storyboard.md`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/continuity.md`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/image-manifest.md`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/qa-checklist.md`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/publish-package.md`

**Interfaces:**
- Consumes: Task 1 剧情规则与 Task 2 资产 ID。
- Produces: 四段故事节拍、完整对白、12 镜头编号 `EP001-S01-01` 至 `EP001-S04-03`、跨段继承状态和图像清单。

- [ ] **Step 1: 写入完整 60 秒剧本**

对白固定包含：“别出声，他们在找醒过来的人。”、“原来真有一个没死透。”、“停。”、“敕令者……不是百年前就死绝了吗？”、“我终于等到你了。”；对白之外只保留必要环境声，不增加解释性长旁白。

- [ ] **Step 2: 写入总分镜和连续性表**

12 个镜头必须逐一写清画面、景别、动作、运镜、台词/声音、关键帧文件名，以及上一镜头如何继承到下一镜头。

- [ ] **Step 3: 写入图像清单、QA 与发布包**

发布包包含 3 个原创标题、封面大字建议（后期添加，不生成进图片）、评论引导和 3 个标签方向。

- [ ] **Step 4: 验证镜头编号和四段覆盖**

Run:

```bash
for s in 01 02 03 04; do rg -c "EP001-S${s}-0[1-3]" stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/overview-storyboard.md; done
```

Expected: each command reports at least 3 matches.

- [ ] **Step 5: 独立提交剧集根文件**

```bash
git add stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows
git commit --no-verify -m "feat: write demon prisoner episode one"
```

### Task 4: 编写四个 Segment 交付包

**Files:**
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_01_00-15s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,director-promt.txt,api-request.md}`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_02_15-30s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,director-promt.txt,api-request.md}`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_03_30-45s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,director-promt.txt,api-request.md}`
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_04_45-60s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,director-promt.txt,api-request.md}`
- Create: four `frames/.gitkeep` files and four `output/.gitkeep` files under the segment directories.

**Interfaces:**
- Consumes: Task 3 镜头编号、对白和跨段连续性状态。
- Produces: 可人工审阅、可交给图生视频模型的四段完整提示词和 API 交接记录。

- [ ] **Step 1: 写入 Segment 01 和 02**

每段恰好包含 3 个分镜；按分镜而非机械逐秒组织正文，同时在导演提示词中保留镜头次序、动作因果和总时长约束。

- [ ] **Step 2: 写入 Segment 03 和 04**

Segment 03 明确“放箭 → 沈烬抬眼说停 → 箭、雨、刀同时凝固”；Segment 04 明确“牵手穿行 → 眼角渗血 → 时间恢复 → 妖王影子显现”。

- [ ] **Step 3: 补齐首尾帧职责和 API 记录模板**

每个 `api-request.md` 状态写为“未提交”，不得包含 key、任务 ID、签名 URL 或虚构返回值。

- [ ] **Step 4: 运行结构验证**

Run:

```bash
for d in stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/segment_*; do for f in storyboard.md first-frame.md last-frame.md prompt.md director-promt.txt api-request.md; do test -s "$d/$f" || exit 1; done; test -d "$d/frames"; test -d "$d/output"; done
```

Expected: exit 0.

- [ ] **Step 5: 独立提交 Segment 包**

```bash
git add stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows
git commit --no-verify -m "feat: add demon prisoner segment prompts"
```

### Task 5: 生成并落盘图像资产

**Files:**
- Create: character reference PNGs under `stories/demon-prisoner-edict/assets/characters/*/references/`.
- Create: scene reference PNGs under `stories/demon-prisoner-edict/assets/scenes/*/references/`.
- Create: prop reference PNGs under `stories/demon-prisoner-edict/assets/props/*/references/`.
- Create: `shot-01.png`, `shot-02.png`, `shot-03.png`, `first-frame.png`, `last-frame.png` under each segment `frames/`.
- Create: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/cover-assets/cover-clean.png`.
- Modify: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/image-manifest.md`.

**Interfaces:**
- Consumes: Task 2 的 22 个独立提示词和 Task 4 的首尾帧职责。
- Produces: 所有后续 HyperFrames 或图生视频任务需要的本地 PNG 资产。

- [ ] **Step 1: 生成角色锚点并视觉验收**

使用内置 image generation，每个角色独立调用。先生成沈烬，再把已确认的人物外观文字锁传递到阿璃和韩枭提示词；检查五官、服装、轮廓和无文字要求。

- [ ] **Step 2: 生成场景与道具锚点并落盘**

每个资产独立调用，生成后复制到对应 `references/`，不得只保留在默认生成目录。

- [ ] **Step 3: 按镜头顺序生成 12 张分镜图**

每次调用只生成一个镜头；提示词重复角色不变量、场景锚点和上一镜头末态。若人物身份明显漂移，只重做该镜头。

- [ ] **Step 4: 选择首尾帧并生成封面**

将每段 shot-01/shot-03 复制为 first-frame/last-frame；封面使用凝固箭雨英雄画面，但图片内不生成标题文字。

- [ ] **Step 5: 检查资产数量、尺寸和格式**

Run:

```bash
find stories/demon-prisoner-edict -type f -name '*.png' | sort
find stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows -type f -name 'shot-*.png' | wc -l
```

Expected: 12 张 `shot-*.png`，每个 segment 均有非空 `first-frame.png` 和 `last-frame.png`，所有构图为竖屏或明确标注的资产卡构图。

- [ ] **Step 6: 更新清单并独立提交媒体资产**

```bash
git add stories/demon-prisoner-edict
git commit --no-verify -m "feat: generate demon prisoner episode assets"
```

### Task 6: 完整 QA 与交付核验

**Files:**
- Modify: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/qa-checklist.md`
- Modify: `stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/image-manifest.md`

**Interfaces:**
- Consumes: Task 1–5 的完整 story 包。
- Produces: 可追踪的 PASS/PARTIAL/BLOCKED 结果和最终文件地址。

- [ ] **Step 1: 运行仓库现有 episode validator**

Run:

```bash
python3 scripts/validate_episode.py stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows
```

Expected: validation passes；若脚本参数契约不同，先运行 `python3 scripts/validate_episode.py --help`，按实际参数执行并记录命令。

- [ ] **Step 2: 检查占位符、泄密和禁用视觉词**

Run:

```bash
rg -n "TBD|TODO|YOUR_KEY|api[_-]?key|红圈锁定|游戏UI" stories/demon-prisoner-edict
```

Expected: 不存在占位符或密钥；“红圈锁定”和“游戏 UI”只允许出现在负面约束中。

- [ ] **Step 3: 视觉检查全部 12 张分镜和封面**

检查人物身份、服装、道具、场景方向、动作因果、文字水印、锐化和纹理伪影；把每项结果写入 `qa-checklist.md`。

- [ ] **Step 4: 最终差异与路径核验**

Run:

```bash
git status --short -- stories/demon-prisoner-edict
find stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows -maxdepth 3 -type f | sort
```

Expected: 只显示本 story 的预期变更；所有交付文件路径完整可读。

- [ ] **Step 5: 提交 QA 更新**

```bash
git add stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/qa-checklist.md stories/demon-prisoner-edict/episodes/EP001_a-word-stops-the-arrows/image-manifest.md
git commit --no-verify -m "chore: validate demon prisoner episode one"
```
