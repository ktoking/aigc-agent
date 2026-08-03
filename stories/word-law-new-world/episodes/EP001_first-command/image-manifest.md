# EP001 图像资产清单

| ID | 文件 | 用途 | 风格 |
| --- | --- | --- | --- |
| EP001_REAL_STYLE_LOCK | `assets/style/real-cinematic/references/ep001-s01-live-action.png` | 陆野、宁晚、巡界犬的真人服装、色调与三人关系锁定 | live-cinematic |
| EP001_S01_SHOT_01 | `segment_01_00-15s/frames/shots/shot_01_hound_drop.png` | 巡界犬扑落，危险建立 | live-cinematic |
| EP001_S01_SHOT_02 | `segment_01_00-15s/frames/shots/shot_02_ning_wan_cornered.png` | 宁晚反应近景 | live-cinematic |
| EP001_S01_SHOT_03 | `segment_01_00-15s/frames/shots/shot_03_lu_ye_raise_hand.png` | 陆野抬手、能力前摇 | live-cinematic |
| EP001_S01_SHOT_04 | `segment_01_00-15s/frames/shots/shot_04_stop_hook.png` | “停下”后冻结的段尾钩子 | live-cinematic |
| LEGACY_2D_REFERENCE | `assets/characters/`、`assets/scenes/` | 旧 2D 试验素材，仅作备选参考，不进入 EP001 当前剪辑 | archive |

首尾帧是相邻段落的衔接锚点，不代表 15 秒视频的输入输出。当前主流程直接用各段 `frames/shots/` 下的 3-4 张镜头图合成；视频 API 只在某个短动作必须连续时单独测试。
