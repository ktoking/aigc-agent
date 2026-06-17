# Twin Dawn 生产工作流

## 目标

把《末日重生：双生曙光》制作成连续竖屏 AI 短剧。生产时必须使用固定故事记忆、锁定角色参考、可复用场景/道具资产、每集四段结构和首尾帧连续性。

## 生成或更新剧集前必须读取

1. `docs/story-memory.md`
2. `docs/production-rules.md`
3. `docs/audience-strategy.md`
4. `docs/season-arc.md`
5. `assets/style/global-style.md`
6. `assets/style/camera-language.md`
7. `assets/style/negative-prompts.md`
8. 上一集的 `episode.md`、`continuity.md`、`overview-storyboard.md`
9. 相关角色卡
10. 相关场景卡
11. 相关道具/特效卡
12. 本目录 `templates/`，如果没有对应模板再使用根目录模板

## 剧集目录

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
    prompt.md
    first-frame.md
    last-frame.md
    api-request.md
    frames/
    output/
  segment_02_15-30s/
    storyboard.md
    prompt.md
    first-frame.md
    last-frame.md
    frames/
    output/
  segment_03_30-45s/
    storyboard.md
    prompt.md
    first-frame.md
    last-frame.md
    frames/
    output/
  segment_04_45-60s/
    storyboard.md
    prompt.md
    first-frame.md
    last-frame.md
    frames/
    output/
```

## 四段节奏

- Segment 01：承接上一集钩子，制造即时压力。
- Segment 02：迫使角色做选择、揭示信息或加重危险。
- Segment 03：释放异能爽点、情绪爽点、反转或秘密。
- Segment 04：展示后果，并用新钩子结束。

## 每段必须包含

- `storyboard.md`：镜头表、首帧要求、尾帧要求、优化后视频提示词、连续性检查。
- `first-frame.md`：本段首帧图提示词，继承上一段尾帧。
- `last-frame.md`：本段尾帧图提示词，为下一段首帧提供状态。
- `prompt.md`：可直接给视频 API / 图生视频工具使用的 15 秒以内视频提示词。
- `api-request.md`：推荐生成，用于记录视频 API 参数、提交结果和重试策略。

## 每集推荐包含

- `qa-checklist.md`：检查留存、剧情、连续性、视频 API 可提交性和发布包装。
- `publish-package.md`：标题候选、封面大字、简介、评论区引导和标签方向。

## 质量检查

- 林晚是否匹配 `assets/characters/double-hero-final-reference.png` 左侧人物。
- 沈清雪是否匹配 `assets/characters/double-hero-final-reference.png` 右侧人物。
- 林晚左眼下淡痣是否保留。
- 沈清雪是否保持短发和白色服装方向。
- 顾景辰是否保持精英、克制、危险感，不能脸谱化。
- 本集是否有明确爽点、情绪推进和结尾钩子。
- 四段首尾帧是否能自然接上。
- Prompt 是否避免动漫、游戏 UI、AI 脸、过度血腥、低成本 cosplay 和风格漂移。
