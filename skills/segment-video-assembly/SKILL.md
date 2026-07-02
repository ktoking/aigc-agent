---
name: segment-video-assembly
description: Assemble AI short-drama shot videos into a complete segment video. Use after mini shot videos under a segment shots/ directory finish generating, especially when some shots may have audio and others may need silent audio padding before ffmpeg concat.
---

# Segment Video Assembly

## Workflow

Use this skill when the user asks to stitch, merge, assemble, concatenate, or export generated shot videos into one segment video.

1. Confirm `ffmpeg` and `ffprobe` are available.
2. Poll/download pending shot tasks first if the user asks to assemble after generation.
3. Prefer final named files in each shot `output/` directory:
   - `video-*-audio.mp4`
   - `video-*.mp4`
   - `video.mp4`
4. Run `scripts/assemble_segment.py` against the segment directory.
5. Verify the assembled output with `ffprobe` for duration, resolution, frame rate, and audio stream.

## Standard Command

```bash
python3 scripts/assemble_segment.py \
  --segment stories/<story-id>/episodes/<episode>/segment_01_00-15s \
  --output-name segment01-assembled.mp4
```

The script reads `shots/shot_*`, normalizes all videos to 720x1280, 24 fps, H.264/AAC, adds silent audio if a shot has no audio, then concatenates them into `segment/output/<output-name>`.

## Rules

- Do not include `output/api-result.json`, signed URLs, task ids, or generated videos in Git unless explicitly requested.
- If a shot is missing a video, stop and report the missing shot instead of assembling a partial segment.
- If the latest shot with audio and an older silent shot both exist, prefer the audio version.
