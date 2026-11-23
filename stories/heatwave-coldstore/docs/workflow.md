# 生产工作流：热浪吞城后，我拥有全城最后的冷库

## 生成前读取

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. `../drafts/` 下最新已确认剧本与 `../reviews/` 检查记录
6. `assets/` 角色卡、场景卡、道具卡、风格文件（建立后）

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

## EP001 四段节奏

- Segment 01（0-15s）：温度计对比钩子——室外 51°C，我睡在冷库门口；身份反差（五天前理货员/今天只剩我）。
- Segment 02（15-30s）：闪回疏散日——老周拉人上车、主角留下；当晚电网崩溃，拉起柴油机。
- Segment 03（30-45s）：家底与规则——药、冻货、柴油倒计时；冻西瓜与添油巡检兑现"冷"的爽点与代价。
- Segment 04（45-60s）：月台敲门——监控里的女人与提货单；她身后的五个人影收尾。

## 生成顺序

1. 确认本集任务和短视频钩子。
2. 选择角色、场景、道具、特效。
3. 写 `episode.md`。
4. 写 `overview-storyboard.md`、`continuity.md`。
5. 写 4 段 `storyboard.md`、`first-frame.md`、`last-frame.md`。
6. 写 4 段 `prompt.md`、`api-request.md`（如走视频 API）。
7. MiniMax 配音，按实测语音时长排画面。
8. 生图、合成，写 `qa-checklist.md`、`publish-package.md`。

## 质量检查

- 交稿前执行仓库 `skills/story-film-workflow/references/script-language-checklist.md`（L01—L06、S01—S06），记录存 `../reviews/`。
- 每段首尾帧继承、门禁方向、温度计与油表读数纳入 `continuity.md` 核对。
- 视频产物放对应 segment 的 `output/`；不接入 Skynet，不加 Git hooks。
