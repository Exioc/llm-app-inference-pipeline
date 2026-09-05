from pydantic import BaseModel, Field
from typing import List, Optional

# Structured output model for a single inferred permission
class PermissionInference(BaseModel):
    permission_name: str = Field(
        description="The exact name of the Android permission (e.g. CAMERA, RECORD_AUDIO) or 'NONE'."
    )
    reasoning: str = Field(
        default="No permission required.",
        description="Logical explanation for the permission. If permission_name is 'NONE', write 'No permission required.'"
    )

# Structured output model for the LLM response
class PermissionResponse(BaseModel):
    inferences: List[PermissionInference] = Field(
        description="List of inferred permissions with reasoning."
    )

# Structured output model that combines the feature and its inferred permissions as well as the group name that the permission belongs to
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

# Structured output model for the final result of permission extraction
class FeaturePermissionResult(BaseModel):
    features: List[FeaturePermission] = Field(
        description="The list of extracted app features containing their finalized Android permission inferences."
    )

# Structured output model that combines the permission name and reasoning from PermissionInference with the LLM models that inferred it
class PermissionInferenceAggregate(PermissionInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this permission."
    )

# Structured output model that combines the feature, the permission name and reasoning and the LLM models that inferred it
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

# Structured output model for the final result of feature permission extraction with aggregated permission inferences
class FeaturePermissionAggregateResult(BaseModel):
    features: List[FeaturePermissionAggregate]