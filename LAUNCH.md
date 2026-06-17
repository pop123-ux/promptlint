# Launch copy for promptlint (DRAFTS — nothing here is posted)

Reviewed and posted by Pop only. Post the demo GIF first; it carries all of these.

---

## 1. Hacker News — "Show HN"

**Title** (≤ 80 chars, no emoji, no hype — HN hates hype):

```
Show HN: promptlint – ESLint for your LLM prompts
```

**URL:** https://github.com/pop123-ux/promptlint

**First comment** (post immediately after submitting, as the author):

```
I kept seeing the same mistakes in code that calls LLMs: user input
concatenated straight into a prompt (injection), no max_tokens (surprise
bills), a hardcoded sk-... key two lines up, and long prompts with no output
format. So I wrote a small linter for exactly that.

It's zero-dependency Python, runs as a CLI or a pre-commit hook, and has 6
high-signal rules (PL001–PL006). Exits non-zero on errors so it drops into CI.

  pip install llm-promptlint
  promptlint .

It's deliberately high-signal over high-coverage — a linter that nags gets
disabled. Heuristic by nature, so false positives are possible; inline
`# promptlint: disable=PL001` is supported. Rule ideas and PRs very welcome.

Repo: https://github.com/pop123-ux/promptlint
```

**Timing:** weekday, ~8:00–10:00 a.m. US Eastern. Reply to every comment quickly
and without defensiveness — engagement keeps it on the front page.

---

## 2. Reddit

### r/LocalLLaMA / r/Python / r/devtools

**Title:**

```
I built promptlint — a tiny "ESLint for LLM prompts" that catches injection risks and missing token limits
```

**Body:**

```
Prompts are code now, but nothing lints them. promptlint is a small,
zero-dependency tool (CLI + pre-commit hook) that flags the stuff that
actually ships wrong:

- untrusted input interpolated into a prompt (injection risk)
- LLM calls with no max_tokens
- hardcoded API keys
- long prompts with no output-format instruction
- hardcoded model ids / missing system role

  pip install llm-promptlint
  promptlint .

It's high-signal by design and supports inline disables. MIT licensed.
Would love feedback and rule ideas.

GitHub: https://github.com/pop123-ux/promptlint
```

**Notes:** Read each sub's self-promotion rules first. r/Python prefers project
posts with a clear "what my project does / target audience / comparison"
section. Don't cross-post all at once — space them a day apart, and reply to
comments.

---

## 3. X / Twitter (thread)

```
1/ Prompts are code now. But nothing lints them.

So I built promptlint — ESLint for your LLM prompts.

pip install llm-promptlint
[attach the demo GIF]

2/ It catches the mistakes that actually ship:
• user input glued into a prompt → injection
• no max_tokens → surprise bills
• hardcoded API keys
• long prompts with no output format
• hardcoded model ids, missing system role

3/ Runs as a CLI or a pre-commit hook, exits non-zero on errors so it slots
into CI. Zero dependencies. High-signal by design — a linter that nags gets
turned off.

4/ MIT licensed, rules are just Markdown + regex, PRs welcome.
⭐ https://github.com/pop123-ux/promptlint

What rule should I add next?
```

**Hashtags (use 2–3 max):** #LLM #PromptInjection #DevTools

---

## 4. Other ribbons to pull (low effort, compounding)

- Submit a PR adding promptlint to **awesome-llm**, **awesome-ai-tools**, and
  **awesome-prompt-engineering** lists.
- Mention it in your **Medium** prompt-injection articles (natural funnel) and
  cross-link with **agent-security-skills**.
- Pin the repo on your GitHub profile; add the GIF to a GitHub Release.
- Post in relevant Discord/Slack communities (LLM dev, AppSec) where it's on-topic.

## Honesty guardrails

- Don't fake stars, reviews, or testimonials.
- Be upfront that it's heuristic (false positives possible).
- Engage genuinely; answer criticism with fixes, not spin.
```
