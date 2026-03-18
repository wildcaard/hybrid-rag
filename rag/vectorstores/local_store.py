from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

from config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION
from rag.interfaces import BaseVectorStoreProvider


class LocalVectorStoreProvider(BaseVectorStoreProvider):
    def __init__(self, embeddings: Embeddings,
                 persist_dir: str = CHROMA_PERSIST_DIR,
                 collection: str = CHROMA_COLLECTION):
        self._store = Chroma(
            collection_name=collection,
            embedding_function=embeddings,
            persist_directory=persist_dir,
        )

    def get_store(self) -> Chroma:
        return self._store

    def add_documents(self, documents: list[Document]) -> None:
        self._store.add_documents(documents)

    def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        return self._store.as_retriever(**kwargs)
