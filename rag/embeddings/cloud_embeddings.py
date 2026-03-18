from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from config import OPENAI_EMBED_MODEL
from rag.interfaces import BaseEmbeddingProvider


class CloudEmbeddingProvider(BaseEmbeddingProvider):
    def __init__(self, api_key: str, model: str = OPENAI_EMBED_MODEL):
        self._embeddings = OpenAIEmbeddings(api_key=api_key, model=model)

    def get_embeddings(self) -> Embeddings:
        return self._embeddings
