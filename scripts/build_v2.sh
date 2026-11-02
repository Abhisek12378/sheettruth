#!/usr/bin/env bash
# Second-round dataset build: new error shapes on fresh workbooks, hard negatives on more fresh
# workbooks, then one balanced train/val set from every examples file.
#
# Run from the project root inside tmux:
#   bash scripts/build_v2.sh 2>&1 | tee data/dataset/build_v2.log
set -euo pipefail

INDEX=data/index/enron
XLSX=data/xlsx/enron
V1=data/dataset/enron/examples.jsonl
V2=data/dataset/enron_v2
HN=data/dataset/enron_hn
FINAL=data/dataset/final_v2
WORKERS=${WORKERS:-4}

mkdir -p "$V2" "$HN" "$FINAL"

echo "== step 1: error and ok examples with the extended mutator set"
python scripts/build_dataset.py --source enron_v2 --index "$INDEX" --xlsx "$XLSX" --out "$V2" \
  --exclude-workbooks "$V1" --max-workbooks 4000 --workers "$WORKERS"

echo "== step 2: hard negatives (untouched cells a mutator could have broken)"
python scripts/build_dataset.py --source enron_hn --index "$INDEX" --xlsx "$XLSX" --out "$HN" \
  --mode hard_negatives --exclude-workbooks "$V1,$V2/examples.jsonl" --max-workbooks 2500 --workers "$WORKERS"

echo "== step 3: balance and split"
python scripts/finalize_dataset.py "$V1" "$V2/examples.jsonl" "$HN/examples.jsonl" \
  --out "$FINAL" --per-type-cap 1500 --hard-negative-share 0.5

echo "== done: $FINAL/train.jsonl and $FINAL/val.jsonl"
