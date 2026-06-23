import json
import uuid
from pathlib import Path
from pydantic_core import to_jsonable_python

def save_dict_to_json(data: dict, folder_path: str | Path, file_name: str) -> None:
    
    directory = Path(folder_path)

    directory.mkdir(parents=True, exist_ok=True)
  
    unique_id = uuid.uuid4().hex[:6]

    if file_name.endswith(".json"):
        file_name = file_name[:-5]

    full_path = directory / f"{file_name}_{unique_id}.json"

    serializable_data = to_jsonable_python(data)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(serializable_data, f, indent=2, ensure_ascii=False)