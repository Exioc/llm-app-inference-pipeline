import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

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

def calculate_samples_with_std(runs: list, key_true: str, key_pred: str) -> dict:
    """
    Calculates precision, recall, and F1 score specifically for the ‘samples’ metric,
    including the respective standard deviation across all pipeline runs.
    Returns native Python floats.
    """
    # Extract lists and convert them to sets
    truths = [set(run[key_true]) for run in runs]
    preds  = [set(run[key_pred]) for run in runs]

    # Customize MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    mlb.fit(truths + preds)

    # Convert Sets to Binary Matrices
    y_true = mlb.transform(truths)
    y_pred = mlb.transform(preds)

    # Calculate True Positives (TP), False Positives (FP) and False Negatives (FN) per sample
    tp = np.sum(y_true & y_pred, axis=1)
    fp = np.sum((~y_true) & y_pred, axis=1)
    fn = np.sum(y_true & (~y_pred), axis=1)

    # Calculate metrics per sample (handle division by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        precision_per_sample = np.where(tp + fp == 0, 0.0, tp / (tp + fp))
        recall_per_sample = np.where(tp + fn == 0, 0.0, tp / (tp + fn))
        f1_per_sample = np.where(
            precision_per_sample + recall_per_sample == 0, 
            0.0, 
            2 * (precision_per_sample * recall_per_sample) / (precision_per_sample + recall_per_sample)
        )

    # Calculate mean and standard deviation
    metrics_results = {
       "compare": get_file_name(key_true, key_pred),
       "label_gt_pred": get_comparison_name(key_true, key_pred),
       
       "precision_samples": float(np.mean(precision_per_sample)),
       "precision_std": float(np.std(precision_per_sample,ddof=1)),
       
       "recall_samples": float(np.mean(recall_per_sample)),
       "recall_std": float(np.std(recall_per_sample,ddof=1)),
       
       "f1_samples": float(np.mean(f1_per_sample)),
       "f1_std": float(np.std(f1_per_sample,ddof=1))
    }

    return metrics_results