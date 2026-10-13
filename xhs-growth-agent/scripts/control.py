#!/usr/bin/env python3
"""Local lifecycle and API commands; never shells out with user-controlled text."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
RUN = RUNTIME / "run"
LOGS = RUNTIME / "logs"
PYTHON = ROOT / ".venv" / "bin" / "python"
PORTS = {"mcp": 18060, "backend": 18760, "frontend": 18761}
API = "http://127.0.0.1:18760/api"
SERVICES = ("mcp", "backend", "frontend")


class ControlError(RuntimeError):
    pass


def private_dirs() -> None:
    for directory in (RUNTIME, RUN, LOGS, RUNTIME / "mcp"):
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)


def configuration(validate: bool = True) -> dict[str, str]:
    """Read only this project's .env, without evaluating shell substitutions."""
    values = dict(os.environ)
    path = ROOT / ".env"
    if path.exists():
        for original in path.read_text().splitlines():
            line = original.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key.startswith("export "):
                key = key[7:].strip()
            if not key or not key.replace("_", "a").isalnum():
                continue
            if value[:1] in ("'", '"') and value[-1:] == value[:1]:
                value = value[1:-1]
            values.setdefault(key, value)
    values["COOKIES_PATH"] = str(RUNTIME / "mcp" / "cookies.json")
    # Ignore a global uv environment override; this project owns only its .venv.
    values["UV_PROJECT_ENVIRONMENT"] = str(ROOT / ".venv")
    values.setdefault("XHS_MCP_URL", "http://127.0.0.1:18060/mcp")
    if validate:
        validate_loopback(values["XHS_MCP_URL"])
    return values


def validate_loopback(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or parsed.hostname not in ("127.0.0.1", "localhost", "::1"):
        raise ControlError("XHS_MCP_URL 必须使用本机 loopback 地址。")
    if parsed.username or parsed.password:
        raise ControlError("XHS_MCP_URL 不允许包含凭证。")


def emit(value) -> None:
    """Do not expose credentials even when an error response echoes configuration."""
    secret_names = ("key", "token", "cookie", "secret", "password", "authorization")
    secrets = [v for k, v in configuration(validate=False).items() if len(v) >= 8 and any(word in k.lower() for word in secret_names)]

    def clean(item):
        if isinstance(item, dict):
            return {k: ("[REDACTED]" if any(word in k.lower() for word in secret_names) else clean(v)) for k, v in item.items()}
        if isinstance(item, list):
            return [clean(v) for v in item]
        if isinstance(item, str):
            for secret in secrets:
                item = item.replace(secret, "[REDACTED]")
        return item

    print(json.dumps(clean(value), ensure_ascii=False, indent=2))


def run(command: list[str], cwd: Path = ROOT) -> None:
    completed = subprocess.run(command, cwd=cwd, env=configuration())
    if completed.returncode:
        raise ControlError(f"命令执行失败（退出码 {completed.returncode}）：{Path(command[0]).name}")


def command(service: str) -> list[str]:
    if service == "backend":
        if not PYTHON.exists():
            raise ControlError("后端虚拟环境缺失，请先执行 make setup。")
        return [str(PYTHON), "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", str(PORTS[service])]
    if service == "frontend":
        npm = shutil.which("npm")
        if not npm or not (ROOT / "frontend" / "node_modules").exists():
            raise ControlError("前端依赖缺失，请先执行 make setup。")
        return [npm, "run", "dev", "--", "--host", "127.0.0.1", "--port", str(PORTS[service]), "--strictPort"]
    binary = RUNTIME / "bin" / "xiaohongshu-mcp"
    if not binary.is_file():
        raise ControlError("MCP 二进制缺失：.runtime/bin/xiaohongshu-mcp；请使用已审查的普通 Chrome 适配构建。")
    if not valid_mcp_build():
        raise ControlError("MCP 构建证明与二进制不一致；请先执行 make setup-mcp，禁止启动原始指纹浏览器 Release。")
    return [str(binary), "-port", "127.0.0.1:18060"]


def valid_mcp_build() -> bool:
    try:
        manifest = json.loads((RUNTIME / "bin" / "mcp-build.json").read_text())
        binary_hash = hashlib.sha256((RUNTIME / "bin" / "xiaohongshu-mcp").read_bytes()).hexdigest()
        patch_hash = hashlib.sha256((ROOT / "docs" / "mcp-standard-browser.patch").read_bytes()).hexdigest()
        return (manifest.get("browser") == "standard Chrome"
                and manifest.get("official_repository") == "https://github.com/xpzouying/xiaohongshu-mcp"
                and manifest.get("tag") == "v2.5.5"
                and manifest.get("commit") == "a5c8f7799980ba1fdd501999843eb2d17e4c9a9f"
                and manifest.get("binary_sha256") == binary_hash
                and manifest.get("patch_sha256") == patch_hash)
    except (OSError, ValueError):
        return False


def cwd_for(service: str) -> Path:
    return ROOT / "frontend" if service == "frontend" else (RUNTIME / "mcp" if service == "mcp" else ROOT)


def port_open(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def start_signature(pid: int) -> str | None:
    completed = subprocess.run(["ps", "-p", str(pid), "-o", "lstart="], capture_output=True, text=True)
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and value else None


def command_signature(pid: int) -> str | None:
    completed = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True)
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and value else None


def state_path(service: str) -> Path:
    return RUN / f"{service}.json"


def read_state(service: str) -> dict | None:
    try:
        value = json.loads(state_path(service).read_text())
        if value.get("root") == str(ROOT) and value.get("service") == service:
            return value
    except (OSError, ValueError):
        pass
    return None


def owned_process(service: str) -> dict | None:
    state = read_state(service)
    if not state:
        return None
    pid = state.get("pid")
    if (isinstance(pid, int) and pid > 1
            and state.get("start_signature") == start_signature(pid)
            and (not state.get("command_signature") or state["command_signature"] == command_signature(pid))):
        return state
    return None


def write_state(service: str, state: dict) -> None:
    private_dirs()
    path = state_path(service)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False))
    temporary.chmod(0o600)
    temporary.replace(path)


