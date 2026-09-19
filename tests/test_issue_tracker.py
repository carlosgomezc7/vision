import sys
import os
import tempfile
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.tools.issue_tracker import record_issue, list_recorded_issues
from src.config import DB_PATH, ISSUES_MD_PATH


class TestIssueTracker:
    def setup_method(self):
        # Backup the real DB and ISSUES.md paths
        self.original_db = str(DB_PATH)
        self.original_md = str(ISSUES_MD_PATH)
        self.tmp_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.tmp_dir, "test_issues.db")
        self.test_md = os.path.join(self.tmp_dir, "test_issues.md")

        # Monkey-patch config paths in the module
        import src.tools.issue_tracker as it
        it.DB_PATH = self.test_db
        it.ISSUES_MD_PATH = self.test_md
        # Force re-initialization of the table
        it._init_issues_db()

    def teardown_method(self):
        # Restore original paths
        import src.tools.issue_tracker as it
        it.DB_PATH = self.original_db
        it.ISSUES_MD_PATH = self.original_md
        # Clean up temp files
        for ext in ["", "-wal", "-shm"]:
            p = self.test_db + ext
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(self.test_md):
            os.remove(self.test_md)
        os.rmdir(self.tmp_dir)

    def test_record_issue_returns_success(self):
        result = record_issue(
            title="Test Issue",
            category="Testing",
            description_es="Descripción de prueba",
            description_en="Test description",
            solution="Ninguna",
            status="Solucionado"
        )
        assert "Issue #1 recorded successfully" in result

    def test_record_issue_creates_markdown(self):
        record_issue(
            title="Markdown Test",
            category="Testing",
            description_es="Desc",
            description_en="Desc EN",
            solution="Fix",
            status="Solucionado"
        )
        assert os.path.exists(self.test_md)
        with open(self.test_md, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Markdown Test" in content
        assert "Desc" in content
        assert "Fix" in content

    def test_list_recorded_issues(self):
        record_issue("Issue A", "Cat", "Desc", "Desc EN", "Fix", "Open")
        record_issue("Issue B", "Cat", "Desc", "Desc EN", "Fix", "Open")
        result = list_recorded_issues()
        assert "Issue A" in result
        assert "Issue B" in result
        assert "#1" in result
        assert "#2" in result

    def test_list_empty_issues(self):
        result = list_recorded_issues()
        assert "No issues recorded in the database." in result

    def test_update_issue_status(self):
        from src.tools.issue_tracker import update_issue_status
        record_issue("Bug X", "Frontend", "Desc ES", "Desc EN", "None", "Open")
        res = update_issue_status(1, "Resolved", "Fixed CSS flexbox overflow")
        assert "updated to 'Resolved' successfully" in res
        listing = list_recorded_issues()
        assert "[Resolved]" in listing

    def test_list_recorded_issues_with_filter(self):
        record_issue("Frontend Bug", "UI", "Desc", "Desc", "", "Open")
        record_issue("Backend Bug", "Database", "Desc", "Desc", "", "Open")
        ui_only = list_recorded_issues(category="UI")
        assert "Frontend Bug" in ui_only
        assert "Backend Bug" not in ui_only

