import sqlite3
import json
import os
from datetime import datetime
from src.config import DB_PATH, ISSUES_MD_PATH
from src.logger import get_logger

logger = get_logger("vision.tools.issue_tracker")

DB_PATH = str(DB_PATH)
ISSUES_MD_PATH = str(ISSUES_MD_PATH)


def _connect():
    """Crea una conexión SQLite con WAL mode habilitado."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def _init_issues_db():
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_number INTEGER UNIQUE,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description_es TEXT NOT NULL,
                description_en TEXT NOT NULL,
                solution TEXT,
                status TEXT DEFAULT 'Open',
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Base de datos de issues inicializada.")
    except Exception as e:
        logger.error("Error al inicializar DB de issues: %s", e, exc_info=True)
        raise


_init_issues_db()


def _append_to_issues_md(
    issue_number: int,
    title: str,
    category: str,
    description_es: str,
    description_en: str,
    solution: str,
    status: str,
    created_at: str,
) -> None:
    """Appendea el issue al archivo ISSUES.md en formato Markdown bilingüe."""
    status_emoji = "🟢" if "Solucionado" in status or "Resolved" in status or "Closed" in status else "🔴"

    md_block = f"""
### {status_emoji} Incidente / Issue #{issue_number}: {title}

- **ID:** #{issue_number}
- **Fecha / Date:** {created_at}
- **Categoría / Category:** {category}
- **Estado / Status:** {status_emoji} {status}
- **Prioridad / Priority:** Media / Medium

#### 🇲🇽 Descripción (Español)
{description_es}

#### 🇺🇸 Description (English)
{description_en}

#### 🛠️ Solución Implementada / Implemented Solution
{solution if solution else "En análisis / Under analysis."}
---
"""

    try:
        # Si el archivo no existe o está vacío, crear con header
        if not os.path.exists(ISSUES_MD_PATH) or os.path.getsize(ISSUES_MD_PATH) == 0:
            header = """# Base de Registro de Incidencias e Issues (VISION - CTI Soluciones)
*Incident & Issue Tracking Log*

Este documento almacena el registro estructurado de incidencias, errores y mejoras del sistema **VISION MCP**, permitiendo seguimiento bilingüe (Español / English).

---

## 📌 Resumen de Incidencias / Issues Summary

| ID | Título / Title | Categoría / Category | Estado / Status | Fecha / Date |
|:--:|:---------------|:---------------------|:---------------:|:------------:|
"""
            with open(ISSUES_MD_PATH, "w", encoding="utf-8") as f:
                f.write(header)

        # Appendear el issue
        with open(ISSUES_MD_PATH, "a", encoding="utf-8") as f:
            f.write(md_block)

        logger.info("Issue #%d appendeado a ISSUES.md", issue_number)
    except Exception as e:
        logger.error("Error al escribir en ISSUES.md: %s", e, exc_info=True)
        raise


def record_issue(title: str, category: str, description_es: str, description_en: str, solution: str = "", status: str = "Open") -> str:
    """Registra una incidencia en SQLite e ISSUES.md."""
    try:
        conn = _connect()
        cursor = conn.cursor()

        cursor.execute('SELECT MAX(issue_number) FROM issues')
        row = cursor.fetchone()
        next_num = (row[0] or 0) + 1 if row and row[0] is not None else 1

        created_at = datetime.now().strftime("%Y-%m-%d")

        cursor.execute('''
            INSERT INTO issues (issue_number, title, category, description_es, description_en, solution, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (next_num, title, category, description_es, description_en, solution, status, created_at))
        conn.commit()
        conn.close()

        # Sincronizar con ISSUES.md
        _append_to_issues_md(next_num, title, category, description_es, description_en, solution, status, created_at)

        logger.info("Incidente #%d registrado: %s", next_num, title)
        return f"Incidente #{next_num} registrado exitosamente: {title}"
    except Exception as e:
        logger.error("Error al registrar issue: %s", e, exc_info=True)
        return f"⚠️ Error al registrar incidencia: {e}"


def list_recorded_issues() -> str:
    """Lista todos los incidentes/issues registrados."""
    try:
        conn = _connect()
        cursor = conn.cursor()
        cursor.execute('SELECT issue_number, title, category, status, created_at FROM issues ORDER BY issue_number ASC')
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No hay incidencias registradas en la base de datos."

        output = ["=== Base de Incidencias / Issues Log ==="]
        for num, title, cat, status, date in rows:
            output.append(f"#{num} [{status}] ({date}) {title} - Categoría: {cat}")
        return "\n".join(output)
    except Exception as e:
        logger.error("Error al listar issues: %s", e, exc_info=True)
        return f"⚠️ Error al consultar incidencias: {e}"
