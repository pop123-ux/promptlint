"""Core linting engine for promptlint.

Pure-stdlib, language-agnostic heuristics that scan source/text files for
common LLM-prompt anti-patterns. Each rule is intentionally high-signal:
the goal is to flag the mistakes that actually ship, not to nag.
"""

import re
from collections import namedtuple

Finding = namedtuple("Finding", "line col code severity message")

# code -> (severity, message)
RULES = {
    "PL001": ("warning",
              "Untrusted input is interpolated into a prompt — delimit or validate it "
              "to reduce prompt-injection risk."),
    "PL002": ("warning",
              "LLM call has no token limit (max_tokens) — set one to cap cost and "
              "runaway output."),
    "PL003": ("error",
              "Hardcoded API key/secret — move it to an environment variable."),
    "PL004": ("warning",
              "Long prompt has no output-format instruction — tell the model the "
              "expected format (JSON/schema/structure)."),
    "PL005": ("info",
              "Hardcoded model id — centralize it in config so models are easy to swap."),
    "PL006": ("info",
              "messages[] has a user role but no system role — add a system message "
              "to anchor behavior."),
}

DEFAULT_MAX_PROMPT_LENGTH = 200

_PROMPT_KW = re.compile(
    r"(?i)\b(system_prompt|system|user_prompt|prompt|instructions?|messages|content|template|query)\b"
)
_MODEL_LITERAL = re.compile(
    r"""(?ix)
    \bmodel\b \s* [:=] \s* ["']
    (gpt-|gpt4|o1|o3|o4-|claude-|claude_|gemini-|gemini_|llama|mistral|mixtral|deepseek|qwen|grok)
    """
)
# Known secret token shapes (high-signal, prefix-anchored to avoid false positives).
_SECRET = re.compile(
    r"(sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_\-]{20,}"
    r"|gsk_[A-Za-z0-9]{20,}|xai-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,})"
)
_SECRET_CTX = re.compile(r"(?i)(api[_-]?key|secret|token|authorization|bearer)")

# An f-string prefix on the line (template/JS backtick handled separately by concat rule).
_FSTRING = re.compile(r"(?<![\w])[fF][\"']")
# Untrusted input interpolated INSIDE an f-string brace, e.g. f"...{user_input}..."
_INTERP_UNTRUSTED = re.compile(
    r"\{[^{}]*(?:user_?input|request\b|req\.|sys\.argv|argv|params\b|event\[|input\s*\(|\.body|get_json)[^{}]*\}",
    re.I,
)
# Untrusted input glued on with string concatenation.
_CONCAT_UNTRUSTED = re.compile(
    r"""(?ix)
    (?: ["']\s*\+\s* | \+\s* ) (?:user_?input|request\b|req\.|argv|params\b|event\[|input\s*\()
    | (?:user_?input|request\.\w+|params\[[^\]]*\]|argv\[[^\]]*\]) \s* \+
    """
)

_LLM_CALL = re.compile(
    r"(?i)(chat\.completions\.create|messages\.create|responses\.create"
    r"|\.generate_content|\.create_message|completions\.create|\.complete\s*\()"
)
_MAX_TOKENS = re.compile(
    r"(?i)max[_]?(tokens|output_tokens)|maxoutputtokens|max_tokens_to_sample"
)
_MESSAGES_ARRAY = re.compile(r"(?i)messages\s*[:=]\s*\[")
_ROLE_USER = re.compile(r"""(?i)["']role["']\s*:\s*["']user["']""")
_ROLE_SYSTEM = re.compile(r"""(?i)["']role["']\s*:\s*["']system["']""")

_TRIPLE_STRING = re.compile(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', re.DOTALL)
_PROMPTY_WORDS = re.compile(
    r"(?i)\b(you are|act as|your task|system prompt|summar|extract|classif|translate"
    r"|rewrite|generate|answer|respond|explain|analy[sz]|write a|list the)\b"
)
_FORMAT_KW = re.compile(
    r"(?i)(\b(json|yaml|xml|markdown|format|schema|bullet points?|table|csv)\b"
    r"|step[\s-]by[\s-]step|return only|respond with|reply with|output (a|the|only)"
    r"|in the form|```|^\s*[-*]\s|\d\.\s)"
)

_DISABLE = re.compile(r"promptlint:\s*disable(?:=([A-Z0-9,\s]+))?", re.I)


def _line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def _is_disabled(line_text, code):
    m = _DISABLE.search(line_text)
    if not m:
        return False
    if m.group(1) is None:  # bare "disable" turns off everything on the line
        return True
    return code.upper() in {c.strip().upper() for c in m.group(1).split(",")}


def lint_text(text, max_prompt_length=DEFAULT_MAX_PROMPT_LENGTH):
    """Return a list of Findings for a single file's text."""
    lines = text.splitlines()
    findings = []

    def add(line, code):
        if 0 <= line - 1 < len(lines) and _is_disabled(lines[line - 1], code):
            return
        severity, message = RULES[code]
        findings.append(Finding(line, 1, code, severity, message))

    # --- line-based rules ---
    for i, ln in enumerate(lines, start=1):
        # PL003: hardcoded secret
        if _SECRET.search(ln):
            add(i, "PL003")
        # PL001: untrusted input interpolated/concatenated into a prompt.
        # Brace interpolation only counts inside an actual f-string (not a dict literal).
        has_fstring = _FSTRING.search(ln) is not None
        if _PROMPT_KW.search(ln) and (
            (has_fstring and _INTERP_UNTRUSTED.search(ln)) or _CONCAT_UNTRUSTED.search(ln)
        ):
            add(i, "PL001")
        # PL005: hardcoded model id
        if _MODEL_LITERAL.search(ln):
            add(i, "PL005")

    # --- block / multiline rules ---
    # PL002: LLM call without a token limit
    for m in _LLM_CALL.finditer(text):
        window = text[m.start():m.start() + 600]
        if not _MAX_TOKENS.search(window):
            add(_line_of(text, m.start()), "PL002")

    # PL006: messages[] with a user role but no system role
    for m in _MESSAGES_ARRAY.finditer(text):
        window = text[m.start():m.start() + 800]
        if _ROLE_USER.search(window) and not _ROLE_SYSTEM.search(window):
            add(_line_of(text, m.start()), "PL006")

    # PL004: long prompt (triple-quoted) with no output-format instruction
    for m in _TRIPLE_STRING.finditer(text):
        s = m.group(1) if m.group(1) is not None else m.group(2)
        if s and len(s) >= max_prompt_length and _PROMPTY_WORDS.search(s) and not _FORMAT_KW.search(s):
            add(_line_of(text, m.start()), "PL004")

    findings.sort(key=lambda f: (f.line, f.code))
    return findings
