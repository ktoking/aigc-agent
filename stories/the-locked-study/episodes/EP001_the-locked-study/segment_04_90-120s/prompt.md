# Segment 04 视频提示词

## 视频规格

- 画幅：16:9 横屏。
- 时长：30 秒。
- 模型：Seedance 2.5（seedance_2.5），图生视频。
- 风格：与前三段同一连续性；真实密室投毒揭示；克制反转。
- 无字幕、无屏幕文字。

## 输入帧

- 首帧：`first-frame.md`（Hale 跨入书房，视线扫过门锁/尸体/怀表/酒杯）
- 尾帧：`last-frame.md`（Arthur 孤立于壁炉前，门框画中画，CUT TO BLACK 前）

## 角色锁定

- `EDWARD_HALE`：皮手套戴回，拿酒杯；无胜利表情，只有确定。
- `ARTHUR_VALE`：口误“白兰地”前最平静；僵住后崩溃控诉；结尾明暗分脸。
- `LADY_ELEANOR`：第一次真正看向尸体（警觉）。
- `CLARA_VALE`：烟停在半空；结尾低头。
- `OWEN`：停止移动；结尾沉默。
- `MORRIS`：站得更直。

## 场景与道具

- 场景：`SCENE_STUDY`（90-106s）→ `SCENE_DRAWING_ROOM` 壁炉前（111-120s）。
- 道具：门锁、书桌、尸体、怀表、白兰地酒杯（核心证据）。
- 光线：台灯光锥 → 壁炉火光（明暗分脸）。
- 色调：低饱和。

## 动作链路

```text
90-96s：Hale 进书房，镜头跟视线扫过门锁、书桌、尸体、怀表、半杯白兰地；轻声说“他不是在这间屋子里被杀的”；众人神色变化。
96-101s：Hale 说“门锁着，说明没人进来，可这并不意味着没人先动过手”；镜头扫过所有人：Eleanor 第一次看向尸体，Clara 烟停在半空，Owen 不再抱怨，Morris 站得更直，Arthur 最平静。
101-106s：Hale 拿起酒杯却不回头，说“他走进书房的时候，谋杀已经开始了”；Arthur 下意识接“如果毒在白兰地里，那谁都可以——”话没说完。
106-111s：全场静住；Hale 缓缓转头看向 Arthur，只反问一个词“白兰地？”；Arthur 表情第一次僵住（眼睛周围轻微僵硬）。
111-116s：Hale 举起酒杯，说“我还没告诉任何人，毒是怎么下的”；其他人自然地、不自觉地与 Arthur 拉开半步。
116-120s：Arthur 站壁炉前，火光把脸切成明暗两半，低声说出动机；Hale 平静看着他；镜头后拉退出书房门框；CUT TO BLACK。
```

## 运镜

- 90-101s：跟进视线 + 横扫众人反应。
- 106-111s：缓缓转头特写 + 长停顿（昂贵感停顿）。
- 111-120s：中景后拉 → 门框画中画 → 黑场。

## 台词（钉子句，建议后期配音；原生音频只做环境声）

- HALE: "He wasn't attacked in this room. By the time he locked that door... it may already have been too late."
- ARTHUR: "That's absurd. If the poison was in the brandy, anyone could have—"
- HALE: "Brandy?"
- HALE: "I never mentioned the drink."
- ARTHUR: "That proves nothing. Nothing. You have a glass and a dead man. That's all."
- ARTHUR: "You don't know what he was like. None of you do. He owned this house. He owned everyone in it. Tomorrow morning he was going to the police. He would have taken everything. My work. My name. Clara— Everything! He would've destroyed this family!"
- HALE: "That's all."

## 音效

- 脚步、酒杯轻响、彻底安静、衣料摩擦、壁炉噼啪、窗外风雪、落地钟再次敲响、静默。

## 视频 Prompt 摘要（API 直投原文，逐字透传）

本文件为人工审阅版；API 直投版请使用 `director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词）。

## 负面提示词

```text
不要字幕，不要水印，不要logo，不要可读文字；不要动漫风，不要游戏CG感，不要塑料皮肤；不要静态拉图，不要图片变形过渡，不要人物瞬移，不要换房间；不要换脸，不要东方面孔，不要夸张表情，不要戏剧化手势；不要血腥，不要伤口特写；不要金黄色满屏（壁炉暖光仅限光源范围）；不要静态定格超过1秒
```