def start_service(service: str) -> None:
    private_dirs()
    if owned_process(service):
        emit({"service": service, "status": "already_running", "port": PORTS[service]})
        return
    if port_open(PORTS[service]):
        raise ControlError(f"端口 {PORTS[service]} 已被其他进程占用；未启动或终止任何占用者。")
    state_path(service).unlink(missing_ok=True)
    log_path = LOGS / f"{service}.log"
    with log_path.open("ab") as log:
        log_path.chmod(0o600)
        process = subprocess.Popen(command(service), cwd=cwd_for(service), env=configuration(), stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
    signature = start_signature(process.pid)
    if not signature:
        raise ControlError(f"{service} 启动后立即退出，请本地查看 .runtime/logs/{service}.log。")
    write_state(service, {"root": str(ROOT), "service": service, "pid": process.pid, "start_signature": signature, "launcher": "manual"})
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if port_open(PORTS[service]):
            state = read_state(service)
            state["command_signature"] = command_signature(process.pid)
            write_state(service, state)
            emit({"service": service, "status": "running", "port": PORTS[service], "log": str(log_path)})
            return
        if process.poll() is not None:
            state_path(service).unlink(missing_ok=True)
            raise ControlError(f"{service} 启动失败，请本地查看 .runtime/logs/{service}.log。")
        time.sleep(0.2)
    stop_service(service)
    raise ControlError(f"{service} 未在 30 秒内监听端口，已停止本次启动进程。")


def stop_service(service: str) -> None:
    state = owned_process(service)
    if not state:
        state_path(service).unlink(missing_ok=True)
        emit({"service": service, "status": "not_owned_or_not_running"})
        return
    if state.get("launcher") == "launchd":
        result = subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{launchd_label(service)}"], capture_output=True)
        if result.returncode:
            raise ControlError(f"{service} launchd 卸载失败；保持进程记录，请检查 launchctl。")
    else:
        pid = state["pid"]
        try:
            # Manual starts own an isolated process group. PID signature protects reuse.
            if os.getpgid(pid) != pid:
                raise ControlError(f"{service} 的进程组不属于本项目；拒绝终止。")
            os.killpg(pid, signal.SIGTERM)
            deadline = time.monotonic() + 6
            while time.monotonic() < deadline and owned_process(service):
                time.sleep(0.1)
            if owned_process(service):
                os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    state_path(service).unlink(missing_ok=True)
    emit({"service": service, "status": "stopped"})


def setup() -> None:
    private_dirs()
    uv = shutil.which("uv")
    npm = shutil.which("npm")
    if not uv or not npm:
        raise ControlError("需要 uv 和 Node.js/npm；安装后重新执行 make setup。")
    if not PYTHON.exists():
        run([uv, "venv", "--python", "3.12", str(ROOT / ".venv")])
    run([str(PYTHON), "-c", "import sys; assert sys.version_info >= (3, 12), 'Python 3.12+ required'"])
    run([uv, "sync", "--python", "3.12"])
    npm_command = "ci" if (ROOT / "frontend" / "package-lock.json").exists() else "install"
    run([npm, npm_command], ROOT / "frontend")
    if not (ROOT / ".env").exists():
        shutil.copyfile(ROOT / ".env.example", ROOT / ".env")
        (ROOT / ".env").chmod(0o600)
    if not valid_mcp_build():
        run([str(PYTHON), str(ROOT / "scripts" / "setup_mcp.py")])
    emit({"setup": "ready", "backend": "http://127.0.0.1:18760", "frontend": "http://127.0.0.1:18761", "mcp_binary": (RUNTIME / "bin" / "xiaohongshu-mcp").exists(), "model": "本机 Codex CLI：gpt-6.1-sol / high；使用已有 Codex 登录，不接外部模型 API"})


def api(method: str, path: str, body: dict | None = None):
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    request = urllib.request.Request(API + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        # Local operator requests must never pass through a global HTTP proxy.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        # One HTTP attempt only. A platform write can legitimately take minutes;
        # longer waiting never implies retrying an unknown submission.
        timeout = max(900, int(configuration().get("XHS_CLI_HTTP_TIMEOUT_SECONDS", "1800")))
        with opener.open(request, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read()).get("detail", "API 请求失败")
        except ValueError:
            detail = "API 请求失败"
        # Redaction is handled by the sole error printer in main.
        raise ControlError(f"HTTP {error.code}: {detail}") from None
    except urllib.error.URLError:
        raise ControlError("无法连接本机后端；请先运行 make dev 或 make doctor。") from None


def doctor() -> None:
    results = {"python_venv": PYTHON.exists(), "uv": bool(shutil.which("uv")), "node": bool(shutil.which("node")), "npm": bool(shutil.which("npm")), "mcp_binary": (RUNTIME / "bin" / "xiaohongshu-mcp").is_file(), "mcp_standard_chrome_build": valid_mcp_build(), "ports": {service: {"listening": port_open(port), "owned": bool(owned_process(service))} for service, port in PORTS.items()}}
    if port_open(PORTS["backend"]):
        try:
            dashboard = api("GET", "/dashboard")
            mcp = api("GET", "/mcp/status")
            results["model"] = dashboard.get("model", {})
            results["mcp"] = {"connected": mcp.get("connected", False), "logged_in": mcp.get("logged_in", False)}
            settings = api("GET", "/settings")
            results["approval_to_queue"] = settings.get("approval_to_queue", False)
            results["publishing"] = "BLOCKED：等待账号登录" if not mcp.get("logged_in") else ("审批即进入已绑定账号的发布队列" if settings.get("approval_to_queue") else "登录已就绪，审批入队策略尚未启用")
            results["model_note"] = "Codex CLI 未找到，真实模型调用阻塞" if not dashboard.get("model", {}).get("configured") else "Codex CLI 可执行；登录与模型权限以实际调用为准"
        except ControlError as error:
            results["backend_check"] = str(error)
    results["chrome"] = Path(configuration().get("XHS_CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")).is_file()
    emit(results)


def test() -> None:
    if not PYTHON.exists():
        raise ControlError("请先执行 make setup。")
    run([str(PYTHON), "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py", "-v"])
    run([str(PYTHON), "-m", "pytest", "tests", "-q"])
    run([shutil.which("npm") or "npm", "run", "build"], ROOT / "frontend")
    emit({"local_checks": "passed", "real_model": "未通过此命令验证", "real_publish": "未执行", "live_mcp": "运行 make doctor 查看外部状态"})


def launchd_label(service: str) -> str:
    suffix = hashlib.sha256(str(ROOT).encode()).hexdigest()[:10]
    return f"local.xhs-growth-agent.{suffix}.{service}"


def install_services() -> None:
    """Optional persistent local agents; never modifies global MCP configuration."""
    import plistlib
    if sys.platform != "darwin":
        raise ControlError("launchd 仅支持 macOS。")
    private_dirs()
    for service in SERVICES:
        command(service)
        if port_open(PORTS[service]) or owned_process(service):
            raise ControlError(f"{service} 当前正在运行；请先停止本项目服务，再安装 launchd。")
    directory = Path.home() / "Library" / "LaunchAgents"
    directory.mkdir(parents=True, exist_ok=True)
    installed = []
    try:
        for service in SERVICES:
            label = launchd_label(service)
            path = directory / f"{label}.plist"
            if path.exists():
                raise ControlError(f"{service} launchd 配置已存在；请先 make uninstall-service。")
            plist = {"Label": label, "ProgramArguments": [str(PYTHON), str(Path(__file__).resolve()), "run-service", service], "WorkingDirectory": str(ROOT), "RunAtLoad": True, "KeepAlive": {"SuccessfulExit": False}, "ThrottleInterval": 10, "Umask": 0o077, "StandardOutPath": str(LOGS / f"{service}.log"), "StandardErrorPath": str(LOGS / f"{service}.log"), "EnvironmentVariables": {"PATH": os.environ.get("PATH", "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin")}}
            path.write_bytes(plistlib.dumps(plist))
            path.chmod(0o600)
            installed.append(path)
            run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(path)])
    except (ControlError, OSError):
        for path in installed:
            subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(path)], capture_output=True)
            path.unlink(missing_ok=True)
        raise
    emit({"launchd": "installed", "scope": "当前 macOS 用户；登录后运行，退出 Codex 不影响后台"})


