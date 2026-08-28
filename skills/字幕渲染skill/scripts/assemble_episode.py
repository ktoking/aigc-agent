#!/usr/bin/env python3
"""Normalize and concatenate the four standard episode segment videos."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


SEGMENTS = (
    "segment_01_00-15s",
    "segment_02_15-30s",
    "segment_03_30-45s",
    "segment_04_45-60s",
)


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def probe(path: Path) -> dict:
    result = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_type,width,height,r_frame_rate",
        "-of", "json", str(path),
    ])
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", required=True, type=Path)
    parser.add_argument("--output-name", default="episode-assembled-source.mp4")
    args = parser.parse_args()

    episode = args.episode.resolve()
    videos = [episode / segment / "output" / "video.mp4" for segment in SEGMENTS]
    missing = [str(path) for path in videos if not path.is_file()]
    if missing:
        raise SystemExit("Missing required segment video(s):\n" + "\n".join(missing))

    metadata = [probe(path) for path in videos]
    video_streams = [next((stream for stream in item["streams"] if stream["codec_type"] == "video"), None) for item in metadata]
    audio_streams = [next((stream for stream in item["streams"] if stream["codec_type"] == "audio"), None) for item in metadata]
    if any(stream is None for stream in video_streams) or any(stream is None for stream in audio_streams):
        raise SystemExit("Every segment must include both video and audio streams.")

    target = video_streams[0]
    width, height = target["width"], target["height"]
    frame_rate = target.get("r_frame_rate") or "24/1"
    output_dir = episode / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / args.output_name

    filters: list[str] = []
    concat_inputs: list[str] = []
    for index in range(len(videos)):
        filters.append(
            f"[{index}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={frame_rate},"
            f"format=yuv420p[v{index}]"
        )
        filters.append(
            f"[{index}:a]aresample=48000,aformat=channel_layouts=stereo[a{index}]"
        )
        concat_inputs.append(f"[v{index}][a{index}]")
    filters.append(f"{''.join(concat_inputs)}concat=n={len(videos)}:v=1:a=1[v][a]")

    command = ["ffmpeg", "-y"]
    for video in videos:
        command.extend(["-i", str(video)])
    command.extend([
        "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output),
    ])
    subprocess.run(command, check=True)
    print(json.dumps({
        "output": str(output),
        "segments": [str(path) for path in videos],
        "duration_seconds": sum(float(item["format"]["duration"]) for item in metadata),
        "target": {"width": width, "height": height, "frame_rate": frame_rate},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
