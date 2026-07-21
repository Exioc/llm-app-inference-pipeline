from datetime import datetime
from pathlib import Path

from src.config.config import RESULTS_BASE_DIR

def initialize_run_folder(path=None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if path is None:
        run_dir = RESULTS_BASE_DIR / timestamp

    elif isinstance(path, str):
        name = path.strip().replace(" ", "_").lower()
        run_dir = RESULTS_BASE_DIR / f"{timestamp}_{name}"

    else:
        run_dir = Path(path)

    run_dir.mkdir(parents=True, exist_ok=True)
    return str(run_dir)