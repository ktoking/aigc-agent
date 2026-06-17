# Twin Dawn 故事包说明

## 故事范围

本目录维护《末日重生：双生曙光 / 末日降临：我和闺蜜觉醒双SSS异能》的所有非通用规则。

生成剧情、分镜、首尾帧、视频 prompt、角色资产或连续性文件时，优先遵循：

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. `docs/workflow.md`
6. `episodes/` 下已有剧集
7. `assets/` 下角色、场景、道具、风格资产
8. `templates/` 下本剧本专属模板

## 已知事实

- 完整剧本记忆、人设、对白和分镜摘要见 `docs/story-memory.md`。
- 生产工作流、资产库结构、每集 4 段拆分规则、首尾帧连续性规则见 `docs/workflow.md`。
- 抖音受众、标题、封面和评论引导方向见 `docs/audience-strategy.md`。
- 长线阶段和前 10 集方向见 `docs/season-arc.md`。
- 双女主最终定妆参考图是 `assets/characters/double-hero-final-reference.png`：林晚按左侧人物，沈清雪按右侧人物。
- 后续不得重新设计林晚或沈清雪的外貌。参考图优先级高于文字描述。
- 每集必须包含 `overview-storyboard.md`，作为 60 秒总览故事板。
- 继续生成 EP005 及后续剧集时，使用根目录通用 skill `skills/ai-microdrama-episode-production/`，并把目标 story 指定为 `stories/twin-dawn`。

## 角色锁定

- 林晚：`LIN_WAN_001`，重生者，SSS 级空间异能者，冷静但保护欲强，黑色超长直发，冷白皮，左眼下淡痣。
- 沈清雪：`SHEN_QINGXUE_001`，SSS 级精神系异能者，短发到下颌/锁骨之间，空气刘海，白色服装方向，温柔成熟且坚定。
- 顾景辰：`GU_JINGCHEN_001`，表面温和的商业精英，隐藏控制欲和危险感。不要写成大喊大叫的脸谱化反派。

## 剧集规则

- 一集 60 秒，拆成 4 段，每段 15 秒以内。
- 每段必须有 `storyboard.md`、`first-frame.md`、`last-frame.md`、`prompt.md`。
- 新剧集推荐补齐 `api-request.md`、`qa-checklist.md`、`publish-package.md`。
- 开头 5 秒必须有视觉钩子或情绪压力。
- 每集需要一个冲突、一个情绪点、一个爽点/揭示、一个结尾钩子。
- 对白短、狠、可演，不写长篇解释。
- 分段首尾帧必须连续，除非有明确可见转场。
