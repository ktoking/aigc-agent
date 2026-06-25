# EP001 图片资产清单

## Story 概念资产

| 资产 | 路径 | 状态 |
| --- | --- | --- |
| 米拉定妆 | `../../assets/characters/HYS_MIRA_001/mira-concept.png` | 已生成，SHA256 `a50d6e45...c0147bc` |
| 猎手定妆 | `../../assets/characters/HYS_HUNTER_001/hunter-concept.png` | 已生成，SHA256 `1874c270...80532` |
| 黑雨钟城 | `../../assets/scenes/SCENE_BLACK_RAIN_CLOCK_CITY/clock-city-concept.png` | 已生成，SHA256 `a715a191...6453d` |
| 故事主视觉 | `../../assets/style/hunt-yesterday-self-key-art.png` | 已生成，SHA256 `fca294d0...6efe8` |

四张图片尺寸均为 `941 x 1672`，纵横比约为 9:16。

## Segment 最终帧

| Segment | 类型 | 路径 | 连续性策略 | 状态 |
| --- | --- | --- | --- | --- |
| 01 | 首帧 | `segment_01_00-15s/frames/first-frame.png` | 独立开场锚点 | 已落位 |
| 01 | 尾帧 | `segment_01_00-15s/frames/last-frame.png` | 与 Segment 02 首帧同源复制 | 已落位 |
| 02 | 首帧 | `segment_02_15-30s/frames/first-frame.png` | 精确复用 Segment 01 尾帧 | 已落位 |
| 02 | 尾帧 | `segment_02_15-30s/frames/last-frame.png` | 与 Segment 03 首帧同源复制 | 已落位 |
| 03 | 首帧 | `segment_03_30-45s/frames/first-frame.png` | 精确复用 Segment 02 尾帧 | 已落位 |
| 03 | 尾帧 | `segment_03_30-45s/frames/last-frame.png` | 与 Segment 04 首帧同源复制 | 已落位 |
| 04 | 首帧 | `segment_04_45-60s/frames/first-frame.png` | 精确复用 Segment 03 尾帧 | 已落位 |
| 04 | 尾帧 | `segment_04_45-60s/frames/last-frame.png` | 独立结尾钩子锚点 | 已落位 |

## Segment 故事板图

| Segment | 路径 | 内容 |
| --- | --- | --- |
| 01 | `segment_01_00-15s/frames/storyboard-sheet.png` | 高架追逐、斩链、坠落、救人 |
| 02 | `segment_02_15-30s/frames/storyboard-sheet.png` | 少年衰老、断光丝、误判、护表 |
| 03 | `segment_03_30-45s/frames/storyboard-sheet.png` | 齿轮脱身、二次按表、击飞怀表、揭面 |
| 04 | `segment_04_45-60s/frames/storyboard-sheet.png` | 身份确认、六次反光、归还选择、六表钩子 |

## 图片规则

- 相邻段桥接帧使用同一源文件复制，不重新生成近似图。
- 少年所有剧情帧删除胸前吊坠，避免被误读为第二块怀表。
- EP001 主体始终只有第七块怀表；另外六块只在 Segment 04 最后出现。
- 所有最终图片执行无鱼鳞纹、无网格、无菱格绗缝、无塑料皮肤、无颗粒和无过度锐化约束。

## 校验产物

- 首尾帧 contact sheet：`EP001-frames-contact-sheet.png`
- 全视觉包 contact sheet：`EP001-visual-package-contact-sheet.png`
- 剧集总览图：`overview-storyboard.png`

## 最终首尾帧校验

8 张首尾帧统一为 `941 x 1672`，9:16，无缺失和画幅警告。

| 桥接 | SHA256 前 16 位 | 结果 |
| --- | --- | --- |
| Segment 01 尾帧 = Segment 02 首帧 | `314881f579e61432` | 完全一致 |
| Segment 02 尾帧 = Segment 03 首帧 | `98b751d1caf1f42c` | 完全一致 |
| Segment 03 尾帧 = Segment 04 首帧 | `803194896312357b` | 完全一致 |

独立开场帧 SHA256 前 16 位：`06c2d5dc28b244f7`。

独立结尾帧 SHA256 前 16 位：`bfa0cfc27618770a`。
