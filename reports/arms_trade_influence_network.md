# Arms Trade Influence Network: The Security Dependency Graph

*Subtitle: alliances are nice; spare parts are binding contracts.*

## Executive Takeaways

1. **US security architecture remains the gravity well of high-end interoperability.** In this SIPRI-derived sample, US-origin equipment accounts for **~77.5%** of all `NATO_standard` transfer volume. NATO armies can disagree on lunch, but not on Link-16, Patriot logistics, and F-35 sustainment chains.
2. **Russia's export position has sharply contracted.** Export TIV in the comparison file declines **~53.0%** from 2014-2018 to 2019-2023, matching the broad trendline discussed in recent SIPRI assessments.
3. **China's equipment footprint is widening in the Global South.** In the regional series, combined China-linked transfers to **Africa + South America** rise from 730 to 1700 TIV-equivalent units from 2014 to 2023, about **9.8% CAGR**.
4. **Dependency is concentrated and therefore coercible.** The network shock simulator shows many importers with >80% reliance on a single exporter in their active procurement pipeline.

---

## 1) Research Design

### Core question
> If exporter **X** is suddenly unavailable (sanctions, war demand, political rupture), which states lose near-term combat capability acquisition capacity?

### Data used in this repo
- `data/arms_transfers_sample_2019_2023.csv`
  - Bilateral exporter→importer flows (weighted by TIV-like magnitude), system family tags, and interoperability tags.
- `data/exporter_period_totals_tiv.csv`
  - Aggregated exporter totals across two periods for trend comparison.
- `data/china_regional_footprint_tiv.csv`
  - Regional time series used to track China's directional expansion.

### Method
- Construct directed weighted graph **G(exporter → importer, weight=TIV)**.
- Compute:
  - weighted outflow (export influence volume),
  - importer dependency ratio = top supplier share of current pipeline,
  - removal shock = removed supplier weight / importer total weight.
- Build an interactive HTML for scenario testing.

### Scope caveat (important)
This is a **structured analytical demonstrator** with SIPRI-style fields and trend baselines, not a full SIPRI database mirror. It is designed for workflow and inference logic: the same code can be dropped onto a complete SIPRI extract.

---

## 2) Findings

## A. US equipment + NATO interoperability: architecture, not just market share

- In this sample, `NATO_standard` tagged flows total **22,700** TIV, and **17,600** of that is US-origin (**77.5%**).
- This matters because combat value is not only in platforms, but in:
  - compatible datalinks,
  - ammunition and missile ecosystems,
  - maintenance tooling,
  - training pipelines.

**Interpretation:** The US isn't just selling kit; it is underwriting a shared operating system. If interoperability is software, hardware is merely the annual subscription fee.

## B. Russia: shrinking export surface, denser client risk

- Russia's comparison series: **96,000 → 45,100** (2014-2018 to 2019-2023), a **-53.0%** move.
- In the network, remaining buyers (e.g., Armenia, Vietnam, Algeria share) are relatively concentrated.

**Implication:** As volumes contract, Moscow's client set becomes more selective and potentially more politically exposed to supply disruptions.

## C. China: regional expansion where affordability + availability matter

- China regional series shows steady gains, especially in:
  - **Africa:** 620 → 1280
  - **South America:** 110 → 420
- Combined Africa+South America growth approximates **9.8% CAGR (2014-2023)**.

**Interpretation:** China's footprint growth appears less about replacing US/NATO premium systems and more about filling capability gaps with acceptable cost, faster delivery, and bundled political financing.

---

## 3) Visual Products

- Interactive network (with exporter removal simulator):
  - `visuals/security_dependency_graph.html`
- Exporter trend comparison chart:
  - `visuals/exporter_shift.svg`
- China's regional footprint chart:
  - `visuals/china_footprint.svg`
- Computed network metrics:
  - `visuals/network_metrics.json`

---

## 4) Strategic Readout (Plain English, mildly caffeinated)

- **US:** still the backbone for high-end allied interoperability; the network has both scale and standards lock-in.
- **Russia:** export compression reduces optionality and may raise fragility among remaining clients.
- **China:** quietly broadening arms relationships across regions where procurement friction beats doctrinal purity.

In other words: everyone talks sovereignty; everyone still needs spare parts by Tuesday.

---

## 5) Reproducibility

Run:

```bash
python analysis/security_dependency_graph.py
```

This regenerates all visuals and the metrics JSON from the data files in `data/`.
