import sqlite3
import json
import os
from datetime import datetime
from src.config import DB_PATH as CONFIG_DB_PATH, ISSUES_MD_PATH as CONFIG_ISSUES_MD_PATH
from src.logger import get_logger

logger = get_logger("vision.tools.issue_tracker")

# Exported module-level paths (configurable for testing)
DB_PATH = str(CONFIG_DB_PATH)
ISSUES_MD_PATH = str(CONFIG_ISSUES_MD_PATH)


def _connect() -> sqlite3.Connection:
    """Creates a SQLite connection with WAL mode and timeout enabled."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def _init_issues_db() -> None:
    """Initializes the issues schema idempotently."""
    try:
        with _connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_number INTEGER UNIQUE,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description_es TEXT NOT NULL,
                    description_en TEXT NOT NULL,
                    solution TEXT,
                    status TEXT DEFAULT 'Open',
                    created_at TEXT NOT NULL,
                    updated_at TEXT
                )
            """)
        logger.info("Issues database initialized.")
    except Exception as e:
        logger.error("Error initializing issues DB: %s", e, exc_info=True)
        raise


def _ensure_db() -> None:
    """Ensures the issues database schema exists before access."""
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
    """Appends the issue to the ISSUES.md file in bilingual Markdown format."""
    status_emoji = "🟢" if any(k in status for k in ["Resolved", "Closed", "Solucionado"]) else "🔴"

    md_block = f"""
### {status_emoji} Issue #{issue_number}: {title}

- **ID:** #{issue_number}
- **Date:** {created_at}
- **Category:** {category}
- **Status:** {status_emoji} {status}
- **Priority:** Medium

#### 🇲🇽 Description (Spanish)
{description_es}

#### 🇺🇸 Description (English)
{description_en}

#### 🛠️ Implemented Solution
{solution if solution else "Under analysis."}
---
"""

    try:
        # If the file does not exist or is empty, create it with a header
        if not os.path.exists(ISSUES_MD_PATH) or os.path.getsize(ISSUES_MD_PATH) == 0:
            header = """# Incident & Issue Tracking Log (VISION - CTI Soluciones)

This document stores the structured record of incidents, errors, and improvements for the **VISION MCP** system, enabling bilingual tracking (Spanish / English).

---

## 📌 Issues Summary

| ID | Title | Category | Status | Date |
|:--:|:------|:---------|:------:|:----:|
"""
            with open(ISSUES_MD_PATH, "w", encoding="utf-8") as f:
                f.write(header)

        # Append the issue
        with open(ISSUES_MD_PATH, "a", encoding="utf-8") as f:
            f.write(md_block)

        logger.info("Issue #%d appended to ISSUES.md", issue_number)
    except Exception as e:
        logger.error("Error writing to ISSUES.md: %s", e, exc_info=True)
        raise


def record_issue(
    title: str,
    category: str,
    description_es: str,
    description_en: str,
    solution: str = "",
    status: str = "Open",
) -> str:
    """Records an incident in SQLite and ISSUES.md."""
    _ensure_db()
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(issue_number) FROM issues")
            row = cursor.fetchone()
            next_num = (row[0] or 0) + 1 if row and row[0] is not None else 1

            now_date = datetime.now().strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO issues (issue_number, title, category, description_es, description_en, solution, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (next_num, title, category, description_es, description_en, solution, status, now_date, now_date))

        # Sync with ISSUES.md
        _append_to_issues_md(next_num, title, category, description_es, description_en, solution, status, now_date)

        logger.info("Issue #%d recorded: %s", next_num, title)
        return f"Issue #{next_num} recorded successfully: {title}"
    except Exception as e:
        logger.error("Error recording issue: %s", e, exc_info=True)
        return f"⚠️ Error recording issue: {e}"


def update_issue_status(issue_number: int, new_status: str, solution: str = "") -> str:
    """Updates the status and solution for an existing issue in SQLite."""
    _ensure_db()
    try:
        now_date = datetime.now().strftime("%Y-%m-%d")
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, category FROM issues WHERE issue_number = ?", (issue_number,))
            row = cursor.fetchone()
            if not row:
                return f"⚠️ Issue #{issue_number} not found."

            title, category = row
            if solution:
                cursor.execute("""
                    UPDATE issues
                    SET status = ?, solution = ?, updated_at = ?
                    WHERE issue_number = ?
                """, (new_status, solution, now_date, issue_number))
            else:
                cursor.execute("""
                    UPDATE issues
                    SET status = ?, updated_at = ?
                    WHERE issue_number = ?
                """, (new_status, now_date, issue_number))

        logger.info("Issue #%d updated to status '%s'", issue_number, new_status)
        return f"Issue #{issue_number} updated to '{new_status}' successfully."
    except Exception as e:
        logger.error("Error updating issue #%d: %s", issue_number, e, exc_info=True)
        return f"⚠️ Error updating issue: {e}"


def list_recorded_issues(category: str = None, status: str = None, limit: int = 50, offset: int = 0) -> str:
    """Lists recorded incidents/issues with optional filtering and pagination."""
    _ensure_db()
    try:
        query = "SELECT issue_number, title, category, status, created_at FROM issues"
        params = []
        conditions = []

        if category:
            conditions.append("category = ?")
            params.append(category)
        if status:
            conditions.append("status = ?")
            params.append(status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY issue_number ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

        if not rows:
            return "No issues recorded in the database."

        output = ["=== Issues Log ==="]
        for num, title, cat, stat, date in rows:
            output.append(f"#{num} [{stat}] ({date}) {title} - Category: {cat}")
        return "\n".join(output)
    except Exception as e:
        logger.error("Error listing issues: %s", e, exc_info=True)
        return f"⚠️ Error retrieving issues: {e}"
