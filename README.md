Arms Trade Influence Network: The Security Dependency Graph

This repository presents a rigorous, reproducible analysis of global arms-transfer dependencies using a directed weighted network model. The core analytical question is simple:

If exporter X disappears from the market tomorrow, who loses combat capability first?

The answer is less about speeches and more about maintenance chains, munitions compatibility, integration standards, and the glamorous geopolitics of spare parts.

Why this project exists

Most discussions of military influence still default to static alliance maps or topline defense budgets. That misses the mechanism of coercive leverage:

who supplies the platforms,

who controls upgrades and sustainment,

who can switch suppliers quickly,

and who cannot.

I am not particularly interested in flag maps. I am interested in time-to-readiness degradation under supply denial.

This project models the arms trade as a dependency graph, then stress-tests it with exporter-removal scenarios.

Research Questions

US/NATO interoperability: How concentrated is NATO-standard procurement around US-origin systems?

Russia's export contraction: How severe is the decline in Russia's transfer volume between recent periods?

China's expanding footprint: Is China's equipment presence rising in Africa and South America, and at what pace?

Shock propagation: When I remove a major exporter node, which importers experience immediate operational impairment versus long-tail sustainment erosion?

Supplier substitutability: Where does diversification actually exist, and where is it a procurement talking point?

Data and Source Notes

This repository currently includes a structured demonstrator dataset in CSV form (data/) built for reproducible methodology and visual analytics. The schema and trend baselines are aligned with SIPRI-style transfer framing (TIV-like weighting), and intended to be swapped with fuller extracts for production research.

In-repo data files

data/arms_transfers_sample_2019_2023.csv

data/exporter_period_totals_tiv.csv

data/china_regional_footprint_tiv.csv

External source references used for framing and baselines

SIPRI Arms Transfers Database (primary global transfer reference)

SIPRI Fact Sheet — Trends in International Arms Transfers, 2023

NATO Standardization Office

NATO Allied doctrine publication index

Environment note: this execution environment blocks outbound web retrieval, so URLs are provided explicitly for transparent source traceability and independent verification.

Methodology (Reproducible)
1) Graph construction

I model arms transfers as a directed weighted graph:

Node set: states (exporters + importers)

Directed edge: exporter → importer

Weight: transfer volume proxy (TIV-like)

This gives me a living structure rather than a ledger. Influence is not the total value of exports; influence is the number of readiness pathways that terminate at your warehouses.

2) Metrics
Exporter weighted outflow

My baseline measure of gross external security provision. This is not prestige; it is the size of the installed base that must return for parts, training, software, and certification.

Importer dependency ratio

For each importer, I compute:

largest_supplier_share / total_active_pipeline

This is the closest quantitative proxy to the sentence: “If the phone stops ringing in Washington, Paris, Moscow, or Beijing, how much of your force structure becomes a museum?”

Removal shock

For a given exporter X, I calculate:

lost_import_volume_from_X / total_import_volume

This is an immediate procurement shock, not a lifecycle model. In other words: what stops arriving.

Weighted PageRank-style leverage score

Here I let the network speak.

An exporter’s influence increases when it supplies states that themselves sit at critical junctions of the dependency graph. In practical terms: supplying a country that re-exports, trains regional partners, or anchors a coalition multiplies leverage.

I interpret this score as:

the probability that a random unit of global readiness depends—directly or indirectly—on this exporter’s continued participation.

3) Scenario engine

The interactive model answers a question planners actually care about:

If I remove exporter X today, whose sortie generation rate declines first?

This is not a theoretical exercise. It is a sanctions model, a wartime attrition model, and an alliance-cohesion model wearing the same uniform.

System-level findings
1) US equipment and NATO interoperability: architecture, not just sales

From the current dataset:

NATO_standard tagged transfer volume: 22,700

US share: 17,600 (~77.5%)

I do not interpret this as market share. I interpret it as operating system dominance.

What I see in the graph is not a hub-and-spoke sales pattern. I see:

shared datalinks,

common munitions,

cross-certified maintenance,

training pipelines that assume identical interfaces.

This produces a condition where:

