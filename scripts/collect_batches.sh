#!/usr/bin/env bash
# Wait for one or more assisted-mutation Message Batches and collect each one as soon as it ends.
# Collection applies every proposal to a workbook copy and recalculates it, so it is slow; running
# it here, unattended, keeps the examples file filling up while nobody is watching.
#
# Run from the project root inside tmux, with ANTHROPIC_API_KEY exported in that shell:
#   bash scripts/collect_batches.sh range arith 2>&1 | tee data/dataset/enron_opus/collect_v3.log
# OUT and XLSX select the examples folder and the workbook root (defaults: the Enron assisted set).
set -uo pipefail

OUT=${OUT:-data/dataset/enron_opus}
XLSX=${XLSX:-data/xlsx/enron}
POLL_SECONDS=${POLL_SECONDS:-300}

if [ "$#" -eq 0 ]; then
  echo "usage: bash scripts/collect_batches.sh <batch name> [<batch name> ...]"
  exit 1
fi

pending=("$@")
while [ "${#pending[@]}" -gt 0 ]; do
  still=()
  for name in "${pending[@]}"; do
    status=$(python scripts/assisted_mutate_batch.py status --out "$OUT" --name "$name" 2>&1) || true
    echo "$(date '+%H:%M:%S') $status"
    if echo "$status" | grep -q ": ended;"; then
      echo "== collecting $name"
      python scripts/assisted_mutate_batch.py collect --out "$OUT" --name "$name" --xlsx "$XLSX"
      echo "== $name collected"
    else
      still+=("$name")
    fi
  done
  pending=("${still[@]+"${still[@]}"}")
  if [ "${#pending[@]}" -gt 0 ]; then
    sleep "$POLL_SECONDS"
  fi
done
echo "== all batches collected"
