"""Tests for promptlint rules. Run with: python -m pytest  (or python tests/test_rules.py)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promptlint import lint_text


def codes(text, **kw):
    return {f.code for f in lint_text(text, **kw)}


def test_pl003_hardcoded_secret():
    assert "PL003" in codes('client = OpenAI(api_key="sk-ant-abcdef1234567890ABCDEF")')


def test_pl003_env_var_is_clean():
    assert "PL003" not in codes('client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])')


def test_pl001_interpolated_user_input():
    assert "PL001" in codes('prompt = f"Answer: {user_input}"')


def test_pl001_concatenated_request():
    assert "PL001" in codes('prompt = "Q: " + request.body')


def test_pl001_passing_as_field_is_clean():
    # The correct pattern: user input as a separate message field, not interpolated.
    assert "PL001" not in codes('messages = [{"role": "user", "content": user_input}]')


def test_pl002_missing_max_tokens():
    assert "PL002" in codes("resp = client.chat.completions.create(model=m, messages=msgs)")


def test_pl002_with_max_tokens_is_clean():
    assert "PL002" not in codes(
        "resp = client.chat.completions.create(model=m, messages=msgs, max_tokens=256)")


def test_pl005_hardcoded_model():
    assert "PL005" in codes('resp = call(model="claude-opus-4-8")')


def test_pl005_variable_model_is_clean():
    assert "PL005" not in codes("resp = call(model=MODEL)")


def test_pl006_messages_without_system():
    assert "PL006" in codes('messages = [{"role": "user", "content": q}]')


def test_pl006_with_system_is_clean():
    text = 'messages = [{"role": "system", "content": s}, {"role": "user", "content": q}]'
    assert "PL006" not in codes(text)


def test_pl004_long_prompt_without_format():
    text = '"""You are an assistant. Summarize the document and explain everything ' \
           'in great detail so the reader fully understands the whole situation here ' \
           'including all of the nuance and context that matters most of all.\n"""'
    assert "PL004" in codes(text)


def test_pl004_with_format_instruction_is_clean():
    text = '"""You are an assistant. Summarize the document and respond only with ' \
           'valid JSON using the schema {"summary": string} and nothing else at all ' \
           'so the output is always machine readable for the caller downstream.\n"""'
    assert "PL004" not in codes(text)


def test_inline_disable():
    assert "PL003" not in codes(
        'key = "sk-ant-abcdef1234567890ABCDEF"  # promptlint: disable=PL003')


if __name__ == "__main__":
    funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in funcs:
        try:
            fn()
            print("PASS", fn.__name__)
        except AssertionError:
            failed += 1
            print("FAIL", fn.__name__)
    print("\n{} passed, {} failed".format(len(funcs) - failed, failed))
    sys.exit(1 if failed else 0)
