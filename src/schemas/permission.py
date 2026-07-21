from pydantic import BaseModel, Field
from typing import List, Optional

class PermissionInference(BaseModel):
    permission_name: str = Field(
        description="The exact name of the Android permission (e.g. CAMERA, RECORD_AUDIO) or 'NONE'."
    )
    reasoning: str = Field(
        default="No permission required.",
        description="Logical explanation for the permission. If permission_name is 'NONE', write 'No permission required.'"
    )

class PermissionResponse(BaseModel):
    inferences: List[PermissionInference] = Field(
        description="List of inferred permissions with reasoning."
    )

class FeaturePermission(BaseModel):
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

class FeaturePermissionResult(BaseModel):
    features: List[FeaturePermission] = Field(
        description="The list of extracted app features containing their finalized Android permission inferences."
    )

# Aggregation (Groupname and Reasoning from GroupInference)
class PermissionInferenceAggregate(PermissionInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this permission."
    )

class FeaturePermissionAggregate(BaseModel):
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

class FeaturePermissionAggregateResult(BaseModel):
    features: List[FeaturePermissionAggregate]