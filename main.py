import json
import argparse
from pathlib import Path
from datetime import datetime

from src.models.schema import AppBaseModel
from src.chains.pipeline import build_pipeline
from src.config.config import RESULTS_BASE_DIR, LLM_MODEL, TEMPERATURE, OLLAMA_BASE_URL, OLLAMA_API_KEY

# Helper-function to read a specific line from a JSONL file
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

# Helper-function to initialize a run folder for saving results
def initialize_run_folder() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RESULTS_BASE_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return str(run_dir)

# Helper-function to save the input
def save_stage(app: AppBaseModel, stage_name: str, run_dir: str = "results/unknown_run") -> None:
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    path = run_dir / f"{stage_name}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(app.model_dump(), f, indent=2, ensure_ascii=False)

def main() -> None:
    
    # Argument Parser einrichten
    parser = argparse.ArgumentParser(description="Liest eine App-Metadaten-Zeile aus einer JSONL-Datei.")
    
    # Positionale Argumente definieren
    parser.add_argument("path", type=str, help="Pfad zur .jsonl Datei")
    parser.add_argument("index", type=int, help="Index der Zeile (beginnend bei 0)")

    args = parser.parse_args()

    # Extract the specified line from the JSONL file
    app_data = get_jsonl_line(args.path, args.index)

    # Create AppBaseModel instance from the extracted data
    app = AppBaseModel(**app_data)

    # Initialize run folder and save input
    storage_path = initialize_run_folder()
    save_stage(app, "00_Metadata", storage_path)

    # Build the pipeline
    pipeline = build_pipeline()

    # Input for the pipeline
    initial_input = {"app_data": app, "storage_path": storage_path, "llm_model": LLM_MODEL, "temperature": TEMPERATURE}

    # Start the pipeline
    final_state = pipeline.invoke(initial_input)

    # Ausgabe der Ergebnisse
    #print(f"Input: {final_state['label']}")
    #print(f"Stage 1 Log: {final_state['stage1_result']}")
    #print(f"Stage 2 Features: {final_state['stage2_result'].features[0].functionality}")
    #print(f"Stage 3 Log: {final_state['stage3_result']}")

if __name__ == "__main__":
    main()




