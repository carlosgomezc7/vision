import os
from src.memory.vector_store import VisionMemoryStore

def seed_vision_mind():
    store = VisionMemoryStore()
    seed_dir = os.path.expanduser("~/Documents/vision/src/seed_data")
    
    if not os.path.exists(seed_dir):
        print(f"Directorio seed_data no encontrado: {seed_dir}")
        return

    files = [f for f in os.listdir(seed_dir) if f.endswith(".md")]
    
    for file_name in files:
        file_path = os.path.join(seed_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        doc_id = f"seed_{file_name}"
        store.add_memory(
            doc_id=doc_id,
            text=content,
            metadata={"source": file_name, "type": "seed_knowledge"}
        )
        print(f"Memoria sembrada e indexada: {file_name}")

if __name__ == "__main__":
    seed_vision_mind()
    print("¡VISION ha absorbido todo el conocimiento semilla con éxito!")
