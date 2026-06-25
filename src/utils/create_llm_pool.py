from langchain_ollama import ChatOllama
from src.models.llm_worker import LLMWorker
from src.schemas.llm import LLMConfig
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL
from src.schemas.func_result import FunctionalityResult
from src.schemas.group_result import SingleFeatureGroupsResult

def create_llm_pool(models: list[dict]) -> list[LLMWorker]:
    llm_pool = []
    
    for model in models:
        config = LLMConfig.model_validate(model)
        handler = LLMWorker(config)
        llm_pool.append(handler)
        
    return llm_pool