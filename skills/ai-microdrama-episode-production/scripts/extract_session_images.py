#!/usr/bin/env python3
"""Extract image_generation_end images from Codex JSONL session files."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SEGMENT_RE = re.compile(r"Segment\s*0?(\d{1,2})\s*(FIRST|LAST)\s*FRAME", re.I)
ALT_SEGMENT_RE = re.compile(r"segment[_\s-]*0?(\d{1,2}).*?(first|last)[_\s-]*frame", re.I)


def iter_nodes(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_nodes(child)


def infer_segment(prompt: str) -> tuple[int | None, str]:
    match = SEGMENT_RE.search(prompt) or ALT_SEGMENT_RE.search(prompt)
    if not match:
        return None, "asset"
    return int(match.group(1)), match.group(2).lower()


def image_extension(raw: bytes) -> str | None:
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
        return "webp"
    return None


def safe_call_id(node: dict[str, Any]) -> str:
    raw = str(node.get("call_id") or node.get("id") or "noid")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw)[:80]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_jsonl", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--story-id", help="Only keep images whose revised prompt contains this story id.")
    parser.add_argument("--episode-id", help="Only keep images whose revised prompt contains this episode id.")
    parser.add_argument("--only-segment-frames", action="store_true")
    parser.add_argument("--no-dedupe", action="store_true")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    seen: set[str] = set()

    with args.session_jsonl.open("r", encoding="utf-8", errors="ignore") as fh:
        for line_no, line in enumerate(fh, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            for node in iter_nodes(record):
                if node.get("type") != "image_generation_end":
                    continue
                encoded = node.get("result")
                if not isinstance(encoded, str):
                    continue
                prompt = str(node.get("revised_prompt") or "")
                if args.story_id and args.story_id not in prompt:
                    continue
                if args.episode_id and args.episode_id not in prompt:
                    continue
                segment, kind = infer_segment(prompt)
                if args.only_segment_frames and segment is None:
                    continue
                try:
                    raw = base64.b64decode(encoded, validate=False)
                except Exception:
                    continue
                ext = image_extension(raw)
                if ext is None:
                    continue
                sha = hashlib.sha256(raw).hexdigest()
                if not args.no_dedupe and sha in seen:
                    continue
                seen.add(sha)
                seg_label = f"seg{segment:02d}" if segment is not None else "seg00"
                filename = f"line{line_no:04d}-{seg_label}-{kind}-{safe_call_id(node)}.{ext}"
                path = args.out / filename
                path.write_bytes(raw)
                manifest.append(
                    {
                        "line": line_no,
                        "path": str(path),
                        "sha256": sha,
                        "bytes": len(raw),
                        "segment": segment,
                        "kind": kind,
                        "prompt_preview": prompt[:240].replace("\n", " "),
                    }
                )

    manifest_path = args.out / "extracted-images-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"extracted={len(manifest)} out={args.out}")
    print(f"manifest={manifest_path}")
    for item in manifest:
        segment = item["segment"] if item["segment"] is not None else "-"
        print(f"{item['line']:>5} seg={segment} kind={item['kind']:<5} {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
