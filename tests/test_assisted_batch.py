"""Tests for the batch form of the assisted mutation step: request shape, reply parsing, seed
exclusion. No API calls are made. The build code needs the Linux-only `resource` module, so the
whole module is skipped elsewhere."""
import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("resource")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import assisted_mutate_batch as amb  # noqa: E402

SEED = {"id": "enron_v2-000123", "window": "=== TARGET ===\nSheet1!B9 =SUM(B2:B8)", "original_formula": "=SUM(B2:B8)"}


def test_build_request_carries_seed_id_and_prompt():
    req = amb.build_request(SEED, "model-x", "extra_rows, skipped_rows")
    assert req["custom_id"] == "enron_v2-000123"
    assert req["params"]["model"] == "model-x"
    prompt = req["params"]["messages"][0]["content"]
    assert "=SUM(B2:B8)" in prompt
    assert "extra_rows, skipped_rows" in prompt
    assert "skipped_rows: the range stops short" in prompt


def test_parse_reply_text_takes_the_json_object_only():
    text = 'Sure.\n{"type": "extra_rows", "broken_formula": "=SUM(B1:B8)", "reason": "r", "evidence": ["Sheet1!B1"]}\nDone.'
    assert amb.parse_reply_text(text)["broken_formula"] == "=SUM(B1:B8)"
    assert amb.parse_reply_text("no json here") is None
    assert amb.parse_reply_text("{not valid}") is None


def test_seed_ids_in_reads_only_existing_files(tmp_path):
    seeds = tmp_path / "batch_a_seeds.jsonl"
    seeds.write_text(json.dumps({"id": "s1"}) + "\n" + json.dumps({"id": "s2"}) + "\n")
    assert amb.seed_ids_in([str(seeds), str(tmp_path / "missing.jsonl"), ""]) == {"s1", "s2"}
