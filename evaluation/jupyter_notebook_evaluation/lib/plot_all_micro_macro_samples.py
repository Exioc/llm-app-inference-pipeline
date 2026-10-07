import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional

# Global styling for a clean, academic look
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 9

def plot_all_micro_macro_samples(metrics_list: list, output_dir: Optional[str] = None, file_format: str = "png") -> None:
    """
    Generates a single grouped bar plot comparing Micro, Macro, and Samples F1-Scores 
    across all evaluation pairs in the provided list.
    """
    # Extract labels and data arrays from the list of dictionaries
    x_labels = [entry.get("label_gt_pred", "Unknown") for entry in metrics_list]
    
    micro_vals = [entry.get("f1_micro", 0.0) for entry in metrics_list]
    macro_vals = [entry.get("f1_macro", 0.0) for entry in metrics_list]
    samples_vals = [entry.get("f1_samples", 0.0) for entry in metrics_list]

    # Setup the x-axis locations and bar width
    x = np.arange(len(x_labels))
    width = 0.20

    # Colors matched to the requested theme
    colors = {
        "Micro": "#2B4C7E",
        "Macro": "#4682B4",
        "Samples": "#5A9EAF",
    }

    # Initialize a wide figure with 150 DPI for a clean, non-oversized display in Jupyter
    fig, ax = plt.subplots(figsize=(14.0, 4.5), dpi=150)

    # Plot the three sets of grouped bars
    rects1 = ax.bar(x - width, micro_vals, width, label="Micro F1", color=colors["Micro"])
    rects2 = ax.bar(x, macro_vals, width, label="Macro F1", color=colors["Macro"])
    rects3 = ax.bar(x + width, samples_vals, width, label="Samples F1", color=colors["Samples"])

    # Axis styling
    ax.set_ylabel("F1-Score (0.0 - 1.0)", fontweight="bold", labelpad=12)
    ax.set_xlabel("Evaluation Pairs (Ground Truth / Expected)", fontweight="bold", labelpad=12)
    
    # Configure x-ticks
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=9.5)
    
    # Expand y-limit to leave room for percentage labels above the bars
    ax.set_ylim(0, 1.35)

    # Place a subtle grid behind the bars
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Position the legend outside the plot area
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        borderaxespad=0,
        frameon=True,
        facecolor="#FFFFFF",
        edgecolor="#DDDDDD",
    )

    # Display percentage values slightly above each bar
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height * 100:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 6), # 6 points vertical offset
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
    
    # Save the figure securely with high resolution (300 DPI) if a directory is provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / f"f1_score_summary.{file_format}"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Render the plot inline for Jupyter Notebooks
    plt.show()
    
    # Release memory
    plt.close(fig)