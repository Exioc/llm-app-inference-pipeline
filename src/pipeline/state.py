from typing import TypedDict, Dict, Optional, List, Any
from pydantic import BaseModel, Field

from src.schemas.app_data_schema import AppMetadata
from src.schemas.group_result_schema import PermissionGroupsResult
from src.schemas.func_result_schema import FunctionalityResult

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]] = Field(default_factory=dict)

    # Results from functionality extraction 
    functionality_result: FunctionalityResult
    number_of_features: int

    # Result from group permission filter
    group_permissions_result: PermissionGroupsResult
    current_group_index: int

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str
    subdirectory_path: str
