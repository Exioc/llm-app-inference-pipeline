import os  
import json
import base64
from pathlib import Path
from typing import Callable
from datetime import datetime

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from src.prompts.templates import APP_ANALYSIS_PROMPT_WITH_EXAMPLE
from src.config.config import OLLAMA_API_KEY, OLLAMA_BASE_URL, LLM_MODEL, TEMPERATURE
from src.models.schema import AppAnalysis, PipelineState

# Define LLM with Ollama and structured output
llm = ChatOllama(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        base_url=OLLAMA_BASE_URL,
        client_kwargs={ "headers": { "Authorization": f"Bearer {OLLAMA_API_KEY}"}}
    )

function_llm = llm.with_structured_output(AppAnalysis)

# ──────────────────────────────── Hilfsfunktion ────────────────────────────────

def save_stage(state: PipelineState, stage_name: str):
    
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


# ──────────────────────────────── Stages ────────────────────────────────

def preprocess_node(state: PipelineState):
    metadata = state["metadata"]

    # Base64 Decoding
    def safe_decode(b64_str):
        try:
            return base64.b64decode(b64_str).decode('utf-8')
        except:
            return b64_str

    label = safe_decode(metadata.label)
    description = safe_decode(metadata.description.long)

    # Flatten permissions: Category -> List of strings
    flattened_perms = {
        item.category: item.permissions 
        for item in metadata.permissions
    }

    updates = {
        "pkg": metadata.pkg,
        "label": label,
        "description_long": description,
        "llmodel": state["llm_model"],
        "temperature": state["temperature"],
        "storage_path": state["storage_path"],
        "permissions_map": flattened_perms,
        "metadata": None
    }
    temp_state = {**state, **updates}
    save_stage(temp_state, "01_preprocessing")

    return updates
        

def functionality_node(state: PipelineState):
    messages = APP_ANALYSIS_PROMPT_WITH_EXAMPLE.invoke({
        "label": state["label"],
        "description": state["description_long"]
    })

    result = function_llm.invoke(messages)
    temp_state = {**state, **result.model_dump()}
    save_stage(temp_state, "02_functionality_extraction")

    return {"functionality_result": result}

# ─────────────────────────────── Pipeline ────────────────────────────────

def build_app():
    # 1. Initialisierung mit dem State-Schema
    workflow = StateGraph(PipelineState)

    # 2. Nodes registrieren
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("function", functionality_node)

    # 3. Kanten (Edges) ziehen
    workflow.add_edge(START, "preprocess")
    workflow.add_edge("preprocess", "function")
    workflow.add_edge("function", END)

    # 4. Kompilieren (Das macht den Graph ausführbar)
    app = workflow.compile()
    
    return workflow.compile()