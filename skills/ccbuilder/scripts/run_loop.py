#!/usr/bin/env python3
"""
Skill description optimization loop.

Iteratively improves a skill's description for better trigger accuracy.
Uses train/test split to prevent overfitting.

Usage:
    python -m scripts.run_loop \
        --eval-set trigger-eval.json \
        --skill-path /path/to/skill \
        --model claude-sonnet-4-6 \
        --max-iterations 5
"""

import argparse
import json
import os
import random
import subprocess
from pathlib import Path

from .utils import parse_skill_md


def split_eval_set(
    eval_set: list[dict],
    holdout: float = 0.4,
    seed: int = 42,
) -> tuple[list[dict], list[dict]]:
    """Stratified train/test split by should_trigger."""
    rng = random.Random(seed)

    positives = [e for e in eval_set if e["should_trigger"]]
    negatives = [e for e in eval_set if not e["should_trigger"]]

    rng.shuffle(positives)
    rng.shuffle(negatives)

    def split_group(group):
        n_test = max(1, int(len(group) * holdout))
        return group[n_test:], group[:n_test]

    train_pos, test_pos = split_group(positives)
    train_neg, test_neg = split_group(negatives)

    return train_pos + train_neg, test_pos + test_neg


def improve_description(
    current_desc: str,
    skill_content: str,
    failures: list[dict],
    history: list[dict],
    model: str,
) -> str:
    """Call claude -p to generate an improved description."""
    missed = [f for f in failures if f["should_trigger"] and not f["passed"]]
    false_triggers = [
        f for f in failures if not f["should_trigger"] and not f["passed"]
    ]

    prompt = f"""You are optimizing a Claude Code skill's description field for better triggering accuracy.

Current description:
{current_desc}

Missed triggers (should have triggered but didn't):
{json.dumps(missed, indent=2, ensure_ascii=False) if missed else "None"}

False triggers (should NOT have triggered but did):
{json.dumps(false_triggers, indent=2, ensure_ascii=False) if false_triggers else "None"}

Previous attempts (test scores hidden to prevent overfitting):
{json.dumps(history, indent=2, ensure_ascii=False) if history else "None"}

Full SKILL.md for context:
{skill_content[:3000]}

Rules:
- Stay under 1024 characters
- Use imperative form ("Use this skill for...")
- Focus on user intent, not implementation
- Make the description distinctive vs other skills
- Change structure across iterations, not just wording
- Generalize — don't overfit to the specific failing queries

Output ONLY the new description between <new_description> tags."""

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    cmd = ["claude", "-p", prompt, "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])

    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env, timeout=60
    )

    output = result.stdout
    if "<new_description>" in output and "</new_description>" in output:
        desc = (
            output.split("<new_description>")[1]
            .split("</new_description>")[0]
            .strip()
        )
        if len(desc) > 1024:
            # Ask for shorter version
            trim_cmd = [
                "claude",
                "-p",
                f"This description is {len(desc)} chars, max is 1024. "
                f"Shorten it while keeping the meaning:\n{desc}",
                "--output-format",
                "text",
            ]
            if model:
                trim_cmd.extend(["--model", model])
            trim_result = subprocess.run(
                trim_cmd, capture_output=True, text=True, env=env, timeout=30
            )
            desc = trim_result.stdout.strip()[:1024]
        return desc
    return current_desc


def run_loop(
    eval_set: list[dict],
    skill_path: str,
    model: str,
    max_iterations: int = 5,
    runs_per_query: int = 3,
    trigger_threshold: float = 0.5,
    holdout: float = 0.4,
    timeout: int = 30,
    verbose: bool = False,
) -> dict:
    """Run the optimization loop."""
    from .run_eval import run_eval

    skill_name, original_desc, skill_content = parse_skill_md(
        Path(skill_path) / "SKILL.md"
    )
    train_set, test_set = split_eval_set(eval_set, holdout=holdout)

    if verbose:
        print(f"Train: {len(train_set)} queries, Test: {len(test_set)} queries")

    current_desc = original_desc
    history: list[dict] = []
    best_desc = original_desc
    best_test_score = -1
    iteration = 0

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n=== Iteration {iteration} ===")
            print(f"Description: {current_desc[:80]}...")

        # Eval on all queries
        all_queries = train_set + test_set
        result = run_eval(
            eval_set=all_queries,
            skill_path=skill_path,
            model=model,
            timeout=timeout,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            description=current_desc,
            verbose=verbose,
        )

        # Split results back
        train_results = result["results"][: len(train_set)]
        test_results = result["results"][len(train_set) :]

        train_passed = sum(1 for r in train_results if r["passed"])
        test_passed = sum(1 for r in test_results if r["passed"])

        # Track history
        history.append(
            {
                "iteration": iteration,
                "description": current_desc,
                "train_score": f"{train_passed}/{len(train_set)}",
                "test_score": f"{test_passed}/{len(test_set)}",
            }
        )

        if verbose:
            print(
                f"  Train: {train_passed}/{len(train_set)}, "
                f"Test: {test_passed}/{len(test_set)}"
            )

        # Track best by test score
        if test_passed > best_test_score:
            best_test_score = test_passed
            best_desc = current_desc

        # Stop if train is 100%
        if train_passed == len(train_set):
            if verbose:
                print("All train queries passed!")
            break

        # Improve based on train failures only (with blinded history)
        blinded_history = [
            {
                "iteration": h["iteration"],
                "description": h["description"],
                "train_score": h["train_score"],
            }
            for h in history
        ]
        train_failures = [r for r in train_results if not r["passed"]]
        current_desc = improve_description(
            current_desc, skill_content, train_failures, blinded_history, model
        )

    return {
        "exit_reason": (
            f"all_passed (iteration {iteration})"
            if train_passed == len(train_set)
            else f"max_iterations ({max_iterations})"
        ),
        "original_description": original_desc,
        "best_description": best_desc,
        "best_test_score": f"{best_test_score}/{len(test_set)}",
        "final_description": current_desc,
        "iterations_run": iteration,
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Skill description optimization loop"
    )
    parser.add_argument(
        "--eval-set", required=True, help="Path to trigger eval JSON"
    )
    parser.add_argument(
        "--skill-path", required=True, help="Path to skill directory"
    )
    parser.add_argument("--model", required=True, help="Model ID")
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--holdout", type=float, default=0.4)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    with open(args.eval_set, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    result = run_loop(
        eval_set=eval_set,
        skill_path=args.skill_path,
        model=args.model,
        max_iterations=args.max_iterations,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        holdout=args.holdout,
        timeout=args.timeout,
        verbose=args.verbose,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
