# World Cup 2026

Data analysis on the World Cup, starting with a look at how often UEFA Euro
semifinalists carry over into the following World Cup semifinals.

## Question

Euro 2024's semifinalists were Spain, France, Netherlands, and England. Three
of those four (Spain, France, England) also reached the World Cup 2026
semifinals. How unusual is that, historically?

## Structure

- `data/euro_to_world_cup_semifinalists.json` — the four semifinalists of
  every UEFA Euro from 1960 to 2024, and of the World Cup immediately after,
  for all 17 editions.
- `analysis/data_utils.py` — shared loading and derivation logic: overlap
  count, European-nation classification, and the relative-overlap metric.
  Used by both scripts below so their numbers always agree.
- `analysis/euro_to_world_cup_overlap.py` — CLI report of overlap counts and
  relative overlap per edition.
  ```
  python3 analysis/euro_to_world_cup_overlap.py
  ```
- `analysis/plot_charts.py` — renders the same data as static PNGs with
  matplotlib.
  ```
  pip install matplotlib
  python3 analysis/plot_charts.py
  ```
- `charts/` — output charts:
  - `overlap_by_edition.png` / `overlap_distribution.png` / `relative_overlap_by_edition.png`
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
