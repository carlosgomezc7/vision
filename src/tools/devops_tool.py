import os
import json
import sqlite3
import subprocess
from datetime import datetime
from src.config import DB_PATH, SEED_DATA_DIR, PROJECT_ROOT, LOG_FILE
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.devops")


def get_project_health_status(store: VisionMemoryStore = None) -> str:
    """
    Performs a comprehensive diagnostic of the VISION MCP server:
    - SQLite database integrity and table counts
    - Memory documents count & FTS5 status
    - Issues tracker status (Open vs Resolved)
    - Seed files integrity
    - Git status summary
    """
    if store is None:
        store = VisionMemoryStore()

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "database": {},
        "knowledge_base": {},
        "issue_tracker": {},
        "git_status": {},
        "system_health": "OPTIMAL"
    }

    # 1. Database check
    db_file = str(store.db_path)
    if os.path.exists(db_file):
        size_kb = round(os.path.getsize(db_file) / 1024, 2)
        try:
            conn = sqlite3.connect(db_file, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            integrity = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM memory;")
            mem_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM memory_fts;")
            fts_count = cursor.fetchone()[0]

            conn.close()
            report["database"] = {
                "path": db_file,
                "size_kb": size_kb,
                "integrity": integrity,
                "memories_indexed": mem_count,
                "fts5_records": fts_count
            }
        except Exception as dbe:
            report["database"] = {"error": str(dbe)}
            report["system_health"] = "DEGRADED"
    else:
        report["database"] = {"status": "not_created_yet"}

    # 2. Seed files check
    seed_path = str(SEED_DATA_DIR)
    if os.path.exists(seed_path):
        seeds = [f for f in os.listdir(seed_path) if f.endswith(".md")]
        report["knowledge_base"] = {
            "seed_files_count": len(seeds),
            "directory": seed_path
        }
    else:
        report["knowledge_base"] = {"error": "seed directory not found"}

    # 3. Issue tracker count
    try:
        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file, timeout=5.0)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues';")
            if cursor.fetchone():
                cursor.execute("SELECT status, COUNT(*) FROM issues GROUP BY status;")
                counts = dict(cursor.fetchall())
                report["issue_tracker"] = {
                    "total_issues": sum(counts.values()),
                    "by_status": counts
                }
            conn.close()
    except Exception as ie:
        report["issue_tracker"] = {"error": str(ie)}

    # 4. Git status check
    try:
        git_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        dirty_lines = [line.strip() for line in git_res.stdout.strip().split("\n") if line.strip()]

        branch_res = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = branch_res.stdout.strip() or "detached"

        log_res = subprocess.run(
            ["git", "log", "-1", "--format=%h - %s (%cr)"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        last_commit = log_res.stdout.strip()

        report["git_status"] = {
            "current_branch": current_branch,
            "is_clean": len(dirty_lines) == 0,
            "modified_files_count": len(dirty_lines),
            "last_commit": last_commit
        }
    except Exception as ge:
        report["git_status"] = {"error": str(ge)}

    return json.dumps(report, indent=2, ensure_ascii=False)


def trigger_git_checkpoint(message: str) -> str:
    """
    Creates an on-demand Git checkpoint commit for the current project state.
    Ensures safe conventional message format and staging of modifications.
    """
    if not message or not message.strip():
        raise ValueError("Commit message cannot be empty.")

    clean_msg = message.strip()
    if not any(clean_msg.startswith(prefix) for prefix in ["feat:", "fix:", "refactor:", "chore:", "checkpoint:", "docs:"]):
        clean_msg = f"checkpoint: {clean_msg}"

    try:
        # Check for changes
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        if not status_res.stdout.strip():
            return "No changes detected. Working directory is clean."

        # Stage and commit
        subprocess.run(["git", "add", "."], cwd=str(PROJECT_ROOT), check=True, timeout=10)
        commit_res = subprocess.run(
            ["git", "commit", "-m", clean_msg],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )

        # Get new commit hash
        hash_res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5
        )
        commit_hash = hash_res.stdout.strip()

        logger.info("Git checkpoint created: %s (%s)", commit_hash, clean_msg)
        return f"✅ Git checkpoint created: [{commit_hash}] '{clean_msg}'"

    except subprocess.CalledProcessError as cpe:
        logger.error("Git checkpoint failed: %s", cpe.stderr, exc_info=True)
        return f"⚠️ Git checkpoint error: {cpe.stderr}"
    except Exception as e:
        logger.error("Unexpected error in trigger_git_checkpoint: %s", e, exc_info=True)
        return f"⚠️ Checkpoint error: {e}"
