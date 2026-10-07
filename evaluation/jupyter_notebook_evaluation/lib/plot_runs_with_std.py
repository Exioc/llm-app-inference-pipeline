import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, List

# Global styling for a clean, academic look
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 9

def plot_runs_with_std(
    metrics_list: List[dict], 
    targets_to_compare: List[str], 
    output_dir: Optional[str] = None, 
    file_format: str = "png"
) -> None:
    """
    Creates a side-by-side bar plot for Precision, Recall, and F1.
    If standard deviations (_std) are provided, they are plotted as error bars.
    """
    
    extracted_data = []
    
    # 1. Extract data based on the requested target list
    for target in targets_to_compare:
        entry = next((item for item in metrics_list if item.get("compare") == target), None)
        
        if entry:
            extracted_data.append({
                "label": entry.get("label_gt_pred", target), 
                "precision": entry.get("precision_samples", 0.0),
                "precision_std": entry.get("precision_std", 0.0),
                "recall": entry.get("recall_samples", 0.0),
                "recall_std": entry.get("recall_std", 0.0),
                "f1": entry.get("f1_samples", 0.0),
                "f1_std": entry.get("f1_std", 0.0),
            })
        else:
            print(f"Warning: Dataset '{target}' was not found in the list.")

    if not extracted_data:
        print("No valid data found to plot.")
        return

    # 2. Prepare axis labels and values (Convert to percentages)
    x_labels = [data["label"] for data in extracted_data]
    
    precision_vals = [data["precision"] * 100 for data in extracted_data]
    precision_stds = [data["precision_std"] * 100 for data in extracted_data]
    
    recall_vals = [data["recall"] * 100 for data in extracted_data]
    recall_stds = [data["recall_std"] * 100 for data in extracted_data]
    
    f1_vals = [data["f1"] * 100 for data in extracted_data]
    f1_stds = [data["f1_std"] * 100 for data in extracted_data]

    # Exact colors from the template
    colors = {
        "Precision": "#2B4C7E",
        "Recall": "#4682B4",
        "F1-Score": "#5A9EAF",
    }

    x = np.arange(len(x_labels))
    width = 0.22

    # Compact figsize for a clean 2-item comparison
    fig, ax = plt.subplots(figsize=(6.3, 4.0), dpi=300)

    # Helper function to convert 0.0 standard deviations to np.nan
    # This prevents Matplotlib from drawing error bar caps for single runs
    def get_yerr(stds):
        return [np.nan if std == 0.0 else std for std in stds]

    error_kw = dict(ecolor='black', capsize=3, elinewidth=1, markeredgewidth=1)

    # Use the helper function `get_yerr` for the yerr parameter
    rects1 = ax.bar(x - width, precision_vals, width, yerr=get_yerr(precision_stds), label="Precision", color=colors["Precision"], error_kw=error_kw)
    rects2 = ax.bar(x, recall_vals, width, yerr=get_yerr(recall_stds), label="Recall", color=colors["Recall"], error_kw=error_kw)
    rects3 = ax.bar(x + width, f1_vals, width, yerr=get_yerr(f1_stds), label="F1-Score", color=colors["F1-Score"], error_kw=error_kw)

    # Axis styling
    ax.set_ylabel("Metric Value (%)", fontweight="bold", labelpad=12)
    ax.set_xlabel("Number of pipeline runs", fontweight="bold", labelpad=12)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=9.5)
    
    # Adjust Y-limit and ticks for percentage display
    ax.set_ylim(0, 115) 
    ax.set_yticks(np.arange(0, 101, 20))

    # Place grid behind the bars
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Position legend outside the plot
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.04, 1.0),
        borderaxespad=0,
        frameon=True,
        facecolor="#FFFFFF",
        edgecolor="#DDDDDD",
    )

    # Display percentage values - height is extended by std to place text ABOVE the error bar
    def autolabel(rects, stds):
        for rect, std in zip(rects, stds):
            height = rect.get_height()
            # Text is placed at (bar height + standard deviation). 
            # We use the original `stds` list here, so 0.0 does not break the math.
            ax.annotate(
                f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height + std),
                xytext=(0, 4), # Shifted slightly upwards
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold" 
            )

    autolabel(rects1, precision_stds)
    autolabel(rects2, recall_stds)
    autolabel(rects3, f1_stds)

    plt.tight_layout()
    
    # Save the figure securely with high resolution if an output directory is provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / f"runs_comparison_std_waze.{file_format}"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Display the plot
    plt.show() 
    
    # Close the figure to free up memory
    plt.close(fig)