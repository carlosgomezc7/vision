"""
auto_commit.py — VISION Auto Commit Tool
Automatically commits and pushes changes every 30 minutes if any are detected.

Usage:
    python src/auto_commit.py
    Ctrl+C to stop.
"""

import subprocess
import time
from datetime import datetime

INTERVAL_MINUTES = 30
INTERVAL_SECONDS = INTERVAL_MINUTES * 60


def has_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def commit_and_push() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"auto: checkpoint {now}"
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"[{now}] ✅ Commit and push: '{message}'")


def main() -> None:
    print(f"🚀 VISION Auto Commit active — cycle every {INTERVAL_MINUTES} min. Ctrl+C to stop.\n")
    try:
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            if has_changes():
                print(f"[{now}] 🔍 Changes detected. Committing...")
                commit_and_push()
            else:
                print(f"[{now}] ✔ No changes.")
            print(f"   ⏳ Next cycle in {INTERVAL_MINUTES} minutes...")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n⛔ Auto-commit stopped.")


if __name__ == "__main__":
    main()
