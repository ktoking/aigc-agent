# 生产工作流：极寒末日，我的房车是移动堡垒（v2）

## 生成前读取

1. `docs/story-memory.md`（人物表、手账台账、伏笔）
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. `drafts/` 最新剧本与 `reviews/` 检查记录
6. `assets/` 角色卡、场景卡（建立后）

## 每集目录（进入制作后按此建立）

```text
episodes/EPXXX_slug/
  episode.md
  continuity.md
  overview-storyboard.md
  image-manifest.md
  qa-checklist.md
  publish-package.md
  segment_01_00-15s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    api-request.md
    frames/
    output/
  segment_02_15-30s/
  segment_03_30-45s/
  segment_04_45-60s/
```

## 第一季四段节奏对照（v2）

| 集 | S01 钩子 | S02 加压 | S03 爽点/反转 | S04 后果+钩子 |
| --- | --- | --- | --- | --- |
| EP001 | 住车第三年+中期预报 | 全部家当算账 | 十天准备清单 | 红色预警升格＋老板灯还亮着 |
| EP002 | 车行断资 | 欠薪对账 | 挑货（发电机+雪铲） | 发电机点亮＋温度计下爬 |
| EP003 | 一夜-26℃ | 爆管+收运转费 | 修爆管换人情 | 手账记账＋锅炉房收钱 |
| EP004 | 油表对不上 | 蹲守 | 头发丝验锁、反拿 | 柴万仓名字浮出 |
| EP005 | 菜价八块 | 团长垄断+谣言 | 批发市场残次菜直采 | 网格员征用登记 |
| EP006 | 条子贴窗 | 民生保供压力 | 修锅炉+孙大爷出山 | 应急煤被上锁 |
| EP007 | 皮卡接人 | 考题（热风炉） | 四十分钟修复+独家谈判 | 车窗贴条 |
| EP008 | 协调会断会 | CO 中毒、救护车占线 | 自驾送医 | 黄牛卖床位 |
| EP009 | 床位没有 | 修发电机换床 | 拦路者的绝望 | 院门被撬 |
| EP010 | 盘点损失 | 排不上号 | 夜移地下车库 | 恶人下场快报＋请柬 |
| EP011 | 红色请柬 | 鸿门宴摊牌 | "这叫门面" | 第二波-45℃预告 |
| EP012 | 钢梁冻响 | 车库人口涌入 | 规矩上墙+炉火成排 | 救援48小时，"油，够" |

## 生成顺序

1. 确认本集冲突目标与尾钩。
2. 角色/场景/道具选型（对照 production-rules）。
3. `episode.md` → `overview-storyboard.md` → `continuity.md`。
4. 4 段 `storyboard.md`、`first-frame.md`、`last-frame.md`。
5. 4 段 `prompt.md`、`api-request.md`。
6. MiniMax 配音，实测时长排画面。
7. 生图、合成，`qa-checklist.md`、`publish-package.md`。

## 质量检查

- 剧本层：L01—L06、S01—S06 全 PASS 后存 `../reviews/`，未处理项为零。
- 制作层：首尾帧继承、冷暖光线、手账/油桶/锁等道具台账纳入 continuity 核对。
- 视频产物放对应 segment 的 `output/`；不接入 Skynet，不加 Git hooks。
