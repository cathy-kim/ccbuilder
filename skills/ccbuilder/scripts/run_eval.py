#!/usr/bin/env python3
"""
Skill trigger detection evaluator.

Tests whether a skill's description causes Claude to invoke the skill
for a given query. Uses `claude -p` with stream-json output.

Usage:
    python -m scripts.run_eval \
        --eval-set trigger-eval.json \
        --skill-path /path/to/skill \
        --model claude-sonnet-4-6
"""

import argparse
import json
import os
import subprocess
import uuid
from pathlib import Path

from .utils import parse_skill_md


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    model: str,
    timeout: int = 30,
) -> bool:
    """Run a single query and detect if the skill triggers."""
    # Create a temporary command file with the skill description
    unique_name = f"{skill_name}-skill-{uuid.uuid4().hex[:8]}"
    # Find .claude/commands dir (create if needed)
    commands_dir = Path.home() / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    cmd_file = commands_dir / f"{unique_name}.md"

    try:
        cmd_file.write_text(
            f"---\ndescription: {skill_description}\n---\n\nThis is a test skill.\n",
            encoding="utf-8",
        )

        # Run claude -p with stream-json
        env = os.environ.copy()
        env.pop("CLAUDECODE", None)  # Allow nesting

        cmd = [
            "claude",
            "-p",
            query,
            "--output-format",
            "stream-json",
            "--verbose",
        ]
        if model:
            cmd.extend(["--model", model])

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
        )

        triggered = False
        try:
            stdout, _ = proc.communicate(timeout=timeout)
            for line in stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    # Check for tool_use with Skill or Read targeting our skill
                    if event.get("type") == "content_block_start":
                        cb = event.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            tool_name = cb.get("name", "")
                            if tool_name == "Skill" or (
                                tool_name == "Read"
                                and unique_name in str(cb)
                            ):
                                triggered = True
                                break
                    # Check deltas for skill name mention
                    if event.get("type") == "content_block_delta":
                        delta = event.get("delta", {})
                        if unique_name in str(delta):
                            triggered = True
                            break
                except json.JSONDecodeError:
                    continue
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            return False

        return triggered
    finally:
        cmd_file.unlink(missing_ok=True)


def run_eval(
    eval_set: list[dict],
    skill_path: str,
    model: str,
    num_workers: int = 10,
    timeout: int = 30,
    runs_per_query: int = 3,
    trigger_threshold: float = 0.5,
    description: str | None = None,
    verbose: bool = False,
) -> dict:
    """Run the full trigger evaluation."""
    skill_name, skill_desc, _ = parse_skill_md(Path(skill_path) / "SKILL.md")
    if description:
        skill_desc = description

    results = []

    for item in eval_set:
        query = item["query"]
        should_trigger = item["should_trigger"]

        trigger_count = 0
        for _ in range(runs_per_query):
            if run_single_query(query, skill_name, skill_desc, model, timeout):
                trigger_count += 1

        trigger_rate = trigger_count / runs_per_query
        passed = (trigger_rate >= trigger_threshold) == should_trigger

        results.append(
            {
                "query": query,
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "trigger_count": trigger_count,
                "runs": runs_per_query,
                "passed": passed,
            }
        )

        if verbose:
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] [{trigger_rate:.0%}] {query[:60]}...")

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
    }

    return {
        "skill_name": skill_name,
        "description": skill_desc,
        "results": results,
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Skill trigger detection evaluator"
    )
    parser.add_argument(
        "--eval-set", required=True, help="Path to trigger eval JSON"
    )
    parser.add_argument(
        "--skill-path", required=True, help="Path to skill directory"
    )
    parser.add_argument("--description", help="Override skill description")
    parser.add_argument(
        "--model", default="claude-sonnet-4-6", help="Model ID"
    )
    parser.add_argument("--num-workers", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    with open(args.eval_set, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    result = run_eval(
        eval_set=eval_set,
        skill_path=args.skill_path,
        model=args.model,
        num_workers=args.num_workers,
        timeout=args.timeout,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        description=args.description,
        verbose=args.verbose,
    )

    print(
        f"\n=== Results: {result['summary']['passed']}/{result['summary']['total']} passed ==="
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
