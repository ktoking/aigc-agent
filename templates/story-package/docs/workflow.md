# STORY_TITLE 生产工作流

## 生成前读取

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. 上一集 `episode.md`、`continuity.md`、`overview-storyboard.md`
6. 相关角色卡、场景卡、道具卡、风格文件

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

- Segment 01：
- Segment 02：
- Segment 03：
- Segment 04：

## 生成顺序

1. 确认本集任务和短视频钩子。
2. 选择角色、场景、道具、特效。
3. 写 `episode.md`。
4. 写 `overview-storyboard.md`。
5. 写 `continuity.md`。
6. 写 4 段 `storyboard.md`。
7. 写 4 段 `first-frame.md` 和 `last-frame.md`。
8. 写 4 段 `prompt.md`。
9. 写 4 段 `director-promt.txt`，用于视频 API 直投。
10. 写 4 段 `api-request.md`，Prompt 默认指向 `director-promt.txt`。
11. 写 `qa-checklist.md` 和 `publish-package.md`。

## 质量检查

-
