from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.retrospect")


def record_lesson_learned(project_name: str, lesson: str, store: VisionMemoryStore = None) -> str:
    """Records a lesson learned or key decision in VISION's long-term memory."""
    if store is None:
        store = VisionMemoryStore()

    try:
        doc_id = f"retrospective_{project_name.lower().replace(' ', '_')}_{hash(lesson)}"
        store.add_memory(
            doc_id=doc_id,
            text=f"Project: {project_name}. Lesson/Decision: {lesson}",
            metadata={"type": "retrospective", "project": project_name}
        )
        logger.info("Lesson recorded for project: %s", project_name)
        return f"Lesson successfully recorded in VISION's memory for project '{project_name}'."
    except Exception as e:
        logger.error("Error recording lesson for %s: %s", project_name, e, exc_info=True)
        raise
