"""幂等迁移 v2：绑定经 MCP 核验的账号，撤销没有账号绑定的旧授权。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.db import migrate

if __name__ == "__main__":
    migrate()
    print("数据库 schema version 2 已就绪")
