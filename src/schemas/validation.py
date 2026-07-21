from typing import TypedDict, List

class MetricData(TypedDict):
    total_predicted: int
    total_ground_truth: int
    true_positives: int
    false_positives: int
    false_negatives: int
    precision: str
    recall: str
    f1_score: str

class ComparisonRow(TypedDict):
    permission: str
    truth: bool
    inference: bool

class ValidationResults(TypedDict):
    metrics: MetricData
    comparison: List[ComparisonRow]