import os
import sqlite3
import json

class VisionMemoryStore:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/Documents/vision/vision_memory.db")
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
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

    def add_memory(self, doc_id: str, text: str, metadata: dict = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO memory (doc_id, text, metadata)
            VALUES (?, ?, ?)
        ''', (doc_id, text, json.dumps(metadata or {})))
        conn.commit()
        conn.close()

    def query_memory(self, query_text: str, n_results: int = 3) -> list:
        conn = sqlite3.connect(self.db_path)
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
        return {"documents": [top_docs]}
