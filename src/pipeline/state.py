from typing import TypedDict, Dict, Optional, List, Any, Annotated
from pydantic import BaseModel, Field

from src.schemas.app_data_schema import AppMetadata
from src.schemas.group_result_schema import PermissionGroupsResult
from src.schemas.func_result_schema import FunctionalityResult

import operator

def merge_permission_results(left: PermissionGroupsResult, right: PermissionGroupsResult) -> PermissionGroupsResult:
    """
    Führt die Features von zwei parallelen LLM-Ergebnissen zusammen,
    wenn die Branches am Ende verschmelzen.
    """
    if not left: return right
    if not right: return left
    
    # Wir nehmen die bestehenden Features von 'left' und hängen die von 'right' an
    combined_features = left.features + right.features
    
    # Wir geben ein neues Pydantic-Modell mit allen gesammelten Features zurück
    return PermissionGroupsResult(features=combined_features)

def take_last_reducer(left: str, right: str) -> str:
    return right or left

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
    group_permissions_result: Annotated[PermissionGroupsResult, merge_permission_results]
    current_group_index: int

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str
    subdirectory_path: str

    current_llm_model: Annotated[str, take_last_reducer]
    final_aggregated_result: list
