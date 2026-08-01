# 《我是所有系统的主人》生产工作流

## 生成前读取

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. 上一集 `episode.md`、`continuity.md`、`overview-storyboard.md`
6. 相关角色、场景、道具和风格资产卡
7. 根目录 `docs/methods/douyin-short-drama-method.md`
8. 根目录 `docs/contracts/video-api-handoff.md`

## 每集目录

```text
episodes/EPXXX_slug/
  episode.md
  overview-storyboard.md
  continuity.md
  image-manifest.md
  qa-checklist.md
  publish-package.md
  segment_01_00-15s/
    storyboard.md
    first-frame.md
    last-frame.md
    prompt.md
    director-promt.txt
    api-request.md
    frames/
    output/
  segment_02_15-30s/
  segment_03_30-45s/
  segment_04_45-60s/
```

## 四段节奏

- Segment 01：前 5 秒给出资格、医疗、工资或尊严上的具体损失。
- Segment 02：反派加码，让顾沉必须在反抗与保护妹妹之间选择。
- Segment 03：顾沉表面服从，同时取得证据或完成一次不暴露身份的小反制。
- Segment 04：管理员权限推进一个明确数值或模块，并抛出下一步审计目标。

## 隐忍进度检查

每集写作前必须回答：

1. 顾沉本集具体失去或承受了什么？
2. 他为什么现在不能公开反击？
3. 他利用这次忍让拿到了什么？
4. 反派为 EP010 的清算增加了哪一条证据？
5. 观众本集得到的暗爽是什么？

如果第 3-5 项没有明确答案，不得继续写“顾沉隐忍”。

## 生成顺序

1. 确认本集在 EP001-EP010 审计链中的证据任务。
2. 选择不超过 3 个主要场景与必要角色。
3. 写 `episode.md`、`overview-storyboard.md`、`continuity.md`。
4. 写四段故事板和首尾帧。
5. 写四段 `prompt.md` 和 `director-promt.txt`。
6. 写 `api-request.md`，默认上传首帧、尾帧和最易漂移的角色/场景参考。
7. 写 `qa-checklist.md` 和 `publish-package.md`。
8. 检查系统 UI 是否克制、台词是否真实、隐忍是否有收益。

## 质量检查

- 是否遵守 EP001-EP009 不公开彻底复仇。
- 是否每集至少推进一条证据或一个权限模块。
- 是否用现实资源制造压迫，而不是只让反派辱骂。
- 是否让顾沉保持主动判断，而非被动等待。
- 是否有 5 秒钩子、四段留存和具体结尾问题。
- 是否保持角色服装、场景光线、系统特效和首尾帧连续。
