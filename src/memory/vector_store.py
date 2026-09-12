import os
import sqlite3
import json
from src.config import DB_PATH
from src.logger import get_logger

logger = get_logger("vision.memory.vector_store")


class VisionMemoryStore:
    def __init__(self, db_path: str = None):
        self.db_path = str(db_path or DB_PATH)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _connect(self):
        """Crea una conexión SQLite con WAL mode habilitado para mejor concurrencia."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    doc_id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    metadata TEXT
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("Base de datos de memoria inicializada: %s", self.db_path)
        except Exception as e:
            logger.error("Error al inicializar la base de datos: %s", e, exc_info=True)
            raise

    def add_memory(self, doc_id: str, text: str, metadata: dict = None):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO memory (doc_id, text, metadata)
                VALUES (?, ?, ?)
            ''', (doc_id, text, json.dumps(metadata or {})))
            conn.commit()
            conn.close()
            logger.debug("Memoria agregada: doc_id=%s", doc_id)
        except Exception as e:
            logger.error("Error al agregar memoria (doc_id=%s): %s", doc_id, e, exc_info=True)
            raise

    def query_memory(self, query_text: str, n_results: int = 3) -> dict:
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute('SELECT doc_id, text, metadata FROM memory')
            rows = cursor.fetchall()
            conn.close()

            results = []
            query_lower = query_text.lower()
            for doc_id, text, metadata in rows:
                score = 0
                for word in query_lower.split():
                    if word in text.lower():
                        score += 1
                if score > 0 or not query_text:
                    results.append({"doc_id": doc_id, "text": text, "metadata": json.loads(metadata), "score": score})

            results.sort(key=lambda x: x["score"], reverse=True)
            top_docs = [r["text"] for r in results[:n_results]]
            logger.debug("Consulta '%s' devolvió %d resultados", query_text, len(top_docs))
            return {"documents": [top_docs]}
        except Exception as e:
            logger.error("Error al consultar memoria: %s", e, exc_info=True)
            raise
