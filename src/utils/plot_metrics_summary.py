import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from src.schemas.metrics import metrics

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

def plot_metrics_summary(
    metrics_list: List[metrics],
    output_dir: str = '.',
    filename: str = 'evaluation_metrics_summary.png'
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    full_save_path = os.path.join(output_dir, filename)

    x_labels = []
    precision_vals = []
    recall_vals = []
    f1_vals = []

    for item in metrics_list:
        gt_name = item.ground_truth or 'GT'
        pred_name = item.prediction or 'Pred'
        x_labels.append(f"{gt_name} / {pred_name}")

        p_str = str(item.precision).replace('%', '')
        r_str = str(item.recall).replace('%', '')
        f_str = str(item.f1_score).replace('%', '')

        precision_vals.append(float(p_str) / 100.0)
        recall_vals.append(float(r_str) / 100.0)
        f1_vals.append(float(f_str) / 100.0)

    x = np.arange(len(x_labels))
    
    width = 0.18  

    fig, ax = plt.subplots(figsize=(max(8.5, len(x_labels) * 3.0), 5.0), dpi=300)

    rects1 = ax.bar(x - width, precision_vals, width, label='Precision', color='#2B4C7E')
    rects2 = ax.bar(x, recall_vals, width, label='Recall', color='#4682B4')
    rects3 = ax.bar(x + width, f1_vals, width, label='F1-Score', color='#5A9EAF')

    ax.set_ylabel('Metric Value (0.0 - 1.0)', fontweight='bold', labelpad=12)
    ax.set_xlabel('Evaluation Pairs (Ground Truth / Inferred Model)', fontweight='bold', labelpad=12)
    
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=9.5, linespacing=1.3)

    ax.set_ylim(0, 1.35)

    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    ax.legend(
        loc='upper left',
        bbox_to_anchor=(1.04, 1.0),
        borderaxespad=0,
        frameon=True,
        facecolor='#FFFFFF',
        edgecolor='#DDDDDD'
    )

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f'{height * 100:.1f}%',
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 6),
                textcoords='offset points',
                ha='center', va='bottom',
                fontsize=8.5, fontweight='bold'
            )

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.savefig(full_save_path, bbox_inches='tight')
    plt.close()