import os
from src.memory.vector_store import VisionMemoryStore
from src.config import SEED_DATA_DIR
from src.logger import get_logger

logger = get_logger("vision.memory.seeder")


def seed_vision_mind():
    store = VisionMemoryStore()
    seed_dir = str(SEED_DATA_DIR)

    if not os.path.exists(seed_dir):
        logger.warning("Directorio seed_data no encontrado: %s", seed_dir)
        return

    files = [f for f in os.listdir(seed_dir) if f.endswith(".md")]

    for file_name in files:
        file_path = os.path.join(seed_dir, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            doc_id = f"seed_{file_name}"
            store.add_memory(
                doc_id=doc_id,
                text=content,
                metadata={"source": file_name, "type": "seed_knowledge"}
            )
            logger.info("Memoria sembrada e indexada: %s", file_name)
        except Exception as e:
            logger.error("Error al sembrar %s: %s", file_name, e, exc_info=True)

    logger.info("Sembrado completado. %d archivos procesados.", len(files))

if __name__ == "__main__":
    seed_vision_mind()
    print("¡VISION ha absorbido todo el conocimiento semilla con éxito!")
