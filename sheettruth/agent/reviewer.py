"""Second opinion on a finding from a hosted reviewer model.

The meaning model proposes, the code checks test, and the reviewer reads the same context window
with the claim and answers as a careful human auditor would: real_error, not_error or
cannot_tell, with one sentence of evidence. The reviewer never sees the code checks' results, so
its view is independent of them. Any OpenAI-compatible chat endpoint works.
"""
from __future__ import annotations

import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Optional, Protocol

REVIEW_VERDICTS = ("real_error", "not_error", "cannot_tell")

REVIEWER_PROMPT = """You are an experienced spreadsheet auditor. One formula cell from a real workbook was flagged
by an automated tool as a possible error. You get the cell, the tool's claim and a context window:
a plain-text description of the cell's surroundings.

How to read the context window:
- TARGET: the cell under review, its formula, its recalculated value, number format.
- ROW_PATH / COL_PATH: the labels of the cell's row and column, nearest label first, then section headers.
- GRID: the 5x5 block of cells around the target; the target row is marked with *.
- COL / ROW: cells above and below in the same column, and left and right in the same row, with labels.
- PEERS_ROW / PEERS_COL: how many formula cells in the same row or column share the target's formula pattern (R1C1); PEER_DIFF lists ones that differ.
- REF_RANGE / IN_RANGE / BEFORE_RANGE / AFTER_RANGE: the referenced cells, a few inside the range, and the cells just before and after the range ends.
- REF_CELL: a single referenced cell with its labels and value.
- ASSUMPTION: labelled constants on the sheet that formulas reference.
- A line ending in -> value shows a formula and its value.

Decide whether the formula as written is a mistake, judging from the labels and surroundings only.
Do not trust the tool's reason; form your own view. If the window does not hold enough
information, say cannot_tell instead of guessing.

Answer with one JSON object and nothing else:
{{"verdict": "real_error" | "not_error" | "cannot_tell", "reason": "<one sentence naming the evidence>"}}

Cell: {sheet}!{addr}
Formula as written: {formula}
Tool's claim: type={type}, proposed fix={expected}
Tool's reason: {reason}

Context window:
{window}
"""


@dataclass
class Review:
    verdict: str
    reason: str

    def to_dict(self) -> dict:
        return {"verdict": self.verdict, "reason": self.reason}


class ReviewerClient(Protocol):
    def review(self, items: list[dict]) -> list[Review]: ...


def complete_text(client, model: str, system: Optional[str], user: str, max_tokens: int) -> str:
    """One text reply from an OpenAI-compatible endpoint. Chat completions first; endpoints that
    only offer the Responses API are handled by the fallback."""
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    try:
        resp = client.chat.completions.create(model=model, max_tokens=max_tokens, temperature=0, messages=messages)
        return resp.choices[0].message.content or ""
    except Exception as chat_error:
        if not hasattr(client, "responses"):
            raise chat_error
    resp = client.responses.create(model=model, max_output_tokens=max_tokens, input=messages)
    return getattr(resp, "output_text", "") or ""


def parse_review(text: str) -> Review:
    start, end = text.find("{"), text.rfind("}")
    try:
        data = json.loads(text[start:end + 1])
    except (ValueError, TypeError):
        return Review("cannot_tell", "reviewer reply could not be parsed")
    verdict = data.get("verdict") if data.get("verdict") in REVIEW_VERDICTS else "cannot_tell"
    return Review(verdict, re.sub(r"\s+", " ", str(data.get("reason", ""))).strip())


def review_prompt(item: dict) -> str:
    return REVIEWER_PROMPT.format(sheet=item["sheet"], addr=item["addr"], formula=item["formula"], type=item.get("type"),
                                  expected=item.get("expected"), reason=item.get("reason", ""), window=item["window"])


class HostedReviewer:
    """Reviewer behind an OpenAI-compatible chat endpoint (settings from the environment unless given).

    Reasoning models spend output tokens on their hidden reasoning before the visible answer, so
    max_tokens must be generous or the visible answer is cut off and nothing can be parsed."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None,
                 concurrency: int = 4, max_tokens: int = 16000):
        self.base_url = base_url or os.environ.get("SHEETTRUTH_REVIEWER_BASE_URL", "")
        self.model = model or os.environ.get("SHEETTRUTH_REVIEWER_MODEL", "")
        self.api_key = api_key or os.environ.get("SHEETTRUTH_REVIEWER_API_KEY", "")
        self.concurrency = concurrency
        self.max_tokens = max_tokens

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.model and self.api_key)

    def _ask(self, item: dict) -> Review:
        from openai import OpenAI

        client = OpenAI(base_url=self.base_url, api_key=self.api_key, timeout=180, max_retries=1)
        try:
            return parse_review(complete_text(client, self.model, None, review_prompt(item), self.max_tokens))
        except Exception as ex:
            return Review("cannot_tell", f"reviewer unavailable: {type(ex).__name__}: {str(ex)[:120]}")

    def review(self, items: list[dict]) -> list[Review]:
        if not items:
            return []
        with ThreadPoolExecutor(self.concurrency) as pool:
            return list(pool.map(self._ask, items))


class NoReviewer:
    """Used when no reviewer endpoint is configured; every finding is left unreviewed."""

    def review(self, items: list[dict]) -> list[Review]:
        return [Review("cannot_tell", "no reviewer configured") for _ in items]
