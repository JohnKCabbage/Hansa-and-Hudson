from __future__ import annotations

import csv
from pathlib import Path

DATA_PATH = Path("data/military_spending_snapshot.csv")
OUTPUT_PATH = Path("outputs/defense_market_map.csv")
BRIEF_PATH = Path("outputs/executive_brief.md")


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open() as f:
        return list(csv.DictReader(f))


def cagr(start: float, end: float, years: int = 9) -> float:
    if start <= 0 or end <= 0:
        return 0.0
    return (end / start) ** (1 / years) - 1


def score_rows(rows: list[dict[str, str]]) -> list[dict[str, float | str | bool]]:
    enriched = []
    total_2023 = sum(float(r["mil_spend_2023_usd_b"]) for r in rows)

    for r in rows:
        spend_2014 = float(r["mil_spend_2014_usd_b"])
        spend_2023 = float(r["mil_spend_2023_usd_b"])
        gdp_2023 = float(r["gdp_2023_usd_b"])
        burden_pct = (spend_2023 / gdp_2023) * 100
        growth = cagr(spend_2014, spend_2023)
        share = spend_2023 / total_2023
        enriched.append(
            {
                "iso3": r["iso3"],
                "country": r["country"],
                "mil_spend_2023_usd_b": spend_2023,
                "mil_spend_cagr_2014_2023": growth,
                "mil_spend_pct_gdp_2023": burden_pct,
                "global_share_2023": share,
                "nato_member": r["nato_member"] == "yes",
            }
        )

    for key, weight in [
        ("mil_spend_pct_gdp_2023", 0.45),
        ("mil_spend_cagr_2014_2023", 0.35),
        ("global_share_2023", 0.20),
    ]:
        values = [float(x[key]) for x in enriched]
        lo, hi = min(values), max(values)
        span = hi - lo if hi != lo else 1.0
        for x in enriched:
            x.setdefault("modernization_pressure_score", 0.0)
            x["modernization_pressure_score"] += ((float(x[key]) - lo) / span) * weight

    enriched.sort(key=lambda x: float(x["modernization_pressure_score"]), reverse=True)
    return enriched


def write_market_map(rows: list[dict[str, float | str | bool]]) -> None:
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    fields = [
        "iso3",
        "country",
        "mil_spend_2023_usd_b",
        "mil_spend_cagr_2014_2023",
        "mil_spend_pct_gdp_2023",
        "global_share_2023",
        "modernization_pressure_score",
        "nato_member",
    ]
    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_brief(rows: list[dict[str, float | str | bool]]) -> None:
    by_spend = sorted(rows, key=lambda x: float(x["mil_spend_2023_usd_b"]), reverse=True)
    top_spenders = ", ".join(f"{r['country']} (${float(r['mil_spend_2023_usd_b']):.0f}B)" for r in by_spend[:5])
    fastest = sorted(rows, key=lambda x: float(x["mil_spend_cagr_2014_2023"]), reverse=True)[:5]
    fastest_txt = ", ".join(
        f"{r['country']} ({float(r['mil_spend_cagr_2014_2023']) * 100:.1f}% CAGR)" for r in fastest
    )

    nato = [r for r in rows if bool(r["nato_member"])]
    at_target = [r for r in nato if float(r["mil_spend_pct_gdp_2023"]) >= 2.0]

    top_decile_count = max(1, len(rows) // 10)
    priority = ", ".join(r["country"] for r in rows[:top_decile_count])

    brief = f"""# Defense Market Signal Brief

## Method
This analysis uses a local snapshot of military spending and GDP data for 20 strategically relevant countries (2014 and 2023 endpoints). It computes:
- CAGR of defense spending
- Defense burden (% of GDP)
- Share of covered global defense spend
- Composite `modernization_pressure_score`

## Key Findings
- **Top 2023 spenders:** {top_spenders}
- **Fastest growth cohort:** {fastest_txt}
- **NATO burden-sharing:** {len(at_target)}/{len(nato)} NATO members in this dataset meet or exceed 2% of GDP.
- **Priority demand markets:** {priority}

## Interview-ready framing
- Built a reproducible analytics pipeline from raw tabular data to scored market segmentation.
- Combined macro-financial indicators into a weighted prioritization model suitable for strategy teams.
- Generated concise executive messaging directly from the model output.
"""
    BRIEF_PATH.write_text(brief)


def main() -> None:
    rows = load_rows()
    scored = score_rows(rows)
    write_market_map(scored)
    write_brief(scored)
    print("Generated outputs/defense_market_map.csv and outputs/executive_brief.md")


if __name__ == "__main__":
    main()
