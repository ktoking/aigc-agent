# Seedance API 交接

- 模型：`doubao-seedance-2-0-mini-260615`
- 时长：15 秒；比例：16:9；分辨率：720p；生成音频并返回尾帧。
- 数字人：`asset://asset-20260320075237-29hdx`、`asset://asset-20260320075131-k78qt`、`asset://asset-20260310030618-88hlb`。
- 场景与道具参考：`stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/rainy-energy-shed-micro-reactor-complete-16x9.png`、`stories/forest-villa-apocalypse/assets/scenes/SCENE_FOREST_VILLA_001/references/backup-battery-system-16x9.png`、`stories/forest-villa-apocalypse/assets/props/references/auto-defense-turret-balcony-radar-16x9.png`。
- 首帧状态：模块已通过自检，许砚等待把它切入储能支路。
- 尾帧状态：能源棚低噪运行，储能回升，白板留下维护清单。
- 连续性：优先使用 Segment 03 的真实尾帧；只生成本段，不自动重试已有视频。
