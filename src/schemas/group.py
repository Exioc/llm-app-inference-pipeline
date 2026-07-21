from pydantic import BaseModel, Field, AliasChoices
from typing import List, Optional

class GroupInference(BaseModel):
    group_name: str = Field(
        description="The exact name of the Android permission group (e.g. CAMERA, STORAGE) or 'NONE'."
    )
    reasoning: str = Field(
        default="No permission required.",
        description="Logical explanation for the group. If group_name is 'NONE', write 'No permission required.'"
    )

class GroupResponse(BaseModel):
    inferences: List[GroupInference] = Field(
        description="List of inferred permission groups with reasoning."
    )

class FeatureGroups(BaseModel):
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

class FeatureGroupsResult(BaseModel):
    features: List[FeatureGroups]


# Aggregation (Groupname and Reasoning from GroupInference)
class GroupInferenceAggregate(GroupInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this group."
    )

class FeatureGroupsAggregate(BaseModel):
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

class FeatureGroupsAggregateResult(BaseModel):
    total_number_of_groups: int = Field(
        description="Total number of groups found"
    )
    features: List[FeatureGroupsAggregate]