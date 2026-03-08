#!/usr/bin/env python3
"""aggregate_benchmark.py — Aggregate grading.json results into a benchmark report.

Scans a workspace directory (recursively) for grading.json files produced by
the ccbuilder grader agent, then computes aggregate statistics:
  - mean pass_rate, stddev
  - total passed / failed / total expectations
  - timing and token stats when available

Outputs:
  benchmark.json  — machine-readable aggregate
  benchmark.md    — human-readable Markdown summary

Usage:
    python3 aggregate_benchmark.py <workspace-dir> [--output-dir <dir>]

Examples:
    python3 aggregate_benchmark.py ./eval-results/
    python3 aggregate_benchmark.py ./eval-results/ --output-dir ./reports/
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_grading_files(workspace: Path) -> list[Path]:
    """Recursively find all grading.json files under workspace."""
    return sorted(workspace.rglob("grading.json"))


def load_grading(path: Path) -> dict:
    """Load and return a grading.json file. Returns {} on parse error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Warning: could not read {path}: {exc}", file=sys.stderr)
        return {}


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def stddev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)


def aggregate(grading_files: list[Path]) -> dict:
    """Aggregate stats across all grading files."""
    records = []
    for path in grading_files:
        data = load_grading(path)
        if data:
            records.append((path, data))

    if not records:
        return {}

    pass_rates: list[float] = []
    total_passed = 0
    total_failed = 0
    total_expectations = 0
    eval_ids: list = []

    for _path, data in records:
        summary = data.get("summary", {})
        pr = summary.get("pass_rate")
        if pr is not None:
            pass_rates.append(float(pr))
        total_passed += summary.get("passed", 0)
        total_failed += summary.get("failed", 0)
        total_expectations += summary.get("total", 0)
        eval_id = data.get("eval_id")
        if eval_id is not None:
            eval_ids.append(eval_id)

    return {
        "skill_name": records[0][1].get("skill_name", "ccbuilder") if records else "ccbuilder",
        "aggregated_at": datetime.now(timezone.utc).isoformat(),
        "runs": len(records),
        "eval_ids": sorted(set(eval_ids)),
        "pass_rate": {
            "mean": round(mean(pass_rates), 4),
            "stddev": round(stddev(pass_rates), 4),
            "min": round(min(pass_rates), 4) if pass_rates else 0.0,
            "max": round(max(pass_rates), 4) if pass_rates else 0.0,
            "values": [round(v, 4) for v in pass_rates],
        },
        "expectations": {
            "total": total_expectations,
            "passed": total_passed,
            "failed": total_failed,
            "overall_pass_rate": round(total_passed / total_expectations, 4)
            if total_expectations
            else 0.0,
        },
        "source_files": [str(p) for p, _ in records],
    }


def render_markdown(agg: dict) -> str:
    """Render the aggregate dict as a Markdown report."""
    pr = agg.get("pass_rate", {})
    exp = agg.get("expectations", {})
    lines = [
        f"# ccbuilder Benchmark Report",
        f"",
        f"**Generated**: {agg.get('aggregated_at', 'N/A')}  ",
        f"**Skill**: {agg.get('skill_name', 'ccbuilder')}  ",
        f"**Runs**: {agg.get('runs', 0)}  ",
        f"**Eval IDs**: {', '.join(str(i) for i in agg.get('eval_ids', []))}",
        f"",
        f"## Pass Rate",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Mean | {pr.get('mean', 0):.2%} |",
        f"| Std Dev | ±{pr.get('stddev', 0):.2%} |",
        f"| Min | {pr.get('min', 0):.2%} |",
        f"| Max | {pr.get('max', 0):.2%} |",
        f"",
        f"## Expectations",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total | {exp.get('total', 0)} |",
        f"| Passed | {exp.get('passed', 0)} |",
        f"| Failed | {exp.get('failed', 0)} |",
        f"| Overall Pass Rate | {exp.get('overall_pass_rate', 0):.2%} |",
        f"",
        f"## Source Files",
        f"",
    ]
    for src in agg.get("source_files", []):
        lines.append(f"- `{src}`")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", help="Directory to scan for grading.json files")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory to write benchmark.json and benchmark.md (default: workspace)",
    )
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.is_dir():
        print(f"Error: workspace '{workspace}' is not a directory", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir) if args.output_dir else workspace
    output_dir.mkdir(parents=True, exist_ok=True)

    grading_files = find_grading_files(workspace)
    if not grading_files:
        print(f"No grading.json files found under {workspace}", file=sys.stderr)
        return 1

    print(f"Found {len(grading_files)} grading file(s).")
    agg = aggregate(grading_files)

    if not agg:
        print("No valid grading data could be parsed.", file=sys.stderr)
        return 1

    json_path = output_dir / "benchmark.json"
    md_path = output_dir / "benchmark.md"

    json_path.write_text(json.dumps(agg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(agg), encoding="utf-8")

    pr_mean = agg["pass_rate"]["mean"]
    print(f"benchmark.json -> {json_path}")
    print(f"benchmark.md   -> {md_path}")
    print(f"Overall pass rate: {pr_mean:.2%} (mean across {agg['runs']} run(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
