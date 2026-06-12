from pydantic import BaseModel, Field
from typing import List

class PermissionGroupsContainer(BaseModel):
    title: str = Field(
        description="The distinct English name of the extracted app feature."
    )
    description: str = Field(
        description="The detailed, multi-sentence description of what the feature does."
    )
    groups: List[str] = Field(
        default_factory=list, 
        description=(
            "The inferred Android permission groups required for this feature "
            "(e.g., STORAGE, CAMERA, LOCATION). Initialized as empty, filled by the filter node."
        )
    )

class PermissionGroupsResult(BaseModel):
    features: List[PermissionGroupsContainer]

class SingleFeatureGroups(BaseModel):
    groups: List[str] = Field(
        description=(
            "Select the relevant Android permission categories for this specific feature. "
            "Options: [STORAGE, CAMERA, LOCATION, NETWORK, AUDIO, CONTACTS]. "
            "If no permissions are required, return ['NONE']."
        )
    )