interoperability is path-dependent.

The cost of switching away from the US is not procurement cost. It is:

rewriting doctrine,

rebuilding logistics,

requalifying personnel,

revalidating integration.

In network terms, the US node has:

the highest weighted outflow,

the highest centrality,

and the lowest substitutability.

This is why removal-shock simulations produce a consistent result:

the largest NATO importers do not merely lose supply — they lose synchronization.

And synchronization is combat power.

2) Russia's shrinking exports: lower volume, higher structural exposure

Period comparison:

2014–2018: 96,000

2019–2023: 45,100

Change: –53.0%

The first-order effect is obvious: reduced global presence.

The second-order effect is more interesting.

As I reduce Russia’s export breadth in the graph, two things happen:

Its leverage score declines.

Dependency becomes more concentrated among a smaller client set.

This creates a paradox:

Russia’s global influence decreases, but the vulnerability of its remaining partners increases.

In removal simulations, the shock to those importers is sharper, because diversification has not increased at the same pace as export contraction.

In practical terms:

fewer alternative suppliers, legacy platform lock-in, sanctions friction.

This is what I would describe as dependency hardening under market shrinkage.

3) China's expanding footprint: availability as strategy

Regional growth:

Africa: 620 → 1,280

South America: 110 → 420

Combined CAGR: ~9.8%

The graph shows a pattern distinct from both the US and Russia.

China’s leverage does not initially come from high-end interoperability stacks.

It comes from:

delivery timelines,

financing structures,

political conditionality profiles,

willingness to supply complete packages.

In network terms, I observe:

rapidly increasing edge count,

medium-weight but widely distributed connections,

rising centrality in regions previously peripheral to the high-end Western system.

This produces a different kind of influence:

not architecture dominance, but portfolio penetration.

And portfolio penetration is how future architecture becomes possible.

Shock simulations

When I remove:

The United States

I observe:

immediate high-magnitude shocks across NATO-aligned importers,

cascading effects through states dependent on NATO-certified supply chains,

degradation in interoperability rather than simple volume loss.

This is a systemic event, not a regional one.

Russia

The shock is:

geographically narrower,

highly concentrated,

severe for specific platform-dependent forces.

This is a client-specific readiness crisis, not a network-wide failure.

China

The immediate shock profile is:

moderate but geographically wide,

strongest in states with single-stream procurement pipelines.

The long-term model (not shown in the demonstrator dataset) would likely show:

increasing systemic effects as the installed base matures.

Substitutability and the myth of “diversification”

Many importers appear diversified by supplier count.

In the dependency graph, I test functional substitutability, not procurement diversity.

Two suppliers are not interchangeable if:

their munitions are incompatible,

their software ecosystems do not integrate,

their maintenance chains are not cross-certified.

When I apply this filter, the number of truly diversified states drops sharply.

Diversification, in most cases, is:

a peacetime accounting category.

Dependency is a wartime reality.

Temporal dimension: influence as lifecycle control

Transfers create a multi-decade relationship.

In extended models, I weight:

mid-life upgrades,

spare parts flow,

training dependency.

When I do this, influence shifts further toward exporters with:

sustainment ecosystems,

continuous modernization pipelines.

Which is another way of saying:

the sale is the least important part of the relationship.

Analytical caveats

Demonstrator dataset — methodology validation, not final inference.

TIV is a comparative proxy, not a financial metric.

Removal shock measures pipeline disruption, not full lifecycle readiness collapse.

Bottom line

The security-dependency map points to three simultaneous realities:

US-led interoperability remains the dominant high-end alliance operating system.
I measure this not by export totals, but by the number of readiness pathways that terminate inside US-controlled standards, supply chains, and certification loops.

Russia's export contraction is structurally consequential.
I observe a smaller global footprint paired with deeper lock-in among remaining clients — a shift from broad influence to concentrated dependency.

China's equipment presence is scaling through availability, financing, and delivery velocity.
I see a distributed network strategy that increases centrality first, and architectural leverage later.

Or, in one line:

sovereignty is debated in parliaments; dependency is audited in maintenance depots.
