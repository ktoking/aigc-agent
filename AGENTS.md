# Project Notes

## Learned Workspace Facts

- 本项目当前承载 AI 短剧《末日重生：双生曙光 / 末日降临：我和闺蜜觉醒双SSS异能》的设定记忆；完整剧本、人设、对白和分镜摘要见 `docs/story-memory.md`。
- 后续生成剧情、分镜、提示词或角色资产时，应优先保持林晚、沈清雪、顾景辰的人设一致性，并遵循 `docs/story-memory.md` 中的视觉锚点、对白和短剧节奏规则。
- AI 漫剧生产工作流、资产库结构、每集 4 段拆分规则、首尾帧连续性规则见 `docs/workflow.md`；新剧集应优先复制 `templates/` 的结构并参考 `episodes/EP001_rebirth-before-apocalypse/`。
- 双女主最终定妆参考图是 `assets/characters/double-hero-final-reference.png`：林晚按左侧人物，沈清雪按右侧人物。后续不得重新设计双女主外貌；所有提示词和分镜必须以该图为最高优先级。
- 每一集除了 4 个分段故事板外，还必须生成 `overview-storyboard.md`，作为 60 秒总览故事板，汇总每个视频段落的背景叙事、分镜描述、首帧和尾帧。
- 继续生成 EP003 及后续剧集时，优先使用项目内 skill：`skills/ai-microdrama-episode-production/`，按固定剧集目录、首尾帧、分段故事板和视频提示词格式输出。
