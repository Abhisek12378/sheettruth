"""The prompt the meaning model is trained on and served with, in one place.

The chat template of the base model appends its own "Reasoning strength: <value>." line to the
system message, so the reasoning line is never written into the system text here; it is passed to
the template as `reasoning_strength` instead. Datasets built before this module existed carry the
line at the top of the system prompt; `normalise_messages` strips it so old and new data match.
"""
from __future__ import annotations

import json
import re

REASONING_STRENGTH = "low"
REASONING_LINE = re.compile(r"^Reasoning strength:[^\n]*\n?")

SYSTEM_PROMPT = """You audit one spreadsheet formula cell at a time. You receive a context window describing the target cell, its labels, its neighbours, the cells it references and comparable formulas nearby.
Decide whether the formula computes what its labels and surroundings say it should.
Reply with one JSON object and nothing else, using exactly these keys:
{"verdict": "ok" | "error" | "unsupported", "type": null | "wrong_function" | "skipped_rows" | "extra_rows" | "double_count" | "wrong_sign" | "wrong_reference" | "missing_term" | "wrong_operator" | "missing_factor", "expected": null | "<corrected formula>", "reason": "<one sentence>"}
Use "unsupported" when the formula's main function is outside the supported set or the window does not hold enough evidence."""

VERDICTS = {"ok", "error", "unsupported"}
ERROR_TYPES = {"wrong_function", "skipped_rows", "extra_rows", "double_count", "wrong_sign", "wrong_reference",
               "missing_term", "wrong_operator", "missing_factor"}


def strip_reasoning_line(system_text: str) -> str:
    return REASONING_LINE.sub("", system_text, count=1)


def normalise_messages(messages: list[dict]) -> list[dict]:
    """Drop the reasoning line from the system prompt; the chat template adds its own."""
    out = []
    for m in messages:
        if m["role"] == "system":
            m = {"role": "system", "content": strip_reasoning_line(m["content"])}
        out.append(m)
    return out


def build_messages(window: str) -> list[dict]:
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": window}]


def parse_reply(text: str) -> dict:
    """Turn the model's reply into a verdict dict; anything unparseable becomes an unsupported verdict."""
    body = text.split("<|message|>")[-1]
    start, end = body.find("{"), body.rfind("}")
    try:
        data = json.loads(body[start:end + 1])
    except (ValueError, TypeError):
        return {"verdict": "unsupported", "type": None, "expected": None, "reason": "unparseable reply", "parsed": False}
    verdict = data.get("verdict") if data.get("verdict") in VERDICTS else "unsupported"
    etype = data.get("type") if data.get("type") in ERROR_TYPES else None
    return {"verdict": verdict, "type": etype if verdict == "error" else None,
            "expected": data.get("expected") if verdict == "error" else None,
            "reason": str(data.get("reason", "")), "parsed": True}
