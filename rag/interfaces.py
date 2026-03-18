from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document


class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        ...


class BaseVectorStoreProvider(ABC):
    @abstractmethod
    def get_store(self):
        ...

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> None:
        ...

    @abstractmethod
    def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        ...


class BaseLLMProvider(ABC):
    @abstractmethod
    def get_llm(self) -> BaseChatModel:
        ...
