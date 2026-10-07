import json
from pathlib import Path
from typing import List, Dict, Any

def extract_all_set_collection(search_dir: Path) -> List[Dict[str, Any]]:
    """
    Searches for '06_validation.json' and extracts 'set_collection'.
    Uses the parent directory name as a unique identifier.
    """
    search_dir = Path(search_dir)
    extracted_data = []

    for file_path in search_dir.rglob('06_validation.json'):
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        if 'set_collection' in data:
            extracted_data.append({
                'folder_name': file_path.parent.name,
                'set_collection_data': data['set_collection']
            })

    return extracted_data