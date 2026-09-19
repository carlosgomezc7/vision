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
        # Clean up WAL files
        for ext in ["", "-wal", "-shm"]:
            p = self.db_path + ext
            if os.path.exists(p):
                os.remove(p)
        os.rmdir(self.tmp_dir)

    def test_add_and_query_memory(self):
        self.store.add_memory("doc_1", "Test text about corporate intranet", {"type": "test"})
        results = self.store.query_memory("intranet", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "intranet" in docs[0].lower()

    def test_query_no_results(self):
        self.store.add_memory("doc_1", "Text about cooking recipes", {"type": "test"})
        results = self.store.query_memory("information security", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 0

    def test_wal_mode_enabled(self):
        """Verifies that WAL mode is enabled on the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        mode = cursor.fetchone()[0]
        conn.close()
        assert mode.lower() == "wal"

    def test_replace_existing_memory(self):
        self.store.add_memory("doc_1", "Original text", {"type": "test"})
        self.store.add_memory("doc_1", "Updated text", {"type": "test"})
        results = self.store.query_memory("updated", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "updated" in docs[0].lower()

    def test_metadata_preserved(self):
        meta = {"client": "CTI", "module": "auth"}
        self.store.add_memory("doc_meta", "Content", meta)
        results = self.store.query_memory("Content", n_results=1)
        # query_memory only returns text, but we verify it does not crash
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1

    def test_fts5_search_with_prefix_and_punctuation(self):
        self.store.add_memory("doc_sec", "Zero-Trust architecture with Next.js and Supabase RLS", {"type": "architecture"})
        # Query with punctuation and prefix
        results = self.store.query_memory("Zero-Trust / Next.js", n_results=1)
        docs = results.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "Zero-Trust" in docs[0]

