from src.models.llm_worker import LLMWorker
from src.schemas.llm import LLMConfig

# Creates a pool of LLMWorker instances based on the provided model configurations.
def create_llm_pool(models: list[dict]) -> list[LLMWorker]:
    llm_pool = []
    
    for model in models:
        config = LLMConfig.model_validate(model)
        handler = LLMWorker(config)
        llm_pool.append(handler)
        
    return llm_pool