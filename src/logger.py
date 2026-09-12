"""
logger.py — Configuración centralizada de logging para VISION.
Todos los módulos deben importar get_logger() en lugar de usar print().
"""

import logging
import sys
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = logging.INFO, log_file: Path = None) -> None:
    """Configura el logger raíz de VISION con handlers para consola y archivo opcional."""
    handlers = [logging.StreamHandler(sys.stderr)]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(str(log_file), encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger con el namespace dado."""
    return logging.getLogger(name)
