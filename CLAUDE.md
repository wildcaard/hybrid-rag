# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt    # Install dependencies
streamlit run app.py               # Run the app (default: http://localhost:8501)
```

Local mode requires Ollama running with models pulled:
```bash
ollama pull llama3.2 && ollama pull nomic-embed-text
```

## Architecture

Hybrid RAG app with two interchangeable backends — **Local** (Ollama + ChromaDB) and **Cloud** (OpenAI + MongoDB Atlas) — behind a unified interface, with a Streamlit chat UI.

### Key design pattern: Provider ABCs

`rag/interfaces.py` defines three ABCs (`BaseEmbeddingProvider`, `BaseVectorStoreProvider`, `BaseLLMProvider`). Each mode has concrete implementations in `rag/embeddings/`, `rag/vectorstores/`, `rag/llm/`. The `RAGPipeline` in `rag/pipeline.py` only depends on these interfaces, never concrete classes.

### Layer separation

- **`rag/`** — Pure backend logic with no Streamlit imports. All LangChain integration lives here.
- **`ui/`** — Streamlit components (sidebar, uploader, chat). Depends on `st.session_state.pipeline`.
- **`state/session.py`** — Centralized session state management. Mode switching clears pipeline, chat history, and indexed files.
- **`app.py`** — Entry point. Contains `build_pipeline()` factory that uses delayed imports to avoid loading both backends.

### Data flow

Upload → `loader.py` (tempfile + PyPDFLoader/TextLoader) → `chunker.py` (RecursiveCharacterTextSplitter 512/64) → vector store `add_documents()` → retrieval via LCEL chain (`create_history_aware_retriever` + `create_retrieval_chain`).

### Configuration

All tunables in `config.py`, loaded from `.env` via `python-dotenv`. Cloud credentials (OpenAI key, MongoDB URI) are entered at runtime via the sidebar, not from env vars alone.

### LangChain API usage

Uses modern LangChain >=0.3 APIs. Do NOT use deprecated `ConversationalRetrievalChain` — use `create_history_aware_retriever` and `create_retrieval_chain` from `langchain.chains`.
