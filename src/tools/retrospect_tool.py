from src.memory.vector_store import VisionMemoryStore

store = VisionMemoryStore()

def record_lesson_learned(project_name: str, lesson: str) -> str:
    """Registra una lección aprendida o decisión clave en la memoria a largo plazo de VISION."""
    doc_id = f"retrospective_{project_name.lower().replace(' ', '_')}_{hash(lesson)}"
    store.add_memory(
        doc_id=doc_id,
        text=f"Proyecto: {project_name}. Lección/Decisión: {lesson}",
        metadata={"type": "retrospective", "project": project_name}
    ]
    return f"Lección registrada exitosamente en la memoria de VISION para el proyecto '{project_name}'."