def uninstall_services() -> None:
    if sys.platform != "darwin":
        raise ControlError("launchd 仅支持 macOS。")
    for service in reversed(SERVICES):
        path = Path.home() / "Library" / "LaunchAgents" / f"{launchd_label(service)}.plist"
        if path.exists():
            import plistlib
            plist = plistlib.loads(path.read_bytes())
            if plist.get("ProgramArguments") != [str(PYTHON), str(Path(__file__).resolve()), "run-service", service]:
                raise ControlError(f"{service} launchd 配置与本项目不匹配；拒绝删除。")
            subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}/{launchd_label(service)}"], capture_output=True)
            path.unlink(missing_ok=True)
        state = read_state(service)
        if state and state.get("launcher") == "launchd":
            state_path(service).unlink(missing_ok=True)
    emit({"launchd": "uninstalled"})


def run_service(service: str) -> None:
    private_dirs()
    if port_open(PORTS[service]):
        raise ControlError(f"端口 {PORTS[service]} 已占用；launchd 服务拒绝接管。")
    arguments = command(service)
    pid = os.getpid()
    write_state(service, {"root": str(ROOT), "service": service, "pid": pid, "start_signature": start_signature(pid), "launcher": "launchd"})
    os.chdir(cwd_for(service))
    # exec changes the command string while preserving PID/start time. Launchd
    # stop uses the registered job label rather than a Unix process-group signal.
    os.execvpe(arguments[0], arguments, configuration())


