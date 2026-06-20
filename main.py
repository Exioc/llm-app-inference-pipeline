import json
import argparse
from pathlib import Path
from datetime import datetime

#from src.pipeline.state import AppMetadata
from src.schemas.app_data_schema import AppMetadata
from src.pipeline.graph import build_app
from src.utils.notify_me import notification
from src.config.config import RESULTS_BASE_DIR, LLM_MODEL, TEMPERATURE, OLLAMA_BASE_URL, OLLAMA_API_KEY, load_permission_groups ,load_permissions_by_groups, LANGSMITH_TRACING

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
def initialize_run_folder(path=None) -> str:
    if path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = RESULTS_BASE_DIR / timestamp
    else: 
        run_dir = Path(path)
    run_dir.mkdir(parents=True, exist_ok=True)
    return str(run_dir)

# Helper-function to save the input
def save_stage(app: AppMetadata, stage_name: str, run_dir: str = "results/unknown_run") -> None:
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    path = run_dir / f"{stage_name}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(app.model_dump(), f, indent=2, ensure_ascii=False)

def main() -> None:
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Liest eine App-Metadaten-Zeile aus einer JSONL-Datei.")
    
    # Define required input arguments
    parser.add_argument("path", type=str, help="Pfad zur .jsonl Datei")
    parser.add_argument("index", type=int, help="Index der Zeile (beginnend bei 0)")

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract the specified line from the JSONL file
    app_data = get_jsonl_line(args.path, args.index)

    # Create a AppMetadata instance from the extracted data
    app_data = AppMetadata(**app_data)

    # Initialize run folder and save input
    storage_path = initialize_run_folder()
    subdirectory_path = initialize_run_folder(storage_path + "/run_group")
    save_stage(app_data, "00_Metadata", storage_path)

    #____________________________________________________________

    permission_groups_model = load_permission_groups()
    permissions_by_group_model = load_permissions_by_groups()

    #____________________________________________________________

    # Build the pipeline
    app = build_app()

    # Input for the pipeline
    initial_input = {
        "metadata": app_data,
        "llm_model": LLM_MODEL,
        "temperature": float(TEMPERATURE),
        "storage_path": storage_path,
        "subdirectory_path": subdirectory_path,
        "current_group_index": 0
    }

    # Start the pipelin
    if LANGSMITH_TRACING == "true": print("tracing is active")
    print(f"Start analyze ({datetime.now().strftime('%H:%M')})")
    final_state = app.invoke(
        initial_input,
        {"configurable": {
            "permission_groups": permission_groups_model,
            "permissions_by_group": permissions_by_group_model
        }}
    )
    print(f"Finish analyze ({datetime.now().strftime('%H:%M')})")
    notification.send()

if __name__ == "__main__":
    main()




