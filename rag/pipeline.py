from langchain_core.messages import AIMessage, HumanMessage

from rag.document.loader import load_uploaded_file
from rag.document.chunker import chunk_documents
from rag.interfaces import BaseEmbeddingProvider, BaseVectorStoreProvider, BaseLLMProvider
from rag.retrieval.chain import build_rag_chain


class RAGPipeline:
    """Facade that composes embedding, vector store, LLM, and retrieval chain."""

    def __init__(self, embedding_provider: BaseEmbeddingProvider,
                 vectorstore_provider: BaseVectorStoreProvider,
                 llm_provider: BaseLLMProvider):
        self._embedding_provider = embedding_provider
        self._vectorstore_provider = vectorstore_provider
        self._llm_provider = llm_provider
        self._chain = None

    def _ensure_chain(self):
        if self._chain is None:
            retriever = self._vectorstore_provider.as_retriever(
                search_kwargs={"k": 4},
            )
            self._chain = build_rag_chain(
                self._llm_provider.get_llm(), retriever,
            )

    def index_file(self, uploaded_file) -> int:
        """Load, chunk, and index an uploaded file. Returns chunk count."""
        docs = load_uploaded_file(uploaded_file)
        chunks = chunk_documents(docs)
        self._vectorstore_provider.add_documents(chunks)
        # Reset chain so retriever picks up new documents
        self._chain = None
        return len(chunks)

    def query(self, question: str, chat_history: list[dict]) -> str:
        """Run the RAG chain with conversational history."""
        self._ensure_chain()
        # Convert chat history dicts to LangChain messages
        lc_history = []
        for msg in chat_history:
            if msg["role"] == "user":
                lc_history.append(HumanMessage(content=msg["content"]))
            else:
                lc_history.append(AIMessage(content=msg["content"]))

        result = self._chain.invoke({
            "input": question,
            "chat_history": lc_history,
        })
        return result["answer"]
