"""幂等迁移 v3：记录每篇授权源于手动确认或显式启用的人工审批发布策略。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.db import migrate

if __name__ == "__main__":
    migrate()
    print("数据库 schema version 3 已就绪")
