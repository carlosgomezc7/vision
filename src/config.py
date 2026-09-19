"""
config.py — Global paths and constants for the VISION project.
All paths are resolved dynamically from this file's location,
working consistently in local, Docker, CI, or any other environment.
"""

import os
from pathlib import Path

# Project root: src/config.py → parent = src/ → parent = vision/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Base directory for persistent data (allows override via env var, e.g. for Docker volume at /app/data)
DATA_DIR = Path(os.getenv("VISION_DATA_DIR", str(PROJECT_ROOT)))

# SQLite database path (memory + issues)
DB_PATH = Path(os.getenv("VISION_DB_PATH", str(DATA_DIR / "vision_memory.db")))

# Seed knowledge data directory
SEED_DATA_DIR = PROJECT_ROOT / "src" / "seed_data"

# Incident tracking markdown file
ISSUES_MD_PATH = DATA_DIR / "ISSUES.md" if os.getenv("VISION_DATA_DIR") else PROJECT_ROOT / "ISSUES.md"

# Logs directory
LOGS_DIR = DATA_DIR / "logs"
LOG_FILE = LOGS_DIR / "vision.log"

