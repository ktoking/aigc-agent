# Hunt Yesterday Self Story Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建《猎杀昨日的我》完整 story 包、60 秒 EP001 生产文件和四张项目概念图。

**Architecture:** 按仓库通用 story contract 分为 story 规则层、资产卡层、episode 生产层和图片资产层。EP001 使用单场追逐逐步进入钟楼，以怀表、少年衰老和猎手攻击目标作为贯穿的可视化因果。

**Tech Stack:** Markdown story contract、仓库本地 `ai-microdrama-episode-production` skill、内置 imagegen、Python frame verifier。

---

### Task 1: 创建 Story 基础结构

**Files:**
- Create: `stories/hunt-yesterday-self/README.md`
- Create: `stories/hunt-yesterday-self/AGENTS.md`
- Create: `stories/hunt-yesterday-self/docs/story-memory.md`
- Create: `stories/hunt-yesterday-self/docs/production-rules.md`
- Create: `stories/hunt-yesterday-self/docs/audience-strategy.md`
- Create: `stories/hunt-yesterday-self/docs/season-arc.md`
- Create: `stories/hunt-yesterday-self/docs/workflow.md`

- [ ] **Step 1:** 从已批准设计写入故事定位、三条硬规则、角色欲望与核心反转。
- [ ] **Step 2:** 写入无对白优先、每 3-5 秒信息变化、单场景可见转场和画质负面约束。
- [ ] **Step 3:** 运行 `rg -n "身份偷|虚拟现实|TBD|TODO" stories/hunt-yesterday-self`，预期无匹配。

### Task 2: 创建资产卡与风格锁

**Files:**
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_MIRA_001/00-character-card.md`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_HUNTER_001/00-character-card.md`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_BOY_001/00-character-card.md`
- Create: `stories/hunt-yesterday-self/assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/scene-card.md`
- Create: `stories/hunt-yesterday-self/assets/scenes/SCENE_REVERSING_STATION/scene-card.md`
- Create: `stories/hunt-yesterday-self/assets/props/PROP_LIFETIME_WATCH_07/prop-card.md`
- Create: `stories/hunt-yesterday-self/assets/props/PROP_TIME_BLADE/prop-card.md`
- Create: `stories/hunt-yesterday-self/assets/style/global-style.md`
- Create: `stories/hunt-yesterday-self/assets/style/camera-language.md`
- Create: `stories/hunt-yesterday-self/assets/style/negative-prompts.md`

- [ ] **Step 1:** 为角色写不可变外形、动作签名和剧情职责。
- [ ] **Step 2:** 为场景和道具写可视化规则及连续性约束。
- [ ] **Step 3:** 把鱼鳞纹、网格、塑料皮肤、过度锐化和颗粒写入全局负面提示词。

### Task 3: 创建 EP001 根文件

**Files:**
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/episode.md`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/continuity.md`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/overview-storyboard.md`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/image-manifest.md`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/qa-checklist.md`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/publish-package.md`

- [ ] **Step 1:** 写入 0-60 秒完整无对白剧情和四段留存任务。
- [ ] **Step 2:** 在连续性表记录米拉、猎手、少年、怀表、光丝和损伤状态。
- [ ] **Step 3:** 确认 57-60 秒以六块旧怀表结束，不引入身份盗取支线。

### Task 4: 创建四个 Segment 生产包

**Files:**
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_01_00-15s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,api-request.md}`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_02_15-30s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,api-request.md}`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_03_30-45s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,api-request.md}`
- Create: `stories/hunt-yesterday-self/episodes/EP001_saved-boy-aged/segment_04_45-60s/{storyboard.md,first-frame.md,last-frame.md,prompt.md,api-request.md}`
- Create directories: four segment `frames/` and `output/`

- [ ] **Step 1:** 每段写 3-4 个时间节拍、单一核心运镜和无对白音效。
- [ ] **Step 2:** 保证 Segment 02-04 首帧逐字继承上一段尾帧的姿态、位置和道具状态。
- [ ] **Step 3:** 每个视频 prompt 写入角色锁、动作因果、首尾状态及全局画质负面约束。

### Task 5: 生成四张项目概念图

**Files:**
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_MIRA_001/mira-concept.png`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_HUNTER_001/hunter-concept.png`
- Create: `stories/hunt-yesterday-self/assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/clock-city-concept.png`
- Create: `stories/hunt-yesterday-self/assets/style/hunt-yesterday-self-key-art.png`

- [ ] **Step 1:** 分别生成米拉、猎手、钟城和双人追逐主视觉。
- [ ] **Step 2:** 检查人物身份、怀表、面具、同眼伏笔与黑雨方向。
- [ ] **Step 3:** 检查无鱼鳞网纹、无塑料皮肤、无过度锐化、无文字水印。
- [ ] **Step 4:** 将选定图片复制进 story 资产目录，并在 `image-manifest.md` 登记。

### Task 6: 验证 Story 包

**Files:**
- Verify: `stories/hunt-yesterday-self/`

- [ ] **Step 1:** 运行 `find stories/hunt-yesterday-self -type f | sort`，确认 contract 文件齐全。
- [ ] **Step 2:** 运行脚本检查每段文档与目录；图片仅为概念资产时，不伪称首尾帧已交付。
- [ ] **Step 3:** 运行 `git diff --check -- stories/hunt-yesterday-self docs/superpowers`。
- [ ] **Step 4:** 扫描 `output/`、API key、提交返回和签名 URL，预期没有敏感产物。

### Task 7: 建立制作级角色与战斗参考资产

**Files:**
- Create: `stories/hunt-yesterday-self/assets/asset-manifest.md`
- Create: `stories/hunt-yesterday-self/assets/action-choreography/README.md`
- Create: `stories/hunt-yesterday-self/assets/action-choreography/CHOREO_EP001_01_chase-and-miss.md`
- Create: `stories/hunt-yesterday-self/assets/action-choreography/CHOREO_EP001_02_watch-defense.md`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_MIRA_001/{01-face-reference,02-expression-sheet,03-360-turnaround,04-outfits,05-action-poses,06-negative-reference}/`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_HUNTER_001/{01-face-reference,02-expression-sheet,03-360-turnaround,04-outfits,05-action-poses,06-negative-reference}/`
- Create: `stories/hunt-yesterday-self/assets/characters/HYS_BOY_001/{01-face-reference,02-age-progression,03-outfits,04-action-poses,05-negative-reference}/`
- Create: corresponding PNG reference sheets under the directories above.
- Create: prop reference sheets and clock-city chase spatial reference.

- [x] **Step 1:** 以现有米拉和猎手概念图为身份参考，生成两人的三视图、表情表和动作表。
- [x] **Step 2:** 生成两张三拍式双人战斗编排图，锁定左右站位、持械手、攻防方向和结束状态。
- [x] **Step 3:** 生成少年四阶段年龄渐变、怀表/时间刃比例和黑雨钟城追逐空间参考。
- [x] **Step 4:** 在角色卡、道具卡和资产清单中登记文件、用途、引用顺序与禁止漂移项。
- [x] **Step 5:** 用图像尺寸、hash 和人工预览检查所有新增图片；不把预览或生成中间产物提交到 `output/`。
- [x] **Step 6:** 运行 `git diff --check`、敏感信息扫描和 `git status --ignored`，只提交 story 资产与文档。
