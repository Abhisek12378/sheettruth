#!/usr/bin/env bash
# Fetch the ExceLint benchmark (70 hand-audited spreadsheets) and make it ready as a second test set:
#   1. shallow clone of the ExceLint-core repository, which ships the workbooks and annotations
#   2. copy the workbooks into the test layout and write the overview file
#   3. build one window per formula run, the input for scoring
#   4. report how many training workbooks in the given index look like these test files
#
# Run from the project root:
#   bash scripts/prepare_excelint.sh [index folder for the leakage report, default data/index/enron]
set -euo pipefail

INDEX=${1:-data/index/enron}
RAW=data/raw/excelint
XLSX=data/test/excelint_xlsx
OVERVIEW=data/test/excelint_overview.json
WINDOWS=data/test/windows_excelint.jsonl

if [ ! -d "$RAW/.git" ]; then
  git clone --quiet --depth 1 https://github.com/ExceLint/ExceLint-core.git "$RAW"
fi

echo "== prepare workbooks and overview"
python scripts/prepare_excelint_benchmark.py --source "$RAW/test" --xlsx-out "$XLSX" --overview-out "$OVERVIEW"

echo "== build test windows"
python scripts/build_test_windows.py --overview "$OVERVIEW" --xlsx-dir "$XLSX" --out "$WINDOWS" | tail -1

if [ -f "$INDEX/workbooks.jsonl" ]; then
  echo "== leakage report against $INDEX"
  python scripts/filter_leakage.py "$INDEX/workbooks.jsonl" "$XLSX" "$RAW/leakage_check.json" --threshold 0.6
fi
echo "== done: $WINDOWS"
