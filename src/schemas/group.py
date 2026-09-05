from pydantic import BaseModel, Field, AliasChoices
from typing import List, Optional

# Structured output model for a single inferred permission group
class GroupInference(BaseModel):
    group_name: str = Field(
        description="The exact name of the Android permission group (e.g. CAMERA, STORAGE) or 'NONE'."
    )
    reasoning: str = Field(
        default="No permission required.",
        description="Logical explanation for the group. If group_name is 'NONE', write 'No permission required.'"
    )

# Structured output model for the LLM response
class GroupResponse(BaseModel):
    inferences: List[GroupInference] = Field(
        description="List of inferred permission groups with reasoning."
    )

# Structured output model that combines the feature and its inferred permission groups
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

# Structured output model for the final result of group extraction
class FeatureGroupsResult(BaseModel):
    features: List[FeatureGroups]


# Structured output model that combines the groupname and reasoning from GroupInference with the LLM models that inferred it
class GroupInferenceAggregate(GroupInference):
    models_inferred: List[str] = Field(
        default_factory=list,
        description="List of all LLM model names that inferred this group."
    )

# Structured output model that combines the feature, the groupname and reasoning and the LLM models that inferred it
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

# Structured output model for the final result of feature group extraction with aggregated group inferences
class FeatureGroupsAggregateResult(BaseModel):
    total_number_of_groups: int = Field(
        description="Total number of groups found"
    )
    features: List[FeatureGroupsAggregate]