import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional

# Global styling for a clean, academic look
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 9

def plot_micro_macro_samples(metrics_list: list, target_compare: str, output_dir: Optional[str] = None, file_format: str = "png") -> None:
    """
    Finds a specific dictionary in the list based on 'target_compare' and generates a bar plot.
    If output_dir is provided, the plot is saved in high resolution. Otherwise, it is only displayed.
    """
    # Find the target dictionary in the list
    target_entry = None
    for entry in metrics_list:
        if entry.get("compare") == target_compare:
            target_entry = entry
            break
            
    # Exit early if the target string was not found
    if not target_entry:
        return

    # Exact colors from the template
    colors = {
        "Precision": "#2B4C7E",
        "Recall": "#4682B4",
        "F1-Score": "#5A9EAF",
    }

    x_labels = ["Micro", "Macro", "Samples"]
    avg_types = ["micro", "macro", "samples"]
    x = np.arange(len(x_labels))
    width = 0.25

    # Extract filename from the target entry
    file_name = target_entry.get("compare", target_compare)
    
    # Dynamically extract values from the dictionary
    precision_vals = [target_entry.get(f"precision_{avg}", 0.0) * 100 for avg in avg_types]
    recall_vals    = [target_entry.get(f"recall_{avg}", 0.0) * 100 for avg in avg_types]
    f1_vals        = [target_entry.get(f"f1_{avg}", 0.0) * 100 for avg in avg_types]

    # Initialize the figure with 150 DPI for a sharp but reasonably sized display in Jupyter
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=300)

    rects1 = ax.bar(x - width, precision_vals, width, label="Precision", color=colors["Precision"])
    rects2 = ax.bar(x, recall_vals, width, label="Recall", color=colors["Recall"])
    rects3 = ax.bar(x + width, f1_vals, width, label="F1-Score", color=colors["F1-Score"])

    # Axis styling
    ax.set_ylabel("Metric Value (%)", fontweight="bold", labelpad=12)
    ax.set_xlabel("Averaging Method (Micro / Macro / Samples)", fontweight="bold", labelpad=12)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=9.5)
    
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

    # Display percentage values above the bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
            )

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    
    # Save the figure securely with high resolution (300 DPI) if an output directory is provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / f"{file_name}.{file_format}"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Display the plot in the notebook
    plt.show() 
    
    # Close the figure to free up memory
    plt.close(fig)