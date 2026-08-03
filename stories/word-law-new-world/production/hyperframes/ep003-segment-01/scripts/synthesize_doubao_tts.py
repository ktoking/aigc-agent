#!/usr/bin/env python3
"""Synthesize one Segment 01 voice line with Doubao TTS 2.0.

The API key is read only from macOS Keychain. It is never written to the repo.
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import uuid
from pathlib import Path
from urllib.request import Request, urlopen

ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
TTS_RESOURCE_ID = "seed-tts-2.0"
KEYCHAIN_SERVICE = "codex-volcengine-tts-api-key"
KEYCHAIN_ACCOUNT = "aigc-agent"


def api_key() -> str:
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT, "-w"],
        text=True,
    ).strip()


def decode_chunks(payload: str) -> bytes:
    decoder = json.JSONDecoder()
    index = 0
    audio = bytearray()
    while index < len(payload):
        while index < len(payload) and payload[index].isspace():
            index += 1
        if index >= len(payload):
            break
        chunk, index = decoder.raw_decode(payload, index)
        code = chunk.get("code")
        if code not in (0, 20000000, None):
            raise RuntimeError(f"Doubao TTS failed: code={code}, message={chunk.get('message', '')}")
        encoded = chunk.get("data")
        if encoded:
            audio.extend(base64.b64decode(encoded))
    if not audio:
        raise RuntimeError("Doubao TTS returned no audio bytes")
    return bytes(audio)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--speech-rate", type=int, default=0, help="Doubao speech-rate adjustment")
    args = parser.parse_args()

    # These selected ICL_uranus_*_tob catalogue voices are entitled through
    # the TTS 2.0 resource for this account; use the server-validated route.
    resource_id = TTS_RESOURCE_ID
    req_params = {
        "text": args.text,
        "speaker": args.speaker,
        "audio_params": {"format": "mp3", "sample_rate": 24000, "speech_rate": args.speech_rate},
        "context_texts": [args.context],
    }
    if args.speaker.startswith("ICL_"):
        req_params["model"] = "seed-tts-2.0-standard"
    body = {
        "user": {"uid": "aigc-agent"},
        "req_params": req_params,
    }
    request = Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "X-Api-Key": api_key(),
            "X-Api-Resource-Id": resource_id,
            "X-Api-Request-Id": str(uuid.uuid4()),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=45) as response:
        audio = decode_chunks(response.read().decode("utf-8"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(audio)
    print(f"wrote {output.name}: {len(audio)} bytes")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
