#!/usr/bin/env python3
"""仓库入口；实现随 story-film-workflow skill 一同分发。"""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "skills/story-film-workflow/scripts/minimax_tts.py"), run_name="__main__")
