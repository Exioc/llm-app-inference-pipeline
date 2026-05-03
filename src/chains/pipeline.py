from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_ollama import ChatOllama
from src.prompts.templates import APP_ANALYSIS_PROMPT, APP_ANALYSIS_PROMPT_WITH_EXAMPLE
from src.models.schema import AppAnalysis, PipelineState

import os  
import json
from pathlib import Path
from typing import Callable
from datetime import datetime

RESULTS_BASE_DIR = Path("results")

api_key = os.getenv("OLLAMA_API_KEY")
url = os.getenv("OLLAMA_BASE_URL")
modell = os.getenv("LLM_MODEL")
temperature = float(os.getenv("TEMPERATURE"))


# ──────────────────────────────── Hilfsfunktion ────────────────────────────────

def initialize_run_folder(state: PipelineState) -> PipelineState:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RESULTS_BASE_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    state["run_dir"] = str(run_dir)
    return state

def save_stage(state: PipelineState, stage_name: str) -> PipelineState:
    run_dir = Path(state.get("run_dir", str(RESULTS_BASE_DIR)))
    timestamp = datetime.now().strftime("%H%M%S_%f")
    path = run_dir / f"{stage_name}.json"
    
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

def stage_1_logic(state: PipelineState) -> str:
    return f"Stage 1 hat den Titel '{state['app_title']}' empfangen."

def stage_3_logic(state: PipelineState) -> str:
    analysis = state['stage2_result']
    count = len(analysis.features)
    return f"Stage 3 hat {count} Features aus Stage 2 erhalten und validiert."

def build_pipeline():

    llm = ChatOllama(
        model=modell,
        temperature=1.0,
        base_url=url,
        client_kwargs={ "headers": { "Authorization": f"Bearer {api_key}"}}
    )

    structured_llm = llm.with_structured_output(AppAnalysis)
    
    # Analyse-Chain Stage 2
    analysis_chain = APP_ANALYSIS_PROMPT_WITH_EXAMPLE | structured_llm

    pipeline = (

        # Run-Ordner erstellen
        RunnableLambda(initialize_run_folder)

        # 1. Input speichern
        | RunnableLambda(lambda x: save_stage(x, "00_input"))
        
        # 2. Stage 1 ausführen und Ergebnis speichern
        | RunnablePassthrough.assign(stage1_result=RunnableLambda(stage_1_logic))
        | RunnableLambda(lambda x: save_stage(x, "01_stage1"))
        
        # 3. Stage 2 (Analyse) ausführen und Ergebnis speichern
        | RunnablePassthrough.assign(stage2_result=analysis_chain)
        | RunnableLambda(lambda x: save_stage(x, "02_stage2"))
        
        # 4. Stage 3 ausführen und Endzustand speichern
        | RunnablePassthrough.assign(stage3_result=RunnableLambda(stage_3_logic))
        | RunnableLambda(lambda x: save_stage(x, "03_final"))
    )
    
    return pipeline
