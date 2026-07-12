"""
Render the three follow-on analyses (reverse overlap, champion carryover,
finalist stickiness) as static PNGs using matplotlib.

Usage:
    python3 analysis/plot_related_charts.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from data_utils import ROUND_RANK_LABELS, compute_reverse_overlaps, load_champion_results, load_editions

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
GOOD = "#0ca30c"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]


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


def plot_reverse_overlap(editions, path):
    pairs = compute_reverse_overlaps(editions)
    max_val = max(p["overlap"] for p in pairs)
    colors = [RED if p["overlap"] == max_val else BLUE for p in pairs]

    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=200)
    style_axes(ax)

    x = range(len(pairs))
    ax.bar(x, [p["overlap"] for p in pairs], width=0.62, color=colors, zorder=3)

    labels = [f"'{str(p['world_cup_year'])[2:]}→'{str(p['next_euro_year'])[2:]}" for p in pairs]
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, 4)

    for i, p in enumerate(pairs):
        if p["overlap"] > 0:
            ax.text(i, p["overlap"] + 0.08, str(p["overlap"]), ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color=TEXT_PRIMARY)

    fig.suptitle("World Cup semifinalists carrying into the next Euro", x=0.01, ha="left",
                 fontsize=14, fontweight="bold", color=TEXT_PRIMARY)
    ax.set_title(
        "Mirror image of the main analysis — red = joint-highest (2 shared teams)",
        loc="left", fontsize=9.5, color=TEXT_SECONDARY, pad=10,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_champion_carryover(path):
    results = load_champion_results()
    labels = [f"{r['euro_year']}→{r['world_cup_year']}" for r in results]
    ranks = [r["round_rank"] for r in results]

    def color_for(rank, provisional):
        if provisional:
            return TEXT_MUTED
        if rank == 0:
            return RED
        if rank == 6:
            return GOOD
        return BLUE

    colors = [color_for(r["round_rank"], r.get("provisional", False)) for r in results]

    fig, ax = plt.subplots(figsize=(12, 5.6), dpi=200)
    style_axes(ax)

    x = range(len(results))
    bar_heights = [max(r, 0.12) for r in ranks]
    ax.bar(x, bar_heights, width=0.55, color=colors, zorder=3)

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8.5, rotation=45, ha="right")
    ax.set_ylim(0, 9.5)
    ax.set_yticks(list(ROUND_RANK_LABELS.keys()))
    ax.set_yticklabels([ROUND_RANK_LABELS[k] for k in ROUND_RANK_LABELS], fontsize=8.5)

    for i, r in enumerate(results):
        champ = r["champion"]
        suffix = " *" if r.get("provisional") else ""
        ax.text(i, r["round_rank"] + 0.15, champ + suffix, ha="center", va="bottom",
                 fontsize=7.5, fontweight="bold", color=TEXT_PRIMARY, rotation=90)

    fig.suptitle("How far did the reigning Euro champion get at the next World Cup?",
                 x=0.01, ha="left", fontsize=13.5, fontweight="bold", color=TEXT_PRIMARY)
    ax.set_title(
        "Red = didn't even qualify (4 of 17) · Green = won the World Cup too (2 of 17) · "
        "* = 2026, in progress as of Jul 12",
        loc="left", fontsize=9, color=TEXT_SECONDARY, pad=10,
    )

    fig.tight_layout(rect=[0, 0.08, 1, 0.90])
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def plot_finalist_stickiness(editions, path):
    max_val = max(ed["finalist_carryover_count"] for ed in editions)
    colors = [RED if ed["finalist_carryover_count"] == max_val else BLUE for ed in editions]

    fig, ax = plt.subplots(figsize=(11, 4.2), dpi=200)
    style_axes(ax)

    x = range(len(editions))
    ax.bar(x, [ed["finalist_carryover_count"] for ed in editions], width=0.62, color=colors, zorder=3)

    labels = [f"'{str(ed['euro_year'])[2:]}→'{str(ed['world_cup_year'])[2:]}" for ed in editions]
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 2.6)
    ax.set_yticks([0, 1, 2])

    for i, ed in enumerate(editions):
        c = ed["finalist_carryover_count"]
        if c > 0:
            ax.text(i, c + 0.08, str(c), ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color=TEXT_PRIMARY)

    fig.suptitle("Did the Euro's two finalists reach the next World Cup semis?",
                 x=0.01, ha="left", fontsize=13.5, fontweight="bold", color=TEXT_PRIMARY)
    ax.set_title(
        "0, 1, or 2 of the Euro champion + runner-up · red = both carried over (only twice)",
        loc="left", fontsize=9.5, color=TEXT_SECONDARY, pad=10,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    editions = load_editions()
    plot_reverse_overlap(editions, OUT_DIR / "reverse_overlap_by_edition.png")
    plot_champion_carryover(OUT_DIR / "champion_next_wc_result.png")
    plot_finalist_stickiness(editions, OUT_DIR / "finalist_stickiness.png")
    print(f"Wrote PNGs to {OUT_DIR}")


if __name__ == "__main__":
    main()
