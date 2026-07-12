"""
Shared loading/derivation helpers for the Euro <-> World Cup semifinalist
analysis and chart scripts.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_PATH = DATA_DIR / "euro_to_world_cup_semifinalists.json"
CHAMPION_RESULTS_PATH = DATA_DIR / "euro_champion_next_wc_result.json"

# European (UEFA) nations that show up as a World Cup semifinalist but never
# as a Euro semifinalist in this dataset, so they can't be inferred from the
# euro_semifinalists lists alone.
EXTRA_EUROPEAN_TEAMS = {"Poland", "Bulgaria", "Croatia"}

# Ordinal scale used by euro_champion_next_wc_result.json's round_rank.
ROUND_RANK_LABELS = {
    0: "Did not qualify",
    1: "Group stage",
    2: "Round of 16",
    3: "Quarterfinal",
    4: "Semifinal",
    5: "Runner-up",
    6: "Champion",
}


def load_editions():
    with DATA_PATH.open() as f:
        editions = json.load(f)

    european_teams = set(EXTRA_EUROPEAN_TEAMS)
    for ed in editions:
        european_teams.update(ed["euro_semifinalists"])

    for ed in editions:
        euro_set = set(ed["euro_semifinalists"])
        wc_set = set(ed["world_cup_semifinalists"])

        ed["shared"] = sorted(euro_set & wc_set)
        ed["overlap"] = len(ed["shared"])

        ed["european_wc_semifinalists"] = sorted(t for t in wc_set if t in european_teams)
        european_count = len(ed["european_wc_semifinalists"])
        ed["european_wc_count"] = european_count
        ed["relative_overlap"] = (ed["overlap"] / european_count) if european_count else None

        # Finalist stickiness: did the Euro champion and/or runner-up
        # individually reach the following World Cup semifinals?
        ed["champion_carried"] = ed["euro_champion"] in wc_set
        ed["runner_up_carried"] = ed["euro_runner_up"] in wc_set
        ed["finalist_carryover_count"] = int(ed["champion_carried"]) + int(ed["runner_up_carried"])

    return editions


def load_champion_results():
    with CHAMPION_RESULTS_PATH.open() as f:
        return json.load(f)


def compute_reverse_overlaps(editions):
    """
    For each World Cup, how many of its European semifinalists went on to
    reach the semifinals of the *next* Euro (mirror image of the main
    Euro -> World Cup analysis). The last edition's World Cup (2026) has no
    "next Euro" yet, so it's excluded.
    """
    pairs = []
    for i in range(len(editions) - 1):
        wc_ed = editions[i]
        next_euro_ed = editions[i + 1]

        wc_set = set(wc_ed["world_cup_semifinalists"])
        next_euro_set = set(next_euro_ed["euro_semifinalists"])
        shared = sorted(wc_set & next_euro_set)

        pairs.append({
            "world_cup_year": wc_ed["world_cup_year"],
            "world_cup_semifinalists": wc_ed["world_cup_semifinalists"],
            "european_wc_count": wc_ed["european_wc_count"],
            "next_euro_year": next_euro_ed["euro_year"],
            "next_euro_semifinalists": next_euro_ed["euro_semifinalists"],
            "shared": shared,
            "overlap": len(shared),
            "relative_overlap": (len(shared) / wc_ed["european_wc_count"]) if wc_ed["european_wc_count"] else None,
        })
    return pairs
