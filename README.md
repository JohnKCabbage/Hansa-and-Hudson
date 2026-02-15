# Defense Market Signal Brief (2-Minute Portfolio Build)

This is a fast, professional, defense-analytics-adjacent project you can ship to GitHub.

It takes a military spending snapshot, computes growth/burden/market-share metrics, and produces a scored country market map plus an executive brief.

## Skills this showcases
- Data wrangling and metric engineering
- Prioritization model design
- Business-facing analysis output
- Reproducible Python workflow

## Run it
```bash
python src/defense_market_analysis.py
```

## Inputs
- `data/military_spending_snapshot.csv`
  - 2014 vs 2023 defense spend (USD billions)
  - 2023 GDP (USD billions)
  - NATO membership flag

## Outputs
- `outputs/defense_market_map.csv`
- `outputs/executive_brief.md`

## Why this is employable
Instead of reposting obvious facts, this project creates a **decision product**:
- ranks markets with a transparent scoring model
- surfaces burden-sharing and growth hotspots
- translates quant outputs into an executive narrative

## Easy upgrades (if you want to level it up)
- swap snapshot CSV for SIPRI/World Bank API pulls
- add sanctions or conflict-event features
- build a simple Streamlit dashboard on top of the output CSV
