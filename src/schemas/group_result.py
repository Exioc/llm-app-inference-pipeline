from pydantic import BaseModel, Field
from typing import List, Optional

class GroupInference(BaseModel):
    group_name: Optional[str] = Field(
        default=None,
        description=(
            "The exact name of the Android permission group inferred from the allowed context (e.g., CAMERA, STORAGE). "
            "If the feature requires NO permissions at all, set this field strictly to 'NONE'."
        )
    )
    reasoning: Optional[str] = Field(
        default=None,
        description=(
            "A concise, logical explanation proving why this specific permission group is assumed to be necessary. "
            "If the group_name is 'NONE' (no permissions needed), set this field strictly to null."
        )
    )

class SingleFeatureGroupsOutput(BaseModel):
    inferences: List[GroupInference] = Field(
        description=(
            "A list containing each inferred permission group along with its logical reasoning. "
            "If the feature requires NO permissions, return exactly ONE entry where group_name is 'NONE' and reasoning is null."
        )
    )

class PermissionGroupsContainer(BaseModel):
    title: str = Field(
        description="The distinct English name of the extracted app feature."
    )
    description: str = Field(
        description="The detailed, multi-sentence description of what the feature does."
    )

    inferred_by_model: str = Field(
        description="The name of the LLM model used to perform the inference."
    )

    inferences: List[GroupInference] = Field(
        default_factory=list,
        description=(
          "The detailed Android permission group inferences for this feature." 
          "Initialized as an empty list and filled with metadata including reasoning models by the group node."
        )
    )

class PermissionGroupsResult(BaseModel):
    tmp_model: Optional[str] = Field(
        default=None,
        description="Temporary holder for the specific LLM model name assigned to this parallel execution branch."
    )
    tmp_feature_idx: Optional[int] = Field(
        default=None,
        description="Temporary zero-based index pointing to the exact feature array element processed by this task."
    )
    features: List[PermissionGroupsContainer]

# Aggregation (Groupname and Reasoning from GroupInference)
class GroupInferenceAggregate(GroupInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this group."
    )

class PermissionGroupsAggregateContainer(BaseModel):
    title: str = Field(
        description="The distinct English name of the extracted app feature."
    )
    description: str = Field(
        description="The detailed, multi-sentence description of what the feature does."
    )

    inferences: List[GroupInferenceAggregate] = Field(
        default_factory=list,
        description=(
            "Contains all Android permission groups inferred for this feature, together with metadata including reasoning and the LLM models that contributed to each inference." 
            "Empty if no groups were inferred."
        )
    )

class PermissionGroupsAggregateResult(BaseModel):
    total_number_of_groups: int = Field(
        description="Total number of groups found"
    )
    features: List[PermissionGroupsAggregateContainer]