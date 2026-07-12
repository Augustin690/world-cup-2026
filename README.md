# World Cup 2026

Data analysis on the World Cup, starting with a look at how often UEFA Euro
semifinalists carry over into the following World Cup semifinals.

## Question

Euro 2024's semifinalists were Spain, France, Netherlands, and England. Three
of those four (Spain, France, England) also reached the World Cup 2026
semifinals. How unusual is that, historically?

## Structure

- `data/euro_to_world_cup_semifinalists.json` — the four semifinalists of
  every UEFA Euro from 1960 to 2024 (plus its champion and runner-up), and of
  the World Cup immediately after, for all 17 editions.
- `data/euro_champion_next_wc_result.json` — how far the reigning Euro
  champion got at the following World Cup, on a 0 (did not qualify) to 6
  (won it) ordinal scale.
- `analysis/data_utils.py` — shared loading and derivation logic: overlap
  count, European-nation classification, relative overlap, reverse overlap,
  and finalist-carryover flags. Used by every script below so their numbers
  always agree.
- `analysis/euro_to_world_cup_overlap.py` — CLI report of overlap counts and
  relative overlap per edition.
  ```
  python3 analysis/euro_to_world_cup_overlap.py
  ```
- `analysis/related_analyses.py` — CLI report for three follow-on questions:
  reverse overlap (World Cup → next Euro), champion carryover, and finalist
  stickiness (see Findings below).
  ```
  python3 analysis/related_analyses.py
  ```
- `analysis/plot_charts.py` / `analysis/plot_related_charts.py` — render the
  same data as static PNGs with matplotlib.
  ```
  pip install matplotlib
  python3 analysis/plot_charts.py
  python3 analysis/plot_related_charts.py
  ```
- `charts/` — output charts:
  - `overlap_by_edition.png` / `overlap_distribution.png` / `relative_overlap_by_edition.png`
  - `reverse_overlap_by_edition.png` / `champion_next_wc_result.png` / `finalist_stickiness.png`
  - `euro_to_world_cup_overlap.html` — self-contained interactive version
    (hover tooltips, data tables, light/dark mode) — open directly in a
    browser.

## Findings

- **Absolute overlap**: across all 17 Euro → World Cup transitions since
  1960, the previous ceiling was **2** shared semifinalists (hit 4 times).
  Euro 2024 → World Cup 2026 is the only edition to reach **3**.
- **Relative overlap** (shared teams ÷ European World Cup semifinalists that
  year, which controls for how many European sides even made that World
  Cup's final four): 2026 **ties** Euro 1960 → World Cup 1962 at **100%**.
  1988→90 and 2008→10 follow at 67%.
- **0% editions**: Euro 2000 → World Cup 2002 and Euro 2020 → World Cup 2022
  both saw a complete changeover — none of the (2) European World Cup
  semifinalists that year had been Euro semifinalists.
- **Reverse direction** (World Cup semifinalists → next Euro semifinals): the
  best a World Cup has ever done is **2** shared teams, hit four times
  (1966→68, 1974→76, 1998→2000, 2010→12) — the reverse direction has never
  matched 2026's 3-team carryover.
- **Champion carryover**: the reigning Euro champion has failed to even
  *qualify* for the next World Cup **4 times out of 17** (Czechoslovakia '76,
  Denmark '92, Greece '04, Italy '20) — and gone on to win the next World Cup
  ("the double") only **twice** (West Germany '72→'74, Spain '08→'10). Spain
  are currently a Euro champion in the WC 2026 semifinals, chasing a third.
- **Finalist stickiness**: of the Euro's two finalists (champion + runner-up),
  **both** have carried into the next World Cup semis only **twice**:
  2008→2010 (Spain, Germany) and 2024→2026 (Spain, England). Seven times,
  *neither* finalist made it back.
