import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel

def save_state(state: Any, name: str, path: str | Path | None = None) -> None:
    # Determine the target folder (either from a parameter or from the state)
    if path:
        storage_dir = Path(path)
    elif isinstance(state, dict) and "storage_path" in state:
        storage_dir = Path(state["storage_path"])
    elif hasattr(state, "storage_path") and state.storage_path:
        storage_dir = Path(state.storage_path)
    else:
        raise ValueError(
            f"Could not determine storage path to save '{name}.json'. "
            "Please provide a 'path' argument or define 'storage_path' in the state."
        )

    file_path = storage_dir / f"{name}.json"

    # Create folder if it does not already exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Prepare serializable output data
    data_to_save = state.model_dump() if isinstance(state, BaseModel) else state

    # Writing JSON with a fallback encoder for nested Pydantic models
    def pydantic_encoder(obj: Any) -> Any:
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data_to_save,
            f,
            indent=2,
            ensure_ascii=False,
            default=pydantic_encoder
        )