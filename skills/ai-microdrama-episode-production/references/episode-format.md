# Episode Format Reference

## Files To Create

Each episode must create exactly these narrative files:

- `episode.md`
- `continuity.md`
- `overview-storyboard.md`
- `segment_01_00-15s/storyboard.md`
- `segment_01_00-15s/first-frame.md`
- `segment_01_00-15s/last-frame.md`
- `segment_01_00-15s/prompt.md`
- Repeat the same four segment files for `segment_02_15-30s`, `segment_03_30-45s`, and `segment_04_45-60s`.

Also create empty `frames/` and `output/` directories for each segment if missing.

## `episode.md`

Use these sections:

- Title: `# EPXXX 标题`
- `## 基本信息`
- `## 出场角色`
- `## 剧情梗概`
- `## 情绪曲线`
- `## 分段概览`
- `## 关键对白`
- `## 发布标题候选`
- `## 备注`

## `continuity.md`

Use these sections:

- Title: `# EPXXX 连续性表`
- `## 上一集承接`
- `## 本集固定状态`
- `## 人物连续性`
- `## 分段桥接`
- `## 禁止偏差`

Always include the sentence that the double-hero final reference image has highest priority.

## `overview-storyboard.md`

Use these sections:

- Title: `# EPXXX 60秒概述故事板：标题`
- `## 本集一句话`
- `## 总体节奏`
- `## 总览表`
- `## 本集关键画面`
- `## 本集关键对白`
- `## 本集生成总提示词`
- `## 检查清单`

## Segment `storyboard.md`

Use these sections:

- Title: `# Segment XX 故事板：段落标题`
- `## 分段信息`
- Shot table with columns: `镜头 | 时间 | 画面内容 | 运镜方式 | 台词 | 音效`
- `## 首帧要求`
- `## 尾帧要求`
- `## 优化后提示词`
- `## 连续性检查`

## Segment `prompt.md`

Use this order:

1. Video spec: 9:16, duration, style, live-action quality, lighting, resolution.
2. Character locks and reference image instructions.
3. Narrative action and camera movement.
4. Dialogue.
5. Sound design.
6. Negative prompt.

## Naming

- Use `EP003_short-english-slug` for new episode directories.
- Use Chinese titles inside content.
- Keep segment directory names fixed:
  - `segment_01_00-15s`
  - `segment_02_15-30s`
  - `segment_03_30-45s`
  - `segment_04_45-60s`

## Director Checklist

- Does the opening connect to the previous hook?
- Does the first 5 seconds create pressure or curiosity?
- Is there one unmistakable payoff or reversal?
- Does the final shot force the next episode?
- Are all faces locked to reference images?
- Are all props and scene cards used consistently?
- Can each segment be generated independently with first/last frames?
- Are negative prompts specific enough to prevent face drift, style drift, and video artifacts?
