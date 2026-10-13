# Segment 03 视频提示词

## 视频规格

- 画幅：16:9 横屏。
- 时长：30 秒。
- 模型：Seedance 2.5（seedance_2.5），图生视频。
- 风格：与 Segment 01/02 同一连续性；受控的 Fincher 式运镜 + 韩式悬疑张力 + Apple 式电影摄影。
- 无字幕、无屏幕文字。

## 输入帧

- 首帧：`first-frame.md`（落地钟敲响，房间静止一瞬）
- 尾帧：`last-frame.md`（Hale 停在书房门口，众人跟随，尸体深背景）

## 角色锁定

- `EDWARD_HALE`：主体，不看钟看人；最后走向书房，表情沉静坚定。
- `LADY_ELEANOR`：皱眉嫌失礼；轻声指认 Arthur 是最后一个陪酒的人。
- `CLARA_VALE`：掐灭烟立刻点第二支；吐烟盯尸体方向补刀。
- `ARTHUR_VALE`：冷淡一句化解；被指认时轻轻一笑；微笑在尾帧出现第一道裂纹。
- `OWEN`：爆发抱怨暴风雪；抓住机会跟进“对，我也看见了”。
- `MORRIS`：平稳打断“那并不能说明什么”，眼里有紧张。

## 场景与道具

- 场景：`SCENE_DRAWING_ROOM`（落地钟、壁炉、书房门口）。
- 道具：香烟、打火机、茶杯。
- 光线：壁炉暖金 + 窗外冷蓝；尾段书房台灯光锥入画。
- 色调：低饱和。

## 动作链路

```text
60-65s：落地钟响，低沉一声；整个房间安静一瞬；Hale 不看钟，看的是人。
65-72s：Clara 掐灭一支烟立刻点起第二支；Owen 烦躁爆发“这该死的风雪到底还要多久”；Eleanor 皱眉嫌他失礼；Arthur 淡淡一句化解。
72-78s：Eleanor 轻声指认 Arthur 是最后一个陪丈夫喝酒的人；切 Arthur：轻轻一笑不慌；Owen 立刻跟进“对，我也看见了”。
78-83s：Morris 平稳打断，说那并不能说明什么，眼里有紧张；Clara 吐一口烟，盯着尸体方向说谁都可以趁晚餐后动手。
83-90s：Hale 终于开口，慢慢走向书房门口；摄影机倒退跟拍，众人下意识跟着移动；他说“你们都在告诉我他死的时候你们在哪，可这不是我要问的”；所有人安静，停在门槛外。
```

## 运镜

- 60-72s：镜头在反应间细微移动（优雅环绕）。
- 72-83s：切近景（Arthur）→ 中景（Morris → Clara）。
- 83-90s：倒退跟拍，形成移动群像，停在书房门口。

## 台词（钉子句，建议后期配音；原生音频只做环境声）

- OWEN: "How long is this bloody storm going to last?"
- ARTHUR: "Long enough for complaining to remain useless."
- ELEANOR: "You were the last person drinking with Adrian."
- OWEN: "I saw them."
- ARTHUR: "Having a drink with an old friend is hardly murder."
- MORRIS: "It proves nothing."
- CLARA: "If hating Adrian makes one a suspect... you'll need a larger room."
- HALE: "You're all telling me where you were when Adrian died. That's the wrong question. The question is... when did his murder begin?"

## 音效

- 落地钟低沉一声、打火机、吐烟、风声拍窗、脚步、壁炉、静默。

## 视频 Prompt 摘要（API 直投原文，逐字透传）

本文件为人工审阅版；API 直投版请使用 `director-promt.txt`（homecoming 式生产详版：超细节镜头拆解 + 英文台词）。

## 负面提示词

```text
不要字幕，不要水印，不要logo，不要可读文字；不要动漫风，不要游戏CG感，不要塑料皮肤；不要静态拉图，不要图片变形过渡，不要人物瞬移，不要换房间；不要换脸，不要东方面孔，不要夸张表情，不要戏剧化手舞足蹈；不要金黄色满屏（壁炉暖光仅限光源范围）；不要静态定格超过1秒
```
