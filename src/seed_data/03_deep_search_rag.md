# Deep Search Architecture (Deep Search / RAG)

The Deep Search engine allows employees to query corporate documents (PDFs, guides, policies in Markdown or DOCX) in natural language.

## Technical Components
1. **Ingestion & Chunking Pipeline:** Text extraction from corporate documents and division into context-optimized chunks.
2. **Vector Embeddings:** Generation of dense vectors using efficient language models.
3. **Vector Storage:** Supabase with the `pgvector` extension for hybrid queries (text + vector similarity).
4. **Retrieval and Generation (RAG):** Context securely injected into the language model to guarantee accurate responses without hallucinations, with direct references to the source document.
