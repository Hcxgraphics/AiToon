import json
from pathlib import Path
from typing import Any


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


def _extract_json_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    stack: list[str] = []
    start = None
    in_string = False
    escape = False

    for index, char in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char in "{[":
            if not stack:
                start = index
            stack.append(char)
            continue

        if char in "}]":
            if not stack:
                continue

            opening = stack[-1]
            if (opening == "{" and char == "}") or (opening == "[" and char == "]"):
                stack.pop()
                if not stack and start is not None:
                    candidates.append(text[start:index + 1])
                    start = None
            else:
                stack = []
                start = None

    return candidates


def parse_json_response(text: str) -> Any:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("LLM returned an empty response")

    decoder = json.JSONDecoder()
    stripped = text.strip()

    try:
        parsed, end_index = decoder.raw_decode(stripped)
        if stripped[end_index:].strip():
            raise ValueError("Trailing non-JSON content detected")
        return parsed
    except json.JSONDecodeError:
        pass

    for candidate in _extract_json_candidates(text):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    raise ValueError("LLM output is not valid JSON")


def render_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


def load_prompt(filename: str) -> str:
    prompt_path = PROMPTS_DIR / filename
    return prompt_path.read_text(encoding="utf-8")
