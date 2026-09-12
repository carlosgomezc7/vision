from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.retrospect")
store = VisionMemoryStore()


def record_lesson_learned(project_name: str, lesson: str) -> str:
    """Registra una lección aprendida o decisión clave en la memoria a largo plazo de VISION."""
    try:
        doc_id = f"retrospective_{project_name.lower().replace(' ', '_')}_{hash(lesson)}"
        store.add_memory(
            doc_id=doc_id,
            text=f"Proyecto: {project_name}. Lección/Decisión: {lesson}",
            metadata={"type": "retrospective", "project": project_name}
        )
        logger.info("Lección registrada para proyecto: %s", project_name)
        return f"Lección registrada exitosamente en la memoria de VISION para el proyecto '{project_name}'."
    except Exception as e:
        logger.error("Error al registrar lección para %s: %s", project_name, e, exc_info=True)
        raise
