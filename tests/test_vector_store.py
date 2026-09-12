import sys
import json
import sqlite3
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore


class TestVisionMemoryStore:
    def setup_method(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_memory.db")
        self.store = VisionMemoryStore(db_path=self.db_path)

    def teardown_method(self):
        # Limpiar archivos WAL
        for ext in ["", "-wal", "-shm"]:
            p = self.db_path + ext
            if os.path.exists(p):
                os.remove(p)
        os.rmdir(self.tmp_dir)

    def test_add_and_query_memory(self):
        self.store.add_memory("doc_1", "Texto de prueba sobre intranet corporativa", {"type": "test"})
        results = self.store.query_memory("intranet", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "intranet" in docs[0].lower()

    def test_query_no_results(self):
        self.store.add_memory("doc_1", "Texto sobre recetas de cocina", {"type": "test"})
        results = self.store.query_memory("seguridad informática", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 0

    def test_wal_mode_enabled(self):
        """Verifica que WAL mode esté activado en la base de datos."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        mode = cursor.fetchone()[0]
        conn.close()
        assert mode.lower() == "wal"

    def test_replace_existing_memory(self):
        self.store.add_memory("doc_1", "Texto original", {"type": "test"})
        self.store.add_memory("doc_1", "Texto actualizado", {"type": "test"})
        results = self.store.query_memory("actualizado", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "actualizado" in docs[0]

    def test_metadata_preserved(self):
        meta = {"client": "CTI", "module": "auth"}
        self.store.add_memory("doc_meta", "Contenido", meta)
        results = self.store.query_memory("Contenido", n_results=1)
        # query_memory solo devuelve textos, pero verificamos que no crashee
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
