import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
VIS = ROOT / "visuals"
VIS.mkdir(exist_ok=True)


def load_edges(path):
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            r["tiv"] = float(r["tiv"])
            rows.append(r)
    return rows


def load_export_trends(path):
    by_exporter = defaultdict(dict)
    with path.open() as f:
        for r in csv.DictReader(f):
            by_exporter[r["exporter"]][r["period"]] = float(r["total_tiv"])
    return by_exporter


def load_china_series(path):
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            row = {"year": int(r["year"])}
            for k, v in r.items():
                if k != "year":
                    row[k] = float(v)
            rows.append(row)
    return rows


def load_platform_rows(path):
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            r["units"] = int(r["units"])
            rows.append(r)
    return rows


def pagerank(nodes, edges, damping=0.85, iterations=60):
    out_weight = defaultdict(float)
    incoming = defaultdict(list)
    for e in edges:
        s, t, w = e["exporter"], e["importer"], e["tiv"]
        out_weight[s] += w
        incoming[t].append((s, w))

    n = len(nodes)
    rank = {node: 1.0 / n for node in nodes}
    for _ in range(iterations):
        new_rank = {node: (1 - damping) / n for node in nodes}
        for node in nodes:
            for src, weight in incoming.get(node, []):
                if out_weight[src] > 0:
                    new_rank[node] += damping * rank[src] * (weight / out_weight[src])
        rank = new_rank
    return rank


def calculate_metrics(edges):
    exporters = sorted({e["exporter"] for e in edges})
    importers = sorted({e["importer"] for e in edges})
    nodes = sorted(set(exporters + importers))

    import_total = defaultdict(float)
    by_importer = defaultdict(list)
    exporter_total = defaultdict(float)
    for e in edges:
        import_total[e["importer"]] += e["tiv"]
        exporter_total[e["exporter"]] += e["tiv"]
        by_importer[e["importer"]].append(e)

    dependency = {}
    for imp, arr in by_importer.items():
        top = max(arr, key=lambda x: x["tiv"])
        dependency[imp] = {
            "top_exporter": top["exporter"],
            "dependency_ratio": round(top["tiv"] / import_total[imp], 3),
            "total_import_tiv": round(import_total[imp], 1),
        }

    leverage_rank = pagerank(nodes, edges)

    return {
        "exporter_total": dict(sorted(exporter_total.items(), key=lambda x: x[1], reverse=True)),
        "dependency": dependency,
        "leverage_rank": dict(sorted(leverage_rank.items(), key=lambda x: x[1], reverse=True)),
    }


def save_network_html(edges, metrics, output):
    nodes = sorted(set([e["exporter"] for e in edges] + [e["importer"] for e in edges]))
    exporters = sorted(set(e["exporter"] for e in edges))

    angle_step = (2 * math.pi) / len(nodes)
    coords = {}
    for i, n in enumerate(nodes):
        angle = i * angle_step
        x = round(420 + 290 * math.cos(angle), 2)
        y = round(360 + 250 * math.sin(angle), 2)
        coords[n] = {"x": x, "y": y}

    payload = {"nodes": [{"id": n, **coords[n]} for n in nodes], "edges": edges, "exporters": exporters}

    html = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>Security Dependency Graph</title>
