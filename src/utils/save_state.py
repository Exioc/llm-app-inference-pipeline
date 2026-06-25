import json
from pathlib import Path
from pydantic import BaseModel
from src.pipeline.state import PipelineState
from src.schemas.app_data_schema import AppMetadata


def save_state(state: PipelineState | AppMetadata, name: str, path=None) -> None:
    
    # Convert pydantic models to dicts for JSON serialization
    if not isinstance(state, BaseModel):
        storage_path = Path(state.get("storage_path", "results/unknown_run"))
        path = storage_path / f"{name}.json"
        serializable_state = {}
        for key, value in state.items():
            if hasattr(value, "model_dump"):
                serializable_state[key] = value.model_dump()
            else:
                serializable_state[key] = value
    else:
        storage_path = Path(path or "results/unknown_run")
        path = storage_path / f"{name}.json"
        serializable_state = state.model_dump()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable_state, f, indent=2, ensure_ascii=False)
