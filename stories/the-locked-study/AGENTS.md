# THE LOCKED STUDY 故事包说明

## 故事范围

本目录维护《THE LOCKED STUDY / 雪夜密室》的所有非通用规则。生成剧情、分镜、首尾帧、视频 prompt、角色资产或连续性文件时，必须优先遵循本目录规则。

## 必读顺序

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. `docs/workflow.md`
6. `episodes/` 下已有剧集
7. `assets/` 下角色、场景、道具、风格资产

## 已知事实

- 完整剧本记忆、人物关系、隐藏动机和关键对白见 `docs/story-memory.md`。
- 生产工作流、4 段 × 30 秒拆分规则、首尾帧连续性规则见 `docs/workflow.md`。
- 视觉总控、人物外观锁定、负面提示词见 `assets/style/` 与 `assets/characters/`。人物外观优先级：参考图 > 角色卡 > 文字描述。
- 后续不得重新设计 6 位角色的外貌；参考图优先级高于文字描述。

## 角色锁定

- Edward Hale：`EDWARD_HALE`，45 岁英国侦探朋友，深灰三件套西装 + 黑色羊毛大衣 + 皮手套，深色带灰短发，眼神锐利克制，先观察再说话。
- Lady Eleanor Blackwood：`LADY_ELEANOR`，52 岁英国贵妇，黑色丝绒长裙 + 珍珠项链，灰金盘发，苍白高贵冷淡，手持凉茶。
- Clara Vale：`CLARA_VALE`，28 岁，Arthur 之女，深褐长发，深色精致连衣裙，夹烟，眼神飘忽望向窗外。
- Arthur Vale：`ARTHUR_VALE`，55 岁家族律师，银灰背头，深色三件套西装，整洁无破绽，礼貌而冰冷的微笑。
- Morris：`MORRIS`，65 岁老管家，白发，黑色燕尾服管家制服，白手套，站姿笔直，克制守礼。
- Owen：`OWEN`，38 岁司机，工人阶层，深棕乱发，粗花呢外套，湿靴，焦躁搓手。

## 剧集规则

- 一集 120 秒，拆成 4 段，每段 30 秒以内。
- 画幅固定 16:9 横屏；禁止竖版构图。
- 每段必须有 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`、`director-promt.txt`、`api-request.md`。
- 视频模型固定 Seedance 2.5（seedance_2.5），duration=30，ratio=16:9，图生视频优先。
- `director-promt.txt` 是用户确认过的原文提示词，禁止改写、润色、增删。
- 对白极简（全片 18 句以内），靠动作、表情、空间调度建立人物。
- 无字幕、无屏幕文字；原生音频优先环境声；关键台词建议后期配音，避免多角色口型风险。
- 分段首尾帧必须连续，除非有明确可见转场。
- 四段串行验收：上一段视频 QA 通过后才允许提交下一段。
