"""
Three follow-on analyses to the main Euro <-> World Cup overlap study:

  1. Reverse direction — of a World Cup's European semifinalists, how many
     reached the semifinals of the *next* Euro.
  2. Champion carryover — how far did the reigning Euro champion get at the
     following World Cup.
  3. Finalist stickiness — did the Euro's two finalists (champion + runner-up)
     individually reach the following World Cup semifinals.

Usage:
    python3 analysis/related_analyses.py
"""

from data_utils import ROUND_RANK_LABELS, compute_reverse_overlaps, load_champion_results, load_editions


def print_reverse_overlap(editions):
    print("1. REVERSE OVERLAP — World Cup semifinalists carrying into the next Euro")
    print("-" * 78)
    pairs = compute_reverse_overlaps(editions)

    header = f"{'World Cup':<11}{'Next Euro':<11}{'Overlap':<9}{'Euro WC-SFs':<13}{'Relative':<10}Shared teams"
    print(header)
    print("-" * len(header))
    for p in pairs:
        rel = f"{p['relative_overlap']:.0%}" if p["relative_overlap"] is not None else "n/a"
        print(
            f"{p['world_cup_year']:<11}{p['next_euro_year']:<11}{p['overlap']:<9}"
            f"{p['european_wc_count']:<13}{rel:<10}{', '.join(p['shared']) if p['shared'] else '-'}"
        )

    best = max(pairs, key=lambda p: p["overlap"])
    print(f"\nHighest reverse overlap: World Cup {best['world_cup_year']} -> Euro {best['next_euro_year']} "
          f"({best['overlap']} shared: {', '.join(best['shared'])})")
    print()


def print_champion_carryover():
    print("2. CHAMPION CARRYOVER — how far did the reigning Euro champion get at the next World Cup")
    print("-" * 78)
    results = load_champion_results()

    header = f"{'Euro':<6}{'Champion':<16}{'World Cup':<11}Result"
    print(header)
    print("-" * len(header))
    for r in results:
        flag = " *" if r.get("provisional") else ""
        print(f"{r['euro_year']:<6}{r['champion']:<16}{r['world_cup_year']:<11}{r['round_reached']}{flag}")

    def label(r):
        return f"{r['champion']} {r['euro_year']}->{r['world_cup_year']}"

    dnq = [r for r in results if r["round_rank"] == 0]
    doubles = [r for r in results if r["round_rank"] == 6]
    print(f"\nFailed to even qualify for the next World Cup: {len(dnq)}/{len(results)} "
          f"({', '.join(label(r) for r in dnq)})")
    print(f"Went on to win the next World Cup (\"the double\"): {len(doubles)}/{len(results)} "
          f"({', '.join(label(r) for r in doubles)})")
    print("(Rank scale: " + ", ".join(f"{k}={v}" for k, v in ROUND_RANK_LABELS.items()) + ")")
    print()


def print_finalist_stickiness(editions):
    print("3. FINALIST STICKINESS — did the Euro's two finalists reach the next World Cup semis")
    print("-" * 78)

    header = f"{'Euro':<6}{'Champion':<16}{'Runner-up':<16}{'World Cup':<11}Carried over"
    print(header)
    print("-" * len(header))
    for ed in editions:
        carried = []
        if ed["champion_carried"]:
            carried.append(ed["euro_champion"])
        if ed["runner_up_carried"]:
            carried.append(ed["euro_runner_up"])
        print(
            f"{ed['euro_year']:<6}{ed['euro_champion']:<16}{ed['euro_runner_up']:<16}"
            f"{ed['world_cup_year']:<11}{', '.join(carried) if carried else '-'}"
        )

    both = [ed for ed in editions if ed["finalist_carryover_count"] == 2]
    neither = [ed for ed in editions if ed["finalist_carryover_count"] == 0]

    def label(ed):
        return f"{ed['euro_year']}->{ed['world_cup_year']}"

    print(f"\nBoth finalists carried over: {len(both)}/{len(editions)} "
          f"({', '.join(label(ed) for ed in both)})")
    print(f"Neither finalist carried over: {len(neither)}/{len(editions)}")


def main():
    editions = load_editions()
    print_reverse_overlap(editions)
    print_champion_carryover()
    print_finalist_stickiness(editions)


if __name__ == "__main__":
    main()
