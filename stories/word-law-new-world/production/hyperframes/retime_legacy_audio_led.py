#!/usr/bin/env python3
"""Re-time a legacy HyperFrames segment so every existing TTS line can finish."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


def attr(attrs: str, name: str, default: str = "") -> str:
    match = re.search(rf'\b{name}="([^"]*)"', attrs)
    return match.group(1) if match else default


def media_duration(path: Path) -> float:
    return float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True).strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--output", required=True)
    parser.add_argument("--copy-output-to", required=True)
    args = parser.parse_args()
    project = Path(args.project).resolve()
    source = (project / "index.html").read_text()
    composition = re.search(r'data-composition-id="([^"]+)"', source).group(1)
    style = re.search(r'(<style>.*?</style>)', source, re.S).group(1)
    root_attrs = re.search(r'<div id="root"([^>]*)>', source).group(1)
    root_attrs = re.sub(r'\sdata-duration="[^"]*"', "", root_attrs)
    audios = []
    for attrs in re.findall(r'<audio\s+([^>]*)></audio>', source):
        audios.append({
            "raw": attrs,
            "id": attr(attrs, "id"),
            "start": float(attr(attrs, "data-start")),
            "duration": float(attr(attrs, "data-duration")),
            "track": attr(attrs, "data-track-index"),
            "src": attr(attrs, "src"),
            "volume": attr(attrs, "data-volume"),
        })
    spoken = [item for item in audios if item["src"].endswith(".mp3")]
    if not spoken:
        raise ValueError("No TTS MP3 tracks found")

    old_to_new = []
    cursor = 0.15
    for item in spoken:
        old_to_new.append((item["start"], cursor))
        item["start"] = round(cursor, 3)
        item["duration"] = round(media_duration(project / item["src"]), 3)
        cursor += item["duration"] + 0.24
    duration = round(cursor + 0.65, 3)

    def mapped(old: float) -> float:
        candidate = old_to_new[0][1]
        for planned, actual in old_to_new:
            if planned > old:
                break
            candidate = actual
        return candidate

    for item in audios:
        if item in spoken:
            continue
        if item["id"] == "ambient":
            item["start"], item["duration"] = 0, duration
        else:
            item["start"] = round(mapped(item["start"]) + 0.12, 3)
            item["duration"] = round(media_duration(project / item["src"]), 3)

    sections = []
    for attrs, body in re.findall(r'<section\s+([^>]*)>(.*?)</section>', source, re.S):
        sections.append({"attrs": attrs, "body": body, "start": float(attr(attrs, "data-start"))})
    new_starts = [0.0] + [mapped(section["start"]) for section in sections[1:]]
    for index, section in enumerate(sections):
        section["new_start"] = round(new_starts[index], 3)
        section["new_duration"] = round((new_starts[index + 1] if index + 1 < len(sections) else duration) - new_starts[index], 3)

    audio_html = []
    for item in audios:
        volume = f' data-volume="{item["volume"]}"' if item["volume"] else ""
        audio_html.append(
            f'<audio id="{item["id"]}" data-start="{item["start"]}" data-duration="{item["duration"]}" '
            f'data-track-index="{item["track"]}"{volume} src="{item["src"]}"></audio>'
        )
    sections_html = []
    for index, section in enumerate(sections, 1):
        body = section["body"]
        sections_html.append(
            f'<section id="s{index}" class="clip" data-start="{section["new_start"]}" '
            f'data-duration="{section["new_duration"]}" data-track-index="1" '
            f'data-layout-allow-overflow data-layout-allow-overlap>{body}</section>'
        )

    timeline = []
    moves = [(1.03, 50, 45, 1.23, -35, -55), (1.0, -55, 35, 1.2, 40, -45)]
    for index, section in enumerate(sections, 1):
        image = re.search(r'<img id="([^"]+)"', section["body"]).group(1)
        m = moves[(index - 1) % len(moves)]
        start = section["new_start"]
        shot_duration = section["new_duration"]
        if index > 1:
            timeline.append(f".to('#s{index}',{{opacity:1,duration:.24}},{start})")
        timeline.append(
            f".fromTo('#{image}',{{scale:{m[0]},x:{m[1]},y:{m[2]}}},"
            f"{{scale:{m[3]},x:{m[4]},y:{m[5]},duration:{shot_duration},ease:'power1.inOut'}},{start})"
        )
        for element_id in re.findall(r'<div id="([^"]+)"', section["body"]):
            trigger = re.search(rf"#{re.escape(element_id)}.*?,([0-9.]+)\)", source)
            when = mapped(float(trigger.group(1))) if trigger else start + 0.15
            if element_id.startswith("rift"):
                timeline.append(f".to('#{element_id}',{{opacity:1,duration:.4}},{when})")
            else:
                timeline.append(f".from('#{element_id}',{{opacity:0,y:18,duration:.25}},{when})")

    html = f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>Audio-led cut</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>{style}</head><body><div id="root"{root_attrs} data-duration="{duration}">{''.join(audio_html)}{''.join(sections_html)}</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl{''.join(timeline)};window.__timelines['{composition}']=tl;</script></body></html>'''
    (project / "index.html").write_text(html)
    subprocess.run(["npx", "--yes", "hyperframes@0.7.58", "check", "."], cwd=project, check=True)
    subprocess.run(["npx", "--yes", "hyperframes@0.7.58", "render", ".", "--output", args.output, "--quiet"], cwd=project, check=True)
    target = Path(args.copy_output_to).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(project / args.output, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
