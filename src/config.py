"""
config.py — Rutas y constantes globales del proyecto VISION.
Todas las rutas se resuelven dinámicamente a partir de la ubicación de este archivo,
funcionando igual en local, Docker, CI o cualquier máquina.
"""

from pathlib import Path

# Raíz del proyecto: src/config.py → parent = src/ → parent = vision/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Base de datos SQLite (memoria + issues)
DB_PATH = PROJECT_ROOT / "vision_memory.db"

# Directorio de datos semilla (seed knowledge)
SEED_DATA_DIR = PROJECT_ROOT / "src" / "seed_data"

# Archivo de registro de incidencias
ISSUES_MD_PATH = PROJECT_ROOT / "ISSUES.md"
