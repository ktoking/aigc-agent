#!/usr/bin/env python3
"""Copy each segment last frame to the next segment first frame."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


class LinkError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument("--apply", action="store_true", help="Actually copy files. Default is dry-run.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing next first-frame.png.")
    parser.add_argument("--manifest", type=Path, help="Manifest path. Defaults to episode frame-inheritance-manifest.json.")
    args = parser.parse_args()

    episode_dir = args.episode_dir.resolve()
    segments = sorted(path for path in episode_dir.glob("segment_*") if path.is_dir())
    if len(segments) < 2:
        raise LinkError(f"Need at least two segment_* directories under {episode_dir}")

    manifest: dict[str, object] = {
        "episode_dir": str(episode_dir),
        "mode": "apply" if args.apply else "dry-run",
        "overwrite": args.overwrite,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "links": [],
    }

    for current, nxt in zip(segments, segments[1:]):
        source = current / "frames" / "last-frame.png"
        target = nxt / "frames" / "first-frame.png"
        if not source.is_file():
            raise LinkError(f"Missing source frame: {source}")
        if target.exists() and not args.overwrite:
            action = "skip-existing"
        else:
            action = "copy" if args.apply else "would-copy"
            if args.apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        entry = {
            "from_segment": current.name,
            "to_segment": nxt.name,
            "source": str(source),
            "target": str(target),
            "action": action,
            "source_sha256": sha256(source),
            "target_sha256": sha256(target) if target.is_file() else None,
        }
        manifest["links"].append(entry)
        print(f"{action}: {current.name}/last-frame.png -> {nxt.name}/first-frame.png")

    manifest_path = args.manifest or (episode_dir / "frame-inheritance-manifest.json")
    if args.apply:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LinkError as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
