#!/usr/bin/env python3
"""Generate trusted Ark/Seedream image assets for video references."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seedream-5-0-lite-260128"


class ArkImageError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def require_api_key() -> str:
    key = os.environ.get("ARK_API_KEY")
    if not key:
        raise ArkImageError("ARK_API_KEY is not set")
    return key


def request_json(path: str, api_key: str, payload: dict[str, Any], timeout: int = 180) -> tuple[int, dict[str, Any]]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return exc.code, parsed


def download(url: str, out_path: Path, timeout: int = 240) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        out_path.write_bytes(resp.read())


def read_text(path: Path | None) -> str:
    if not path:
        return ""
    if not path.exists():
        raise ArkImageError(f"prompt file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def extract_url(data: dict[str, Any]) -> str | None:
    items = data.get("data")
    if isinstance(items, list) and items:
        first = items[0]
        if isinstance(first, dict):
            return first.get("url")
    if isinstance(data.get("data"), dict):
        return data.get("url") or data["data"].get("url")
    return data.get("url")


def build_prompt(args: argparse.Namespace) -> str:
    aspect_note = args.aspect_note.strip()
    parts = [
        read_text(Path(args.prompt_file).resolve()) if args.prompt_file else "",
        args.prompt_text or "",
        read_text(Path(args.context_file).resolve()) if args.context_file else "",
        f"""

信任资产生成要求：画面中的所有人物都是 AI 生成的虚构短剧角色，不对应、不冒充、不还原任何真实人物；
不要生成名人、公众人物、真人照片、证件照、监控画面或任何个人隐私信息。保持原创虚拟人物、影视剧照质感、
{aspect_note}、可作为后续 Seedance 2.0 视频参考图的可信图像资产。
""",
    ]
    prompt = "\n\n".join(part.strip() for part in parts if part.strip())
    if not prompt:
        raise ArkImageError("prompt is empty")
    return prompt


def generate(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(args)
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": prompt,
        "size": args.size,
        "response_format": "url",
    }
    if args.seed is not None:
        payload["seed"] = args.seed

    if args.dry_run:
        redacted = dict(payload)
        redacted["prompt"] = prompt
        print(json.dumps(redacted, ensure_ascii=False, indent=2))
        return 0

    status_code, data = request_json("/images/generations", require_api_key(), payload)
    (output_dir / f"{args.name}-submit.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if status_code >= 300:
        print(f"image_failed name={args.name} http={status_code} output={output_dir / f'{args.name}-submit.json'}")
        return 1

    image_url = extract_url(data)
    if not image_url:
        print(f"image_failed name={args.name} no_url output={output_dir / f'{args.name}-submit.json'}")
        return 1

    preview_path = output_dir / f"{args.name}.png"
    download(image_url, preview_path)
    manifest_path = output_dir / "trusted-assets.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {"generated_at": now_iso(), "assets": {}}
    manifest["updated_at"] = now_iso()
    manifest["assets"][args.name] = {
        "model": args.model,
        "size": args.size,
        "url": image_url,
        "preview": str(preview_path),
        "created_at": now_iso(),
        "trust_note": "Seedream 5.0 lite text-to-image output; use URL directly for Seedance within platform trust window.",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.quiet:
        print(f"success name={args.name} preview={preview_path} manifest={manifest_path}")
    else:
        print(json.dumps(manifest["assets"][args.name], ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Ark Seedream trusted image assets.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default="1440x2560")
    parser.add_argument("--aspect-note", default="9:16 竖屏构图")
    parser.add_argument("--prompt-file")
    parser.add_argument("--prompt-text")
    parser.add_argument("--context-file")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return generate(args)
    except ArkImageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
