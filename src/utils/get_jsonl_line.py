import json
from pathlib import Path

def get_jsonl_line(file_path: str, line_number: int):
    """Liest eine spezifische Zeile aus einer JSONL-Datei."""
    path = Path(file_path)
    
    if not path.exists():
        print(f"Fehler: Die Datei {file_path} wurde nicht gefunden.")
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i+1 == line_number:
                    return json.loads(line)
        
        print(f"Fehler: Zeile {line_number} existiert nicht in der Datei.")
        return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None