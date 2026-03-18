from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

from config import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL
from rag.interfaces import BaseEmbeddingProvider


class LocalEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_EMBED_MODEL):
        self._embeddings = OllamaEmbeddings(base_url=base_url, model=model)

    def get_embeddings(self) -> Embeddings:
        return self._embeddings
