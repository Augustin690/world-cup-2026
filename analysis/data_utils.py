"""
Shared loading/derivation helpers for the Euro <-> World Cup semifinalist
analysis and chart scripts.
"""

import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "euro_to_world_cup_semifinalists.json"

# European (UEFA) nations that show up as a World Cup semifinalist but never
# as a Euro semifinalist in this dataset, so they can't be inferred from the
# euro_semifinalists lists alone.
EXTRA_EUROPEAN_TEAMS = {"Poland", "Bulgaria", "Croatia"}


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

    return editions
