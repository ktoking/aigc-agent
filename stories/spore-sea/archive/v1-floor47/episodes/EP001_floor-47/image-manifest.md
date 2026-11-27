# EP001 图像计划

所有图像状态为待生成。本表提供后续制作路径，实际选图后更新。每段 `frames/` 存放首尾帧，跨段映射按实测剪辑确认。

| 资产 | 输入职责 | 存放位置 |
| --- | --- | --- |
| 韩峥、叶岑、罗秀 | 各自的脸、发型、服装、饰物 | `assets/characters/<角色ID>/` |
| 枝甲人 | 人形比例、三根木指、灰袖、右肩 | `assets/characters/BRANCHBOUND_001/` |
| 转运间、检修桥 | 门、窗、坡向、色温、隔板和货箱坐标 | `assets/scenes/<场景ID>/` |
| 118 货箱 | 掀盖结构、物证构图和后期文字区 | `assets/props/PROP_FREIGHT_CASE/` |
| 各段首尾帧 | 分段视觉锚点，共 8 个文件槽位 | `segment_*/frames/first-frame.png` 和 `segment_*/frames/last-frame.png` |

首尾接点为 01 尾 → 02 首、02 尾 → 03 首、03 尾 → 04 首。主体站位、朝向、光色和道具状态按对应提示词继承。