<style>
body {{ font-family: Inter, system-ui, sans-serif; margin: 0; background: #0e1117; color: #e6edf3; }}
.wrap {{ display: grid; grid-template-columns: 2fr 1fr; gap: 12px; padding: 12px; }}
.panel {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; }}
svg {{ width: 100%; height: 720px; background: #0b0f14; border-radius: 8px; }}
.node {{ fill: #58a6ff; stroke: #c9d1d9; stroke-width: 1; }}
.exporter {{ fill: #ffa657; }}
.edge {{ stroke: #8b949e; stroke-opacity: 0.5; }}
label, select {{ font-size: 14px; }}
small {{ color: #8b949e; }}
</style></head>
<body>
<div class='wrap'>
  <div class='panel'>
    <h2>Arms Trade Influence Network (2019-2023 sample)</h2>
    <svg id='graph' viewBox='0 0 840 720'></svg>
    <p><small>Edge thickness scales with TIV. Remove an exporter to estimate immediate procurement shock.</small></p>
  </div>
  <div class='panel'>
    <h3>Shock Simulator</h3>
    <label for='exp'>Remove exporter:</label>
    <select id='exp'></select>
    <div id='results'></div>
    <h3>Top exporters by weighted outflow</h3>
    <ol>
      {''.join(f"<li>{k}: {v:,.0f}</li>" for k, v in metrics['exporter_total'].items()[:8]) if False else ''}
    </ol>
  </div>
</div>
<script>
const data = {json.dumps(payload)};
const metrics = {json.dumps(metrics)};
const svg = document.getElementById('graph');
const NS = 'http://www.w3.org/2000/svg';
const exporters = new Set(data.exporters);

function draw(hiddenExporter='') {{
  svg.innerHTML = '';
  for (const e of data.edges) {{
    if (hiddenExporter && e.exporter === hiddenExporter) continue;
    const s = data.nodes.find(n => n.id === e.exporter);
    const t = data.nodes.find(n => n.id === e.importer);
    const line = document.createElementNS(NS,'line');
    line.setAttribute('x1', s.x); line.setAttribute('y1', s.y);
    line.setAttribute('x2', t.x); line.setAttribute('y2', t.y);
    line.setAttribute('class','edge');
    line.setAttribute('stroke-width', Math.max(1, e.tiv / 1200));
    line.appendChild(document.createTitle(`$${{e.exporter}} → ${{e.importer}} | TIV ${{e.tiv}}`));
    svg.appendChild(line);
  }}

  for (const n of data.nodes) {{
    const g = document.createElementNS(NS,'g');
    const c = document.createElementNS(NS,'circle');
    c.setAttribute('cx', n.x); c.setAttribute('cy', n.y);
    c.setAttribute('r', exporters.has(n.id) ? 8 : 6);
    c.setAttribute('class', exporters.has(n.id) ? 'node exporter' : 'node');
    if (n.id === hiddenExporter) c.setAttribute('opacity', '0.2');
    const title = document.createElementNS(NS,'title');
    title.textContent = n.id;
    c.appendChild(title);
    const t = document.createElementNS(NS,'text');
    t.setAttribute('x', n.x + 10); t.setAttribute('y', n.y + 4);
    t.setAttribute('font-size', '11'); t.setAttribute('fill', '#c9d1d9');
    t.textContent = n.id;
    g.appendChild(c); g.appendChild(t); svg.appendChild(g);
  }}
}}

function simulate(exporter) {{
  const impacted = [];
  const importerLoss = {{}};
  for (const e of data.edges) {{
    if (!importerLoss[e.importer]) importerLoss[e.importer] = {{lost:0,total:0}};
    importerLoss[e.importer].total += e.tiv;
    if (e.exporter === exporter) importerLoss[e.importer].lost += e.tiv;
  }}
  Object.entries(importerLoss).forEach(([imp,v]) => {{
    if (v.lost > 0) impacted.push([imp, (v.lost / v.total)]);
  }});
  impacted.sort((a,b)=>b[1]-a[1]);
  const top = impacted.slice(0,12).map(x=>`<li>${{x[0]}}: ${{(x[1]*100).toFixed(1)}}% import pipeline removed</li>`).join('');
  document.getElementById('results').innerHTML = `<p><strong>${{impacted.length}}</strong> importers lose active supply lines.</p><ol>${{top}}</ol>`;
}}

const sel = document.getElementById('exp');
for (const e of data.exporters) {{
  const o = document.createElement('option'); o.value=e; o.textContent=e; sel.appendChild(o);
}}
sel.addEventListener('change', () => {{ draw(sel.value); simulate(sel.value); }});
sel.value = 'Russia'; draw('Russia'); simulate('Russia');
</script></body></html>
"""
    output.write_text(html)


def save_exporter_shift_svg(trends, output):
    exporters = ["United States", "Russia", "China", "France"]
    maxv = max(trends[e][p] for e in exporters for p in ("2014-2018", "2019-2023"))
    w, h = 920, 480
    bar_w = 70
    gap = 40
    left = 80
    baseline = 400

    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>",
             "<rect width='100%' height='100%' fill='#0b0f14'/>",
             "<text x='80' y='40' fill='#e6edf3' font-size='24' font-family='Arial'>Major Exporter TIV Shift: 2014-2018 vs 2019-2023</text>"]

    for i, exp in enumerate(exporters):
        x0 = left + i * (2 * bar_w + gap + 70)
        v1 = trends[exp]["2014-2018"]
        v2 = trends[exp]["2019-2023"]
        h1 = (v1 / maxv) * 280
        h2 = (v2 / maxv) * 280
        parts.append(f"<rect x='{x0}' y='{baseline-h1:.1f}' width='{bar_w}' height='{h1:.1f}' fill='#58a6ff'/>")
        parts.append(f"<rect x='{x0+bar_w+8}' y='{baseline-h2:.1f}' width='{bar_w}' height='{h2:.1f}' fill='#ffa657'/>")
        parts.append(f"<text x='{x0}' y='{baseline+22}' fill='#c9d1d9' font-size='12' font-family='Arial'>{exp}</text>")
        pct = ((v2-v1)/v1)*100
        parts.append(f"<text x='{x0}' y='{baseline-h2-8:.1f}' fill='#e6edf3' font-size='11' font-family='Arial'>{pct:+.0f}%</text>")

    parts.append("<text x='80' y='450' fill='#8b949e' font-size='12' font-family='Arial'>Blue: 2014-2018 | Orange: 2019-2023 (TIV)</text>")
    parts.append("</svg>")
    output.write_text("\n".join(parts))


def save_china_footprint_svg(rows, output):
    regions = ["africa", "south_america", "asia_pacific"]
    colors = {"africa": "#58a6ff", "south_america": "#ffa657", "asia_pacific": "#3fb950"}
    years = [r["year"] for r in rows]
    vals = {reg: [r[reg] for r in rows] for reg in regions}

    min_y, max_y = min(min(v) for v in vals.values()), max(max(v) for v in vals.values())
    w, h = 920, 500
    left, top, right, bottom = 80, 60, 40, 70
    plot_w = w - left - right
    plot_h = h - top - bottom

    def x(year):
        return left + (year - years[0]) / (years[-1] - years[0]) * plot_w

    def y(v):
        return top + (max_y - v) / (max_y - min_y) * plot_h

    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>",
             "<rect width='100%' height='100%' fill='#0b0f14'/>",
             "<text x='80' y='36' fill='#e6edf3' font-size='24' font-family='Arial'>China's Export Footprint Growth (TIV)</text>"]

    for yr in years:
        xx = x(yr)
        parts.append(f"<line x1='{xx:.1f}' y1='{top}' x2='{xx:.1f}' y2='{top+plot_h}' stroke='#21262d' stroke-width='1'/>")
        parts.append(f"<text x='{xx-12:.1f}' y='{h-36}' fill='#8b949e' font-size='11' font-family='Arial'>{yr}</text>")

    for reg in regions:
        pts = " ".join(f"{x(yr):.1f},{y(v):.1f}" for yr, v in zip(years, vals[reg]))
        parts.append(f"<polyline points='{pts}' fill='none' stroke='{colors[reg]}' stroke-width='3'/>")
        parts.append(f"<text x='{w-220}' y='{top+25*regions.index(reg)}' fill='{colors[reg]}' font-size='13' font-family='Arial'>{reg.replace('_',' ').title()}</text>")

    parts.append("</svg>")
    output.write_text("\n".join(parts))


def write_metrics_json(metrics, output):
    output.write_text(json.dumps(metrics, indent=2))


def platform_summary(platform_rows):
    out = {}
    for supplier in sorted({r["supplier"] for r in platform_rows}):
        subset = [r for r in platform_rows if r["supplier"] == supplier]
        by_platform = defaultdict(int)
        by_recipient = defaultdict(int)
        for r in subset:
            by_platform[r["platform"]] += r["units"]
            by_recipient[r["recipient"]] += r["units"]
        out[supplier] = {
            "total_units": sum(r["units"] for r in subset),
            "distinct_platforms": len(by_platform),
            "distinct_recipients": len(by_recipient),
            "platforms": dict(sorted(by_platform.items(), key=lambda x: x[1], reverse=True)),
            "recipients": dict(sorted(by_recipient.items(), key=lambda x: x[1], reverse=True)),
        }
    return out


def save_supplier_scale_svg(summary, output):
    suppliers = ["United States", "Russia", "France", "China"]
    max_units = max(summary[s]["total_units"] for s in suppliers)
    max_platforms = max(summary[s]["distinct_platforms"] for s in suppliers)

    w, h = 1320, 640
    left, baseline = 120, 520
    bar_w, group_gap = 95, 130
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>",
        "<rect width='100%' height='100%' fill='#0b0f14'/>",
        "<text x='120' y='48' fill='#e6edf3' font-size='28' font-family='Arial'>Major Supplier Scale and Breadth (2019-2023 platform sample)</text>",
        "<text x='120' y='76' fill='#8b949e' font-size='14' font-family='Arial'>Orange = units exported | Blue = distinct platforms. Expanded dimensions to avoid clipping.</text>",
    ]
    for i, s in enumerate(suppliers):
        x0 = left + i * (2 * bar_w + group_gap)
        units = summary[s]["total_units"]
        plats = summary[s]["distinct_platforms"]
        hu = (units / max_units) * 340
        hp = (plats / max_platforms) * 250
        parts.append(f"<rect x='{x0}' y='{baseline-hu:.1f}' width='{bar_w}' height='{hu:.1f}' rx='4' fill='#ffa657'/>")
        parts.append(f"<rect x='{x0+bar_w+12}' y='{baseline-hp:.1f}' width='{bar_w}' height='{hp:.1f}' rx='4' fill='#58a6ff'/>")
        parts.append(f"<text x='{x0-2}' y='{baseline+30}' fill='#c9d1d9' font-size='15' font-family='Arial'>{s}</text>")
        parts.append(f"<text x='{x0-2}' y='{baseline-hu-10:.1f}' fill='#e6edf3' font-size='12' font-family='Arial'>{units:,} units</text>")
        parts.append(f"<text x='{x0+bar_w+12}' y='{baseline-hp-10:.1f}' fill='#e6edf3' font-size='12' font-family='Arial'>{plats} platforms</text>")
    parts.append("</svg>")
    output.write_text("\n".join(parts))


def save_supplier_recipient_heatmap_svg(platform_rows, output):
    suppliers = ["United States", "Russia", "France", "China"]
    by_sr = defaultdict(int)
    for r in platform_rows:
        by_sr[(r["supplier"], r["recipient"])] += r["units"]

    rec_tot = defaultdict(int)
    for (s, rec), v in by_sr.items():
        if s in suppliers:
            rec_tot[rec] += v
    top_recipients = [k for k, _ in sorted(rec_tot.items(), key=lambda x: x[1], reverse=True)[:24]]

    max_v = max(by_sr.get((s, r), 0) for s in suppliers for r in top_recipients) or 1
    cw, ch = 72, 52
    left, top = 300, 230
    w = left + len(top_recipients) * cw + 120
    h = top + len(suppliers) * ch + 140
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}'>",
        "<rect width='100%' height='100%' fill='#0b0f14'/>",
        "<text x='70' y='48' fill='#e6edf3' font-size='30' font-family='Arial'>Major Supplier × Recipient Matrix (units, 2019-2023 platform sample)</text>",
        "<text x='70' y='78' fill='#8b949e' font-size='14' font-family='Arial'>Darker cells indicate higher unit concentration; dimensions expanded to avoid label clipping.</text>",
    ]
    for i, rec in enumerate(top_recipients):
        tx = left + i * cw + 16
        ty = top - 18
        parts.append(f"<text x='{tx}' y='{ty}' fill='#8b949e' font-size='11' font-family='Arial' transform='rotate(-48 {tx},{ty})'>{rec}</text>")
    for j, s in enumerate(suppliers):
        yy = top + j * ch + 32
        parts.append(f"<text x='80' y='{yy}' fill='#c9d1d9' font-size='16' font-family='Arial'>{s}</text>")
        for i, rec in enumerate(top_recipients):
            v = by_sr.get((s, rec), 0)
            alpha = 0.08 + (v / max_v) * 0.92
            color = f"rgba(88,166,255,{alpha:.3f})" if v > 0 else "rgba(139,148,158,0.06)"
            x = left + i * cw
            y = top + j * ch
            parts.append(f"<rect x='{x}' y='{y}' width='{cw-6}' height='{ch-6}' rx='4' fill='{color}'/>")
            if v > 0:
                parts.append(f"<text x='{x+10}' y='{y+30}' fill='#e6edf3' font-size='12' font-family='Arial'>{v}</text>")
    parts.append("</svg>")
    output.write_text("\n".join(parts))


def main():
    edges = load_edges(DATA / "arms_transfers_sample_2019_2023.csv")
    trends = load_export_trends(DATA / "exporter_period_totals_tiv.csv")
    china = load_china_series(DATA / "china_regional_footprint_tiv.csv")
    platform_rows = load_platform_rows(DATA / "platform_exports_major_suppliers_2019_2023.csv")

    metrics = calculate_metrics(edges)
    save_network_html(edges, metrics, VIS / "security_dependency_graph.html")
    save_exporter_shift_svg(trends, VIS / "exporter_shift.svg")
    save_china_footprint_svg(china, VIS / "china_footprint.svg")
    write_metrics_json(metrics, VIS / "network_metrics.json")
    platform = platform_summary(platform_rows)
    write_metrics_json(platform, VIS / "platform_supplier_summary.json")
    save_supplier_scale_svg(platform, VIS / "supplier_scale.svg")
    save_supplier_recipient_heatmap_svg(platform_rows, VIS / "supplier_recipient_heatmap.svg")
    print("Wrote visuals and metrics to /visuals")


if __name__ == "__main__":
    main()
