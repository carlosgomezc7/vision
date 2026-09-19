import json
from datetime import datetime
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.knowledge")


def ingest_knowledge_document(
    title: str,
    category: str,
    content: str,
    tags: list = None,
    store: VisionMemoryStore = None,
) -> str:
    """
    Dynamically ingests and indexes external documents, company policies,
    or technical specifications into VISION's long-term memory with FTS5 search capability.
    """
    if store is None:
        store = VisionMemoryStore()

    if not title or not title.strip():
        raise ValueError("Title cannot be empty.")
    if not content or not content.strip():
        raise ValueError("Content cannot be empty.")

    try:
        clean_title = title.strip()
        clean_cat = category.strip() if category else "General"
        tag_list = tags or []

        doc_id = f"doc_{clean_cat.lower()}_{clean_title.lower().replace(' ', '_')}_{hash(content[:50])}"
        doc_text = f"Title: {clean_title}\nCategory: {clean_cat}\nTags: {', '.join(tag_list)}\n\nContent:\n{content.strip()}"

        metadata = {
            "type": "custom_knowledge",
            "title": clean_title,
            "category": clean_cat,
            "tags": tag_list,
            "indexed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        store.add_memory(doc_id=doc_id, text=doc_text, metadata=metadata)
        logger.info("Knowledge document '%s' successfully ingested into VISION memory", clean_title)

        result = {
            "status": "SUCCESS",
            "doc_id": doc_id,
            "title": clean_title,
            "category": clean_cat,
            "indexed_characters": len(content),
            "search_index": "SQLite FTS5 (BM25)"
        }
        return json.dumps(result, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Error ingesting knowledge document '%s': %s", title, e, exc_info=True)
        raise
