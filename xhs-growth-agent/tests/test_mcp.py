import json
import httpx
import pytest
from backend.mcp import XiaohongshuMcpAdapter, McpError, safe_data

def tool(name, required=None, properties=None):
    return {"name": name, "inputSchema": {"type": "object", "required": required or [], "properties": properties or {}}}

@pytest.mark.asyncio
async def test_real_protocol_discovery_login_search_and_allowlist():
    calls = []
    def handler(request):
        body = json.loads(request.content)
        calls.append(body)
        method = body["method"]
        if method == "notifications/initialized":
            return httpx.Response(202)
        result = {}
        if method == "initialize":
            result = {"protocolVersion": "2024-11-05"}
        elif method == "tools/list":
            result = {"tools": [tool("check_login_status"), tool("search_feeds", ["keyword"], {"keyword": {"type": "string"}})]}
        elif body["params"]["name"] == "check_login_status":
            result = {"content": [{"type": "text", "text": "✅ 已登录"}]}
        else:
            result = {"structuredContent": {"feeds": [{"id": "one"}]}}
        payload = {"jsonrpc": "2.0", "id": body["id"], "result": result}
        return httpx.Response(200, headers={"Content-Type": "text/event-stream", "Mcp-Session-Id": "test-session"}, content="event: message\ndata: " + json.dumps(payload) + "\n\n")
    adapter = XiaohongshuMcpAdapter("http://test/mcp", httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    status = await adapter.health()
    assert status["connected"] and status["logged_in"]
    assert (await adapter.search("MCP"))["feeds"][0]["id"] == "one"
    with pytest.raises(McpError, match="禁止"):
        await adapter.call("like_feed", {})
    with pytest.raises(McpError, match="必填"):
        await adapter.call("search_feeds", {})
    assert any(call["method"] == "notifications/initialized" for call in calls)
    await adapter.close()

@pytest.mark.asyncio
async def test_read_retry_limited_write_not_retried():
    counts = {"check_login_status": 0, "publish_content": 0}
    def handler(request):
        body = json.loads(request.content)
        name = body["params"]["name"]
        counts[name] += 1
        raise httpx.ConnectError("disconnected")
    adapter = XiaohongshuMcpAdapter("http://test/mcp", httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    adapter.tools = {name: tool(name) for name in counts}
    with pytest.raises(httpx.ConnectError):
        await adapter.call("check_login_status")
    with pytest.raises(httpx.ConnectError):
        await adapter.call("publish_content")
    assert counts == {"check_login_status": 2, "publish_content": 1}
    await adapter.close()

def test_private_access_fields_are_not_returned():
    assert safe_data({"cookie": "private", "xsecToken": "private", "nested": {"api_key": "private"}, "status": "ok"}) == {"nested": {}, "status": "ok"}

@pytest.mark.asyncio
async def test_browser_publish_has_longer_single_attempt_timeout(monkeypatch):
    monkeypatch.setenv("XHS_PUBLISH_TIMEOUT_SECONDS", "600")
    timeouts = []
    def handler(request):
        payload = json.loads(request.content)
        timeouts.append((payload["params"]["name"], request.extensions["timeout"]["read"]))
        return httpx.Response(200, json={"jsonrpc": "2.0", "id": payload["id"], "result": {"structuredContent": {"status": "test"}}})
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler), timeout=45)
    adapter = XiaohongshuMcpAdapter("http://test/mcp", client)
    adapter.tools = {name: tool(name) for name in ("publish_content", "search_feeds")}
    await adapter.call("publish_content")
    await adapter.call("search_feeds")
    assert timeouts == [("publish_content", 600), ("search_feeds", 45)]
    await adapter.close()
