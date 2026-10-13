#!/usr/bin/env python3
"""Build the pinned official source with the standard Chrome patch. No release binary."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
TAG = "v2.5.5"
COMMIT = "a5c8f7799980ba1fdd501999843eb2d17e4c9a9f"
REMOTE = "https://github.com/xpzouying/xiaohongshu-mcp"
PATCH = ROOT / "docs" / "mcp-standard-browser.patch"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(arguments: list[str], cwd: Path, capture: bool = False):
    completed = subprocess.run(arguments, cwd=cwd, text=True, capture_output=capture)
    if completed.returncode:
        raise RuntimeError(f"{Path(arguments[0]).name} 退出码 {completed.returncode}；未安装未经适配的官方 Release 二进制。")
    return completed.stdout.strip() if capture else None


def build() -> None:
    if sys.platform != "darwin" or platform.machine() != "arm64":
        raise RuntimeError("当前 MCP 适配构建仅验收 macOS arm64。")
    git, go = shutil.which("git"), shutil.which("go")
    if not git or not go:
        raise RuntimeError("需要 Git 与 Go 1.24+；不自动安装系统工具。")
    if not PATCH.is_file():
        raise RuntimeError("普通 Chrome 补丁缺失；拒绝构建原始指纹浏览器版本。")
    RUNTIME.mkdir(parents=True, exist_ok=True)
    RUNTIME.chmod(0o700)
    binary_dir = RUNTIME / "bin"
    binary_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mcp-build-", dir=RUNTIME) as directory:
        source = Path(directory) / "source"
        call([git, "-c", "core.hooksPath=/dev/null", "clone", "--depth", "1", "--branch", TAG, REMOTE, str(source)], RUNTIME)
        actual_commit = call([git, "rev-parse", "HEAD"], source, capture=True)
        if actual_commit != COMMIT:
            raise RuntimeError("官方 tag 与已审查 commit 不匹配；拒绝继续构建。")
        call([git, "apply", "--check", str(PATCH)], source)
        call([git, "apply", str(PATCH)], source)
        # Verify that the patch can be cleanly reversed before compiling.
        call([git, "apply", "--reverse", "--check", str(PATCH)], source)
        binary = Path(directory) / "xiaohongshu-mcp"
        call([go, "build", "-trimpath", "-ldflags", f"-X main.version={TAG}-standard-chrome", "-o", str(binary), "."], source)
        binary.chmod(0o700)
        manifest = {"official_repository": REMOTE, "tag": TAG, "commit": COMMIT, "patch_sha256": sha256(PATCH), "binary_sha256": sha256(binary), "browser": "standard Chrome", "platform": "darwin-arm64"}
        # Atomic replacement does not restart an already running daemon.
        os.replace(binary, binary_dir / "xiaohongshu-mcp")
        manifest_path = binary_dir / "mcp-build.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
        manifest_path.chmod(0o600)
    print(json.dumps({"mcp_build": "ready", "tag": TAG, "commit": COMMIT, "browser": "standard Chrome", "binary": str(binary_dir / "xiaohongshu-mcp"), "note": "不自动启动；未下载原始 Release，不配置代理、指纹或全局 MCP。"}, ensure_ascii=False, indent=2))


def check() -> None:
    binary = RUNTIME / "bin" / "xiaohongshu-mcp"
    manifest_path = RUNTIME / "bin" / "mcp-build.json"
    if not binary.is_file() or not manifest_path.is_file():
        raise RuntimeError("二进制或构建证明缺失；运行 make setup-mcp 进行可复现源码构建。")
    manifest = json.loads(manifest_path.read_text())
    expected = {"official_repository": REMOTE, "tag": TAG, "commit": COMMIT, "patch_sha256": sha256(PATCH), "binary_sha256": sha256(binary), "browser": "standard Chrome", "platform": "darwin-arm64"}
    if any(manifest.get(key) != value for key, value in expected.items()):
        raise RuntimeError("MCP 二进制、补丁或版本与构建证明不一致；运行 make setup-mcp 重建。")
    print(json.dumps({"mcp_build_check": "passed", "tag": TAG, "browser": "standard Chrome"}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="固定官方源码 + 普通 Chrome 补丁的 MCP 构建")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    try:
        check() if arguments.check else build()
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "BLOCKED", "detail": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
