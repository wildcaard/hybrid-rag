from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

from config import OLLAMA_BASE_URL, OLLAMA_LLM_MODEL
from rag.interfaces import BaseLLMProvider


class LocalLLMProvider(BaseLLMProvider):
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_LLM_MODEL):
        self._llm = ChatOllama(base_url=base_url, model=model)

    def get_llm(self) -> BaseChatModel:
        return self._llm
