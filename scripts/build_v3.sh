#!/usr/bin/env bash
# Third-round dataset build, part one: error examples of the rarer types on fresh workbooks, then
# hard negatives on more fresh workbooks. Every workbook used by an earlier round is skipped.
# Balancing and the train/val split happen later in finalize_v3.sh, once every top-up is in.
#
# Run from the project root inside tmux:
#   bash scripts/build_v3.sh 2>&1 | tee data/dataset/build_v3.log
set -euo pipefail

CONFIG=configs/v3.yaml
INDEX=data/index/enron
XLSX=data/xlsx/enron
V1=data/dataset/enron/examples.jsonl
V2=data/dataset/enron_v2/examples.jsonl
HN=data/dataset/enron_hn/examples.jsonl
ASSISTED=data/dataset/enron_opus/examples.jsonl
ERR3=data/dataset/enron_v3_errors
HN3=data/dataset/enron_v3_hn
WORKERS=${WORKERS:-3}
RARE_TYPES=extra_rows,missing_term,missing_factor,wrong_operator,wrong_reference,skipped_rows

mkdir -p "$ERR3" "$HN3"

echo "== step 1: error examples of the rarer types on fresh workbooks"
python scripts/build_dataset.py --config "$CONFIG" --source enron_v3e --index "$INDEX" --xlsx "$XLSX" --out "$ERR3" \
  --mode errors_only --only-mutators "$RARE_TYPES" \
  --exclude-workbooks "$V1,$V2,$HN,$ASSISTED" --max-workbooks 3000 --workers "$WORKERS"

echo "== step 2: hard negatives on fresh workbooks"
python scripts/build_dataset.py --config "$CONFIG" --source enron_v3hn --index "$INDEX" --xlsx "$XLSX" --out "$HN3" \
  --mode hard_negatives --exclude-workbooks "$V1,$V2,$HN,$ASSISTED,$ERR3/examples.jsonl" \
  --max-workbooks 1500 --workers "$WORKERS"

echo "== done: $ERR3/examples.jsonl and $HN3/examples.jsonl"
