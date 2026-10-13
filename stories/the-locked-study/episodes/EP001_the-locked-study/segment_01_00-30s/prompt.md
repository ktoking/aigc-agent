# Segment 01 视频提示词

## 视频规格

- 画幅：16:9 横屏。
- 时长：30 秒。
- 模型：Seedance 2.5（seedance_2.5），图生视频。
- 风格：真人实拍电影质感，英国雪夜庄园悬疑，低饱和，冷蓝暴风雪 vs 暖金壁炉。
- 清晰度：目标 720p+。
- 无字幕、无屏幕文字。

## 输入帧

- 首帧：`first-frame.md`（庄园门口，Hale 跺雪登场）
- 尾帧：`last-frame.md`（大客厅，众人目光汇聚 Hale）

## 角色锁定

- `EDWARD_HALE`：45 岁英国男性，深色带灰短发，黑色羊毛大衣（室外覆雪）、深灰三件套、皮手套、暗色皮靴。
- `LADY_ELEANOR`：52 岁，黑丝绒长裙、珍珠项链、灰金盘发、苍白高贵、端凉茶。
- `CLARA_VALE`：28 岁，深褐长发、深色连衣裙、夹烟、眼神飘向风雪。
- `ARTHUR_VALE`：55 岁，银灰背头、深色三件套、礼貌冰冷微笑、整理袖口。
- `OWEN`：38 岁，深棕乱发、粗花呢外套、湿靴、焦躁搓手。
- `MORRIS`：65 岁，白发、燕尾服、白手套、笔直。
- 尸体 Sir Adrian：倒在书桌边，非血腥，压抑构图。

## 场景与道具

- 场景：`SCENE_MANOR_EXTERIOR`（0-5s）→ `SCENE_DRAWING_ROOM`（10-30s）→ STUDY 门口（18-30s）。
- 道具：白兰地酒杯（半杯琥珀色）、怀表、门锁（被撞坏）。
- 光线：门灯昏黄 → 壁炉暖金 + 窗外冷蓝。
- 色调：低饱和。

## 动作链路

```text
0-5s：暴风雪夜庄园外景，门被猛地推开，Hale 从风雪里出现，肩头覆雪，在门垫上重重跺脚抖雪。
5-10s：Hale 摘皮手套、呼出白气；Morris 上前接大衣，压低声音报告发现尸体、书房门从里面反锁、刚刚撞开。
10-18s：肩后跟随 Hale 穿过门厅进大客厅；镜头不拍尸体，一次扫过五人（Eleanor 茶杯 / Clara 长烟灰 / Arthur 袖口 / Owen 湿靴烤手 / Morris 笔直）。
18-24s：Hale 到书房门口停下；过肩第一次看到尸体——Sir Adrian 倒在书桌边，台灯亮，半杯酒，不血腥，压抑。
24-30s：Hale 回头看向众人；Eleanor 开口、Arthur 补一句；所有人视线汇聚到 Hale；他沉默，只看门锁、酒杯、每个人的鞋。
```

## 运镜

- 0-5s：全景→中景，门框构图，轻微手持。
- 5-10s：中景双人。
- 10-18s：肩后跟随长镜头，横向扫过五人。
- 18-24s：过肩固定，缓慢推进。
- 24-30s：中景环绕，众人反应逐个入画。

## 台词（钉子句，建议后期配音；原生音频只做环境声）

- MORRIS: "I found him. The study was locked from the inside. We had to force the door."
- ELEANOR: "So you're Edward Hale. Adrian's detective friend."
- ARTHUR: "Then I suppose this is your evening now, Mr. Hale."

## 音效

- 狂风呼啸、雪粒拍打、门铰链、跺脚声、脚步、布料摩擦、壁炉噼啪、低沉安静。

## 视频 Prompt 摘要（API 直投原文，逐字透传）

本文件为人工审阅版；API 直投版请使用 `director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词）。

```text
16:9, live-action cinematic English detective short film, realistic European cast, British snowstorm manor mystery, ... (详见 director-promt.txt)
```

## 负面提示词

```text
不要字幕，不要水印，不要logo，不要可读文字；不要动漫风，不要游戏CG感，不要塑料皮肤；不要静态拉图，不要图片变形过渡，不要人物瞬移，不要换房间；不要换脸，不要东方面孔，不要血腥，不要夸张表情；不要金黄色满屏（壁炉暖光仅限光源范围）；不要静态定格超过1秒
```
