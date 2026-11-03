"""Send one review request to the configured reviewer endpoint and show the raw reply.

Useful when reviews come back as "could not be parsed": it prints the finish reason, the length
of the reply and its first and last characters, so the cause (truncation, reasoning text mixed
into the answer, empty content) is visible.

Usage (after setting SHEETTRUTH_REVIEWER_BASE_URL, SHEETTRUTH_REVIEWER_MODEL, SHEETTRUTH_REVIEWER_API_KEY):
  python scripts/check_reviewer.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.agent.reviewer import HostedReviewer, parse_review, review_prompt  # noqa: E402

SAMPLE = {
    "sheet": "Sheet1", "addr": "B8", "formula": "=SUM(B3:B6)", "type": "skipped_rows", "expected": "=SUM(B3:B7)",
    "reason": "The SUM range stops short: Marketing belongs to the same block but is left out.",
    "window": "\n".join([
        "TARGET|Sheet1!B8|=SUM(B3:B6)|value=580|fmt=General|bold=1",
        "ROW_PATH|Total expenses", "COL_PATH|Amount",
        "COL|Sheet1!B3|Rent||100", "COL|Sheet1!B4|Salaries||400", "COL|Sheet1!B5|Travel||50",
        "COL|Sheet1!B6|Software||30", "COL|Sheet1!B7|Marketing||80",
        "REF_RANGE|Sheet1!B3:B6|cells=4|all_positive|min=30|max=400|numbers=4|blanks=0",
        "AFTER_RANGE|Sheet1!B7|Marketing||80", "AFTER_RANGE|Sheet1!B8|(target cell)",
    ]),
}


def main() -> None:
    from openai import OpenAI

    reviewer = HostedReviewer(concurrency=1)
    if not reviewer.configured:
        sys.exit("reviewer environment variables are not set")
    print(f"endpoint {reviewer.base_url} model {reviewer.model} max_tokens {reviewer.max_tokens}", flush=True)
    client = OpenAI(base_url=reviewer.base_url, api_key=reviewer.api_key, timeout=180, max_retries=1)
    started = time.time()
    resp = client.chat.completions.create(model=reviewer.model, max_tokens=reviewer.max_tokens, temperature=0,
                                          messages=[{"role": "user", "content": review_prompt(SAMPLE)}])
    elapsed = time.time() - started
    choice = resp.choices[0]
    text = choice.message.content or ""
    extra = {k: v for k, v in choice.message.model_dump().items() if k not in ("content", "role") and v}
    print(f"elapsed {elapsed:.1f}s  finish_reason={choice.finish_reason}  usage={resp.usage}")
    print(f"content length {len(text)} characters; other message fields: {list(extra)}")
    print("--- first 400 characters ---")
    print(text[:400])
    print("--- last 400 characters ---")
    print(text[-400:])
    review = parse_review(text)
    print(f"--- parsed: verdict={review.verdict} reason={review.reason}")


if __name__ == "__main__":
    main()
