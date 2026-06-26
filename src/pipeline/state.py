from typing import TypedDict, Dict, List, Annotated

from src.schemas.app_data import AppMetadata
from src.schemas.group_result import PermissionGroupsAggregateResult, PermissionGroupsResult
from src.schemas.func_result import FunctionalityResult

def merge_permission_results(left: PermissionGroupsResult, right: PermissionGroupsResult) -> PermissionGroupsResult:
    if not left: return right
    if not right: return left
    
    combined_features = left.features + right.features
    
    return PermissionGroupsResult(features=combined_features)

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Storage path
    storage_path: str

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str
    permissions_map: Dict[str, List[str]]

    # Results from functionality extraction 
    functionality_result: FunctionalityResult

    # Result from group permission filter
    group_permissions_result: Annotated[PermissionGroupsResult, merge_permission_results]

    # Aggregation of permission groups
    permission_groups_aggregate_result: PermissionGroupsAggregateResult
