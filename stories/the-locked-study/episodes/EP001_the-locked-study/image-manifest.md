# 图像资产清单（Image Manifest）— EP001 THE LOCKED STUDY

## 固定资产

### 角色参考图

| ID | 文件 | 用途 |
|---|---|---|
| EDWARD_HALE | `assets/characters/EDWARD_HALE/edward-hale-reference.png` | 室外黑大衣状态 |
| EDWARD_HALE | `assets/characters/EDWARD_HALE/edward-hale-interior-reference.png` | 室内无大衣、无手套状态 |
| EDWARD_HALE | `assets/characters/EDWARD_HALE/edward-hale-gloved-reference.png` | Seg4 室内戴皮手套处理证物 |
| LADY_ELEANOR | `assets/characters/LADY_ELEANOR/lady-eleanor-reference.png` | 黑丝绒裙、珍珠、凉茶 |
| CLARA_VALE | `assets/characters/CLARA_VALE/clara-vale-reference.png` | 深绿裙、香烟、窗边站位 |
| ARTHUR_VALE | `assets/characters/ARTHUR_VALE/arthur-vale-reference.png` | 银灰背头、三件套、袖口动作 |
| MORRIS | `assets/characters/MORRIS/morris-reference.png` | 燕尾服、白手套、笔直站姿 |
| OWEN | `assets/characters/OWEN/owen-reference.png` | 粗花呢、湿靴、焦躁状态 |
| 全员 | `assets/characters/cast-reference-sheet.png` | 多人群像身份锁定；上排 Hale/Eleanor/Clara，下排 Arthur/Morris/Owen |

### 场景参考图

| 场景 | 文件 | 锁定内容 |
|---|---|---|
| MANOR_EXTERIOR | `assets/scenes/MANOR_EXTERIOR/manor-exterior-reference.png` | 石砌庄园、门灯、石阶、暴风雪 |
| DRAWING_ROOM | `assets/scenes/DRAWING_ROOM/drawing-room-reference.png` | 壁炉、窗、酒柜、落地钟、书房门轴线 |
| STUDY | `assets/scenes/STUDY/study-reference.png` | 破锁、书桌、绿台灯、尸体、白兰地、怀表 |

## Segment 01（10 张）

1. `frames/first-frame.png` — 暴风雪庄园定场。
2. `frames/02_hale-at-open-door.png` — Hale 出现在门口。
3. `frames/03_hale-stamps-snow.png` — 跺靴抖雪。
4. `frames/04_morris-takes-coat.png` — Morris 接大衣并报告。
5. `frames/05_hale-enters-drawing-room.png` — 肩后进入大客厅。
6. `frames/06_eleanor-cold-tea.png` — Eleanor 凉茶行为。
7. `frames/07_clara-long-ash.png` — Clara 长烟灰。
8. `frames/08_arthur-and-owen.png` — Arthur 袖口与 Owen 湿靴对照。
9. `frames/09_body-reveal-over-shoulder.png` — 过肩揭示尸体与证物。
10. `frames/last-frame.png` — 六人目光汇聚 Hale。

## Segment 02（10 张）

1. `frames/first-frame.png` — Hale 走入中心开始问询。
2. `frames/02_hale-observes-before-speaking.png` — 先观察后开口。
3. `frames/03_eleanor-does-not-drink.png` — 茶杯到唇边却不喝。
4. `frames/04_clara-flicks-long-ash.png` — Clara 弹落烟灰。
5. `frames/05_owen-turns-from-fire.png` — Owen 从火边转身。
6. `frames/06_morris-straightens-table.png` — Morris 扶正桌布。
7. `frames/07_arthur-calm-at-cabinet.png` — Arthur 酒柜旁整理袖口。
8. `frames/08_hale-semicircle-scan.png` — Hale 半圆扫视群像。
9. `frames/09_behavior-tableau.png` — 行为即性格的群像。
10. `frames/last-frame.png` — Hale 与 Arthur 第一次真正对视。

## Segment 03（10 张）

1. `frames/first-frame.png` — 落地钟触发、Hale 看人不看钟。
2. `frames/02_clara-crushes-cigarette.png` — Clara 掐灭第一支烟。
3. `frames/03_clara-lights-second.png` — 立即点燃第二支烟。
4. `frames/04_owen-blizzard-outburst.png` — Owen 对暴风雪爆发。
5. `frames/05_eleanor-rebukes-owen.png` — Eleanor 冷眼制止。
6. `frames/06_arthur-cold-deflection.png` — Arthur 冷静转移话题。
7. `frames/07_eleanor-accuses-arthur.png` — Eleanor 指出 Arthur 最后陪酒。
8. `frames/08_arthur-points-to-locked-room.png` — Arthur 指向破锁密室。
9. `frames/09_hale-walks-to-study.png` — Hale 带众人走向书房。
10. `frames/last-frame.png` — Hale 停在门槛回望，尸体在背景。

## Segment 04（10 张）

1. `frames/first-frame.png` — Hale 戴手套跨入书房。
2. `frames/02_broken-lock-evidence.png` — 破锁近景。
3. `frames/03_body-watch-brandy.png` — 尸体、怀表、白兰地证物组。
4. `frames/04_hale-lifts-brandy.png` — Hale 举起白兰地杯。
5. `frames/05_arthur-glances-at-glass.png` — Arthur 偷瞥酒杯。
6. `frames/06_arthur-blurts-reveal.png` — Arthur 裸手口误，Hale 手套持杯在前景。
7. `frames/07_hale-turns-brandy-question.png` — Hale 缓慢转头反问。
8. `frames/08_arthur-first-freeze.png` — Arthur 眼周第一次僵住。
9. `frames/09_natural-half-step-isolation.png` — 众人自然半步孤立 Arthur。
10. `frames/last-frame.png` — 书房门框画中画，Arthur 壁炉前被孤立。

## 生成状态

- 固定资产：12 张 PNG，已生成并目检。
- 关键帧：4 个 segment × 10 张 = 40 张 PNG，已生成并目检。
- 生成方式：Codex 内置 `image_gen`，未使用 CLI/API fallback。
- 统一规格：16:9 横屏，输出约 1670–1672 × 941，真人 35mm 电影质感。
- 负面约束：无字幕、无水印、无可读文字；无动漫/游戏 CG/塑料皮肤；无过度锐化、鱼鳞网格、满屏微纹理；尸体非血腥。

## 视频输出（未执行）

| 段 | 产物 | 状态 |
|---|---|---|
| segment_01_00-30s | `output/video.mp4` + `output/video-qa.json` | 待提交 |
| segment_02_30-60s | `output/video.mp4` + `output/video-qa.json` | 待提交 |
| segment_03_60-90s | `output/video.mp4` + `output/video-qa.json` | 待提交 |
| segment_04_90-120s | `output/video.mp4` + `output/video-qa.json` | 待提交 |
