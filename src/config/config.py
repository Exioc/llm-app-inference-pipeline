import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Make default results directory and "unknown_run" subdir if not exist
RESULTS_BASE_DIR = Path("results")
UNKNOWN_RUN_DIR = RESULTS_BASE_DIR / "unknown_run"

RESULTS_BASE_DIR.mkdir(parents=True, exist_ok=True)
UNKNOWN_RUN_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
TEMPERATURE = float(os.getenv("TEMPERATURE", "1.0"))