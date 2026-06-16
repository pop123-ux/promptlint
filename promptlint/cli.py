"""Command-line interface for promptlint."""

import argparse
import os
import sys

from . import __version__
from .core import lint_text, RULES, DEFAULT_MAX_PROMPT_LENGTH

SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
    ".java", ".go", ".rb", ".rs", ".php",
    ".prompt", ".txt", ".md", ".mdx", ".yaml", ".yml",
}
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__",
    "dist", "build", ".mypy_cache", ".tox", ".idea", ".next",
}

_COLORS = {"error": "\033[31m", "warning": "\033[33m", "info": "\033[34m"}
_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"


def _iter_files(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for name in files:
                    if os.path.splitext(name)[1].lower() in SCAN_EXTENSIONS:
                        yield os.path.join(root, name)


def _color(enabled, severity, s):
    if not enabled:
        return s
    return _COLORS.get(severity, "") + s + _RESET


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:  # ensure non-ASCII output works on Windows consoles
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(
        prog="promptlint",
        description="ESLint for your LLM prompts. Catches prompt-injection risks, "
                    "missing token limits, and prompt anti-patterns.",
    )
    parser.add_argument("paths", nargs="*", default=["."],
                        help="Files or directories to lint (default: current dir).")
    parser.add_argument("--select", help="Comma-separated rule codes to check exclusively.")
    parser.add_argument("--ignore", help="Comma-separated rule codes to skip.")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on warnings/info too, not just errors.")
    parser.add_argument("--max-prompt-length", type=int, default=DEFAULT_MAX_PROMPT_LENGTH,
                        help="Min length for the PL004 long-prompt check (default: %(default)s).")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output.")
    parser.add_argument("--list-rules", action="store_true", help="Print all rules and exit.")
    parser.add_argument("--version", action="version", version="promptlint " + __version__)
    args = parser.parse_args(argv)

    if args.list_rules:
        for code, (sev, msg) in RULES.items():
            print("{}  {:<8}  {}".format(code, sev, msg))
        return 0

    select = {c.strip().upper() for c in args.select.split(",")} if args.select else None
    ignore = {c.strip().upper() for c in args.ignore.split(",")} if args.ignore else set()
    use_color = sys.stdout.isatty() and not args.no_color and os.name != "nt" or (
        not args.no_color and os.environ.get("FORCE_COLOR"))

    paths = args.paths or ["."]
    total = {"error": 0, "warning": 0, "info": 0}
    files_with_issues = 0

    for filepath in _iter_files(paths):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except (OSError, IOError):
            continue

        findings = lint_text(text, max_prompt_length=args.max_prompt_length)
        findings = [f for f in findings
                    if (select is None or f.code in select) and f.code not in ignore]
        if not findings:
            continue

        files_with_issues += 1
        for f in findings:
            total[f.severity] += 1
            loc = _color(use_color, f.severity, "{}:{}:{}".format(filepath, f.line, f.col))
            tag = _color(use_color, f.severity, "{} {}".format(f.code, f.severity))
            print("{}: {} {}".format(loc, tag, f.message))

    n = total["error"] + total["warning"] + total["info"]
    if n == 0:
        print(_color(use_color, "info", "promptlint: no issues found ✅"))
        return 0

    summary = "promptlint: {} issue(s) in {} file(s) — {} error, {} warning, {} info".format(
        n, files_with_issues, total["error"], total["warning"], total["info"])
    print(("\n" + _BOLD + summary + _RESET) if use_color else "\n" + summary)

    if total["error"] > 0 or (args.strict and n > 0):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
