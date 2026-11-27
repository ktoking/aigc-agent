# 生产工作流 · 302 寝事

## 阶段 0：设定（已完成）

- `AGENTS.md`：故事说明 + 角色锁 + 视觉前缀/负面 + 季节奏。
- `docs/production-rules.md`：硬规则。
- `docs/story-memory.md` / `docs/season-arc.md`：世界观与一季结构。
- `assets/style/*`：风格、镜头、负面。
- `assets/characters/C0X_*/`：三视图 PNG + `lock.md`（锁档）+ `expressions.md`（表情表）。
- `assets/scenes/S0X_*/`：场景参考图 + `lock.md`。

## 阶段 1：分集与分镜

1. 写 `episodes/EP00X_xxx/episode-plan.json`（段表、时间、帧号）。
2. 写 `storyboard.md`（全片镜头表）与 `dialogue-v1.md`（台词表）。
3. 每段写 `director-promt.txt`（15 秒版，含秒级子节拍、首尾帧、声音、负面）。
4. 每段准备 `frames/`：首帧图（必须）、关键动作参考图 2–4 张。

## 阶段 2：生图（首帧与参考）

- 三视图先行，确认三人身份后所有关键帧都以三视图为参考图（image_edit / image_to_video 参考）。
- 关键帧要求：16:9、4K 级、暖绿逆光、人物服装与三视图一致。
- 命名：`frames/01_s01_xxx.png`，编号与分镜号对应。

## 阶段 3：生成视频

- 段与段优先合并 30 秒，用 `seedance_2.5` + 30s；不可用回退 `seedance_2.0` + 15s。
- 提示词直接提交 `director-promt.txt` 全文，不精简。
- 参考图一次最多 10 张（工具限制），按镜头优先级精选。

## 阶段 4：后期

1. 去水印：`mediakit-cli video erase-video-subtitle-pro --mode Text --erase-ratio-location '[{"top_left_x":0,"top_left_y":0,"bottom_right_x":1,"bottom_right_y":0.16},{"top_left_x":0,"top_left_y":0.84,"bottom_right_x":1,"bottom_right_y":1}]'`
2. 画质：`enhance-video --resolution 4k --fps 60 --tool-version professional`（多段并行）。
3. 拼接：`concat-video` 加转场 + `fade-video-audio` 淡入淡出。
4. 片头：`scripts/add_opening_title.py`（《302 寝事 / ROOM 302 DIARIES》）。
5. 字幕与配音在剪辑软件中完成（画面内不生成文字）。

## 交付物

- `episodes/EP001_wake-up/EP001_final.mp4`（2 分钟成片）
- 各段 4K/60 视频、关键帧图、生成记录 `DOUBAO-GEN-RECORD.md`
