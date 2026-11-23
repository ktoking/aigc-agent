#!/usr/bin/env python3
"""MiniMax 中文配音：从环境或 Keychain 取密钥，只输出音频和无密钥元数据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request


API_URL = "https://api.minimax.cn/v1/t2a_v2"
KEYCHAIN_SERVICE = "codex-minimax-api-key"
DEFAULT_MODEL = "speech-2.8-turbo"
DEFAULT_VOICE = "Chinese_calm_streamer_nv1"
PRESETS_FILE = Path(__file__).resolve().parent.parent / "references" / "tts-presets.json"
EMOTIONS = ("happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent", "whisper")
EFFECTS = ("spacious_echo", "auditorium_echo", "lofi_telephone", "robotic")


def presets() -> dict:
    return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))["presets"]


def bounded(value, low, high, label, exclusive_low=False):
    if not math.isfinite(value) or not (low < value <= high if exclusive_low else low <= value <= high):
        raise ValueError(f"{label} 超出范围：{'(' if exclusive_low else '['}{low}, {high}]")
    return value


def build_payload(args: argparse.Namespace) -> dict:
    text = args.text if args.text is not None else args.text_file.read_text(encoding="utf-8")
    text = text.strip()
    if not text or len(text) >= 10000:
        raise ValueError("配音文本须为 1 到 9999 字符；长稿请按场景分段。")
    # 停顿已包含在该段音频中，后期不可为它再补一次相同空档。
    pauses = re.findall(r"<#(.*?)#>", text)
    for pause in pauses:
        if not re.fullmatch(r"\d+(?:\.\d{1,2})?", pause):
            raise ValueError("停顿请写成 <#0.35#>，最多两位小数。")
        bounded(float(pause), 0.01, 99.99, "停顿秒数")
    if re.search(r"^\s*<#|#>\s*$|#>\s*<#", text):
        raise ValueError("停顿必须放在可朗读文本之间，不能首尾放置或连续使用。")
    tags = re.findall(r"\((laughs|chuckle|coughs|clear-throat|groans|breath|pant|inhale|exhale|gasps|sniffs|sighs|snorts|burps|lip-smacking|humming|hissing|emm|sneezes)\)", text)
    if tags and args.model not in ("speech-2.8-hd", "speech-2.8-turbo"):
        raise ValueError("语气词标签仅对 speech-2.8-hd/turbo 开放。")
    options = presets()
    if args.preset not in options:
        raise ValueError(f"未知场景预设：{args.preset}；使用 --list-presets 查看。")
    selected = options[args.preset]
    voice = {"voice_id": args.voice, **selected["voice_setting"]}
    for cli, name in (("speed", "speed"), ("vol", "vol"), ("pitch", "pitch"), ("emotion", "emotion")):
        value = getattr(args, cli)
        if value is not None:
            voice[name] = value
    if voice.get("emotion") == "auto":
        voice.pop("emotion")
    if voice.get("emotion") in ("fluent", "whisper") and args.model not in ("speech-2.6-hd", "speech-2.6-turbo"):
        raise ValueError("官方 fluent/whisper 仅支持 speech-2.6-hd/turbo；不自动更换模型。")
    bounded(voice["speed"], 0.5, 2, "语速")
    bounded(voice["vol"], 0, 10, "音量", exclusive_low=True)
    bounded(voice["pitch"], -12, 12, "语调")
    fmt = args.format or (args.output.suffix.lower().lstrip(".") if args.output else "mp3")
    if fmt not in ("mp3", "wav", "flac"):
        raise ValueError("脚本支持 mp3/wav/flac；其他格式需单独处理封装。")
    if args.output and args.output.suffix.lower() != f".{fmt}":
        raise ValueError("输出后缀与音频格式不一致。")
    payload = {
        "model": args.model, "text": text, "stream": False,
        "voice_setting": voice,
        "audio_setting": {"sample_rate": args.sample_rate, "format": fmt, "channel": args.channel},
        "language_boost": args.language_boost,
        "output_format": "hex", "subtitle_enable": False,
    }
    if fmt == "mp3":
        payload["audio_setting"]["bitrate"] = args.bitrate
    modify = dict(selected.get("voice_modify", {}))
    for cli, name in (("modify_pitch", "pitch"), ("intensity", "intensity"), ("timbre", "timbre"), ("sound_effect", "sound_effects")):
        value = getattr(args, cli)
        if value is not None:
            modify[name] = value
    for name in ("pitch", "intensity", "timbre"):
        if name in modify:
            bounded(modify[name], -100, 100, f"效果器 {name}")
    if args.sound_effect == "none":
        modify.pop("sound_effects", None)
    if modify:
        payload["voice_modify"] = modify
    if args.tone:
        if any('/' not in rule or not all(rule.split('/', 1)) for rule in args.tone):
            raise ValueError("发音规则格式为 原文/替换内容。")
        payload["pronunciation_dict"] = {"tone": args.tone}
    if args.normalization:
        if args.normalization == "quality" and args.model not in ("speech-2.8-hd", "speech-2.8-turbo", "speech-2.6-hd", "speech-2.6-turbo"):
            raise ValueError("quality 归一化仅支持 speech-2.8/2.6-hd/turbo。")
        payload["text_normalization_mode"] = args.normalization
    return payload


def api_key() -> str:
    value = os.environ.get("MINIMAX_API_KEY", "").strip()
    if value:
        return value
    if sys.platform == "darwin":
        result = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    raise ValueError("未找到 MiniMax Key；请设置 MINIMAX_API_KEY 或本机 Keychain。")


def synthesize(args: argparse.Namespace) -> dict:
    payload = build_payload(args)
    if args.dry_run:
        return {"dry_run": True, "preset": args.preset, "request": payload}
    if args.output is None:
        raise ValueError("实际生成必须指定 --output。")
    output = args.output.resolve()
    metadata_path = output.with_suffix(".metadata.json")
    if output.exists() or metadata_path.exists():
        raise ValueError("输出已存在；请使用新文件名，避免重复收费和覆盖。")
    output.parent.mkdir(parents=True, exist_ok=True)
    key = api_key()
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            status = response.status
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        # 不输出原始响应或请求头，避免错误页回显凭据。
        raise ValueError(f"MiniMax HTTP {exc.code}；未自动重试，请检查账户与接口。") from None
    except urllib.error.URLError:
        raise ValueError("MiniMax 网络请求失败；未自动重试，请检查网络。") from None
    base = result.get("base_resp") or {}
    if base.get("status_code") != 0:
        message = str(base.get("status_msg", "unknown")).replace(key, "[REDACTED]")
        raise ValueError(f"MiniMax 业务失败 {base.get('status_code')}: {message}")
    data = result.get("data") or {}
    if data.get("status") != 2 or not data.get("audio"):
        raise ValueError("MiniMax 未返回完整音频。")
    try:
        audio = bytes.fromhex(data["audio"])
    except (ValueError, TypeError):
        raise ValueError("MiniMax 音频不是有效的 hex 数据。") from None
    if not audio:
        raise ValueError("MiniMax 返回的音频为空。")
    with output.open("xb") as handle:
        handle.write(audio)
    metadata = {
        "provider": "MiniMax", "endpoint": API_URL, "http_status": status,
        "base_status_code": base["status_code"], "trace_id": result.get("trace_id"),
        "preset": args.preset, "direction": presets()[args.preset]["direction"], "request": payload,
        "extra_info": result.get("extra_info"),
        "output": str(output), "bytes": len(audio),
        "sha256": hashlib.sha256(audio).hexdigest(),
        "subtitle_files_generated": False,
    }
    with metadata_path.open("x", encoding="utf-8") as handle:
        json.dump(metadata, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {
        "output": str(output), "metadata": str(metadata_path),
        "model": args.model, "voice_id": args.voice,
        "extra_info": result.get("extra_info"),
        "subtitle_files_generated": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="要朗读的文本")
    source.add_argument("--text-file", type=Path, help="UTF-8 配音文本文件")
    parser.add_argument("--output", type=Path, help="输出 mp3/wav/flac 路径")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--preset", default="natural", help="场景预设，可被显式参数覆盖")
    parser.add_argument("--list-presets", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="只看请求参数，不读密钥、不调用 API")
    parser.add_argument("--speed", type=float)
    parser.add_argument("--vol", type=float)
    parser.add_argument("--pitch", type=int)
    parser.add_argument("--emotion", choices=("auto", *EMOTIONS))
    parser.add_argument("--modify-pitch", type=int)
    parser.add_argument("--intensity", type=int)
    parser.add_argument("--timbre", type=int)
    parser.add_argument("--sound-effect", choices=("none", *EFFECTS))
    parser.add_argument("--tone", action="append", help="原文/替换内容，可多次传入")
    parser.add_argument("--normalization", choices=("basic", "quality"))
    parser.add_argument("--language-boost", choices=("Chinese", "Chinese,Yue", "English", "auto"), default="Chinese")
    parser.add_argument("--format", choices=("mp3", "wav", "flac"))
    parser.add_argument("--sample-rate", type=int, choices=(8000,16000,22050,24000,32000,44100), default=32000)
    parser.add_argument("--bitrate", type=int, choices=(32000,64000,128000,256000), default=128000)
    parser.add_argument("--channel", type=int, choices=(1,2), default=1)
    args = parser.parse_args()
    try:
        if args.list_presets:
            print(json.dumps(presets(), ensure_ascii=False, indent=2))
            return 0
        if args.text is None and args.text_file is None:
            raise ValueError("请指定 --text 或 --text-file。")
        print(json.dumps(synthesize(args), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        print(f"配音失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
