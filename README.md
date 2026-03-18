# Hybrid RAG

A **Retrieval-Augmented Generation (RAG)** chat app with two interchangeable backends behind a single Streamlit UI:

- **Local** — Ollama (LLM + embeddings) + ChromaDB. Runs entirely on your machine.
- **Cloud** — OpenAI (LLM + embeddings) + MongoDB Atlas. Uses your API keys and Atlas cluster.

Switch modes in the sidebar; the same chat interface works for both.

## Features

- Upload PDFs and text files; documents are chunked and indexed in the chosen vector store.
- Conversation-style Q&A with history-aware retrieval (LangChain `create_history_aware_retriever` + `create_retrieval_chain`).
- Provider abstraction: embeddings, vector store, and LLM are pluggable via interfaces in `rag/interfaces.py`.

## Prerequisites

- **Python 3.x** with `pip`
- **Local mode:** [Ollama](https://ollama.ai) running with models pulled (see below).
- **Cloud mode:** OpenAI API key and a MongoDB Atlas cluster with a vector index.

## Installation

```bash
git clone <repo-url>
cd hybrid-rag
pip install -r requirements.txt
```

Optional: copy `.env.example` to `.env` and adjust defaults (chunk size, model names, paths, etc.). Cloud credentials can also be entered at runtime in the sidebar.

### Local mode: Ollama models

With Ollama installed and running:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Running the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**. Choose **Local** or **Cloud** in the sidebar, enter Cloud credentials if needed, then upload documents and chat.

## Configuration

| Area | Where | Notes |
|------|--------|------|
| Chunking | `config.py` / env | `CHUNK_SIZE`, `CHUNK_OVERLAP` (defaults 512 / 64) |
| Local | `.env` or sidebar | `OLLAMA_BASE_URL`, `OLLAMA_EMBED_MODEL`, `OLLAMA_LLM_MODEL`, Chroma path/collection |
| Cloud | Sidebar (or `.env`) | OpenAI API key, MongoDB URI; optional embed/LLM model overrides |

See `.env.example` for all optional environment variables.

## Project structure

```
hybrid-rag/
├── app.py              # Entry point; builds pipeline and runs Streamlit UI
├── config.py           # Tunables loaded from .env
├── state/
│   └── session.py      # Session state (mode, pipeline, chat history, indexed files)
├── ui/
│   ├── sidebar.py      # Mode picker and Cloud credentials
│   ├── uploader.py     # Document upload and indexing
│   └── chat.py         # Chat UI and message handling
└── rag/
    ├── interfaces.py   # ABCs: BaseEmbeddingProvider, BaseVectorStoreProvider, BaseLLMProvider
    ├── pipeline.py     # RAGPipeline (depends only on interfaces)
    ├── document/       # loader.py, chunker.py
    ├── embeddings/     # local_embeddings.py, cloud_embeddings.py
    ├── vectorstores/   # local_store.py (Chroma), cloud_store.py (MongoDB)
    ├── llm/            # local_llm.py (Ollama), cloud_llm.py (OpenAI)
    └── retrieval/      # chain.py (history-aware retriever + retrieval chain)
```

- **`rag/`** — Backend only (no Streamlit). All LangChain usage lives here.
- **`ui/`** — Streamlit components; they use `st.session_state.pipeline` built by `app.py`.

## License

See repository license file if present.
