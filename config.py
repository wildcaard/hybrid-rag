import os
from dotenv import load_dotenv

load_dotenv()

# Chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

# Local (Ollama + ChromaDB)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "llama3.2")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "hybrid_rag")

# Cloud (OpenAI + MongoDB Atlas)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o")
MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB = os.getenv("MONGODB_DB", "hybrid_rag")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "documents")
MONGODB_INDEX = os.getenv("MONGODB_INDEX", "vector_index")
