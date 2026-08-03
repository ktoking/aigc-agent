#!/usr/bin/env python3
"""Build a live-action motion-comic HyperFrames segment from a JSON spec."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def media_duration(path: Path) -> float:
    """Return the real duration of an audio asset instead of trusting a planned slot."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def retime_to_complete_voice(project: Path, spec: dict) -> None:
    """Lay each spoken line in full, then let its real duration drive all visuals.

    Earlier drafts assigned every TTS line a guessed sub-second window in a
    fixed 15-second segment. HyperFrames correctly obeyed that window, which
    made otherwise valid TTS audio sound chopped. This pass keeps a short
    breath between lines but never trims spoken audio to satisfy a segment cap.
    """
    tts_outputs = {line["output"] for line in spec.get("tts", [])}
    spoken = [item for item in spec["audio"] if item["src"] in tts_outputs]
    if not spoken:
        raise ValueError("Audio-led timing requires TTS items in spec['audio']")

    original_starts = {id(item): float(item["start"]) for item in spoken}
    cursor = 0.15
    gap = float(spec.get("voice_gap", 0.24))
    retimed_starts: list[tuple[float, float]] = []
    for item in spoken:
        duration = media_duration(project / item["src"])
        item["start"] = round(cursor, 3)
        item["duration"] = round(duration, 3)
        retimed_starts.append((original_starts[id(item)], float(item["start"])))
        cursor += duration + gap

    composition_duration = round(cursor + float(spec.get("tail_hold", 0.65)), 3)

    def map_time(old_time: float) -> float:
        """Map a planned timestamp to the start of its containing spoken beat."""
        prior = retimed_starts[0]
        for point in retimed_starts:
            if point[0] > old_time:
                break
            prior = point
        return prior[1]

    # Ambient beds stretch to the completed dialogue. Non-verbal effects keep
    # their planned relationship to the nearest spoken beat without cutting it.
    for item in spec["audio"]:
        if item in spoken:
            continue
        old_start = float(item["start"])
        source = item["src"]
        if item["id"] == "ambient":
            item["start"] = 0
            item["duration"] = composition_duration
        else:
            item["start"] = round(map_time(old_start) + 0.12, 3)
            item["duration"] = round(media_duration(project / source), 3)

    shots = spec["shots"]
    old_shot_starts = [float(shot["start"]) for shot in shots]
    new_shot_starts = [0.0] + [map_time(start) for start in old_shot_starts[1:]]
    for index, shot in enumerate(shots):
        shot["start"] = round(new_shot_starts[index], 3)
        next_start = new_shot_starts[index + 1] if index + 1 < len(shots) else composition_duration
        shot["duration"] = round(next_start - new_shot_starts[index], 3)
        for field in ("caption_start", "caption2_start", "bubble_start"):
            if field in shot:
                shot[field] = round(map_time(float(shot[field])), 3)

    spec["composition_duration"] = composition_duration


