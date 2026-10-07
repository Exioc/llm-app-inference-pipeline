import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, List

# Global styling for a clean, academic look
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 9

def plot_samples_comparison(
    metrics_list: List[dict], 
    targets_to_compare: List[str], 
    output_dir: Optional[str] = None, 
    file_format: str = "png"
) -> None:
    """
    Searches for specific datasets in 'targets_to_compare' and creates 
    a side-by-side bar plot for the sample metrics (Precision, Recall, F1).
    """
    
    extracted_data = []
    
    # Extract data based on the requested target list
    for target in targets_to_compare:
        # Find the matching dictionary using the 'compare' key
        entry = next((item for item in metrics_list if item.get("compare") == target), None)
        
        if entry:
            extracted_data.append({
                "label": entry.get("label_gt_pred", target), # Use readable label if available
                "precision": entry.get("precision_samples", 0.0),
                "recall": entry.get("recall_samples", 0.0),
                "f1": entry.get("f1_samples", 0.0),
            })
        else:
            print(f"Warning: Dataset '{target}' was not found in the list.")

    # Exit if no valid data was found
    if not extracted_data:
        print("No valid data found to plot.")
        return

    # Prepare X-axis labels and values (Direkt in Prozent umwandeln durch * 100)
    x_labels = [data["label"] for data in extracted_data]
    precision_vals = [data["precision"] * 100 for data in extracted_data]
    recall_vals = [data["recall"] * 100 for data in extracted_data]
    f1_vals = [data["f1"] * 100 for data in extracted_data]

    # Exact colors from the template
    colors = {
        "Precision": "#2B4C7E",
        "Recall": "#4682B4",
        "F1-Score": "#5A9EAF",
    }

    x = np.arange(len(x_labels))
    
    # Balanced width so the bars aren't too thick, but gaps aren't huge either
    width = 0.18

    # Tightly pack the clusters: 
    # Base padding of ~2.0 inches (for axes and legend) + 1.2 inches per dataset
    fig, ax = plt.subplots(figsize=(6.3, 4.0), dpi=300)

    # Draw bars
    rects1 = ax.bar(x - width, precision_vals, width, label="Precision", color=colors["Precision"])
    rects2 = ax.bar(x, recall_vals, width, label="Recall", color=colors["Recall"])
    rects3 = ax.bar(x + width, f1_vals, width, label="F1-Score", color=colors["F1-Score"])

    # Axis styling
    ax.set_ylabel("Metric Value (%)", fontweight="bold", labelpad=12)
    ax.set_xlabel("Evaluation Pairs (Ground Truth / Expected)", fontweight="bold", labelpad=12)

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
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold" 
            )

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    
    # Save the figure securely with high resolution if an output directory is provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_name = "_and_".join(targets_to_compare)
        file_path = output_path / f"samples_{file_name}.{file_format}"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Display the plot
    plt.show() 
    
    # Close the figure to free up memory
    plt.close(fig)