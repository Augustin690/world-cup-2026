"""
How often do teams that reached the UEFA Euro semifinals also reach the
semifinals of the following FIFA World Cup?

Usage:
    python3 analysis/euro_to_world_cup_overlap.py
"""

import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "euro_to_world_cup_semifinalists.json"


def load_editions():
    with DATA_PATH.open() as f:
        return json.load(f)


def overlap(euro_teams, wc_teams):
    return sorted(set(euro_teams) & set(wc_teams))


def main():
    editions = load_editions()

    print(f"{'Euro':<6}{'World Cup':<11}{'Overlap':<8}Shared teams")
    print("-" * 70)

    counts = {}
    for ed in editions:
        shared = overlap(ed["euro_semifinalists"], ed["world_cup_semifinalists"])
        n = len(shared)
        counts[n] = counts.get(n, 0) + 1
        print(f"{ed['euro_year']:<6}{ed['world_cup_year']:<11}{n:<8}{', '.join(shared) if shared else '-'}")

    print("\nDistribution of overlap sizes across all editions:")
    for n in sorted(counts):
        print(f"  {n} shared team(s): {counts[n]} time(s)")

    target = 3
    matches = [
        ed for ed in editions
        if len(overlap(ed["euro_semifinalists"], ed["world_cup_semifinalists"])) >= target
    ]
    print(f"\nEditions with >= {target} shared semifinalists: {len(matches)}")
    for ed in matches:
        shared = overlap(ed["euro_semifinalists"], ed["world_cup_semifinalists"])
        print(f"  Euro {ed['euro_year']} -> World Cup {ed['world_cup_year']}: {', '.join(shared)}")


if __name__ == "__main__":
    main()
