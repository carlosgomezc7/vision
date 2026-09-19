import os
import re
import json
import sqlite3
from src.config import DB_PATH
from src.logger import get_logger

logger = get_logger("vision.memory.vector_store")


class VisionMemoryStore:
    """
    Persistent memory store using SQLite with Full-Text Search (FTS5)
    and BM25 relevance ranking for Deep Search / RAG capabilities.
    """

    def __init__(self, db_path: str = None):
        self.db_path = str(db_path or DB_PATH)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        """Creates a SQLite connection with WAL mode and busy timeout enabled."""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self) -> None:
        try:
            with self._connect() as conn:
                # Base memory storage table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS memory (
                        doc_id TEXT PRIMARY KEY,
                        text TEXT NOT NULL,
                        metadata TEXT
                    )
                """)

                # Virtual table for high-performance Full-Text Search (FTS5) with BM25 ranking
                conn.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                        doc_id UNINDEXED,
                        text,
                        tokenize = 'porter unicode61'
                    )
                """)

                # Backfill FTS index if the base table has items not yet indexed
                conn.execute("""
                    INSERT INTO memory_fts (doc_id, text)
                    SELECT doc_id, text FROM memory
                    WHERE doc_id NOT IN (SELECT doc_id FROM memory_fts)
                """)

            logger.info("Memory database & FTS5 index initialized: %s", self.db_path)
        except Exception as e:
            logger.error("Error initializing the memory database: %s", e, exc_info=True)
            raise

    def add_memory(self, doc_id: str, text: str, metadata: dict = None) -> None:
        """Stores or replaces a memory record and updates the FTS5 index atomically."""
        try:
            with self._connect() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO memory (doc_id, text, metadata)
                    VALUES (?, ?, ?)
                """, (doc_id, text, json.dumps(metadata or {})))

                # Keep FTS5 table strictly synchronized
                conn.execute("DELETE FROM memory_fts WHERE doc_id = ?", (doc_id,))
                conn.execute("INSERT INTO memory_fts (doc_id, text) VALUES (?, ?)", (doc_id, text))

            logger.debug("Memory added & indexed: doc_id=%s", doc_id)
        except Exception as e:
            logger.error("Error adding memory (doc_id=%s): %s", doc_id, e, exc_info=True)
            raise

    def query_memory(self, query_text: str, n_results: int = 3) -> dict:
        """
        Queries memory using SQLite FTS5 with BM25 ranking.
        Falls back to lexical matching if query contains no indexable tokens.
        """
        try:
            if not query_text or not query_text.strip():
                with self._connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT text FROM memory LIMIT ?", (n_results,))
                    docs = [row[0] for row in cursor.fetchall()]
                    return {"documents": [docs]}

            # Extract alphanumeric search tokens
            words = re.findall(r"\w+", query_text)
            if words:
                fts_query = " OR ".join(f'"{w}"*' for w in words)
                try:
                    with self._connect() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT text
                            FROM memory_fts
                            WHERE memory_fts MATCH ?
                            ORDER BY rank ASC
                            LIMIT ?
                        """, (fts_query, n_results))
                        rows = cursor.fetchall()
                        if rows:
                            top_docs = [r[0] for r in rows]
                            logger.debug("FTS5 query '%s' returned %d results", query_text, len(top_docs))
                            return {"documents": [top_docs]}
                except sqlite3.OperationalError as oe:
                    logger.warning("FTS5 match failed (%s), falling back to lexical search", oe)

            # Fallback lexical search if FTS returned nothing
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT doc_id, text, metadata FROM memory")
                rows = cursor.fetchall()

            results = []
            query_lower = query_text.lower()
            for doc_id, text, metadata in rows:
                score = 0
                for word in query_lower.split():
                    if word in text.lower():
                        score += 1
                if score > 0:
                    results.append({"text": text, "score": score})

            results.sort(key=lambda x: x["score"], reverse=True)
            top_docs = [r["text"] for r in results[:n_results]]
            logger.debug("Fallback query '%s' returned %d results", query_text, len(top_docs))
            return {"documents": [top_docs]}

        except Exception as e:
            logger.error("Error querying memory: %s", e, exc_info=True)
            raise
