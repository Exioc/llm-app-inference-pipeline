from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL
from src.schemas.feature import FeatureResponse
from src.schemas.group import GroupResponse
from src.schemas.permission import PermissionResponse
from src.schemas.llm import LLMConfig

class LLMWorker:
    def __init__(self, config: LLMConfig):
        self.config = config
        
        # Chat instance
        self.instance: Runnable = self._build_chat_instance()
        
    def _build_chat_instance(self) -> Runnable:
        llm = ChatOllama(
            model=self.config.model,
            temperature=self.config.temperature,
            base_url=OLLAMA_BASE_URL,
            client_kwargs={"headers": {"Authorization": f"Bearer {OLLAMA_API_KEY}"}}
        )

        if self.config.role == "feature": 
            return llm.with_structured_output(FeatureResponse)
        elif self.config.role == "group": 
            return llm.with_structured_output(GroupResponse)
        elif self.config.role == "permission": 
            return llm.with_structured_output(PermissionResponse)
        else:
            return llm

    def run(self, messages: PromptValue):
        return self.instance.invoke(messages)