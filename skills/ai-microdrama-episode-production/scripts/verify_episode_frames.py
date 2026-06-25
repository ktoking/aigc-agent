#!/usr/bin/env python3
"""Verify first/last frame placement for an AI microdrama episode."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path
from typing import Any


REQUIRED_FRAME_NAMES = ("first-frame.png", "last-frame.png")


def png_size(raw: bytes) -> tuple[int, int] | None:
    if not raw.startswith(b"\x89PNG\r\n\x1a\n") or len(raw) < 24:
        return None
    return struct.unpack(">II", raw[16:24])


def jpeg_size(raw: bytes) -> tuple[int, int] | None:
    if not raw.startswith(b"\xff\xd8"):
        return None
    index = 2
    while index + 9 < len(raw):
        if raw[index] != 0xFF:
            index += 1
            continue
        marker = raw[index + 1]
        index += 2
        if marker in (0xD8, 0xD9):
            continue
        if index + 2 > len(raw):
            return None
        length = struct.unpack(">H", raw[index : index + 2])[0]
        if marker in range(0xC0, 0xC4) or marker in range(0xC5, 0xC8) or marker in range(0xC9, 0xCC) or marker in range(0xCD, 0xD0):
            if index + 7 <= len(raw):
                height = struct.unpack(">H", raw[index + 3 : index + 5])[0]
                width = struct.unpack(">H", raw[index + 5 : index + 7])[0]
                return width, height
        index += length
    return None


def image_size(path: Path) -> tuple[int, int] | None:
    raw = path.read_bytes()
    return png_size(raw) or jpeg_size(raw)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_aspect(value: str | None) -> tuple[float, str] | None:
    if not value:
        return None
    left, right = value.split(":", 1)
    return float(left) / float(right), value


def check_aspect(width: int, height: int, expected: tuple[float, str] | None, tolerance: float) -> str | None:
    if expected is None:
        return None
    ratio = width / height
    if math.isclose(ratio, expected[0], rel_tol=tolerance, abs_tol=tolerance):
        return None
    return f"aspect {ratio:.4f} != {expected[1]}"


def make_contact_sheet(image_paths: list[Path], output: Path, thumb_width: int = 320) -> str | None:
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return make_contact_sheet_with_system_tools(image_paths, output, thumb_width)

    thumbs = []
    for index, path in enumerate(image_paths, 1):
        with Image.open(path) as img:
            img = img.convert("RGB")
            ratio = thumb_width / img.width
            thumb_height = max(1, int(img.height * ratio))
            img = img.resize((thumb_width, thumb_height))
            canvas = Image.new("RGB", (thumb_width, thumb_height + 24), "white")
            canvas.paste(img, (0, 0))
            draw = ImageDraw.Draw(canvas)
            draw.text((6, thumb_height + 5), f"{index:02d} {path.parent.parent.name}/{path.name}", fill="black")
            thumbs.append(canvas)

    columns = 4 if len(thumbs) <= 16 else 5
    rows = math.ceil(len(thumbs) / columns)
    cell_w = thumb_width
    cell_h = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "white")
    for idx, thumb in enumerate(thumbs):
        x = (idx % columns) * cell_w
        y = (idx // columns) * cell_h
        sheet.paste(thumb, (x, y))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    return None


def make_contact_sheet_with_system_tools(image_paths: list[Path], output: Path, thumb_width: int = 320) -> str | None:
    if not shutil.which("sips") or not shutil.which("ffmpeg"):
        return "Pillow, sips, or ffmpeg is not available; skipped contact sheet."
    output.parent.mkdir(parents=True, exist_ok=True)
    columns = 4 if len(image_paths) <= 16 else 5
    rows = math.ceil(len(image_paths) / columns)
    with tempfile.TemporaryDirectory(prefix="episode-frame-thumbs-") as tmp:
        tmp_dir = Path(tmp)
        for index, path in enumerate(image_paths, 1):
            thumb = tmp_dir / f"{index:03d}.png"
            subprocess.run(
                ["sips", "-Z", str(thumb_width), str(path), "--out", str(thumb)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-pattern_type",
                "glob",
                "-i",
                str(tmp_dir / "*.png"),
                "-filter_complex",
                f"tile={columns}x{rows}:padding=8:margin=8:color=white",
                str(output),
            ],
            check=True,
        )
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument("--expected-segments", type=int)
    parser.add_argument("--aspect", help="Expected aspect ratio, e.g. 16:9 or 9:16.")
    parser.add_argument("--aspect-tolerance", type=float, default=0.03)
    parser.add_argument("--allow-mixed-dimensions", action="store_true")
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    episode_dir = args.episode_dir.resolve()
    segment_dirs = sorted([p for p in episode_dir.glob("segment_*") if p.is_dir()])
    expected_aspect = parse_aspect(args.aspect)
    errors: list[str] = []
    warnings: list[str] = []
    frames: list[dict[str, Any]] = []
    frame_paths: list[Path] = []

    if args.expected_segments is not None and len(segment_dirs) != args.expected_segments:
        errors.append(f"segment count {len(segment_dirs)} != expected {args.expected_segments}")
    if not segment_dirs:
        errors.append("no segment_* directories found")

    dimensions: set[tuple[int, int]] = set()
    for segment in segment_dirs:
        frame_dir = segment / "frames"
        if not frame_dir.is_dir():
            errors.append(f"missing frames directory: {segment.relative_to(episode_dir)}")
            continue
        for frame_name in REQUIRED_FRAME_NAMES:
            path = frame_dir / frame_name
            if not path.is_file():
                errors.append(f"missing {path.relative_to(episode_dir)}")
                continue
            size = image_size(path)
            if size is None:
                errors.append(f"unsupported or unreadable image: {path.relative_to(episode_dir)}")
                continue
            dimensions.add(size)
            aspect_error = check_aspect(size[0], size[1], expected_aspect, args.aspect_tolerance)
            if aspect_error:
                errors.append(f"{path.relative_to(episode_dir)} {aspect_error}")
            frame_paths.append(path)
            frames.append(
                {
                    "segment": segment.name,
                    "name": frame_name,
                    "path": str(path),
                    "width": size[0],
                    "height": size[1],
                    "sha256": sha256(path),
                }
            )

    if len(dimensions) > 1 and not args.allow_mixed_dimensions:
        errors.append(f"mixed dimensions: {sorted(dimensions)}")

    contact_sheet_status = None
    if args.contact_sheet and frame_paths:
        contact_sheet_status = make_contact_sheet(frame_paths, args.contact_sheet)
        if contact_sheet_status:
            warnings.append(contact_sheet_status)

    result = {
        "episode_dir": str(episode_dir),
        "segments": len(segment_dirs),
        "frames": len(frames),
        "expected_frames": len(segment_dirs) * len(REQUIRED_FRAME_NAMES),
        "dimensions": sorted([list(item) for item in dimensions]),
        "errors": errors,
        "warnings": warnings,
        "contact_sheet": str(args.contact_sheet.resolve()) if args.contact_sheet else None,
        "items": frames,
    }

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
