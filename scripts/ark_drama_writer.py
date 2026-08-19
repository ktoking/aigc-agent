#!/usr/bin/env python3
"""Call Ark Chat Completions for one constrained AI-drama writer stage.

The caller owns orchestration: persist each stage output, review it, then pass
only approved state to the next stage. This prevents a character from gaining
the author's future knowledge through an opaque all-in-one prompt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
STAGES = {"episode_planner", "scene_planner", "roleplay", "dialogue_director", "continuity_checker"}
BASE_PROMPT = """你是 AI 漫剧生产系统的一个受限节点。你只能完成当前节点职责，不能越权补写其他节点的内容。
所有叙事必须服务于短剧的可拍性：具体冲突、清晰利益、可见动作、少解释、结尾留下可回答的具体问题。
输入中的事实是唯一事实源。不得新增未声明的超能力、关系、历史、角色知识或未来结局。
严格只输出一个合法 JSON 对象，不输出 Markdown、注释、推理过程或代码围栏。"""
STAGE_PROMPTS = {
    "episode_planner": "你是故事规划器。禁止写正式台词、镜头脚本或内心独白。输出本集目标、开场事实、冲突、升级、反转、角色认知边界、伏笔、结尾钩子和四段事件摘要。",
    "scene_planner": "你是场景编剧。禁止写正式台词。按场景输出时长、在场人物、初始状态、人物目标、冲突、信息限制、不可改变事实、事件节拍和结束状态。",
    "roleplay": "你只扮演指定角色。只能使用该角色 knowledge.known、场景可见事实和已发生对白；绝不可暗示 knowledge.unknown。输出该角色的候选行动和台词轮次，不替其他角色说话。",
    "dialogue_director": "你是对白导演。不得改写剧情事实、事件顺序、角色知识边界或场景结果。删解释、增潜台词，用动作代替说明；输出最终对白、动作节拍和修改理由。",
    "continuity_checker": "你是连续性审查员，不重写内容。核对角色知识、秘密、关系情绪、道具状态、伏笔、上一集钩子和可拍性。返回 status=pass 或 status=blocked，blocked 必须给字段路径和最小修复。",
}


class DramaWriterError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DramaWriterError(f"cannot read input JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DramaWriterError("input root must be a JSON object")
    for field in ("story_id", "episode_id"):
        if not isinstance(payload.get(field), str) or not payload[field]:
            raise DramaWriterError(f"missing required input field: {field}")
    return payload


def build_request(stage: str, source: dict[str, Any], model: str) -> dict[str, Any]:
    instruction = STAGE_PROMPTS[stage]
    user = {
        "stage": stage,
        "output_envelope": {"stage": stage, "story_id": source["story_id"], "episode_id": source["episode_id"], "result": "<stage result object>"},
        "input": source,
    }
    return {
        "model": model,
        "temperature": 0.35 if stage in {"episode_planner", "scene_planner"} else 0.55,
        "max_tokens": 5000,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": f"{BASE_PROMPT}\n\n{instruction}"},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
    }


def post(payload: dict[str, Any]) -> dict[str, Any]:
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise DramaWriterError("ARK_API_KEY is not set")
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise DramaWriterError(f"Ark request failed HTTP {exc.code}: {body[:500]}") from exc


def content_from(response: dict[str, Any]) -> str:
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise DramaWriterError("Ark response has no choices[0].message.content") from exc
    if not isinstance(content, str):
        raise DramaWriterError("Ark response content is not text")
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one constrained Ark AI-drama writer stage.")
    parser.add_argument("--stage", choices=sorted(STAGES), required=True)
    parser.add_argument("--input", required=True, help="JSON input/state for this stage")
    parser.add_argument("--output", required=True, help="where the parsed stage JSON is saved")
    parser.add_argument("--model", default=os.environ.get("ARK_TEXT_MODEL"), help="Ark text model ID or endpoint ID")
    parser.add_argument("--dry-run", action="store_true", help="write request JSON; do not call Ark")
    args = parser.parse_args()
    try:
        source = read_json(Path(args.input))
        if not args.model:
            raise DramaWriterError("set ARK_TEXT_MODEL or pass --model with an Ark text model ID or endpoint ID")
        request = build_request(args.stage, source, args.model)
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if args.dry_run:
            out_path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"dry_run request={out_path}")
            return 0
        raw = post(request)
        raw_path = out_path.with_suffix(out_path.suffix + ".raw.json")
        raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            result = json.loads(content_from(raw))
        except json.JSONDecodeError as exc:
            raise DramaWriterError(f"model did not return valid JSON; raw response saved at {raw_path}") from exc
        if not isinstance(result, dict) or result.get("stage") != args.stage:
            raise DramaWriterError(f"invalid output envelope; expected stage={args.stage}; raw response saved at {raw_path}")
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"success stage={args.stage} output={out_path} raw={raw_path}")
        return 0
    except DramaWriterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
