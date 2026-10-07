import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path
from typing import Optional

# Global styling matching previous plots
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10

def plot_permission_counts(
    permission_counts: dict, 
    output_dir: Optional[str] = None, 
    file_format: str = "png"
) -> None:
    """
    Plots a vertical bar chart of permission counts, sorted descending.
    The width of the plot adjusts dynamically based on the number of permissions.
    """
    # Sort the dictionary by count in descending order
    sorted_items = sorted(permission_counts.items(), key=lambda item: item[1], reverse=True)
    permissions = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    if not permissions:
        return

    # Dynamic figure width to accommodate all bars comfortably
    fig_width = max(10.0, len(permissions) * 0.35)
    
    fig, ax = plt.subplots(figsize=(fig_width, 6.0), dpi=150)

    # Create vertical bars
    bars = ax.bar(permissions, counts, color="#4682B4", width=0.7, zorder=3)
    
    # Reduce the empty space on the left and right margins tightly to the bars
    ax.margins(x=0.01)

    # Axis styling (swapped from horizontal)
    ax.set_ylabel("Total Permission Count", fontweight="bold", labelpad=12)
    ax.set_xlabel("Permission", fontweight="bold", labelpad=12)
    
    # Add padding to the top for the text labels
    max_count = max(counts)
    ax.set_ylim(0, max_count + (max_count * 0.15))

    # Force y-axis to only show integer values
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Rotate x-axis labels by 45 degrees so the long permission names are readable
    ax.set_xticks(range(len(permissions)))
    ax.set_xticklabels(permissions, rotation=45, ha="right", fontsize=8.5)

    # Place a subtle grid behind the bars (now on the Y-axis)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Display the exact count value on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),  # 6 points vertical offset upwards
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    plt.tight_layout()
    
    # Save the figure securely with high resolution (300 DPI)
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / f"apk_permission_counts.{file_format}"
        plt.savefig(file_path, bbox_inches="tight", dpi=300)
    
    # Display the plot in the notebook
    plt.show() 
    
    # Close the figure to free up memory
    plt.close(fig)