import os
from src.memory.vector_store import VisionMemoryStore
from src.config import SEED_DATA_DIR
from src.logger import get_logger

logger = get_logger("vision.memory.seeder")


def seed_vision_mind(store: VisionMemoryStore = None) -> int:
    """Reads all markdown files from seed_data and indexes them into the memory store."""
    if store is None:
        store = VisionMemoryStore()

    seed_dir = str(SEED_DATA_DIR)
    if not os.path.exists(seed_dir):
        logger.warning("seed_data directory not found: %s", seed_dir)
        return 0

    files = sorted([f for f in os.listdir(seed_dir) if f.endswith(".md")])

    count = 0
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
            count += 1
            logger.info("Seed memory indexed: %s", file_name)
        except Exception as e:
            logger.error("Error seeding %s: %s", file_name, e, exc_info=True)

    logger.info("Seeding complete. %d files processed.", count)
    return count


if __name__ == "__main__":
    total = seed_vision_mind()
    print(f"VISION has successfully absorbed {total} seed knowledge documents!")
