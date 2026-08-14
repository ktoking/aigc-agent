# EP002 图像资产清单

## 角色与场景参考

| 类型 | 资产 | 用途 | 状态 |
| --- | --- | --- | --- |
| 风格 | assets/style/user-anime-style-reference.png | 暗黑都市幻想动漫风格 | 已有 |
| 角色 | assets/characters/SMA_GU_CHEN_001/canonical-turnaround.png | 顾沉脸、发型、工装 | 已有 |
| 角色 | assets/characters/SMA_ZHAO_TIANLIN_001/canonical-turnaround.png | 赵天麟脸、礼服、腕环 | 已有 |
| 场景 | assets/scenes/SCENE_AWAKENING_HALL_001/canonical-concept.png | 觉醒礼堂空间、阶级站位 | 已有 |
| 道具 | assets/props/PROP_AWAKENING_TERMINAL_001/prop-card.md | 觉醒终端形态与管理员裂线 | 已有 |

## 本集关键帧

| 资产 | 用途 | 状态 |
| --- | --- | --- |
| segment_01_00-15s/frames/first-frame.png | 五类系统升空、顾沉位于最低层 | 已用本地 ImageGen 覆盖 |
| segment_01_00-15s/frames/last-frame.png | 赵天麟启动神豪腕环、付款卡落地、顾沉仍站立 | 已用本地 ImageGen 覆盖 |
| segment_02_15-30s/frames/first-frame.png | 复用 Segment 01 尾帧 | 已复用 |
| segment_02_15-30s/frames/last-frame.png | 封禁后腕环失灵、顾沉与终端暗红线连续 | 已用本地 ImageGen 覆盖 |
| segment_03_30-45s/frames/first-frame.png | 复用 Segment 02 尾帧 | 已复用 |
| segment_03_30-45s/frames/last-frame.png | 神豪节点空白、赵天麟惊讶、顾沉站在台阶中央 | 已用本地 ImageGen 覆盖 |
| segment_04_45-60s/frames/first-frame.png | 复用 Segment 03 尾帧空白神豪节点 | 已复用 |
| segment_04_45-60s/frames/last-frame.png | 顾沉走入暗处，直播关闭、空白神豪节点留在高处，升级提示不对外显示 | 已用本地 ImageGen 覆盖 |

## 生成约束

- 新版关键帧使用本地内置 ImageGen，以顾沉、赵天麟和觉醒礼堂 canonical 作为参考。
- 视频模型只接收首帧、尾帧和必要角色/场景参考，不上传旧版回收站或废核心图片。
- 画面文字只保留少量短词：无系统、神豪系统、权限剥夺、直播中止；权限升级只用顾沉眼底短暂暗红反光表达，其余信息用对白和声音表达。
