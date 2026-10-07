from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd

def calculate_per_label_f1(comparisons: list, key_truth: str, key_pred: str) -> pd.DataFrame:
    """
    Calculate Precision, Recall, and F1-score for each individual label.
    Using average=None calculates the metrics per class (unaggregated).
    """
    # Extract the ground truth and predicted labels as sets to ignore duplicates
    truths = [set(c[key_truth]) for c in comparisons]
    preds  = [set(c[key_pred])  for c in comparisons]

    # Fit the binarizer on all possible labels from both truths and predictions
    mlb = MultiLabelBinarizer()
    mlb.fit(truths + preds)
    
    # Transform the label sets into binary matrices
    y_true = mlb.transform(truths)
    y_pred = mlb.transform(preds)

    # Calculate metrics for each individual label using average=None
    f1_per_label = f1_score(y_true, y_pred, average=None, zero_division=0)
    precision_per_label = precision_score(y_true, y_pred, average=None, zero_division=0)
    recall_per_label = recall_score(y_true, y_pred, average=None, zero_division=0)

    # Calculate support (how often each label actually occurs in the ground truth)
    support = y_true.sum(axis=0) 

    # Combine everything into a pandas DataFrame for easy viewing and sorting
    df = pd.DataFrame({
        "permission": mlb.classes_,
        "support_truth": support,
        "precision": precision_per_label,
        "recall": recall_per_label,
        "f1": f1_per_label,
    }).sort_values("support_truth", ascending=False).reset_index(drop=True)

    return df