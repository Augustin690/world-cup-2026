"""
How often do teams that reached the UEFA Euro semifinals also reach the
semifinals of the following FIFA World Cup?

Also reports the *relative* overlap: of the World Cup semifinalists that
were European, what share had also been Euro semifinalists the previous
summer. This controls for editions where few European teams made the
World Cup semis in the first place.

Usage:
    python3 analysis/euro_to_world_cup_overlap.py
"""

from data_utils import load_editions


def main():
    editions = load_editions()

    header = f"{'Euro':<6}{'World Cup':<11}{'Overlap':<9}{'Euro WC-SFs':<13}{'Relative':<10}Shared teams"
    print(header)
    print("-" * len(header))

    counts = {}
    for ed in editions:
        counts[ed["overlap"]] = counts.get(ed["overlap"], 0) + 1
        rel = f"{ed['relative_overlap']:.0%}" if ed["relative_overlap"] is not None else "n/a"
        print(
            f"{ed['euro_year']:<6}{ed['world_cup_year']:<11}{ed['overlap']:<9}"
            f"{ed['european_wc_count']:<13}{rel:<10}{', '.join(ed['shared']) if ed['shared'] else '-'}"
        )

    print("\nDistribution of overlap sizes across all editions:")
    for n in sorted(counts):
        print(f"  {n} shared team(s): {counts[n]} time(s)")

    print("\nRelative overlap (shared / European WC semifinalists), sorted descending:")
    ranked = sorted(
        (ed for ed in editions if ed["relative_overlap"] is not None),
        key=lambda ed: ed["relative_overlap"],
        reverse=True,
    )
    for ed in ranked:
        print(
            f"  Euro {ed['euro_year']} -> World Cup {ed['world_cup_year']}: "
            f"{ed['relative_overlap']:.0%} ({ed['overlap']}/{ed['european_wc_count']})"
        )

    target = 3
    matches = [ed for ed in editions if ed["overlap"] >= target]
    print(f"\nEditions with >= {target} shared semifinalists: {len(matches)}")
    for ed in matches:
        print(f"  Euro {ed['euro_year']} -> World Cup {ed['world_cup_year']}: {', '.join(ed['shared'])}")

    full_carryover = [ed for ed in editions if ed["relative_overlap"] == 1.0]
    print(f"\nEditions where 100% of European WC semifinalists were Euro semifinalists: {len(full_carryover)}")
    for ed in full_carryover:
        print(f"  Euro {ed['euro_year']} -> World Cup {ed['world_cup_year']}: {', '.join(ed['shared'])}")


if __name__ == "__main__":
    main()
