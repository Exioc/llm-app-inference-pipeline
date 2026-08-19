import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

from src.schemas.permission_set import PermissionCatalog
from src.schemas.data_types_mapping import PermissionDataTypeMappingList
from src.schemas.permission_mapping import AndroidPermissionsModel
from src.schemas.android_data import PermissionGroupSummaries, PermissionGroupCollection

load_dotenv()

DIR = Path(__file__).resolve().parent.parent

#Paths
PERMISSION_GROUPS_PATH = Path(DIR /"data/permission_groups_v3.json")
PERMISSIONS_PATH = Path(DIR /"data/permissions_v3.json")
PERMISSIONS_MAPPING_PATH = Path(DIR /"data/permissions_mapping.json")
DATA_TYPES_MAPPING_PATH = Path(DIR /"data/permission_data_types_mapping.json")
LLM_FEATURE_CONFIG_PATH = Path(DIR /"config/presets/llm_feature_config.json")
LLM_GROUP_CONFIG_PATH = Path(DIR /"config/presets/llm_group_config.json")
LLM_PERMISSION_CONFIG_PATH = Path(DIR /"config/presets/llm_permission_config.json")
RESULTS_BASE_DIR = Path("results")
UNKNOWN_RUN_DIR = RESULTS_BASE_DIR / "unknown_run"

# Make sure the results and unknown_run directories exist
RESULTS_BASE_DIR.mkdir(parents=True, exist_ok=True)
UNKNOWN_RUN_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")

class ExcludeHTTPXFilter(logging.Filter):
    # Filter out any log messages originating from the 'httpx' library.
    def filter(self, record: logging.LogRecord) -> bool:
        # Return False to drop the log, True to let it pass
        return "httpx" not in record.name

def setup_logging():
    # Path and name for the log file
    log_dir = Path("logs")
    log_file = log_dir / "pipeline.log"
    
    # creates missing folders
    log_dir.mkdir(parents=True, exist_ok=True)

    # Define the visual look of the log output
    log_format = "%(asctime)s - %(levelname)s - [%(name)s:%(lineno)d] - %(message)s"
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.addFilter(ExcludeHTTPXFilter())
    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    # Configure the root logger that all sub-loggers will inherit from
    logging.basicConfig(
        level=logging.INFO,            
        format=log_format,
        handlers=[console_handler, file_handler]
    )

    try:
        from androguard.util import set_log
        set_log("INFO")
    except ImportError:
        pass
    
    logging.info("Logging infrastructure successfully initialized.")

def load_permission_groups() -> PermissionGroupSummaries:
    if not PERMISSION_GROUPS_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSION_GROUPS_PATH}")
    else:         
        with open(PERMISSION_GROUPS_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return PermissionGroupSummaries(groups=raw_data)

def load_permissions() -> PermissionGroupCollection:
    if not PERMISSIONS_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSIONS_PATH}")
    else:         
        with open(PERMISSIONS_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return PermissionGroupCollection(groups=raw_data)

def load_llm_config(path: Path) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("models", [])

# Mapped playstore labels to real android permission names 
def load_permissions_mapping() -> AndroidPermissionsModel:
    if not PERMISSIONS_MAPPING_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSIONS_MAPPING_PATH}")

    else:
        with open(PERMISSIONS_MAPPING_PATH, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        return AndroidPermissionsModel(**raw_data)

# Mapped android permissions to data types
def load_data_types_mapping() -> PermissionDataTypeMappingList:
    if not DATA_TYPES_MAPPING_PATH.exists():
        raise FileNotFoundError(f"File not found: {DATA_TYPES_MAPPING_PATH}")

    else:
        with open(DATA_TYPES_MAPPING_PATH, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
        return PermissionDataTypeMappingList(mappings=raw_data)

def load_permissions_set() -> PermissionCatalog:
    if not PERMISSIONS_PATH.exists():
        raise FileNotFoundError(f"File not found: {PERMISSIONS_PATH}")
    else:         
        with open(PERMISSIONS_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return PermissionCatalog.model_validate(raw_data)
        
llm_feature_config =  load_llm_config(LLM_FEATURE_CONFIG_PATH)
llm_group_config =  load_llm_config(LLM_GROUP_CONFIG_PATH)
llm_permission_config =  load_llm_config(LLM_PERMISSION_CONFIG_PATH)