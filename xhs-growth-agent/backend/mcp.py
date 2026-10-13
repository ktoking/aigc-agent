"""HTTP Streamable MCP。只读最多重试一次；发布绝不重试。"""
import asyncio
import base64
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit
import httpx
from .config import DATA_DIR

READ_TOOLS = {"check_login_status", "get_login_qrcode", "search_feeds", "list_feeds", "get_feed_detail", "user_profile", "get_my_profile"}
ALLOWED_TOOLS = READ_TOOLS | {"publish_content"}

class McpError(RuntimeError):
    pass

def safe_data(value):
    if isinstance(value, dict):
        return {k: safe_data(v) for k, v in value.items() if not any(word in k.lower() for word in ("cookie", "token", "password", "secret", "api_key", "authorization"))}
    if isinstance(value, list):
        return [safe_data(v) for v in value]
    if isinstance(value, str):
        return re.sub(r"(Bearer\s+|sk-)[A-Za-z0-9_\-]+", "[redacted]", value)[:12000]
    return value

def result_text(result):
    return "\n".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")

def result_data(result):
    if isinstance(result.get("structuredContent"), dict):
        return result["structuredContent"]
    value = result_text(result)
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {"items": parsed}
    except (ValueError, TypeError):
        return {"text": value}

class XiaohongshuMcpAdapter:
    def __init__(self, url, client=None):
        self.url = url
        local = urlsplit(url).hostname in {"localhost", "127.0.0.1", "::1"}
        # Native profile reads have a 60s browser deadline. Let them finish before
        # closing the HTTP stream; a shorter client deadline spawned overlapping reads.
        self.client = client or httpx.AsyncClient(timeout=httpx.Timeout(75, connect=4), trust_env=not local)
        self.session_id = None
        self.initialized = False
        self.tools = {}
        self.counter = 0
        self._lock = asyncio.Lock()

    async def close(self):
        await self.client.aclose()

    async def _rpc(self, method, params=None, notification=False):
        self.counter += 1
        request = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notification:
            request["id"] = self.counter
        headers = {"Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2024-11-05"}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        # MCP event-stream may intentionally stay open after the JSON-RPC result.
        # Return on the matching result and close the HTTP stream instead of waiting for EOF.
        # Upstream fills the creator form through a real browser; a 500-character
        # post took over two minutes in the first live test. This is one attempt,
        # never a retry. Read-only calls retain their shorter deadline.
        timeout = httpx.Timeout(min(900, max(60, int(os.getenv("XHS_PUBLISH_TIMEOUT_SECONDS", "600")))), connect=4) if method == "tools/call" and (params or {}).get("name") == "publish_content" else self.client.timeout
        async with self.client.stream("POST", self.url, json=request, headers=headers, timeout=timeout) as response:
            response.raise_for_status()
            self.session_id = response.headers.get("Mcp-Session-Id", self.session_id)
            if notification:
                return {}
            if "text/event-stream" in response.headers.get("content-type", ""):
                payload = {}
                async for line in response.aiter_lines():
                    if not line.startswith("data:") or not line[5:].strip():
                        continue
                    message = json.loads(line[5:].strip())
                    if message.get("id") == request["id"]:
                        payload = message
                        break
            else:
                body = await response.aread()
                payload = json.loads(body) if body else {}
        if payload.get("error"):
            raise McpError(f"MCP {method} 返回协议错误 {payload['error'].get('code', '')}")
        if "result" not in payload:
            raise McpError("MCP 响应没有可解析的 result")
        return payload["result"]

    async def discover(self):
        async with self._lock:
            if not self.initialized:
                await self._rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "xhs-growth-agent", "version": "0.1.0"}})
                await self._rpc("notifications/initialized", notification=True)
                self.initialized = True
            result = await self._rpc("tools/list")
            self.tools = {tool["name"]: tool for tool in result.get("tools", [])}
            return list(self.tools.values())

    async def call(self, name, arguments=None):
        if name not in ALLOWED_TOOLS:
            raise McpError(f"禁止调用工具 {name}")
        if not self.tools:
            await self.discover()
        if name not in self.tools:
            raise McpError(f"当前 MCP 未暴露工具 {name}")
        schema = self.tools[name].get("inputSchema", {})
        supplied = arguments or {}
        missing = [key for key in schema.get("required", []) if key not in supplied]
        if missing:
            raise McpError("工具必填参数缺失：" + ", ".join(missing))
        properties = schema.get("properties", {})
        if properties and any(key not in properties for key in supplied):
            raise McpError("传入了当前工具 schema 未声明的参数")
        retries = 1 if name in READ_TOOLS else 0
        for attempt in range(retries + 1):
            try:
                result = await self._rpc("tools/call", {"name": name, "arguments": supplied})
                if result.get("isError"):
                    raise McpError("MCP 工具执行失败：" + result_text(result)[:500])
                return result
            except (httpx.TimeoutException, httpx.NetworkError):
                if attempt == retries:
                    raise
                await asyncio.sleep(0.2)

    async def health(self):
        try:
            tools = await self.discover()
        except Exception as error:
            return {"connected": False, "logged_in": False, "detail": f"MCP 不可用：{type(error).__name__}", "tools": []}
        try:
            result = await self.call("check_login_status")
            content = result_data(result)
            raw = result_text(result)
            login = content.get("is_logged_in", content.get("logged_in"))
            if not isinstance(login, bool):
                login = "已登录" in raw and "未登录" not in raw and "未登陆" not in raw
            return {"connected": True, "logged_in": login, "detail": "账号已登录" if login else "等待人工扫码登录", "tools": [t["name"] for t in tools]}
        except Exception as error:
            return {"connected": True, "logged_in": False, "detail": f"MCP 已连接；登录状态读取失败：{type(error).__name__}", "tools": [t["name"] for t in tools]}

    async def qrcode(self):
        result = await self.call("get_login_qrcode")
        for item in result.get("content", []):
            if item.get("type") == "image":
                suffix = ".png" if item.get("mimeType") == "image/png" else ".jpg"
                folder = DATA_DIR / "media"
                folder.mkdir(parents=True, exist_ok=True)
                path = folder / ("login-qrcode" + suffix)
                path.write_bytes(base64.b64decode(item["data"]))
                return {"image_url": "/media/" + path.name, "detail": "请使用小红书 App 人工扫码，二维码可能有时效。"}
        data = result_data(result)
        # Some server versions return a data URL inside text JSON.
        candidate = data.get("img", data.get("image", data.get("qrcode", "")))
        if isinstance(candidate, str) and candidate.startswith("data:image/"):
            folder = DATA_DIR / "media"
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / "login-qrcode.png"
            path.write_bytes(base64.b64decode(candidate.split(",", 1)[1]))
            return {"image_url": "/media/login-qrcode.png", "detail": "请人工扫码登录。"}
        return {"image_url": None, "detail": result_text(result)[:300] or "当前 MCP 未提供二维码图像。"}

    async def publish(self, title, body, images, tags, visibility):
        await self.discover()
        schema = self.tools.get("publish_content", {}).get("inputSchema", {}).get("properties", {})
        payload = {"title": title, "content": body, "images": images, "tags": tags}
        if "visibility" in schema:
            payload["visibility"] = visibility
        elif visibility != "公开可见":
            raise McpError("当前 MCP 版本未提供 visibility；无法满足指定可见性")
        if "is_original" in schema:
            payload["is_original"] = True
        return await self.call("publish_content", payload)

    async def search(self, keyword):
        return result_data(await self.call("search_feeds", {"keyword": keyword}))

    async def feed_detail(self, feed_id, xsec_token):
        return result_data(await self.call("get_feed_detail", {"feed_id": feed_id, "xsec_token": xsec_token}))

    async def user_profile(self, user_id, xsec_token):
        return result_data(await self.call("user_profile", {"user_id": user_id, "xsec_token": xsec_token}))
