from pydantic import BaseModel, Field

class metrics(BaseModel):
    total_predicted: int = Field(ge=0)
    total_ground_truth: int = Field(ge=0)
    true_positives: int = Field(ge=0)
    false_positives: int = Field(ge=0)
    false_negatives: int = Field(ge=0)
    precision: str
    recall: str
    f1_score: str
    ground_truth: str
    prediction: str