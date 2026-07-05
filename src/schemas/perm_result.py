from pydantic import BaseModel, Field
from typing import List, Optional

class PermissionInference(BaseModel):
    permission_name: Optional[str] = Field(
        default=None,
        description=(
            "The exact name of the Android permission inferred from the allowed context (e.g., CAMERA, RECORD_AUDIO). "
            "If the feature requires NO permissions at all, set this field strictly to 'NONE'."
        )
    )
    reasoning: Optional[str] = Field(
        default=None,
        description=(
            "A concise, logical explanation proving why this specific permission is assumed to be necessary. "
            "If the permission_name is 'NONE' (no permissions needed), set this field strictly to null."
        )
    )

class SingleFeaturePermissionsOutput(BaseModel):
    inferences: List[PermissionInference] = Field(
        description=(
            "A list containing each inferred permission along with its logical reasoning. "
            "If the feature requires NO permissions, return exactly ONE entry where permission_name is 'NONE' and reasoning is null."
        )
    )

class PermissionsContainer(BaseModel):
    title: str = Field(
        description="The distinct English name of the extracted app feature."
    )
    description: str = Field(
        description="The detailed, multi-sentence description of what the feature does."
    )
    inferred_by_model: str = Field(
        description="The name of the LLM model used to perform the inference."
    )
    group_name: str = Field(
        description="The name of the Android permission group being analyzed."
    )
    inferences: List[PermissionInference] = Field(
        default_factory=list,
        description=(
            "The detailed Android permission inferences for this feature. "
            "Initialized as an empty list and filled with metadata including reasoning models by the inference node."
        )
    )

class PermissionsResult(BaseModel):
    tmp_model: Optional[str] = Field(
        default=None,
        description="Temporary holder for the specific LLM model name assigned to this parallel execution branch."
    )
    tmp_feature_idx: Optional[int] = Field(
        default=None,
        description="Temporary zero-based index pointing to the exact feature array element processed by this task."
    )
    tmp_group_name: Optional[str] = Field(
        default=None,
        description="Temporary holder for the specific Android permission group name processed by this task branch."
    )
    features: List[PermissionsContainer] = Field(
        description="The list of extracted app features containing their finalized Android permission inferences."
    )

# Aggregation (Groupname and Reasoning from GroupInference)
class PermissionInferenceAggregate(PermissionInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this permission."
    )

class PermissionAggregateContainer(BaseModel):
    title: str = Field(
        description="The distinct English name of the extracted app feature."
    )
    description: str = Field(
        description="The detailed, multi-sentence description of what the feature does."
    )

    inferences: List[PermissionInferenceAggregate] = Field(
        default_factory=list,
        description=(
            "Contains all Android permissions inferred for this feature, together with metadata including reasoning and the LLM models that contributed to each inference." 
            "Empty if no permission were inferred."
        )
    )

class PermissionAggregateResult(BaseModel):
    features: List[PermissionAggregateContainer]