#!/usr/bin/env bash
# Second Sheetpedia round on the same machine as remote_build_sheetpedia.sh: a much larger sample of
# workbooks the first round did not touch, indexed on top of the existing index, filtered again
# against the test corpus, then one mixed build and one hard-negative build on the new workbooks.
# Waits for the first round to finish before it starts.
#
# Run from $HOME inside tmux, after the first round was started:
#   bash remote_build_sheetpedia_round2.sh 2>&1 | tee $HOME/sheetpedia_round2.log
set -euo pipefail

WORK=${WORK:-$HOME/work}
PROJECT=$WORK/sheettruth
VENV=$WORK/.venv
FIRST_LOG=${FIRST_LOG:-$HOME/sheetpedia_build.log}
SAMPLE=${SAMPLE:-40000}
MIXED_WORKBOOKS=${MIXED_WORKBOOKS:-8000}
HN_WORKBOOKS=${HN_WORKBOOKS:-4000}
WORKERS=${WORKERS:-6}
RESULT=${RESULT:-$HOME/sheetpedia_dataset2.tar.gz}

stamp() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

until grep -q "== done:" "$FIRST_LOG" 2>/dev/null; do
  stamp "waiting for the first round to finish"
  sleep 120
done

cd "$PROJECT"
source "$VENV/bin/activate"
RAW=data/raw/sheetpedia
ROUND1=data/dataset/sheetpedia/examples.jsonl,data/dataset/sheetpedia_hn/examples.jsonl

stamp "== round 2 step 1: sample $SAMPLE more workbooks and index them"
if [ ! -f "$RAW/sample2.txt" ]; then
  find "$RAW/extract" -name '*.xlsx' -size +4k -size -3M -printf '%P\n' \
    | grep -vxF -f "$RAW/sample.txt" \
    | shuf -n "$SAMPLE" --random-source=<(yes 20261104) > "$RAW/sample2.txt"
  rsync -a --files-from="$RAW/sample2.txt" "$RAW/extract/" data/xlsx/sheetpedia/
fi
python scripts/index_corpus.py data/xlsx/sheetpedia data/index/sheetpedia --workers "$WORKERS" --resume
python scripts/filter_leakage.py data/index/sheetpedia/workbooks.jsonl data/test/enron_errors_xlsx \
  data/index/sheetpedia/allowed.json --threshold 0.6

stamp "== round 2 step 2: mixed examples on fresh workbooks"
if [ ! -f data/dataset/sheetpedia2/report.json ]; then
  python scripts/build_dataset.py --config configs/v3.yaml --source sheetpedia2 --index data/index/sheetpedia \
    --xlsx data/xlsx/sheetpedia --out data/dataset/sheetpedia2 --exclude-workbooks "$ROUND1" \
    --max-workbooks "$MIXED_WORKBOOKS" --workers "$WORKERS"
fi

stamp "== round 2 step 3: hard negatives on more fresh workbooks"
if [ ! -f data/dataset/sheetpedia2_hn/report.json ]; then
  python scripts/build_dataset.py --config configs/v3.yaml --source sheetpedia2_hn --index data/index/sheetpedia \
    --xlsx data/xlsx/sheetpedia --out data/dataset/sheetpedia2_hn --mode hard_negatives \
    --exclude-workbooks "$ROUND1,data/dataset/sheetpedia2/examples.jsonl" \
    --max-workbooks "$HN_WORKBOOKS" --workers "$WORKERS"
fi

stamp "== round 2 step 4: pack the results"
tar -czf "$RESULT" -C data/dataset sheetpedia2 sheetpedia2_hn
stamp "== done: $RESULT ($(du -h "$RESULT" | cut -f1))"
