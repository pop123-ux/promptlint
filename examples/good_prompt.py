"""Clean example — promptlint should report no issues here."""

import os

import openai

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.environ.get("MODEL", "gpt-4o")


def reply(user_input):
    system = (
        "You are a helpful assistant. Respond ONLY with valid JSON of the form "
        '{"answer": string}.'
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_input},  # passed as a field, not interpolated
    ]
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=512,
    )
