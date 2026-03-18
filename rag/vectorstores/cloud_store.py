from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever
from pymongo import MongoClient

from config import MONGODB_DB, MONGODB_COLLECTION, MONGODB_INDEX
from rag.interfaces import BaseVectorStoreProvider


class CloudVectorStoreProvider(BaseVectorStoreProvider):
    def __init__(self, embeddings: Embeddings, mongodb_uri: str,
                 db_name: str = MONGODB_DB,
                 collection_name: str = MONGODB_COLLECTION,
                 index_name: str = MONGODB_INDEX):
        self._client = MongoClient(mongodb_uri)
        self._collection = self._client[db_name][collection_name]
        self._store = MongoDBAtlasVectorSearch(
            collection=self._collection,
            embedding=embeddings,
            index_name=index_name,
        )

    def get_store(self) -> MongoDBAtlasVectorSearch:
        return self._store

    def add_documents(self, documents: list[Document]) -> None:
        self._store.add_documents(documents)

    def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        return self._store.as_retriever(**kwargs)
