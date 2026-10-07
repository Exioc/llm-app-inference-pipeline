import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, precision_score, recall_score

def calculate_per_datatype_f1(comparisons: list, key_truth: str, key_pred: str) -> pd.DataFrame:
    """
    Calculate Precision, Recall, and F1-score for each individual data type.
    Extracts data types nested inside permissions within 'data_types_collection_data'.
    """
    def extract_datatypes(item, key):
        dt_set = set()
        # Navigate into data_types_collection_data and fetch the list (e.g., 'inferred_permissions' or 'apk_permissions')
        permissions_list = item.get("data_types_collection_data", {}).get(key, [])
        for perm in permissions_list:
            for dt in perm.get("data_types", []):
                # Using 'data_type' as the label. 
                # Optional: use f"{dt.get('category')} - {dt.get('data_type')}" if categories need distinction.
                val = dt.get("data_type")
                if val:
                    dt_set.add(val)
        return dt_set

    # Extract the ground truth and predicted data type sets for each comparison item
    truths = [extract_datatypes(c, key_truth) for c in comparisons]
    preds  = [extract_datatypes(c, key_pred)  for c in comparisons]

    # Fit the binarizer on all possible data types from both truths and predictions
    mlb = MultiLabelBinarizer()
    mlb.fit(truths + preds)
    
    # Transform the data type sets into binary matrices
    y_true = mlb.transform(truths)
    y_pred = mlb.transform(preds)

    # Calculate metrics for each individual data type using average=None
    f1_per_label = f1_score(y_true, y_pred, average=None, zero_division=0)
    precision_per_label = precision_score(y_true, y_pred, average=None, zero_division=0)
    recall_per_label = recall_score(y_true, y_pred, average=None, zero_division=0)

    # Calculate support (how often each data type actually occurs in the ground truth)
    support = y_true.sum(axis=0) 

    # Combine everything into a pandas DataFrame
    df = pd.DataFrame({
        "data_type": mlb.classes_,
        "support_truth": support,
        "precision": precision_per_label,
        "recall": recall_per_label,
        "f1": f1_per_label,
    }).sort_values("support_truth", ascending=False).reset_index(drop=True)

    return df