#!/usr/bin/env python3
"""Assemble generated shot videos into a complete segment video."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


PREFERRED_PATTERNS = (
    "video-*-audio.mp4",
    "video-*.mp4",
    "video.mp4",
)


class AssembleError(RuntimeError):
    pass


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise AssembleError(f"{name} is not installed or not on PATH")


def probe(path: Path) -> dict:
    result = run([
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,width,height,r_frame_rate,avg_frame_rate",
        "-of",
        "json",
        str(path),
    ])
    return json.loads(result.stdout)


def has_audio(path: Path) -> bool:
    data = probe(path)
    return any(stream.get("codec_type") == "audio" for stream in data.get("streams", []))


def choose_video(shot_dir: Path) -> Path:
    output_dir = shot_dir / "output"
    for pattern in PREFERRED_PATTERNS:
        matches = sorted(output_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        if matches:
            return matches[0]
    raise AssembleError(f"missing generated video in {output_dir}")


def normalize(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    audio_args: list[str]
    map_args: list[str]
    filter_complex: list[str]
    if has_audio(input_path):
        audio_args = []
        map_args = ["-map", "0:v:0", "-map", "0:a:0"]
        filter_complex = []
    else:
        audio_args = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        map_args = ["-map", "0:v:0", "-map", "1:a:0", "-shortest"]
        filter_complex = []

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        *audio_args,
        *filter_complex,
        *map_args,
        "-vf",
        "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        str(output_path),
    ]
    run(cmd)


def concat(normalized_paths: list[Path], output_path: Path) -> None:
    list_path = output_path.parent / f".{output_path.stem}-concat.txt"
    list_text = "".join(f"file '{path.as_posix()}'\n" for path in normalized_paths)
    list_path.write_text(list_text, encoding="utf-8")
    run([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-c",
        "copy",
        str(output_path),
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble shot videos into a segment video.")
    parser.add_argument("--segment", required=True, help="Segment directory containing shots/shot_*")
    parser.add_argument("--output-name", default="segment-assembled.mp4")
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args()

    try:
        require_tool("ffmpeg")
        require_tool("ffprobe")
        segment_dir = Path(args.segment).resolve()
        shots_dir = segment_dir / "shots"
        if not shots_dir.exists():
            raise AssembleError(f"shots directory not found: {shots_dir}")
        shot_dirs = sorted(path for path in shots_dir.glob("shot_*") if path.is_dir())
        if not shot_dirs:
            raise AssembleError(f"no shot directories found under {shots_dir}")

        output_dir = segment_dir / "output"
        work_dir = output_dir / ".assembly-work"
        output_dir.mkdir(parents=True, exist_ok=True)
        work_dir.mkdir(parents=True, exist_ok=True)

        normalized_paths: list[Path] = []
        manifest: list[dict] = []
        for index, shot_dir in enumerate(shot_dirs, start=1):
            source = choose_video(shot_dir)
            normalized = work_dir / f"{index:02d}-{shot_dir.name}.mp4"
            normalize(source, normalized)
            normalized_paths.append(normalized)
            manifest.append({
                "shot": shot_dir.name,
                "source": str(source),
                "normalized": str(normalized),
                "source_has_audio": has_audio(source),
            })

        output_path = output_dir / args.output_name
        concat(normalized_paths, output_path)
        result_probe = probe(output_path)
        manifest_path = output_dir / f"{output_path.stem}-manifest.json"
        manifest_path.write_text(
            json.dumps({"shots": manifest, "output": str(output_path), "probe": result_probe}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if not args.keep_work:
            for path in normalized_paths:
                path.unlink(missing_ok=True)
            try:
                work_dir.rmdir()
            except OSError:
                pass
        print(f"assembled={output_path}")
        print(f"manifest={manifest_path}")
        print(json.dumps(result_probe, ensure_ascii=False))
        return 0
    except (AssembleError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            if exc.stderr:
                print(exc.stderr[-2000:], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
