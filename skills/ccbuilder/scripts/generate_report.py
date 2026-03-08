#!/usr/bin/env python3
"""
Generate live HTML report for description optimization loop.

Produces a self-contained HTML file with:
- Summary: original vs best description, scores
- Table: one row per iteration, columns = each query, cells show trigger rate
- Color coding: green/orange/red by score; blue for test queries

Usage:
    Called internally by run_loop.py, or:
    python -m scripts.generate_report results.json --output report.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def generate_report(
    history: list[dict],
    eval_set: list[dict],
    train_indices: list[int],
    test_indices: list[int],
    skill_name: str = "unknown",
    best_iteration: int | None = None,
    auto_refresh: bool = False,
) -> str:
    """Generate the optimization report HTML."""
    refresh_tag = '<meta http-equiv="refresh" content="5">' if auto_refresh else ""

    # Build query headers
    query_headers = ""
    for i, item in enumerate(eval_set):
        is_test = i in test_indices
        trigger_class = "should-trigger" if item["should_trigger"] else "should-not-trigger"
        bg = "background:#1c3a5c;" if is_test else ""
        short = item["query"][:40] + "..." if len(item["query"]) > 40 else item["query"]
        query_headers += f'<th style="{bg}" class="{trigger_class}" title="{item["query"]}">{short}</th>'

    # Build rows
    rows = ""
    for entry in history:
        it = entry["iteration"]
        is_best = it == best_iteration
        row_style = "background:#1a2e1a;" if is_best else ""
        rows += f'<tr style="{row_style}"><td>{it}{"*" if is_best else ""}</td>'
        rows += f'<td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;" title="{entry["description"]}">{entry["description"][:50]}...</td>'
        rows += f'<td>{entry.get("train_score", "?")}</td>'
        rows += f'<td>{entry.get("test_score", "?")}</td>'

        # Per-query results if available
        for result in entry.get("per_query_results", []):
            rate = result.get("trigger_rate", 0)
            count = result.get("trigger_count", 0)
            total = result.get("runs", 3)
            color = "#3fb950" if rate >= 0.8 else "#d29922" if rate >= 0.5 else "#f85149"
            is_test_q = result.get("is_test", False)
            bg = "background:rgba(28,58,92,0.3);" if is_test_q else ""
            icon = "\u2713" if result.get("passed", False) else "\u2717"
            rows += f'<td style="{bg}color:{color}">{icon} {count}/{total}</td>'

        rows += "</tr>"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
{refresh_tag}
<title>{skill_name} — Description Optimization</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; padding: 24px; }}
h1 {{ color: #58a6ff; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 16px; font-size: 12px; }}
th, td {{ padding: 8px 12px; border: 1px solid #30363d; text-align: left; }}
th {{ background: #1c2128; color: #8b949e; position: sticky; top: 0; }}
.should-trigger {{ text-decoration: underline; text-decoration-color: #3fb950; }}
.should-not-trigger {{ text-decoration: underline; text-decoration-color: #f85149; }}
.legend {{ display: flex; gap: 16px; margin: 12px 0; font-size: 13px; color: #8b949e; }}
.legend span {{ padding: 2px 8px; border-radius: 4px; }}
</style>
</head>
<body>
<h1>{skill_name} — Description Optimization</h1>
<div class="legend">
  <span style="text-decoration:underline;text-decoration-color:#3fb950;">Should trigger</span>
  <span style="text-decoration:underline;text-decoration-color:#f85149;">Should NOT trigger</span>
  <span style="background:#1c3a5c;">Test set (holdout)</span>
  <span style="background:#1a2e1a;">* = Best iteration</span>
</div>
<table>
<thead>
<tr>
<th>Iter</th><th>Description</th><th>Train</th><th>Test</th>
{query_headers}
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_json", help="Path to loop results JSON")
    parser.add_argument("--output", "-o", default="report.html")
    args = parser.parse_args()

    with open(args.results_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_report(
        history=data.get("history", []),
        eval_set=[],
        train_indices=[],
        test_indices=[],
        skill_name=data.get("skill_name", "unknown"),
    )

    Path(args.output).write_text(html, encoding="utf-8")
    print(f"Report written to: {args.output}")


if __name__ == "__main__":
    main()
