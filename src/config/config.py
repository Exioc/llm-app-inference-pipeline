import os
import json
from pathlib import Path

from dotenv import load_dotenv
from src.schemas.driod_data_schema import PermissionGroupList, PermissionGroupDetailList

load_dotenv()

DIR = Path(__file__).resolve().parent.parent

#Paths
PERMISSION_GROUPS_PATH = Path(DIR /"data/permission_groups.json")
PERMISSIONS_BY_GROUP_PATH = Path(DIR /"data/permissions_by_group.json")

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

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")

def load_permission_groups() -> PermissionGroupList:
    if not PERMISSION_GROUPS_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSION_GROUPS_PATH}")
    else:         
        with open(PERMISSION_GROUPS_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return PermissionGroupList(groups=raw_data)

def load_permissions_by_groups() -> PermissionGroupDetailList:
    if not PERMISSIONS_BY_GROUP_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSIONS_BY_GROUP_PATH}")
    else:         
        with open(PERMISSIONS_BY_GROUP_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return PermissionGroupDetailList(groups_details=raw_data)