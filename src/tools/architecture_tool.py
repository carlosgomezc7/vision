from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.architecture")
store = VisionMemoryStore()


def get_architecture_blueprint(topic: str) -> str:
    """Consulta la memoria de VISION para obtener guías de arquitectura (ej: Deep Search, RBAC, Next.js)."""
    try:
        results = store.query_memory(topic, n_results=2)
        documents = results.get("documents", [[]])[0]
        if not documents:
            logger.warning("No se encontró información arquitectónica para: %s", topic)
            return f"No se encontró información arquitectónica específica para: {topic}"
        logger.info("Blueprint encontrado para topic: %s", topic)
        return "\n---\n".join(documents)
    except Exception as e:
        logger.error("Error al consultar blueprint para %s: %s", topic, e, exc_info=True)
        raise
