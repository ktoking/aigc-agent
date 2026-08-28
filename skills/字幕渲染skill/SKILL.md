---
name: 字幕渲染skill
description: 合并四段短剧视频，以本地剧本台词和实际语音时间轴生成无标点中文字幕，渲染并校验最终成片。
---

# Episode Final Video Delivery

Use this skill after an episode's four segment videos have been generated and accepted for delivery. It complements `segment-video-assembly`: that skill assembles shots inside one segment; this one assembles the four completed segments into a 60-second episode.

## Inputs and outputs

- Input episode directory: `stories/<story-id>/episodes/<episode-id>/`
- Required source videos, in this order:
  - `segment_01_00-15s/output/video.mp4`
  - `segment_02_15-30s/output/video.mp4`
  - `segment_03_30-45s/output/video.mp4`
  - `segment_04_45-60s/output/video.mp4`
- Output directory: `<episode>/output/`
- Standard artifacts:
  - `<episode-code>-assembled-source.mp4`: normalized four-segment source.
  - `<episode-code>-captioned.mp4`: final, subtitle-burned delivery video.
  - `<episode-code>-zh.srt`: canonical subtitle sidecar.
  - `<episode-code>-final-delivery.json`: source paths, ChatCut project/export ids, checks, and known warnings.

## Workflow

1. Check that all four source files exist. Use `ffprobe` to verify each has a video stream, an audio stream, sensible duration, and compatible orientation. Do not silently substitute a missing segment.
2. Run `scripts/assemble_episode.py --episode <episode-dir> --output-name <episode-code>-assembled-source.mp4`. The script normalizes streams then concatenates in segment directory order.
3. Create a fresh ChatCut project for the complete episode. Never reuse a single-segment subtitle test project.
4. Import the assembled source using ChatCut's `import_media` session and its official `upload-media.mjs` helper. Add it once at frame zero on the primary video track.
5. Default to **script-first captions**: use the local `storyboard.md` / `director-promt.txt` dialogue as the subtitle text. Use automatic Chinese captions only to obtain approximate phrase timing; correct every text card from the local dialogue before export. This prevents ASR errors caused by mouth slips, homophones, and unclear model diction.
6. Build a semantic timing map before replacing text: keep each actual ASR card's start/end time and actual speaking order, then substitute the closest matching local dialogue phrase. Do not map lines merely by screenplay order: AI video can reorder adjacent lines even when the prompt specifies the intended speaker order.
7. When a spoken delivery is materially shortened, split the canonical dialogue across adjacent ASR timing cards. When the video omits a screenplay phrase entirely, omit its subtitle rather than placing it in an unrelated silence. Do not burn raw ASR text unless the user explicitly asks for verbatim speech captions.
8. Produce **punctuation-free viewer captions** by default: remove Chinese and English commas, periods, question/exclamation marks, colons, semicolons, quotation marks, ellipses, dashes, and enumeration commas from subtitle text only. Never alter SRT timecode punctuation such as `:` and `,`.
9. Apply a readable Chinese subtitle preset such as `white-impact`; keep captions in the lower safe area and avoid covering faces when possible.
10. Preview multiple points across all four quarters of the timeline. Confirm captions render, video is nonblank, dialogue remains aligned, and no viewer-facing punctuation remains.
11. Export both an H.264 480p video and an SRT from ChatCut, or burn the corrected SRT locally with `ffmpeg` when local dialogue correction is more reliable. Download/save both into the episode `output/` directory using stable names above.
12. Use `ffprobe` on the final MP4 and inspect at least two frames from different parts of the final render. Record pass/fail and any pre-existing segment-quality warnings in `<episode-code>-final-delivery.json`.

## Guardrails

- Keep the source segment order fixed: 01, 02, 03, 04.
- Local screenplay dialogue is the canonical subtitle text. ASR is a timing aid, not an authority on Chinese wording.
- Remove punctuation only from subtitle cue text. Keep SRT timecode syntax intact, then validate the SRT before rendering.
- This delivery step does not regenerate videos. If a source segment has a known visual defect, preserve that warning in the delivery manifest and proceed only when the user asked for final assembly.
- Do not use media files as Git artifacts unless the user explicitly asks. Keep prompts, manifests, and code versionable; leave MP4/MP3 output untracked by default.
- Preserve the current story's visual-continuity rules while generating any replacement media upstream; this skill only delivers already-selected sources.
