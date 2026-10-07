# Global styling for a clean, academic look
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10

def plot_precision_recall_by_support_data_types(
    df: pd.DataFrame, 
    top_n_labels: int = 8, 
    save_path: Optional[str] = None
) -> None:
    """
    Plots Precision vs. Recall as a scatter plot.
    The size and color of the points represent the support of the labels.
    """
    # Sweet Spot für Jupyter: Breite 14.0, Höhe 14.0 und scharfe Anzeige (150 DPI)
    fig, ax = plt.subplots(figsize=(8.5, 6.0), dpi=150)

    # Calculate dynamic point sizes based on support
    sizes = 20 + (df["support_truth"] / df["support_truth"].max()) * 400
    
    # Create the scatter plot keeping the visual color gradient
    sc = ax.scatter(
        df["recall"], df["precision"],
        s=sizes, c=df["support_truth"], cmap="viridis",
        edgecolors="black", linewidths=0.6, alpha=0.85, zorder=3
    )

    # Annotate the most reliable/frequent labels using adjustText-Style via standard matplotlib connectionpatch
    top = df.nlargest(top_n_labels, "support_truth")
    
    offsets = [
            (25, 25),   
            (-40, 30),  
            (35, -20),  
            (-50, -25), 
            (20, 40),   
            (-45, 15),  
            (30, -35), 
            (-35, -40)
        ]
    
    for i, (_, row) in enumerate(top.iterrows()):
        offset = offsets[i % len(offsets)]
        ax.annotate(
            row["data_type"], 
            (row["recall"], row["precision"]),
            fontsize=8.5, 
            xytext=offset, 
            textcoords="offset points",
            arrowprops=dict(
                arrowstyle="-|>", 
                color="gray", 
                lw=0.8, 
                alpha=0.7,
                connectionstyle="arc3,rad=0.1"
            ),
            zorder=4
        )

    # Diagonal reference line
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", linewidth=0.8, alpha=0.5, zorder=1)

    # Axis styling
    ax.set_xlabel("Recall (0.0 - 1.0)", fontweight="bold", labelpad=12)
    ax.set_ylabel("Precision (0.0 - 1.0)", fontweight="bold", labelpad=12)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_yticks(np.arange(0, 1.1, 0.1))

    # Place a subtle grid behind the scatter points
    ax.grid(axis="both", linestyle="--", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Colorbar styling
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Support (Occurrences in Ground Truth)", fontweight="bold", labelpad=12)

    plt.tight_layout()
    
    # Save the figure securely with high resolution (300 DPI) if a path is provided
    if save_path:
        out_path = Path(save_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        file_path = out_path / f"scatter_plot_data_types.png"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Display the plot inline
    plt.show()
    
    # Release memory
    plt.close(fig)