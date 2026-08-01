from src.memory.vector_store import VisionMemoryStore

store = VisionMemoryStore()

def get_architecture_blueprint(topic: str) -> str:
    """Consulta la memoria de VISION para obtener guías de arquitectura (ej: Deep Search, RBAC, Next.js)."""
    results = store.query_memory(topic, n_results=2)
    documents = results.get("documents", [[]])[0]
    if not documents:
        return f"No se encontró información arquitectónica específica para: {topic}"
    return "\n---\n".join(documents)
