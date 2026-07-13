#!/usr/bin/env python3
import re
import sys
from pathlib import Path


REQUIRED_EPISODE_FILES = {
    "episode.md",
    "overview-storyboard.md",
    "continuity.md",
    "image-manifest.md",
    "qa-checklist.md",
    "publish-package.md",
}
REQUIRED_SEGMENT_FILES = {
    "storyboard.md",
    "first-frame.md",
    "last-frame.md",
    "prompt.md",
    "director-promt.txt",
    "api-request.md",
}
EXPECTED_SEGMENTS = [
    "segment_01_00-15s",
    "segment_02_15-30s",
    "segment_03_30-45s",
    "segment_04_45-60s",
]
SHOT_FIELDS = ("景别：", "构图：", "运镜手法：", "画面内容：")
EXPECTED_SHOT_NAMES = ("一", "二", "三", "四")
DIGITAL_HUMANS = (
    "asset://asset-20260320075237-29hdx",
    "asset://asset-20260320075131-k78qt",
)


def find_repo_root(path: Path) -> Path:
    for candidate in [path, *path.parents]:
        if (candidate / "stories" / "forest-villa-apocalypse").is_dir():
            return candidate
    raise ValueError("repository root containing stories/forest-villa-apocalypse was not found")


def add_error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def validate_segment(repo_root: Path, segment: Path, errors: list[str]) -> None:
    for name in sorted(REQUIRED_SEGMENT_FILES):
        if not (segment / name).is_file():
            add_error(errors, segment, f"missing {name}")
    for name in ("frames", "output"):
        if not (segment / name).is_dir():
            add_error(errors, segment, f"missing {name}/ directory")

    director = segment / "director-promt.txt"
    if not director.is_file():
        return
    text = director.read_text(encoding="utf-8")
    if "16:9" not in text:
        add_error(errors, director, "missing 16:9 specification")
    if "15秒" not in text and "15 秒" not in text:
        add_error(errors, director, "missing 15-second specification")

    shots = list(re.finditer(r"^镜头([一二三四五六七八九十])｜[^\n]+$", text, re.MULTILINE))
    if len(shots) != 4:
        add_error(errors, director, f"expected 4 shots, found {len(shots)}")
    elif tuple(shot.group(1) for shot in shots) != EXPECTED_SHOT_NAMES:
        add_error(errors, director, "shots must be named 镜头一 through 镜头四 in order")
    for index, shot in enumerate(shots):
        end = shots[index + 1].start() if index + 1 < len(shots) else len(text)
        block = text[shot.start():end]
        for field in SHOT_FIELDS:
            if field not in block:
                add_error(errors, director, f"shot {index + 1} missing {field}")
        positions = [block.find(field) for field in SHOT_FIELDS]
        if all(position >= 0 for position in positions) and positions != sorted(positions):
            add_error(errors, director, f"shot {index + 1} fields are out of order")

    if re.search(r"^镜头[^\n]*\d+\s*(?:-|—|至)\s*\d+\s*秒", text, re.MULTILINE):
        add_error(errors, director, "individual shots must not contain timestamps")
    if not re.search(r"^参考图1：", text, re.MULTILINE):
        add_error(errors, director, "missing numbered reference image description")
    if not re.search(r"^声音：", text, re.MULTILINE):
        add_error(errors, director, "missing sound direction")
    if not re.search(r"^禁止：", text, re.MULTILINE):
        add_error(errors, director, "missing segment-specific negative constraints")
    if not re.search(r"^[^\n：]{1,12}(?:画外音)?：\n[“\"]", text, re.MULTILINE):
        add_error(errors, director, "missing formatted dialogue")
    dialogue_lines = re.findall(r"^[“\"]([^”\"\n]+)[”\"]$", text, re.MULTILINE)
    dialogue_chars = sum(len(re.sub(r"[，。！？、；：,.!?]", "", line)) for line in dialogue_lines)
    if len(dialogue_lines) < 6:
        add_error(errors, director, f"dialogue too sparse: expected at least 6 lines, found {len(dialogue_lines)}")
    if dialogue_chars < 70:
        add_error(errors, director, f"dialogue too sparse: expected at least 70 spoken Chinese characters, found {dialogue_chars}")
    if dialogue_chars > 120:
        add_error(errors, director, f"dialogue too dense for 15 seconds: found {dialogue_chars} spoken characters")

    api_request = segment / "api-request.md"
    if api_request.is_file():
        api_text = api_request.read_text(encoding="utf-8")
        for asset_id in DIGITAL_HUMANS:
            if asset_id not in api_text:
                add_error(errors, api_request, f"missing digital human {asset_id}")

    request_payload = segment / "output" / "api-request-payload.json"
    if request_payload.is_file():
        payload_text = request_payload.read_text(encoding="utf-8")
        for asset_id in DIGITAL_HUMANS:
            if asset_id not in payload_text:
                add_error(errors, request_payload, f"digital human was not submitted as image_url: {asset_id}")
    elif (segment / "output" / "api-submit.json").is_file():
        add_error(errors, request_payload, "missing submitted request payload; digital-human inputs cannot be verified")

    for file_path in segment.glob("*"):
        if not file_path.is_file() or file_path.suffix not in {".md", ".txt"}:
            continue
        file_text = file_path.read_text(encoding="utf-8")
        asset_paths = re.findall(
            r"`(stories/forest-villa-apocalypse/[^`]+\.(?:png|jpg|jpeg|webp))`",
            file_text,
        )
        for relative in asset_paths:
            if not (repo_root / relative).is_file():
                add_error(errors, file_path, f"missing referenced asset {relative}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_episode.py <episode-dir>", file=sys.stderr)
        return 2

    episode = Path(sys.argv[1]).resolve()
    if not episode.is_dir():
        print(f"episode directory not found: {episode}", file=sys.stderr)
        return 2

    try:
        repo_root = find_repo_root(episode)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    errors: list[str] = []
    for name in sorted(REQUIRED_EPISODE_FILES):
        if not (episode / name).is_file():
            add_error(errors, episode, f"missing {name}")

    actual_segments = sorted(path.name for path in episode.glob("segment_*") if path.is_dir())
    if actual_segments != EXPECTED_SEGMENTS:
        add_error(
            errors,
            episode,
            f"expected segments {EXPECTED_SEGMENTS}, found {actual_segments}",
        )

    for name in EXPECTED_SEGMENTS:
        segment = episode / name
        if segment.is_dir():
            validate_segment(repo_root, segment, errors)

    if errors:
        print("episode validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"episode validation passed: {episode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
