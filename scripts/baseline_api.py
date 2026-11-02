"""Score context windows with a hosted chat model through an OpenAI-compatible endpoint.

Same system prompt, same windows, same reply format as the fine-tuned model, so the numbers from
evaluate_enron.py are directly comparable. Works with any endpoint that speaks the chat
completions API (Meta's model API, Baseten, Fireworks, OpenAI).

Usage:
  set OPENAI_COMPAT_API_KEY=...            (PowerShell: $env:OPENAI_COMPAT_API_KEY="...")
  python scripts/baseline_api.py --input data/test/windows_v2.jsonl --out data/test/predictions_spark.jsonl \\
      --base-url https://api.meta.ai/v1 --model <model id> --concurrency 4
  python scripts/baseline_api.py --input ... --out ... --base-url ... --model ... --ids data/test/subset_ids.txt

Finished ids are skipped on a rerun. --ids limits the run to the listed window ids.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.prompt import SYSTEM_PROMPT, parse_reply  # noqa: E402

REASONING_LINE = "Reasoning strength: low\n"


def load_rows(path: str, ids_file: str, done: set[str]) -> list[dict]:
    wanted = None
    if ids_file:
        wanted = {line.strip() for line in open(ids_file) if line.strip()}
    rows = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            if r["id"] in done or (wanted is not None and r["id"] not in wanted):
                continue
            rows.append(r)
    return rows


def done_ids(path: str) -> set[str]:
    if not Path(path).exists():
        return set()
    return {json.loads(line)["id"] for line in open(path) if line.strip()}


def ask(client, model: str, row: dict, max_tokens: int, with_reasoning_line: bool) -> dict:
    if row.get("unsupported_reason"):
        return {"id": row["id"], "verdict": "unsupported", "type": None, "expected": None,
                "reason": row["unsupported_reason"], "parsed": True, "raw": ""}
    system = (REASONING_LINE if with_reasoning_line else "") + SYSTEM_PROMPT
    last = ""
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model, max_tokens=max_tokens, temperature=0,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": row["window"]}],
            )
            raw = resp.choices[0].message.content or ""
            return {"id": row["id"], **parse_reply(raw), "raw": raw[-600:]}
        except Exception as ex:
            last = f"{type(ex).__name__}: {str(ex)[:200]}"
            time.sleep(5 * (attempt + 1))
    return {"id": row["id"], "verdict": "unsupported", "type": None, "expected": None,
            "reason": f"api failure: {last}", "parsed": False, "raw": ""}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--ids", default="", help="file with one window id per line to restrict the run")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--no-reasoning-line", action="store_true", help="omit the 'Reasoning strength: low' line")
    args = ap.parse_args()
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("pip install openai")
    key = os.environ.get("OPENAI_COMPAT_API_KEY")
    if not key:
        sys.exit("set OPENAI_COMPAT_API_KEY")
    client = OpenAI(base_url=args.base_url, api_key=key, timeout=300)

    done = done_ids(args.out)
    rows = load_rows(args.input, args.ids, done)
    print(f"{len(rows)} windows to score ({len(done)} already done)", flush=True)
    written = 0
    with ThreadPoolExecutor(args.concurrency) as pool, open(args.out, "a") as f:
        futures = [pool.submit(ask, client, args.model, r, args.max_tokens, not args.no_reasoning_line) for r in rows]
        for future in as_completed(futures):
            f.write(json.dumps(future.result(), ensure_ascii=False) + "\n")
            f.flush()
            written += 1
            if written % 25 == 0:
                print(f"scored {written}/{len(rows)}", flush=True)
    print(f"done: {written} verdicts appended to {args.out}")


if __name__ == "__main__":
    main()
