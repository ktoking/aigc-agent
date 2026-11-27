# 302 寝事 / Room 302 Diaries

日系 3D CG 泡面番项目。第一季 6 集，每集 2 分钟（8 段 × 15 秒），16:9。
本仓库已完成 **EP001《七点整，闹钟响了第三次》** 的全套前置资产：人设三视图、场景参考、8 段导演提示词、8 张关键帧。

## 三个人

| ID | 角色 | 定位 | 身高 | 一句话 |
|---|---|---|---|---|
| C01 | 桃柒（粉发） | 傲娇，常年挂耳机 | 160 | 嘴硬到最后一秒，然后偷偷把吐司分你一半 |
| C02 | 星籁（紫发） | 鬼点子，人形弹幕 | 168 | 负责把普通早晨搞成事故现场，顺便嗑 CP |
| C03 | 白砚（白发） | 高冷兜底，大四建筑 | 172 | 话最少，动作最多；替人整理时从不看眼睛 |

## 画风

日系 3D CG（Galgame / 游戏宣传 CG 质感），不是 2D 平涂、不是真人。
统一"暖绿逆光"：窗光暖金 4300K 逆光 + 绿植冷绿反射补光 + 室内暖白反光板；轮廓光过曝，发丝透光，体积光里有浮尘，背景压暗成暖绿 bokeh。

## 目录

```
AGENTS.md                     故事说明 / 角色锁 / 视觉前缀与负面 / 季表
docs/production-rules.md      硬规则
docs/season-arc.md            第一季 6 集结构 + EP001 分段表
docs/story-memory.md          世界设定与关系事实
docs/workflow.md              从设定到成片的流程
assets/style/                 全局风格、镜头语言、负面词库
assets/characters/C0X_*/      三视图 PNG + lock.md + three-view.prompt.md
assets/scenes/S0X_*/          场景参考 PNG + lock.md
episodes/EP001_wake-up/
  episode-plan.json           8 段 × 15s 段表
  storyboard.md               全片 32 个镜头表
  dialogue-v1.md              台词与配音提示
  连续性.md                    服装 / 状态 / 距离连续性
  segment_XX_.../             director-promt.txt + first/last-frame.md + frames/ + output/
```

## 下一步

1. 用 `director-promt.txt` 全文提交 seedance 2.5（相邻两段合并 30s），参考图优先用各段 `frames/first-frame.png`。
2. 生成后去水印 → 4K/60 增强 → 拼接 → 片头（详见 `docs/workflow.md`）。
3. EP002–EP006 已有分段大纲，可按同一模板续写。
