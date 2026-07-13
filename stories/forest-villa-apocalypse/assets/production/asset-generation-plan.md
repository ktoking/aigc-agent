# 场景与道具资产生成计划

## 原则

- 人物用火山 Ark 数字人资产，不用通用生图模型生成带真人的首尾帧。
- 场景和道具必须先生成参考图，再进入视频生成。
- 每张参考图只承担一个职责：结构、外观、室内仓储、发电机棚、抽卡道具。
- 参考图尽量不含人物，减少数字人换脸风险。
- 新增和重做资产默认 16:9 横屏。已有 16:9 竖图保留为 legacy reference，可临时给模型理解内容，但最终视频参考图优先使用 16:9 版本。

## 第一批必需资产

| 优先级 | 资产 | 提示词文件 | 目标文件 | 状态 |
| --- | --- | --- | --- | --- |
| P0 | 林中别墅结构三视图 | `assets/scenes/SCENE_FOREST_VILLA_001/structure-three-view-prompt.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-structure-three-view.png` | 已生成，现代三层高围墙版本 |
| P0 | 林中别墅白天外观 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-exterior-day.png` | 已生成，现代三层高围墙版本 |
| P0 | 一楼仓储指挥区 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/ground-floor-storage-command.png` | 已生成 |
| P0 | 抽卡手机界面 | `assets/props/prop-reference-prompts.md` | `assets/props/references/draw-card-phone-interface.png` | 已生成 |
| P0 | 柴油发电机维修包 | `assets/props/prop-reference-prompts.md` | `assets/props/references/generator-repair-kit.png` | 已生成 |
| P1 | 夜晚外观 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/forest-villa-exterior-night.png` | 待生成 |
| P1 | 发电机棚 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/generator-shed.png` | 已生成 |
| P1 | 柴油发电机 | `assets/props/prop-reference-prompts.md` | `assets/props/references/diesel-generator.png` | 已生成 |
| P2 | 地下室仓储 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/basement-storage.png` | 待生成 |
| P2 | 山路铁门 | `assets/scenes/SCENE_FOREST_VILLA_001/scene-reference-prompts.md` | `assets/scenes/SCENE_FOREST_VILLA_001/references/mountain-road-gate.png` | 待生成 |
| P2 | 物资墙 | `assets/props/prop-reference-prompts.md` | `assets/props/references/supply-wall.png` | 待生成，一楼仓储图可临时代替 |
| P2 | 别墅防御平面图 | `assets/props/prop-reference-prompts.md` | `assets/props/references/villa-defense-map.png` | 待生成 |

## EP001 视频参考图建议

| Segment | 数字人 | 场景/道具参考图 |
| --- | --- | --- |
| Segment 01 | 许砚数字人 | `assets/production/city-outbreak-street.png` |
| Segment 02 | 许砚、白棠数字人 | `forest-villa-structure-three-view.png`、`forest-villa-exterior-day.png` |
| Segment 03 | 许砚、白棠数字人 | `ground-floor-storage-command.png`、`supply-wall.png`、`villa-defense-map.png` |
| Segment 04 | 许砚、白棠数字人 | `ground-floor-storage-command.png`、`draw-card-phone-interface.png`、`generator-repair-kit.png`、`generator-shed.png`、`forest-villa-exterior-night.png` |
