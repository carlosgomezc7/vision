from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.architecture")


def get_architecture_blueprint(topic: str, store: VisionMemoryStore = None) -> str:
    """Queries VISION's memory for architecture guides (e.g.: Deep Search, RBAC, Next.js)."""
    if store is None:
        store = VisionMemoryStore()

    try:
        results = store.query_memory(topic, n_results=2)
        documents = results.get("documents", [[]])[0]
        if not documents:
            logger.warning("No architectural information found for: %s", topic)
            return f"No specific architectural information found for: {topic}"
        logger.info("Blueprint found for topic: %s", topic)
        return "\n---\n".join(documents)
    except Exception as e:
        logger.error("Error querying blueprint for %s: %s", topic, e, exc_info=True)
        raise
