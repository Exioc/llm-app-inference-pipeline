from pydantic import BaseModel, Field
from typing import List

# Structured output model for a single extracted feature
class Feature(BaseModel):
    title: str = Field(
        description="A clear, meaningful, and distinct name for the extracted feature in English."
    )
    description: str = Field(
        description=(
            "A highly detailed, comprehensive English description of what the feature does, "
            "including its full scope, limitations, restrictions, and specific conditions mentioned in the text."
        )
    )
    reasoning: str = Field(
        description=(
            "A concise explanation proving why this feature exists by connecting one or multiple clues "
            "from the text. Aggregated Deduction Rule: Compile all relevant observations (Fact 1, Fact 2, ..., Fact N) "
            "to justify your conclusion. This proof must be either:\n"
            "1. DIRECT EVIDENCE: Show how the combination of explicit text mentions directly yields the feature.\n"
            "2. LOGICAL INFERENCE: Show how multiple indirect contextual facts logically interlock to imply the "
            "unspoken feature (e.g., Fact 1: 'stay in touch' + Fact 2: 'share images' -> infers a multimedia messaging tool exists).\n"
            "Do not invent underlying software architecture, APIs, or unmentioned technical components. "
            "Focus strictly on mapping the documented facts to the feature's existence."
        )
    )
    source_quotes: List[str] = Field(
        description=(
            "A list of the original, unaltered sentences from the text that served as the basis or context for this extraction."
        )
    )

# Structured output model for the LLM response
class FeatureResponse(BaseModel):
    features: List[Feature] = Field(
        description=(
            "List of all extracted features. Granularity rule: Bundle sub-features that belong together "
            "and cannot stand alone (e.g., chat messaging + typing indicators). Isolate into a separate feature "
            "ONLY if a completely distinct capability or unique interaction method (e.g., voice/video calling) "
            "is introduced."
        )
    )

# Structured output model for the final result of feature extraction
class FeatureResult(BaseModel):
    inferred_by_model: str = Field(
        description="Which model was used to perform the inference "
    )
    number_of_features: int = Field(
        description="Number of features found"
    )
    features: List[Feature] = Field(
        description=(
            "List of all extracted features. Granularity rule: Bundle sub-features that belong together "
            "and cannot stand alone (e.g., chat messaging + typing indicators). Isolate into a separate feature "
            "ONLY if a completely distinct capability or unique interaction method (e.g., voice/video calling) "
            "is introduced."
        )
    )