def cli(arguments) -> None:
    if arguments.command == "research":
        emit(api("POST", "/research", {"mode": arguments.mode, "count": arguments.count, "keywords": arguments.keywords or []}))
    elif arguments.command == "plan":
        emit(api("POST", "/plan", {"limit": arguments.count, "mode": arguments.mode}))
    elif arguments.command == "generate":
        emit(api("POST", "/generate", {"mode": arguments.mode, "count": arguments.count}))
    elif arguments.command == "demo":
        emit(api("POST", "/demo", {}))
    elif arguments.command == "review":
        if not arguments.ids and not arguments.all:
            emit({"pending": [{"id": item["id"], "title": item["title"], "version": item.get("version"), "quality": item.get("quality")} for item in api("GET", "/articles") if item.get("status") in ("PENDING_REVIEW", "DRAFT", "QUALITY_PASSED")]})
            return
        ids = arguments.ids or [item["id"] for item in api("GET", "/articles") if item.get("status") == "PENDING_REVIEW"]
        emit([api("POST", f"/articles/{urllib.parse.quote(str(identifier), safe='')}/review", {"decision": arguments.decision, "reviewer": arguments.reviewer}) for identifier in ids])
    elif arguments.command == "publish-approved":
        if arguments.mode == "live":
            payload = {"article_ids": arguments.ids} if arguments.ids else {}
            emit({"mode": "live", "queue": api("POST", "/publishing/enqueue-approved", payload), "note": "只提交一次入队请求；已启用审批入队策略时，后台按实际账号/版本/图片哈希检查并串行执行，无需输入逐篇确认字符串。"})
            return
        articles = [item for item in api("GET", "/articles") if item.get("status") == "APPROVED"]
        ids = arguments.ids or [item["id"] for item in articles]
        results = []
        for identifier in ids:
            try:
                job = api("POST", f"/articles/{urllib.parse.quote(str(identifier), safe='')}/publish", {"mode": arguments.mode})
                results.append({"article_id": identifier, "job": job})
            except ControlError as error:
                results.append({"article_id": identifier, "blocked": str(error)})
        emit({"mode": arguments.mode, "results": results, "note": "Mock 不触发真实平台发布；live 通过已启用的审批入队策略执行。"})
    elif arguments.command == "report":
        emit(api("GET", "/report"))


