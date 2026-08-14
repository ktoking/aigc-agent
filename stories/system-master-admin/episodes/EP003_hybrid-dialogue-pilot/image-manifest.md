# EP003 学院管理员审计版图像资产清单

## 资产状态

- 本版只完成剧本、分镜、首尾帧提示词和 API handoff 文档。
- 尚未生成 EP003 首尾帧 PNG，因此每个 `frames/` 目录暂保留 `.gitkeep`。
- 不调用外部 StoryGen Atelier 图像/视频链；后续图片继续使用本地 imagegen，视频继续使用 Ark/Seedance。

## 角色与场景参考

| 资产 ID | 文件 | 用途 | 状态 |
| --- | --- | --- | --- |
| `SMA_GU_CHEN_001` | `assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png` | 顾沉脸、发型、工装锁 | 已有 |
| `SCENE_AWAKENING_HALL_001` | `assets/scenes/SCENE_AWAKENING_HALL_001/canonical-concept.png` | 礼堂、阶梯、后台门和结果屏 | 已有 |
| `PROP_AWAKENING_TERMINAL_001` | `assets/props/PROP_AWAKENING_TERMINAL_001/prop-card.md` | 终端外形和裂痕规则 | 只有文字卡，暂无图片 |

## 学院管理员处理

- 本集只用背影、手部、局部工牌和声音，不上传未确认的人脸。
- 若文本通过，再单独生成 `SMA_ACADEMY_TERMINAL_ADMIN_001` 的剪影/三视图资产；在此之前不把临时图落入 canonical 目录。

## 分段首尾帧

| 分段 | 首帧 | 尾帧 | 状态 |
| --- | --- | --- | --- |
| 01 | `segment_01_00-15s/frames/first-frame.png` | `segment_01_00-15s/frames/last-frame.png` | 待生成 |
| 02 | `segment_02_15-30s/frames/first-frame.png` | `segment_02_15-30s/frames/last-frame.png` | 待生成 |
| 03 | `segment_03_30-45s/frames/first-frame.png` | `segment_03_30-45s/frames/last-frame.png` | 待生成 |
| 04 | `segment_04_45-60s/frames/first-frame.png` | `segment_04_45-60s/frames/last-frame.png` | 待生成 |

## 不上传

- 不上传 EP002 的赵天麟角色图，避免把他的金色腕环误带入本集后台调查。
- 不上传分镜表格图和带大段文字的终端截图。
- 不使用 `draft-turnaround-v1.png` 等废案人物图。
