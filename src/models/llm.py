from langchain_ollama import ChatOllama
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL, LLM_MODEL, TEMPERATURE
from src.schemas.func_result_schema import FunctionalityResult
from src.schemas.group_result_schema import SingleFeatureGroupsResult

# Define LLM with Ollama and structured output
llm = ChatOllama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        client_kwargs={ "headers": { "Authorization": f"Bearer {OLLAMA_API_KEY}"}}
    )

function_llm = llm.with_structured_output(FunctionalityResult)

group_llm = llm.with_structured_output(SingleFeatureGroupsResult)

def create_llms(model_names):
    llms = {}

    for i, model in enumerate(model_names, start=1):
        llms[f"llm_{i}"] = ChatOllama(
            model=model,
            temperature=TEMPERATURE,
            base_url=OLLAMA_BASE_URL,
            client_kwargs={ "headers": { "Authorization": f"Bearer {OLLAMA_API_KEY}"}}
        )

    return llms