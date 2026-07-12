"""
Render the Euro-to-World-Cup semifinalist overlap charts as static PNGs
using matplotlib.

Usage:
    python3 analysis/plot_charts.py
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "euro_to_world_cup_semifinalists.json"
OUT_DIR = Path(__file__).resolve().parent.parent / "charts"

SURFACE = "#fcfcfb"
PAGE = "#f9f9f7"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
TEXT_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"
RED = "#d03b3b"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


def load_editions():
    with DATA_PATH.open() as f:
        editions = json.load(f)
    for ed in editions:
        ed["shared"] = sorted(set(ed["euro_semifinalists"]) & set(ed["world_cup_semifinalists"]))
        ed["overlap"] = len(ed["shared"])
    return editions


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(PAGE)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="x", length=0, colors=TEXT_MUTED, labelsize=9)
    ax.tick_params(axis="y", length=0, colors=TEXT_MUTED, labelsize=9)
    ax.yaxis.grid(True, color=GRIDLINE, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    ax.axhline(0, color=BASELINE, linewidth=1, zorder=1)


def plot_by_edition(editions, path):
    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=200)
    style_axes(ax)

    x = range(len(editions))
    colors = [RED if ed["overlap"] == 3 else BLUE for ed in editions]
    bars = ax.bar(x, [ed["overlap"] for ed in editions], width=0.62, color=colors, zorder=3)

    labels = [f"'{str(ed['euro_year'])[2:]}→'{str(ed['world_cup_year'])[2:]}" for ed in editions]
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, 4)

    ax.axhline(2, color=TEXT_MUTED, linewidth=1, linestyle=(0, (3, 3)), zorder=2)

    for i, ed in enumerate(editions):
        if ed["overlap"] > 0:
            ax.text(i, ed["overlap"] + 0.08, str(ed["overlap"]), ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color=TEXT_PRIMARY)

    record_i = next(i for i, ed in enumerate(editions) if ed["overlap"] == 3)
    ax.text(record_i, 3.55, "First-ever 3-team\ncarryover", ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color=RED)

    fig.suptitle("Euro semifinalists carrying into the next World Cup", x=0.01, ha="left",
                 fontsize=14, fontweight="bold", color=TEXT_PRIMARY)
    ax.set_title(
        "Shared semifinalists per edition · dashed line = previous record (2), before 2026",
        loc="left", fontsize=9.5, color=TEXT_SECONDARY, pad=10,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_distribution(editions, path):
    counts = [0, 0, 0, 0]
    for ed in editions:
        counts[ed["overlap"]] += 1
    cat_labels = ["0 shared", "1 shared", "2 shared", "3 shared"]
    colors = [BLUE, BLUE, BLUE, RED]

    fig, ax = plt.subplots(figsize=(6, 4.2), dpi=200)
    style_axes(ax)

    x = range(4)
    ax.bar(x, counts, width=0.55, color=colors, zorder=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(cat_labels, fontsize=9.5)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(counts) + 1.5)

    for i, c in enumerate(counts):
        ax.text(i, c + 0.15, str(c), ha="center", va="bottom",
                 fontsize=10, fontweight="bold", color=TEXT_PRIMARY)

    fig.suptitle("Distribution of overlap sizes", x=0.01, ha="left",
                 fontsize=14, fontweight="bold", color=TEXT_PRIMARY)
    ax.set_title(
        "Across all 17 Euro → World Cup transitions, 1960–2026",
        loc="left", fontsize=9.5, color=TEXT_SECONDARY, pad=10,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    editions = load_editions()
    plot_by_edition(editions, OUT_DIR / "overlap_by_edition.png")
    plot_distribution(editions, OUT_DIR / "overlap_distribution.png")
    print(f"Wrote PNGs to {OUT_DIR}")


if __name__ == "__main__":
    main()
