from langchain_ollama import ChatOllama
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL, LLM_MODEL, TEMPERATURE
#from src.pipeline.state import FunctionalityResult, SingleFeatureGroup
from src.schemas.functionality import FunctionalityResult
from src.schemas.permissions_groups import SingleFeatureGroups

# Define LLM with Ollama and structured output
llm = ChatOllama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        client_kwargs={ "headers": { "Authorization": f"Bearer {OLLAMA_API_KEY}"}}
    )

function_llm = llm.with_structured_output(FunctionalityResult)

group_llm = llm.with_structured_output(SingleFeatureGroups)