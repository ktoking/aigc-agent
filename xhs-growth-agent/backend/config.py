import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)
DATA_DIR = Path(os.getenv("XHS_DATA_DIR", str(ROOT / "data"))).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'xhs.db'}")
DEFAULTS = {
    "daily_limit": int(os.getenv("XHS_DAILY_LIMIT", "3")),
    "quality_threshold": 80,
    "account_positioning": "自由创作，以本次输入的内容方向为准",
    "model_mode": os.getenv("XHS_MODEL_MODE", "live"),
    "mcp_url": os.getenv("XHS_MCP_URL", "http://127.0.0.1:18060/mcp"),
    "paused": False,
    "approval_to_queue": False,
    "approved_account_id": "",
    "approved_account_name": "",
    "approved_account_verified_at": "",
    "scheduler_enabled": os.getenv("XHS_SCHEDULER_ENABLED", "false").lower() == "true",
    "production_target": int(os.getenv("XHS_PRODUCTION_TARGET", "50")),
    "keywords": [],
    "rss_urls": ["https://news.google.com/rss?hl=zh-CN&gl=CN&ceid=CN:zh-Hans"],
    "user_id": "",
    "model_name": "gpt-6.1-sol",
    "model_provider": "codex_cli",
    "model_reasoning_effort": "high",
}
