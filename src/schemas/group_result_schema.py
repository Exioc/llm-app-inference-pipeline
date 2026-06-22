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

class SingleFeatureGroupsResult(BaseModel):
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
        description="Which model was used to perform the inference "
    )

    inferences: List[GroupInference] = Field(
        default_factory=list,
        description=(
            "The detailed Android permission group inferences for this feature. "
            "Initialized as an empty list, filled with rich metadata (reasoning, quotes) by the filter node."
        )
    )

class PermissionGroupsResult(BaseModel):
    features: List[PermissionGroupsContainer]