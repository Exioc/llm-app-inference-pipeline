from langchain_ollama import ChatOllama
from src.schemas.llm import ConfiguredLLM
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL
from src.schemas.func_result import FunctionalityResult
from src.schemas.group_result import SingleFeatureGroupsResult

def create_llm_pool(model_setup: list[dict]) -> list[ConfiguredLLM]:
    llm_pool = []
    
    for setup in model_setup:

        llm = ChatOllama(
            model=setup["model"],
            temperature=setup.get("temperature", 1.0),
            base_url=OLLAMA_BASE_URL,
            client_kwargs={"headers": {"Authorization": f"Bearer {OLLAMA_API_KEY}"}}
        )
        
        role = setup["role"]
        if role == "function": 
            llm = llm.with_structured_output(FunctionalityResult)
        elif role == "group": 
            llm = llm.with_structured_output(SingleFeatureGroupsResult)

        configured_obj = ConfiguredLLM(
            model=setup["model"],
            temperature=setup.get("temperature", 1.0),
            role=role,
            instance=llm
        )
        llm_pool.append(configured_obj)
        
    return llm_pool