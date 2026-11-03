#!/usr/bin/env bash
# Third-round dataset build, part two: hard negatives from workbooks that earlier rounds used for
# other cells. The corpus has few untouched workbooks left, so this run skips only the workbooks
# that already gave hard negatives or third-round errors, and adds train examples only
# (--val-share 0) so the validation set stays as it was.
#
# Waits for build_v3.sh to finish before it starts, so the two builds never share the machine.
# Run from the project root inside tmux:
#   bash scripts/build_v3_hn.sh 2>&1 | tee data/dataset/build_v3_hn.log
set -euo pipefail

CONFIG=configs/v3.yaml
INDEX=data/index/enron
XLSX=data/xlsx/enron
HN=data/dataset/enron_hn/examples.jsonl
ERR3=data/dataset/enron_v3_errors/examples.jsonl
HN3=data/dataset/enron_v3_hn
BUILD_LOG=data/dataset/build_v3.log
WORKERS=${WORKERS:-3}

until grep -q "^== done" "$BUILD_LOG" 2>/dev/null; do
  echo "$(date '+%H:%M:%S') waiting for build_v3.sh to finish"
  sleep 120
done

mkdir -p "$HN3"
echo "== hard negatives on reused workbooks"
python scripts/build_dataset.py --config "$CONFIG" --source enron_v3hn --index "$INDEX" --xlsx "$XLSX" --out "$HN3" \
  --mode hard_negatives --exclude-workbooks "$HN,$ERR3" --max-workbooks 2500 --val-share 0 --workers "$WORKERS"

echo "== done: $HN3/examples.jsonl"
