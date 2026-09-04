from typing import TypedDict, Dict, List, Annotated

from src.schemas.permission_data_types_mapping import PermissionDataTypeMapping
from src.schemas.metrics import metrics
from src.schemas.label_permission_mapping import ProcessedPermissions
from src.schemas.app_data import AppMetadata
from src.schemas.feature import FeatureResult
from src.schemas.permission import FeaturePermissionAggregateResult, FeaturePermissionResult
from src.schemas.group import FeatureGroupsAggregateResult, FeatureGroupsResult

def merge_group_results(left: FeatureGroupsResult, right: FeatureGroupsResult) -> FeatureGroupsResult:
    if not left: return right
    if not right: return left
    
    combined_features = left.features + right.features
    
    return FeatureGroupsResult(features=combined_features)

def merge_permission_results(left: FeaturePermissionResult, right: FeaturePermissionResult) -> FeaturePermissionResult:
    if not left: return right
    if not right: return left
    
    combined_features = left.features + right.features
    
    return FeaturePermissionResult(features=combined_features)

# State for the Pipeline
class PipelineState(TypedDict, total=False):

    # Storage path
    storage_path: str

    # APK path
    apk_path: str

    group_send_idx: int
    permission_send_idx: int

    # Raw input
    metadata: AppMetadata

    # App metadata
    pkg: str
    label: str
    description_long: str

    # LABEL_TO_PERMISSIONS
    # Map labels to permissions 
    #permissions_map: ProcessedPermissions

    # A list of ground truth sets for the app
    ground_truth_sets: List[List[str]]

    # Permission list from manifest file 
    apk_permissions: List[str]

    # Results from functionality extraction 
    feature_result: FeatureResult

    # Result from group permission filter
    feature_groups_result: Annotated[FeatureGroupsResult, merge_group_results]

    # Aggregation of permission groups
    feature_groups_aggregate_result: FeatureGroupsAggregateResult

    # Result from permission filter
    permissions_result: Annotated[FeaturePermissionResult, merge_permission_results]
    
    # Aggregation of permissions
    feature_permission_aggregate_result: FeaturePermissionAggregateResult

    # List of Permission (cleaned)
    inferred_permissions: List[str]

    # Validation
    metrics_collection: dict[str,metrics]
    threshold: dict
    set_collection: dict

    # DataTypes
    data_types_collection: dict[str,list[PermissionDataTypeMapping]]