import json
from pathlib import Path

# Read a specific line from a JSONL file
def get_jsonl_line(file_path: str, line_number: int):
    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: The file {file_path} was not found.")
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i + 1 == line_number:
                    return json.loads(line)
        
        print(f"Error: Line {line_number} does not exist in the file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None