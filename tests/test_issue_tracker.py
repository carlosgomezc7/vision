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
        # Backup de la DB real y del ISSUES.md
        self.original_db = str(DB_PATH)
        self.original_md = str(ISSUES_MD_PATH)
        self.tmp_dir = tempfile.mkdtemp()
        self.test_db = os.path.join(self.tmp_dir, "test_issues.db")
        self.test_md = os.path.join(self.tmp_dir, "test_issues.md")

        # Monkey-patch config paths en el módulo
        import src.tools.issue_tracker as it
        it.DB_PATH = self.test_db
        it.ISSUES_MD_PATH = self.test_md
        # Forzar reinicialización de la tabla
        it._init_issues_db()

    def teardown_method(self):
        # Restaurar paths originales
        import src.tools.issue_tracker as it
        it.DB_PATH = self.original_db
        it.ISSUES_MD_PATH = self.original_md
        # Limpiar temporales
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
        assert "Incidente #1 registrado exitosamente" in result

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
        assert "No hay incidencias registradas" in result
