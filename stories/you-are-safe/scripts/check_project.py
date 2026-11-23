#!/usr/bin/env python3
"""本地文本与结构核验；不调用模型，不把缺失媒体当作已交付。"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HAN = re.compile(r"[\u4e00-\u9fff]")
SPEAKERS = (
    "客服画外音", "客服画外", "母亲画外", "医生画外", "朵朵画外",
    "陈默很轻", "朵朵母亲", "车站广播", "自动广播", "陈默", "客服",
    "母亲", "医生", "朵朵", "司机", "校长", "矿工", "军官", "旁白",
)
SPEECH = re.compile(
    "(?:" + "|".join(SPEAKERS) + ")：(.*?)"
    "(?=(?:" + "|".join(SPEAKERS) + ")：|$)"
)


def check():
    errors, versions, speech_priority = [], [], []
    source = ROOT / "source/director-design-v2.md"
    original = source.read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "source/source-manifest.json").read_text())
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != manifest["sha256"]:
        errors.append("归档原文SHA-256与初始manifest不符")
    source_prompts = re.findall(r"```text\n(.*?)\n```", original, re.S)
    if len(source_prompts) != 12:
        errors.append("原文导演代码块数量不是12")
    detailed_book = ROOT / "docs/two-minute-detailed-director-prompts-v2.md"
    detailed_blocks = (re.findall(r"```text\n(.*?)\n```", detailed_book.read_text(), re.S)
                       if detailed_book.is_file() else [])
    if len(detailed_blocks) != 8:
        errors.append("两分钟详细总稿必须包含八段完整导演代码块")

    required_docs = [
        "README.md", "AGENTS.md", "docs/story-memory.md", "docs/production-rules.md",
        "docs/workflow.md", "docs/season-arc.md", "docs/audience-strategy.md",
        "docs/design-review.md", "docs/adaptation-notes-2min.md",
        "docs/two-minute-reading-script.md", "docs/two-minute-detailed-director-prompts-v2.md",
    ]
    for name in required_docs:
        if not (ROOT / name).is_file():
            errors.append(f"缺少项目文档：{name}")

    for name, duration, count, per_segment, per_shot in [
        ("SF001_6min-source", 360, 12, 30, 8),
        ("SF002_2min-adaptation", 120, 8, 15, 4),
    ]:
        ep = ROOT / "episodes" / name
        data = json.loads((ep / "timeline.json").read_text())
        segments = data["segments"]
        if data["duration"] != duration or len(segments) != count:
            errors.append(f"{name}总时长或段数不符")
        actual_dirs = {p.name for p in ep.glob("segment_*") if p.is_dir()}
        if actual_dirs != {seg["directory"] for seg in segments}:
            errors.append(f"{name}目录与timeline不同步")
        cursor, shot_count, frames_present = 0, 0, 0
        metrics = []
        for seg in segments:
            sid, folder = seg["id"], ep / seg["directory"]
            expected = f"segment_{sid:02d}_{seg['start']:02d}-{seg['end']:02d}s"
            if seg["directory"] != expected:
                errors.append(f"{name}/{sid}目录未按实际秒数命名")
            if seg["start"] != cursor or seg["end"] - seg["start"] != per_segment:
                errors.append(f"{name}/{sid}分段时间不连续或长度错误")
            cursor = seg["end"]
            for f in ["storyboard.md", "first-frame.md", "last-frame.md", "prompt.md",
                      "director-promt.txt", "api-request.md"]:
                p = folder / f
                if not p.is_file() or not p.read_text().strip():
                    errors.append(f"缺少非空分段文件：{p.relative_to(ROOT)}")
            for d in ["frames", "output"]:
                if not (folder / d).is_dir():
                    errors.append(f"缺少{folder.relative_to(ROOT)}/{d}")
            frames_present += sum((folder / "frames" / f).is_file()
                                  for f in ["first-frame.png", "last-frame.png"])
            for cid in seg["character_ids"]:
                if not (ROOT / "assets/characters" / cid / "00-character-card.md").is_file():
                    errors.append(f"角色卡不存在：{cid}")
            for scid in seg["scene_ids"]:
                if not (ROOT / "assets/scenes" / scid / "scene-card.md").is_file():
                    errors.append(f"场景卡不存在：{scid}")
            shots = seg["shots"]
            if len(shots) != per_shot:
                errors.append(f"{name}/{sid}镜头数错误")
            shot_cursor, spoken_han = 0, 0
            for index, shot in enumerate(shots, 1):
                if (shot["id"] != index or shot["start"] != shot_cursor
                        or shot["end"] <= shot["start"]):
                    errors.append(f"{name}/{sid}/{index}镜头ID或时间错误")
                shot_cursor = shot["end"]
                raw_speech = SPEECH.findall(shot["sound"])
                # 排除表演注记和非台词后缀，统计的是汉字负荷而非实际音频时长。
                cleaned = [re.sub(r"[（(].*?[）)]", "", p).split("；")[0]
                           .split("。随后")[0] for p in raw_speech]
                n = sum(len(HAN.findall(p)) for p in cleaned)
                spoken_han += n
                rate = n / (shot["end"] - shot["start"])
                if rate > 4:
                    speech_priority.append(dict(version=name, segment=sid, shot=index,
                                                han=n, han_per_second=round(rate, 2),
                                                line=shot["sound"]))
                # 防止结构化镜头更新后未同步到人类表格和模型输入。
                for f in ["director-promt.txt", "storyboard.md"]:
                    if shot["action"] not in (folder / f).read_text():
                        errors.append(f"{name}/{sid}/{index}画面与{f}不同步")
                if name.startswith("SF002"):
                    required_fields = {
                        "lens": "景别与机位", "action": "画面内容与人物调度",
                        "composition": "竖屏构图与层次", "camera": "镜头路径与速度",
                        "focus": "对焦与材质", "light": "本镜灯光",
                        "timing": "动作节奏与剪辑", "sound": "声音与台词",
                        "result": "必须看见的结果", "continuity_detail": "连续性与避错",
                        "repair": "偏差重拍边界",
                    }
                    full = shot.get("full_text", "")
                    for key, label in required_fields.items():
                        if not shot.get(key) or f"{label}：{shot[key]}" not in full:
                            errors.append(f"短版{sid}/{index}缺少或未同步{label}")
                    for f in ["director-promt.txt", "storyboard.md"]:
                        if full not in (folder / f).read_text():
                            errors.append(f"短版{sid}/{index}导演详表与{f}不同步")
                    for ref in shot.get("source_refs", []):
                        if not (1 <= ref.get("segment", 0) <= 12 and 1 <= ref.get("shot", 0) <= 8):
                            errors.append(f"短版{sid}/{index}原稿镜头引用不存在")
                    if not shot.get("source_refs"):
                        errors.append(f"短版{sid}/{index}缺少六分钟镜头参考")
            shot_count += len(shots)
            if shot_cursor != per_segment:
                errors.append(f"{name}/{sid}镜头未铺满本段")
            direct = (folder / "director-promt.txt").read_text().strip()
            prompt_blocks = re.findall(r"```text\n(.*?)\n```", (folder / "prompt.md").read_text(), re.S)
            if prompt_blocks != [direct]:
                errors.append(f"{name}/{sid}可读prompt与直投txt不一致")
            if "SF001" in name and sid <= len(source_prompts):
                if direct != source_prompts[sid - 1].strip():
                    errors.append(f"六分钟{sid}导演稿不再与归档原文一致")
                measured = len(HAN.findall(source_prompts[sid - 1]))
                if measured != seg["declared_han"] or measured < 3000:
                    errors.append(f"六分钟{sid}原稿汉字数声明不符")
                metrics.append(dict(segment=sid, declared_han=seg["declared_han"],
                                    measured_han=measured, chars=len(source_prompts[sid - 1]),
                                    spoken_han=spoken_han))
            else:
                if sid > len(detailed_blocks) or detailed_blocks[sid - 1] != direct:
                    errors.append(f"短版{sid}总稿与分段导演稿不一致")
                measured = len(HAN.findall(direct))
                metrics.append(dict(segment=sid, spoken_han=spoken_han, director_han=measured,
                                    director_chars=len(direct), detailed_shots=len(shots)))
        if cursor != duration:
            errors.append(f"{name}末点不是{duration}秒")
        versions.append(dict(version=name, duration_seconds=duration, segments=len(segments),
                             shots=shot_count, average_shot_seconds=duration / shot_count,
                             frames_planned=count * 2, frames_present=frames_present,
                             segment_metrics=metrics))

    placeholders = re.compile(r"STORY_TITLE|STORY_ID|CHARACTER_ID|SCENE_ID|PROP_ID")
    for p in ROOT.rglob("*.md"):
        if "source" not in p.relative_to(ROOT).parts and placeholders.search(p.read_text()):
            errors.append(f"未替换模板占位符：{p.relative_to(ROOT)}")
    report = dict(date="2026-10-21", timezone="Asia/Shanghai",
                  text_structure_status="PASS" if not errors else "FAIL", errors=errors,
                  source_sha256=digest, versions=versions,
                  speech_audition_priority=speech_priority,
                  speech_heuristic="仅汉字/镜头秒数；大于4提示优先试听，不代表已证明过快；小于等于4也不代表音频通过",
                  media_status="NOT_RUN", api_generation_status="NOT_RUN",
                  human_design_review="OPEN：原稿问题及两分钟风险见design-review.md与adaptation-notes-2min.md",
                  note="PASS仅指本脚本列举的文本、目录、同步、原文保真检查；不含语义自动证明、模型生成或成片验收")
    out = ROOT / "docs/validation-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = ["# 本地静态检查结果", "检查日期：2026-10-21（Asia/Shanghai）。",
             f"**文本结构：{report['text_structure_status']}，{len(errors)}个结构错误。**",
             "这不代表设计问题已关闭，也不代表图片、API或视频通过。原稿保真、时间覆盖、目录和表格同步均在本次检查范围。",
             "| 版本 | 秒数 | 段 | 镜 | 平均镜长 | 已有首尾图片/计划 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for v in versions:
        lines.append(f"| {v['version']} | {v['duration_seconds']} | {v['segments']} | {v['shots']} | {v['average_shot_seconds']}秒 | {v['frames_present']}/{v['frames_planned']} |")
    lines += ["## 原稿汉字核验", "统计U+4E00—U+9FFF；只计各段A的text代码块。",
              "| 段 | 声明 | 实测 | 提示词字符数 |", "| --- | --- | --- | --- |"]
    for m in versions[0]["segment_metrics"]:
        lines.append(f"| {m['segment']:02d} | {m['declared_han']} | {m['measured_han']} | {m['chars']} |")
    lines += ["## 两分钟详细导演稿核验", "八段总稿、prompt.md、director-promt.txt与逐镜详表已逐段比对；"
              "每镜检查十一项导演字段及六分钟原稿镜头参考。字段完整不代表实际镜头执行已通过。",
              "| 段 | 导演汉字 | 字符 | 详细镜头数 |", "| --- | --- | --- | --- |"]
    for m in versions[1]["segment_metrics"]:
        lines.append(f"| {m['segment']:02d} | {m['director_han']} | {m['director_chars']} | {m['detailed_shots']} |")
    lines += ["## 优先试听项", report["speech_heuristic"]]
    for p in speech_priority:
        lines.append(f"- {p['version']} 第{p['segment']:02d}段第{p['shot']}镜：{p['han']}字，{p['han_per_second']}字/秒。{p['line']}")
    lines += ["两分钟稿未发现大于4字/秒的标注台词，但停顿、双人轮次、表演和动作完成均未试听或看片。",
              "## 未执行", "图片生成与视觉检查、统一配音试听、模型账号/输入能力核验、视频生成、合成解码、全片观看与发布均为NOT_RUN。",
              "## 设计问题", "原稿未应用勘误；两分钟全球清除升级与母亲情绪铺垫需试片，见design-review.md和adaptation-notes-2min.md。",
              "## 错误明细"]
    lines += errors or ["无本脚本检测到的结构错误。"]
    blocks, table = [], []
    for line in lines:
        if line.startswith("|"):
            table.append(line)
        else:
            if table:
                blocks.append("\n".join(table))
                table = []
            blocks.append(line)
    if table:
        blocks.append("\n".join(table))
    (ROOT / "docs/validation-report.md").write_text("\n\n".join(blocks) + "\n")
    print(json.dumps({k: report[k] for k in ["text_structure_status", "errors", "media_status", "api_generation_status"]}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(check())
