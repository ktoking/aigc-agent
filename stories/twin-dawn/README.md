# Twin Dawn 故事包

本目录是当前 AI 短剧项目的独立 story 包，已从仓库根目录迁移出来。

## 剧名

- 主标题：`末日重生：双生曙光`
- 爆款向标题：`末日降临：我和闺蜜觉醒双SSS异能`

## 项目定位

- 类型：末日重生、双女主、SSS 异能、囤货、基地建设、复仇、生存科幻。
- 形式：9:16 竖屏 AI 短剧 / AI 漫剧。
- 默认单集：60 秒。
- 默认结构：4 段，每段 15 秒以内。
- 生产链路：故事记忆 -> 资产库 -> 单集设计 -> 连续性表 -> 分段故事板 -> 首尾帧 -> 视频 API / 图生视频提示词。

## 关键文件

- `docs/story-memory.md`：完整故事圣经、人物记忆、对白、剧情阶段和视觉锚点。
- `docs/production-rules.md`：本剧本专属人脸锁、风格锁和禁止偏差。
- `docs/workflow.md`：本剧本生产流程。
- `docs/audience-strategy.md`：抖音短剧受众、钩子、标题封面策略。
- `docs/season-arc.md`：长线剧情阶段和前 10 集方向。
- `assets/characters/`：林晚、沈清雪、顾景辰和定妆参考。
- `assets/scenes/`：可复用场景。
- `assets/props/`：道具和异能特效。
- `assets/style/`：末日科幻风格、镜头语言、负面提示词。
- `episodes/`：已生成剧集。
- `templates/`：本剧本专用中文模板，覆盖根通用模板。

## 继续生成

使用根目录通用 skill，但目标 story 必须指向本目录：

```text
使用 stories/twin-dawn，承接 EP004，生成 EP005。
```
