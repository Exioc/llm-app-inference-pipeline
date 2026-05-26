from pathlib import Path
import json


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