<div align="center">

# 🧹 promptlint

**ESLint for your LLM prompts.**

You lint your code. Why not the prompts your code sends to the model?
`promptlint` is a tiny, zero-dependency linter that catches **prompt-injection risks, missing token limits, hardcoded secrets, and prompt anti-patterns** — before they ship.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)
![Pre-commit](https://img.shields.io/badge/pre--commit-ready-orange)

⭐ **If this catches even one bug for you, star the repo so others find it.**

![promptlint demo](demo/promptlint-demo.gif)

</div>

---

## Why?

Prompts are code now — but nothing checks them. The same string gets shipped with user input glued straight into it (hello, prompt injection), no `max_tokens` (hello, surprise bill), and a hardcoded `sk-...` key two lines up. `promptlint` is the linter for exactly that.

```text
$ promptlint app.py
app.py:6:1:  PL003 error    Hardcoded API key/secret — move it to an environment variable.
app.py:11:1: PL001 warning  Untrusted input is interpolated into a prompt — delimit or validate it.
app.py:19:1: PL002 warning  LLM call has no token limit (max_tokens) — set one to cap cost.
app.py:20:1: PL005 info     Hardcoded model id — centralize it in config so models are easy to swap.

promptlint: 4 issue(s) in 1 file(s) — 1 error, 2 warning, 1 info
```

## Install

```bash
pip install llm-promptlint
```

> The PyPI package is **`llm-promptlint`** (the name `promptlint` was taken); the command and import stay `promptlint`.

Or run straight from source (no dependencies, pure stdlib):

```bash
git clone https://github.com/pop123-ux/promptlint.git
cd promptlint && python -m promptlint path/to/your/code
```

## Usage

```bash
promptlint .                       # lint the current project
promptlint app.py prompts/         # lint specific files/dirs
promptlint . --strict              # fail on warnings too (great for CI)
promptlint . --select PL001,PL003  # only these rules
promptlint . --ignore PL005        # everything except this rule
promptlint --list-rules            # show all rules
```

Exit code is **1** when any `error` is found (or any finding with `--strict`), so it drops straight into CI and git hooks.

### Suppress a line

```python
api_key = "sk-..."  # promptlint: disable=PL003
prompt = f"..."     # promptlint: disable   (silences all rules on this line)
```

## The rules

| Code | Severity | Catches |
|------|----------|---------|
| **PL001** | warning | Untrusted input (`user_input`, `request.*`, `argv`, …) interpolated/concatenated into a prompt — **prompt-injection risk**. |
| **PL002** | warning | LLM completion call with **no `max_tokens`** — uncapped cost and output. |
| **PL003** | error | **Hardcoded API key/secret** (`sk-`, `sk-ant-`, `AIza…`, `ghp_…`, …). |
| **PL004** | warning | Long prompt with **no output-format instruction** (no JSON/schema/structure). |
| **PL005** | info | **Hardcoded model id** (`gpt-…`, `claude-…`, `gemini-…`) instead of config. |
| **PL006** | info | `messages[]` with a user role but **no system role**. |

High-signal by design — it flags the mistakes that actually ship, not stylistic noise. Works on Python, JS/TS, and any text/prompt files.

## Use as a pre-commit hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pop123-ux/promptlint
    rev: v0.1.0
    hooks:
      - id: promptlint
```

Now every commit is scanned, and insecure prompts never make it in.

## Use in CI (GitHub Actions)

```yaml
- uses: actions/setup-python@v5
  with: { python-version: "3.x" }
- run: pip install llm-promptlint
- run: promptlint . --strict
```

## Roadmap

- Config via `pyproject.toml` (`[tool.promptlint]`)
- More rules: temperature sanity, retry/backoff, PII in prompts, system-prompt leakage
- JSON output (`--format json`) for dashboards
- Per-rule auto-fix suggestions

PRs welcome — see [CONTRIBUTING](CONTRIBUTING.md). New rule ideas are especially appreciated.

## License

[MIT](LICENSE)

---

<div align="center">

Built by [**@pop123-ux**](https://github.com/pop123-ux) · Lint your prompts. Ship with confidence. ⭐

</div>
