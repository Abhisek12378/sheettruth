#!/usr/bin/env bash
# Steps 2 and 3 of the second-round build, for when step 1 was stopped by hand.
#   bash scripts/build_v2_rest.sh 2>&1 | tee -a data/dataset/build_v2.log
set -euo pipefail

INDEX=data/index/enron
XLSX=data/xlsx/enron
V1=data/dataset/enron/examples.jsonl
V2=data/dataset/enron_v2
HN=data/dataset/enron_hn
ASSISTED=data/dataset/enron_assisted/examples.jsonl
FINAL=data/dataset/final_v2
WORKERS=${WORKERS:-3}

mkdir -p "$HN" "$FINAL"

echo "== step 2: hard negatives (untouched cells a mutator could have broken)"
python scripts/build_dataset.py --source enron_hn --index "$INDEX" --xlsx "$XLSX" --out "$HN" \
  --mode hard_negatives --exclude-workbooks "$V1,$V2/examples.jsonl" --max-workbooks 2500 --workers "$WORKERS"

echo "== step 3: balance and split"
INPUTS=("$V1" "$V2/examples.jsonl" "$HN/examples.jsonl")
if [ -s "$ASSISTED" ]; then INPUTS+=("$ASSISTED"); fi
python scripts/finalize_dataset.py "${INPUTS[@]}" --out "$FINAL" --per-type-cap 1500 --hard-negative-share 0.5

echo "== done: $FINAL/train.jsonl and $FINAL/val.jsonl"
