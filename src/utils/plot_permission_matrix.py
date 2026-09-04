import os
import re
from typing import Iterable, Optional
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10

def plot_permission_matrix(
    ground_truth: Iterable[str],
    prediction: Iterable[str],
    ground_truth_name: str = 'Ground Truth',
    prediction_name: str = 'Inferred Model',
    output_dir: str = '.',
    use_abbreviations: bool = True,
    filename_override: Optional[str] = None,
) -> None:
   
    gt_set = set(ground_truth)
    pred_set = set(prediction)

    if filename_override:
        filename = filename_override
    else:
        clean_gt = re.sub(r'[^\w\-]', '_', ground_truth_name.lower())
        clean_pred = re.sub(r'[^\w\-]', '_', prediction_name.lower())
        filename = f'permission_matrix_{clean_gt}_vs_{clean_pred}.png'

    os.makedirs(output_dir, exist_ok=True)
    full_save_path = os.path.join(output_dir, filename)

    all_permissions = sorted(list(gt_set.union(pred_set)), reverse=True)

    matrix_vals = []
    matrix_labels = []

    for perm in all_permissions:
        actual = perm in gt_set
        pred = perm in pred_set

        if actual and pred:
            eval_text = 'TP' if use_abbreviations else 'True Positive'
        elif not actual and not pred:
            eval_text = 'TN' if use_abbreviations else 'True Negative'
        elif not actual and pred:
            eval_text = 'FP' if use_abbreviations else 'False Positive'
        else:
            eval_text = 'FN' if use_abbreviations else 'False Negative'

        gt_text = 'Present' if actual else 'Absent'
        pred_text = 'Present' if pred else 'Absent'

        matrix_vals.append([1 if actual else 0, 1 if pred else 0, 0])
        matrix_labels.append([gt_text, pred_text, eval_text])

    matrix_data = np.array(matrix_vals)

    fig_height = max(3.5, len(all_permissions) * 0.45 + 1.0)
    fig, ax = plt.subplots(figsize=(8.0, fig_height), dpi=300)

    cmap = ListedColormap(['#F2F4F7', '#1E3A8A'])
    ax.matshow(matrix_data, cmap=cmap, vmin=0, vmax=1, aspect='auto')

    # Grid Lines
    ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(all_permissions), 1), minor=True)
    ax.grid(which='minor', color='#D1D5DB', linestyle='-', linewidth=1.2)
    ax.tick_params(which='minor', size=0)

    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(
        [ground_truth_name, prediction_name, 'Evaluation'], 
        fontweight='bold', 
        fontsize=10.5
    )
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
   
    ax.set_yticks(range(len(all_permissions)))
    ax.set_yticklabels(all_permissions, fontfamily='monospace', fontsize=9.5)
    ax.set_ylabel(
        'Permission Identifier', 
        fontweight='bold', 
        labelpad=12, 
        fontsize=10.5
    )

    for i in range(len(all_permissions)):
        for j in range(3):
            val = matrix_data[i, j]
            text = matrix_labels[i][j]

            color = '#FFFFFF' if val == 1 else '#1F2937'

            ax.text(
                j,
                i,
                text,
                ha='center',
                va='center',
                color=color,
                fontsize=9.5,
                fontweight='bold',
            )

    plt.tight_layout()
    plt.savefig(full_save_path, bbox_inches='tight')
    plt.close()