# 首尾帧资产工作流

## 适用场景

当用户要求生成、整理、找回、落位或校验短剧图片资产时，按本流程执行。目标是避免重复生成、错用其他 story 图片、漏放首尾帧。

## 目录标准

每个 segment 的最终首尾帧固定放在：

```text
segment_XX_<time-range>/frames/first-frame.png
segment_XX_<time-range>/frames/last-frame.png
```

如果 story 明确使用 jpg 或 webp，可改扩展名，但同一 episode 内必须统一。默认使用 png。

## 查找顺序

1. 检查目标 episode 自己的 `frames/`。
2. 检查 episode 根目录的 `image-manifest.md`、`api-request.md`、`output/`、任务返回文件。
3. 检查仓库内生成缓存或 staging 目录，但必须用路径、manifest、hash 或视觉内容确认 story id。
4. 检查用户提供的本地图片路径。
5. 检查最近 Codex 会话 JSONL，使用 `scripts/extract_session_images.py` 解包 `image_generation_end`。
6. 只有确认缺图后，才考虑继续生成。

## 错项目防护

- 不要只凭文件名 `segment-01-first-frame.png` 判断归属。
- staging 目录可能包含其他 story 的图片；必须核对 `assigned-images.json`、目标路径、prompt、hash 或视觉内容。
- 若画面主体与 story 锁不符，先停下排查，不要批量复制。
- 用户纠正某张图片时，以用户给出的图片路径和画面为最高优先级，并记录 hash。

## 修正版优先级

同一个 segment/kind 有多张候选时，按以下优先级：

1. 用户明确指定的图片。
2. revised prompt 标注 final correction / correction / regenerate 的较新图片。
3. 明确包含 `Segment XX FIRST FRAME` 或 `Segment XX LAST FRAME` 的原始生成图。
4. 视觉上符合 story 锁和该段提示词的候选图。

不要把旧版和修正版都放成最终名。需要保留时放入 `frames/archive/` 或 manifest，不要混淆 `first-frame.png` / `last-frame.png`。

## 落位步骤

1. 列出所有 segment 目录并按编号排序。
2. 建立映射表：`segment number + first/last -> source image path`。
3. 复制到目标 `frames/first-frame.png` 或 `frames/last-frame.png`。
4. 运行 `scripts/verify_episode_frames.py <episode-dir> --contact-sheet <episode-dir>/frames-contact-sheet.png`。
5. 打开 contact sheet 做视觉检查，确认无错 story、无明显角色漂移、无横竖比例异常。

## 最终校验必须回答

- 一共找到并落位多少张图。
- 每个 segment 是否都有 first/last。
- 图片尺寸是否一致，是否符合 story 要求的画幅。
- 用户指定图的 hash 是否与落位文件一致。
- 是否生成并查看 contact sheet。
- 是否仍有缺图或疑似错图。

## 从会话记录解包示例

```bash
python3 skills/ai-microdrama-episode-production/scripts/extract_session_images.py \
  /Users/<user>/.codex/sessions/YYYY/MM/DD/rollout-xxx.jsonl \
  --out /tmp/story-images \
  --story-id robot-dream-ban \
  --only-segment-frames
```

解包后先看 manifest，再复制，不要直接覆盖最终 frames。

## 校验示例

```bash
python3 skills/ai-microdrama-episode-production/scripts/verify_episode_frames.py \
  stories/<story-id>/episodes/<episode-id> \
  --aspect 16:9 \
  --contact-sheet /tmp/<episode-id>-contact.png
```

若 story 是竖屏短剧，使用 `--aspect 9:16`。
