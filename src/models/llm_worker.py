from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL
from src.schemas.func_result import FunctionalityOutput
from src.schemas.group_result import SingleFeatureGroupsOutput
from src.schemas.perm_result import SingleFeaturePermissionsOutput
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
        if self.config.role == "function": 
            return llm.with_structured_output(FunctionalityOutput)
        elif self.config.role == "group": 
            return llm.with_structured_output(SingleFeatureGroupsOutput)
        elif self.config.role == "permission": 
            return llm.with_structured_output(SingleFeaturePermissionsOutput)
        else:
            return llm

    def run(self, messages: PromptValue):
        return self.instance.invoke(messages)