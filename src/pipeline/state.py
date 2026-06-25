from typing import TypedDict, Dict, Optional, List, Any, Annotated

from src.schemas.app_data_schema import AppMetadata
from src.schemas.group_result_schema import PermissionGroupsAggregateResult, PermissionGroupsResult
from src.schemas.func_result_schema import FunctionalityResult


def merge_permission_results(left: PermissionGroupsResult, right: PermissionGroupsResult) -> PermissionGroupsResult:
    if not left: return right
    if not right: return left
    
    combined_features = left.features + right.features
    
    return PermissionGroupsResult(features=combined_features)

def take_last_reducer(left: str, right: str) -> str:
    return "EMPTY"

def take_any_index_reducer(left: int | None, right: int | None) -> int:
    return 0

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]]

    # Results from functionality extraction 
    functionality_result: FunctionalityResult
    number_of_features: int

    # Result from group permission filter
    group_permissions_result: Annotated[PermissionGroupsResult, merge_permission_results]

    # Execution config
    llm_model: str
    temperature: float
    storage_path: str

    current_llm_model: Annotated[str, take_last_reducer]
    current_feature_index: Annotated[int, take_any_index_reducer]
    final_aggregated_result: list
    permission_groups_aggregate_result: PermissionGroupsAggregateResult
