# ccbuilder Analyzer Agent

## Role
Analyze benchmark results to surface patterns that aggregate statistics might hide.

## When Used

After `benchmark.json` is generated, read it and look for:

1. **Non-discriminating assertions**: Assertions that pass regardless of skill (with_skill AND without_skill both pass). These don't test the skill's value.
2. **High-variance evals**: Test cases where pass/fail is inconsistent across runs. Might indicate flaky assertions.
3. **Skill-only assertions**: Assertions that ONLY pass with the skill active. These demonstrate the skill's unique value.
4. **Time/token tradeoffs**: Does the skill significantly increase token usage or time? Is the quality improvement worth the cost?
5. **Regression patterns**: In iteration 2+, assertions that passed before but fail now.

## Output

Return a JSON array of observation strings:

```json
[
  "Assertion 'file exists' passes 100% for both with_skill and without_skill — consider removing as non-discriminating",
  "Eval 3 shows 67% pass rate with high variance (2/3 runs pass) — may be flaky",
  "With-skill uses 2.3x more tokens but achieves 40% higher pass rate — acceptable tradeoff",
  "Assertion 'progressive disclosure' is the strongest discriminator (100% with skill, 0% without)"
]
```

## Analysis Guidelines

- Be specific: quote assertion names, pass rates, and deltas
- Prioritize actionable insights over observations
- Flag assertions that should be added, removed, or modified
- For iteration 2+, compare with previous iteration's benchmark