def main() -> int:
    parser = argparse.ArgumentParser(description="小红书内容运营系统本机控制；内容模型使用 Codex CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("setup", "doctor", "status", "test", "install-service", "uninstall-service", "demo", "report"):
        sub.add_parser(name)
    for name in ("start", "stop"):
        child = sub.add_parser(name)
        child.add_argument("--services", nargs="+", choices=SERVICES, default=list(SERVICES))
    child = sub.add_parser("run-service")
    child.add_argument("service", choices=SERVICES)
    for name, count in (("research", 100), ("generate", 3)):
        child = sub.add_parser(name)
        child.add_argument("--mode", choices=("mock", "live"), default="live")
        child.add_argument("--count", type=int, default=count)
        if name == "research":
            child.add_argument("--keywords", nargs="*")
    child = sub.add_parser("plan")
    child.add_argument("--count", type=int, default=50)
    child.add_argument("--mode", choices=("mock", "live"), default="live")
    child = sub.add_parser("review")
    child.add_argument("--ids", nargs="+")
    child.add_argument("--all", action="store_true")
    child.add_argument("--decision", choices=("approve", "reject"), default="approve")
    child.add_argument("--reviewer", default="local-operator")
    child = sub.add_parser("publish-approved")
    child.add_argument("--ids", nargs="+")
    child.add_argument("--mode", choices=("mock", "live"), default="mock")
    arguments = parser.parse_args()
    try:
        if arguments.command == "setup":
            setup()
        elif arguments.command == "start":
            for service in arguments.services:
                start_service(service)
        elif arguments.command == "stop":
            for service in reversed(arguments.services):
                stop_service(service)
        elif arguments.command in ("doctor", "status"):
            doctor()
        elif arguments.command == "test":
            test()
        elif arguments.command == "install-service":
            install_services()
        elif arguments.command == "uninstall-service":
            uninstall_services()
        elif arguments.command == "run-service":
            run_service(arguments.service)
        else:
            cli(arguments)
        return 0
    except (ControlError, OSError, ValueError) as error:
        emit({"status": "BLOCKED", "detail": str(error)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
