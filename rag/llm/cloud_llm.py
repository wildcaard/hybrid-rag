from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from config import OPENAI_LLM_MODEL
from rag.interfaces import BaseLLMProvider


class CloudLLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = OPENAI_LLM_MODEL):
        self._llm = ChatOpenAI(api_key=api_key, model=model)

    def get_llm(self) -> BaseChatModel:
        return self._llm
