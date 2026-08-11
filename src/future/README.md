# 🔮 Futuras Mejoras — VISION MCP

Este directorio documenta mejoras planificadas que aún no están implementadas pero se activarán cuando el proyecto lo requiera.

---

## 🧠 Búsqueda Semántica con Embeddings

### Estado actual

Hoy la memoria de VISION busca por **coincidencia exacta de palabras**:

```python
# vector_store.py — búsqueda actual
for word in query_lower.split():
    if word in text.lower():
        score += 1
```

Esto funciona con pocos documentos (~13 seeds), pero **no escala** cuando la memoria crezca con datos de múltiples clientes.

### ¿Qué son los embeddings?

Un **embedding** es una representación numérica del *significado* de un texto. En lugar de comparar palabras, se comparan vectores de números que capturan conceptos:

```
"seguridad de la intranet"  →  [0.82, -0.15, 0.44, ...]
"Zero Trust authentication" →  [0.79, -0.18, 0.41, ...]   ← Vectores cercanos = mismo tema
"receta de cocina"          →  [0.03, 0.91, -0.67, ...]   ← Vector lejano = tema diferente
```

### ¿Por qué importa para VISION?

| Escenario | Sin embeddings | Con embeddings |
|-----------|:-:|:-:|
| Buscar `"proteger rutas del dashboard"` cuando el doc dice `"middleware auth guard"` | ❌ | ✅ |
| Buscar en español y encontrar docs en inglés | ❌ | ✅ |
| Buscar `"login corporativo"` y encontrar docs sobre `"autenticación SSO"` | ❌ | ✅ |
| 13 documentos en memoria | ⚠️ Funciona OK | ✅ |
| 50+ documentos (5+ clientes) | ❌ Resultados irrelevantes | ✅ Preciso |
| 100+ documentos (producción) | ❌ Inútil | ✅ Sigue preciso |

### ¿Cuándo activar esta mejora?

Implementar cuando se cumpla **cualquiera** de estas condiciones:

- [ ] La memoria supere **30+ documentos**
- [ ] Se agreguen datos de **2+ clientes reales**
- [ ] Las búsquedas actuales empiecen a devolver **resultados irrelevantes**
- [ ] Se necesite búsqueda **cross-language** (español ↔ inglés)

---

## 📦 Dependencias requeridas

```txt
chromadb>=1.5.9
sentence-transformers>=5.6.1
```

### Guía de instalación

#### 1. Agregar al requirements.txt

```bash
echo "chromadb>=1.5.9" >> requirements.txt
echo "sentence-transformers>=5.6.1" >> requirements.txt
```

#### 2. Instalar en el entorno virtual

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

> ⚠️ **Nota:** `sentence-transformers` descarga un modelo de ~400MB la primera vez.
> Asegúrate de tener espacio y conexión estable.

#### 3. Modelo recomendado

```python
from sentence_transformers import SentenceTransformer

# Modelo multilingüe (español + inglés) — ideal para VISION
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
```

| Modelo | Idiomas | Tamaño | Precisión |
|--------|---------|--------|-----------|
| `paraphrase-multilingual-MiniLM-L12-v2` | 50+ (incluye ES) | ~420MB | ⭐⭐⭐⭐ |
| `all-MiniLM-L6-v2` | Solo inglés | ~80MB | ⭐⭐⭐ |
| `all-mpnet-base-v2` | Solo inglés | ~420MB | ⭐⭐⭐⭐⭐ |

**Recomendado para VISION:** `paraphrase-multilingual-MiniLM-L12-v2` porque los seeds y documentos mezclan español e inglés.

#### 4. Implementación en vector_store.py

Cuando decidas activar embeddings, reemplazar el método `query_memory` en `vector_store.py` con una implementación basada en ChromaDB:

```python
import chromadb
from sentence_transformers import SentenceTransformer

class VisionMemoryStore:
    def __init__(self):
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        self.client = chromadb.PersistentClient(path=str(DB_PATH.parent / "chroma_db"))
        self.collection = self.client.get_or_create_collection(
            name="vision_memory",
            metadata={"hnsw:space": "cosine"}
        )

    def add_memory(self, doc_id: str, text: str, metadata: dict = None):
        embedding = self.model.encode(text).tolist()
        self.collection.upsert(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )

    def query_memory(self, query_text: str, n_results: int = 3):
        query_embedding = self.model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
```

#### 5. Actualizar el Dockerfile

Agregar las build deps necesarias para compilar las dependencias nativas:

```dockerfile
# En el stage builder, agregar:
RUN apt-get install -y --no-install-recommends \
    build-essential gcc g++
```

#### 6. Agregar chroma_db/ al .gitignore

```bash
echo "chroma_db/" >> .gitignore
```

> Ya está incluido en el `.gitignore` actual, así que no necesitas hacer nada.

---

## 📝 Notas adicionales

- La imagen Docker aumentará de **~200MB a ~2GB** al activar embeddings.
- El primer arranque tardará **30-60 segundos extra** mientras carga el modelo en memoria.
- ChromaDB crea una carpeta `chroma_db/` para persistir los vectores — asegúrate de montarla como volumen Docker.
