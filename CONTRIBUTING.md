# Contributing to promptlint

Thanks for helping make prompt code safer! Contributions of all sizes are welcome.

## Dev setup

No dependencies are required to run or test promptlint (pure stdlib).

```bash
git clone https://github.com/pop123-ux/promptlint.git
cd promptlint
python tests/test_rules.py        # or: python -m pytest
python -m promptlint examples/    # try it on the examples
```

## Adding a rule

1. Add a `PLxxx` entry to `RULES` in `promptlint/core.py` with a `(severity, message)`.
2. Implement the detection in `lint_text` (line-based or block/regex).
3. Keep it **high-signal** — prefer a few precise patterns over broad ones that nag.
4. Add a passing-and-failing test pair in `tests/test_rules.py`.
5. Document the rule in the README table.

## Guidelines

- High signal beats high coverage. A noisy linter gets disabled.
- No runtime dependencies — keep it stdlib-only.
- Never put real secrets in examples or tests; use obvious fakes.
- Severities: `error` should block a commit/CI; `warning`/`info` should not by default.

## Reporting issues

Found a false positive, false negative, or have a rule idea? Open an issue with a small code snippet that reproduces it.
