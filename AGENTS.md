# 仓库级说明

## 范围

本仓库是通用 AI 短剧 / AI 漫剧生产框架。根目录只保留通用能力，具体剧本内容必须放在 `stories/<story-id>/`。

后续新增剧本时，不要把人物、人脸锁、故事圣经、世界观、剧集产物写到根目录。

## 根目录职责

- `README.md`：框架总览。
- `docs/workflow.md`：通用生产流程。
- `templates/`：通用中文模板，默认沿用 `twin-dawn` 的剧集结构。
- `skills/`：可作用于任意 story 包的通用 skill。
- `stories/`：每个剧本一个独立工作区。

## Story 目录职责

每个剧本独立维护：

- `stories/<story-id>/AGENTS.md`
- `stories/<story-id>/docs/story-memory.md`
- `stories/<story-id>/docs/production-rules.md`
- `stories/<story-id>/docs/workflow.md`
- `stories/<story-id>/docs/season-arc.md`
- `stories/<story-id>/docs/audience-strategy.md`
- `stories/<story-id>/assets/`
- `stories/<story-id>/episodes/`
- `stories/<story-id>/templates/`，可选，只有需要覆盖通用模板时才创建。

生成或修改某个 story 时，优先遵循该 story 自己的 `AGENTS.md`。

## 默认剧集产物格式

除非用户明确要求改格式，所有 story 的 episodes 都按以下规格生成：

- 一集 60 秒。
- 一集拆成 4 段。
- 每段 15 秒以内。
- 目录固定为 `segment_01_00-15s`、`segment_02_15-30s`、`segment_03_30-45s`、`segment_04_45-60s`。
- 每段必须包含：
  - `storyboard.md`：分段故事板和镜头表。
  - `first-frame.md`：本段首帧图提示词。
  - `last-frame.md`：本段尾帧图提示词。
  - `prompt.md`：可交给视频 API / 图生视频工具的完整视频提示词。
  - `api-request.md`：推荐生成，记录视频 API 参数、提交返回和重试策略。
  - `frames/`：首尾帧、故事板图等图片产物。
  - `output/`：视频 API 返回、生成视频、任务提交记录等产物。
- 每集推荐包含：
  - `qa-checklist.md`：剧集、连续性、API、发布质检。
  - `publish-package.md`：标题、封面、评论引导、标签。

## 内容语言

- 仓库说明、生产文档、模板字段、生成的剧集文本默认使用中文。
- 文件名和目录名可以保留英文 slug，方便工具调用和版本管理。
- 视频 prompt 可以包含必要英文模型关键词，但主体说明、镜头、剧情、对白、连续性检查默认写中文。

## 当前故事包

- `stories/twin-dawn/`：《末日重生：双生曙光 / 末日降临：我和闺蜜觉醒双SSS异能》。

## 通用规则

- 不要在根模板或根 skill 中写死某个剧本的人名、设定、脸部参考图或剧情。
- 新剧本必须新建 `stories/<story-id>/`。
- 特定剧本的特殊规则写入该剧本自己的 `AGENTS.md`、`docs/production-rules.md` 或 story-local templates。
- 视频生成输出放在对应 segment 的 `output/` 目录。
- 新 story 接入优先复制 `templates/story-package/` 的骨架，再按剧本内容改写。
- 新剧集生成前要同时参考 `docs/methods/douyin-short-drama-method.md` 和 `docs/contracts/video-api-handoff.md`。

## 提交与生成隔离

- 本仓库的提交、素材生成、图片生成、视频生成和脚本执行不接入 Skynet 统计流程。
- 不主动运行 `skynet gen`、`skynet fast`、`skynet test-code-gen` 或任何会产生 Skynet 统计/上报记录的命令。
- 提交或推送本仓库改动时，使用不会触发本地 Git hook 的方式；如需执行 `git commit` 或 `git push`，默认使用 `--no-verify`。
- 不新增、启用或依赖 `pre-commit`、`prepare-commit-msg`、`commit-msg`、`post-commit`、`pre-push` 等前置或后置 hook。
