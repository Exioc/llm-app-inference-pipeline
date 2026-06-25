from datetime import datetime
from pathlib import Path

from src.config.config import RESULTS_BASE_DIR

def initialize_run_folder(path=None) -> str:
    if path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = RESULTS_BASE_DIR / timestamp
    else: 
        run_dir = Path(path)
    run_dir.mkdir(parents=True, exist_ok=True)
    return str(run_dir)