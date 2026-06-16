"""Intentionally messy example — promptlint should flag several issues here."""

import openai

# PL003: hardcoded secret
client = openai.OpenAI(api_key="sk-ant-abcdef1234567890ABCDEF")


def reply(user_input, request):
    # PL001: untrusted input interpolated straight into the prompt
    prompt = f"Answer the user's question: {user_input}"

    # PL006: messages[] has a user role but no system role
    messages = [
        {"role": "user", "content": prompt},
    ]

    # PL002: no max_tokens -> unbounded cost/output
    resp = client.chat.completions.create(
        model="gpt-4o",  # PL005: hardcoded model id
        messages=messages,
    )
    return resp


# PL004: long prompt with no output-format instruction
SYSTEM = """
You are a helpful assistant. Summarize the user's document and explain the key
points in detail, covering all of the important arguments while giving your own
analysis of what matters most for the reader to fully understand the situation.
"""
