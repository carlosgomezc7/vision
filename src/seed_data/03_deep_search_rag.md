# Arquitectura de Búsqueda Profunda (Deep Search / RAG)

El motor de Deep Search permite a los colaboradores realizar consultas en lenguaje natural sobre los documentos corporativos (PDFs, guías, políticas en Markdown o DOCX).

## Componentes Técnicos
1. **Pipeline de Ingesta & Chunking:** Extracción de texto de documentos corporativos y división en fragmentos (chunks) optimizados para contexto.
2. **Embeddings Vectoriales:** Generación de vectores densos usando modelos de lenguaje eficientes.
3. **Almacenamiento Vectorial:** Supabase con la extensión `pgvector` para consultas híbridas (texto + similitud vectorial).
4. **Recuperación y Generación (RAG):** Contexto inyectado de forma segura al modelo de lenguaje para garantizar respuestas precisas sin alucinaciones, con referencias directas al documento fuente.