def write_index(project: Path, spec: dict) -> None:
    comp_id = spec["composition_id"]
    title = html.escape(spec["title"])
    shots = spec["shots"]
    audios = spec["audio"]
    audio_tags = []
    for item in audios:
        attrs = [
            f'id="{html.escape(item["id"])}"',
            f'data-start="{item["start"]}"',
            f'data-duration="{item["duration"]}"',
            f'data-track-index="{item["track"]}"',
            f'src="{html.escape(item["src"])}"',
        ]
        if "volume" in item:
            attrs.insert(4, f'data-volume="{item["volume"]}"')
        audio_tags.append("<audio " + " ".join(attrs) + "></audio>")

    sections = []
    for idx, shot in enumerate(shots, start=1):
        caption = html.escape(shot.get("caption", ""))
        bubble = html.escape(shot.get("bubble", ""))
        extra = ""
        if caption:
            extra += f'<div id="c{idx}" class="caption">{caption}</div>'
        if shot.get("caption2"):
            extra += f'<div id="c{idx}b" class="caption caption2">{html.escape(shot["caption2"])}</div>'
        if bubble:
            extra += f'<div id="b{idx}" class="bubble">{bubble}</div>'
        if shot.get("rift"):
            extra += f'<div id="rift{idx}" class="rift"></div>'
        if shot.get("gold"):
            extra += f'<div id="gold{idx}" class="gold"></div>'
        sections.append(
            f'<section id="s{idx}" class="clip" data-start="{shot["start"]}" '
            f'data-duration="{shot["duration"]}" data-track-index="1">'
            f'<img id="i{idx}" class="frame" src="assets/{html.escape(shot["image"])}">'
            f'{extra}<div class="grade"></div></section>'
        )

    timeline = []
    for idx, shot in enumerate(shots, start=1):
        start = shot["start"]
        duration = shot["duration"]
        if idx > 1:
            timeline.append(f".to('#s{idx}',{{opacity:1,duration:.24}},{start})")
        timeline.append(
            f".fromTo('#i{idx}',{{scale:{shot['from_scale']},x:{shot['from_x']},y:{shot['from_y']}}},"
            f"{{scale:{shot['to_scale']},x:{shot['to_x']},y:{shot['to_y']},duration:{duration},ease:'power1.inOut'}},{start})"
        )
        if shot.get("caption"):
            timeline.append(f".from('#c{idx}',{{opacity:0,y:18,duration:.25}},{shot.get('caption_start', start + .15)})")
        if shot.get("caption2"):
            timeline.append(f".from('#c{idx}b',{{opacity:0,y:18,duration:.25}},{shot.get('caption2_start', start + 2.5)})")
        if shot.get("bubble"):
            timeline.append(f".from('#b{idx}',{{opacity:0,scale:.9,y:20,duration:.25}},{shot.get('bubble_start', start + .15)})")
        if shot.get("rift"):
            timeline.append(f".to('#rift{idx}',{{opacity:1,duration:.45}},{start + .18})")
        if shot.get("gold"):
            timeline.append(f".to('#gold{idx}',{{opacity:1,duration:.25}},{start + .12}).to('#gold{idx}',{{opacity:.15,duration:.9}},{start + 1.2})")

    duration = spec.get("composition_duration", 15)
    source = f'''<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>{title}</title><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#05080c}}@font-face{{font-family:PingFang SC;src:local("PingFang SC")}}body{{font-family:"PingFang SC",sans-serif}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}.clip{{position:absolute;inset:0;overflow:hidden;opacity:0;background:#05080c}}#s1{{opacity:1}}.frame{{position:absolute;inset:-9%;width:118%;height:118%;object-fit:cover;transform-origin:center;filter:saturate(.8) contrast(1.08) brightness(.9)}}.grade{{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 38%,rgba(0,0,0,.58));pointer-events:none}}.caption{{position:absolute;left:58px;right:58px;bottom:96px;color:#fff;font-size:42px;font-weight:650;line-height:1.35;text-align:center;text-shadow:0 3px 16px #000;opacity:0}}.caption2{{bottom:184px}}.bubble{{position:absolute;left:60px;top:500px;max-width:520px;padding:23px 29px;border:1px solid rgba(255,220,210,.7);border-radius:32px 32px 32px 12px;background:rgba(48,22,29,.82);color:#fff7f2;font-size:44px;font-weight:700;line-height:1.3;opacity:0}}.rift{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 20%,rgba(160,196,255,.36),transparent 33%);opacity:0;pointer-events:none}}.gold{{position:absolute;inset:0;background:radial-gradient(ellipse at 52% 42%,rgba(255,206,92,.38),transparent 30%);mix-blend-mode:screen;opacity:0;pointer-events:none}}</style></head><body><div id="root" data-composition-id="{comp_id}" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920" data-fps="30">{''.join(audio_tags)}{''.join(sections)}</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl{''.join(timeline)};window.__timelines['{comp_id}']=tl;</script></body></html>'''
    (project / "index.html").write_text(source)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    project = Path(spec["project_dir"]).resolve()
    project.mkdir(parents=True, exist_ok=True)
    for name in ["audio", "assets", "output", "scripts"]:
        (project / name).mkdir(exist_ok=True)
    for src in spec.get("copy_audio", []):
        shutil.copy2(src["from"], project / src["to"])
    tts = project / "scripts/synthesize_doubao_tts.py"
    if not tts.exists():
        shutil.copy2(spec["tts_script"], tts)
    for line in spec.get("tts", []):
        out = project / line["output"]
        if not out.exists():
            run([
                "python3", str(tts),
                "--text", line["text"],
                "--speaker", line["speaker"],
                "--context", line["context"],
                "--output", line["output"],
                "--speech-rate", str(line.get("speech_rate", 0)),
            ], project)
    retime_to_complete_voice(project, spec)
    write_index(project, spec)
    run(["npx", "--yes", "hyperframes@0.7.58", "check", "."], project)
    run(["npx", "--yes", "hyperframes@0.7.58", "render", ".", "--output", spec["render_output"], "--quiet"], project)
    target = Path(spec["copy_output_to"]).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(project / spec["render_output"], target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
