from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import VectorStoreRetriever


CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Given the chat history and the latest user question, "
     "reformulate the question so it can be understood without the chat history. "
     "Do NOT answer the question — just reformulate it if needed, otherwise return it as-is."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant for question-answering tasks. "
     "Use the following retrieved context to answer the question. "
     "If you don't know the answer, say so.\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


def build_rag_chain(llm: BaseChatModel, retriever: VectorStoreRetriever):
    """Build a conversational RAG chain using modern LCEL API."""
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, CONTEXTUALIZE_PROMPT,
    )
    qa_chain = create_stuff_documents_chain(llm, QA_PROMPT)
    return create_retrieval_chain(history_aware_retriever, qa_chain)
