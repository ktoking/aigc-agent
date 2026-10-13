"""幂等初始迁移：python migrations/001_initial.py（仓库根目录）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.db import migrate

if __name__ == "__main__":
    migrate()
    print("数据库 schema 已就绪（当前版本 3）")
