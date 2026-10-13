# Segment 02 视频提示词

## 视频规格

- 画幅：16:9 横屏。
- 时长：30 秒。
- 模型：Seedance 2.5（seedance_2.5），图生视频。
- 风格：与 Segment 01 完全同一角色、服装、场景、雪夜；长镜头走位。
- 无字幕、无屏幕文字。

## 输入帧

- 首帧：`first-frame.md`（Hale 走进客厅中央，五人环绕）
- 尾帧：`last-frame.md`（Hale 与 Arthur 第一次真正对视）

## 角色锁定

- `EDWARD_HALE`：主体，深灰三件套，先观察再说话。
- `LADY_ELEANOR`：壁炉旁，抿凉茶不喝，手触珍珠项链，不看尸体。
- `CLARA_VALE`：窗边，弹落长烟灰，冷笑防御。
- `OWEN`：火边，转身外露，抱怨暴风雪。
- `MORRIS`：门边，扶正小边桌后抬头，极正式。
- `ARTHUR_VALE`：酒柜旁，最平静，礼貌近乎冰冷，一句点破“房间比人重要”。

## 场景与道具

- 场景：`SCENE_DRAWING_ROOM`。
- 道具：凉茶杯、香烟、被撞歪的小边桌、酒柜。
- 光线：壁炉暖金 + 窗外冷蓝。
- 色调：低饱和。

## 动作链路

```text
30-35s：Hale 缓缓走进客厅中央，摄影机绕他轻微半圆移动；他开始问“刚才诸位都在做什么”。
35-40s：镜头先到 Eleanor：她抿了一口凉茶却没喝下，手指轻触珍珠项链；说自己在音乐室，不看尸体。
40-44s：镜头滑到 Clara：抽一口烟，弹落长长的烟灰；轻描淡写说在楼上收拾行李，带冷笑。
44-48s：镜头移向 Owen：从烤火中突然转身，情绪外露，说在车库检查车，这种鬼天气哪儿也去不了；不耐烦看向窗外。
48-53s：镜头到 Morris：先扶正被撞歪的小边桌，才抬头，极正式地说端夜酒时发现门锁着、叫来众人撞门。
53-60s：最后到 Arthur：最平静，轻轻抬眼，说自己在台球室，再补一句“一间从里面锁上的书房，比谁在哪里更重要”；Hale 与 Arthur 第一次真正对视。
```

## 运镜

- 全段：缓慢半圆环绕 + 镜头滑行（glide），一人接一人，行为即介绍。
- 尾段：缓慢推近至 Arthur，对视定格。

## 台词（钉子句，建议后期配音；原生音频只做环境声）

- HALE: "Where was everyone?"
- ELEANOR: "The music room."
- CLARA: "Upstairs. Packing."
- OWEN: "Garage. He'd just told me I was finished. Not that anyone's leaving in this bloody storm."
- MORRIS: "I brought Sir Adrian his usual night drink. The door was already locked."
- ARTHUR: "Billiard room. Alone. Though surely the locked door is rather more interesting than any of us."

## 音效

- 脚步、壁炉噼啪、风声拍窗、打火机、吐烟、家具轻响、衣料声、低沉安静。

## 视频 Prompt 摘要（API 直投原文，逐字透传）

本文件为人工审阅版；API 直投版请使用 `director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词）。

## 负面提示词

```text
不要字幕，不要水印，不要logo，不要可读文字；不要动漫风，不要游戏CG感，不要塑料皮肤；不要静态拉图，不要图片变形过渡，不要人物瞬移，不要换房间；不要换脸，不要东方面孔，不要夸张表情，不要手舞足蹈；不要金黄色满屏（壁炉暖光仅限光源范围）；不要静态定格超过1秒
```
