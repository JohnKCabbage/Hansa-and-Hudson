# Defense Market Signal Brief

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
