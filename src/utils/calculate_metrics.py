def calculate_metrics(ground_truth, predicted):
    gt_set = set(ground_truth)
    pred_set = set(predicted)
    
    tp = len(gt_set & pred_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)
    
    total_pred = len(pred_set)
    total_gt = len(gt_set)
    
    precision = (tp / total_pred) if total_pred > 0 else 0.0
    recall = (tp / total_gt) if total_gt > 0 else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    
    return {
        "total_predicted": total_pred,
        "total_ground_truth": total_gt,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": f"{precision * 100:.2f}%",
        "recall": f"{recall * 100:.2f}%",
        "f1_score": f"{f1 * 100:.2f}%"
    }