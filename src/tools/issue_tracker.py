import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/Documents/vision/vision_memory.db")
ISSUES_MD_PATH = os.path.expanduser("~/Documents/vision/ISSUES.md")

def _init_issues_db():
    conn = sqlite3.connect(DB_PATH)
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

_init_issues_db()

def record_issue(title: str, category: str, description_es: str, description_en: str, solution: str = "", status: str = "Open") -> str:
    """Registra una incidencia en SQLite e ISSUES.md."""
    conn = sqlite3.connect(DB_PATH)
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
    
    return f"Incidente #{next_num} registrado exitosamente: {title}"

def list_recorded_issues() -> str:
    """Lista todos los incidentes/issues registrados."""
    conn = sqlite3.connect(DB_PATH)
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
