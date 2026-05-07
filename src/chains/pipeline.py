import os  
import json
import base64
from pathlib import Path
from typing import Callable
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from src.prompts.templates import APP_ANALYSIS_PROMPT, APP_ANALYSIS_PROMPT_WITH_EXAMPLE
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL, LLM_MODEL, TEMPERATURE
from src.models.schema import AppAnalysis, PipelineState


# ──────────────────────────────── Hilfsfunktion ────────────────────────────────

def save_stage(state: PipelineState, stage_name: str) -> PipelineState:
    storage_path = Path(state.get("storage_path", "results/unknown_run"))
    path = storage_path / f"{stage_name}.json"
    
    # Pydantic zu Dict Konvertierung für JSON
    serializable_state = {}
    for key, value in state.items():
        if hasattr(value, "model_dump"):
            serializable_state[key] = value.model_dump()
        else:
            serializable_state[key] = value

    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable_state, f, indent=2, ensure_ascii=False)
    
    return state

# ──────────────────────────────── Pipeline ────────────────────────────────

def stage_1_preprocessing(input_dict: dict) -> PipelineState:
    app: AppBaseModel = input_dict["app_data"]
    storage_path: str = input_dict["storage_path"]
    llm_model: str = input_dict["llm_model"]
    temperature: float = input_dict["temperature"]

    # Base64 Decoding
    def safe_decode(b64_str):
        try:
            return base64.b64decode(b64_str).decode('utf-8')
        except:
            return b64_str

    # Flatten permissions: Category -> List of strings
    flattened_perms = {
        item.category: item.permissions 
        for item in app.permissions
    }

    return PipelineState(
        pkg=app.pkg,
        label=safe_decode(app.label),
        description=safe_decode(app.description.long),
        permissions_map=flattened_perms,
        storage_path=storage_path,
        model=llm_model,
        temperature=temperature,
    )

def build_pipeline():

    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        client_kwargs={ "headers": { "Authorization": f"Bearer {OLLAMA_API_KEY}"}}
    )

    structured_llm = llm.with_structured_output(AppAnalysis)
    
    # Analyse-Chain Stage 2
    analysis_chain = APP_ANALYSIS_PROMPT_WITH_EXAMPLE | structured_llm

    pipeline = (

        # Stage 1 (Preprocessing)
        RunnableLambda(stage_1_preprocessing)
        | RunnableLambda(lambda x: save_stage(x, "01_stage1_preprocessing"))

        # Stage 2 (Functionality extraction)
        | RunnablePassthrough.assign(stage2_result=analysis_chain)
        | RunnableLambda(lambda x: save_stage(x, "02_stage2_functionality_extraction"))
        
    )
    
    return pipeline
