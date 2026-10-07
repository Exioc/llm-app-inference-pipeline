from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, precision_score, recall_score

def get_comparison_name(true_key: str, pred_key: str) -> str:
    """
    Translates the internal keys into readable labels
    (e.g., for plots or tables).
    """

    name_mapping = {
        "apk_permissions": "APK",
        "permissions_set_1": "Set 1",
        "permissions_set_2": "Set 2",
        "inferred_permissions": "Pipeline"
    }
    
    name1 = name_mapping.get(true_key, true_key)
    name2 = name_mapping.get(pred_key, pred_key)
    
    return f"{name1} / {name2}"

def get_file_name(true_key: str, pred_key: str) -> str:
    """
    Converts internal keys to readable names
    """

    name_mapping = {
        "apk_permissions": "APK",
        "permissions_set_1": "Set 1",
        "permissions_set_2": "Set 2",
        "inferred_permissions": "Pipeline"
    }
    
    name1 = name_mapping.get(true_key, true_key)
    name2 = name_mapping.get(pred_key, pred_key)

    return f"{name1}_{name2}".replace(" ", "").lower()

def calculate_micro_macro_samples(runs: list, key_true: str, key_pred: str) -> dict:
    """
    Calculates Precision, Recall, and F1-scores (Micro, Macro, Samples) 
    for multi-label classification.
    """
    # Extract lists and convert them to sets to ignore duplicate permissions
    truths = [set(run[key_true]) for run in runs]
    preds  = [set(run[key_pred]) for run in runs]

    # Fit MultiLabelBinarizer on both to capture the complete label space
    mlb = MultiLabelBinarizer()
    mlb.fit(truths + preds)

    # Transform sets into binary matrices
    y_true = mlb.transform(truths)
    y_pred = mlb.transform(preds)

    # Initialize results dictionary with the found classes
    metrics_results = {
        #'classes': list(mlb.classes_)
       "compare": f"{get_file_name(key_true,key_pred)}",
       "label_gt_pred": f"{get_comparison_name(key_true,key_pred)}"
    }

    # Calculate metrics for each average type dynamically
    for avg in ['micro', 'macro', 'samples']:
        metrics_results[f'precision_{avg}'] = precision_score(y_true, y_pred, average=avg, zero_division=0)
        metrics_results[f'recall_{avg}']    = recall_score(y_true, y_pred, average=avg, zero_division=0)
        metrics_results[f'f1_{avg}']        = f1_score(y_true, y_pred, average=avg, zero_division=0)

    return metrics_results