import json
from pathlib import Path
from typing import List, Dict, Any

def extract_all_data_types_collection(search_dir: Path) -> List[Dict[str, Any]]:
    """
    Searches for '07_data_types.json' and extracts 'data_types_collection'.
    Uses the parent directory name as a unique identifier.
    """
    search_dir = Path(search_dir)
    extracted_data = []

    for file_path in search_dir.rglob('07_data_types.json'):
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        if 'data_types_collection' in data:
            extracted_data.append({
                'folder_name': file_path.parent.name,
                'data_types_collection_data': data['data_types_collection']
            })

    return extracted_data