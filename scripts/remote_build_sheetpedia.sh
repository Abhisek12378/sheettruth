#!/usr/bin/env bash
# Build a training set from the Sheetpedia corpus on a fresh Ubuntu 24.04 machine, end to end:
#   1. install LibreOffice and Python, clone the repository, create the virtual environment
#   2. download and unpack the Sheetpedia archive (211k .xlsx workbooks)
#   3. sample workbooks, index their formula cells, drop anything close to the test corpus
#   4. build error / ok / unsupported examples, then hard negatives on other workbooks
#   5. optionally let a reviewer model propose extra errors through a Message Batch
#   6. pack every examples file into one archive for transfer
#
# Before running, copy the 30 test workbooks to $HOME/enron_errors_xlsx (the leakage filter needs
# them; they are not in the repository). Then, inside tmux:
#   OPUS_COUNT=1000 ANTHROPIC_API_KEY=... bash remote_build_sheetpedia.sh 2>&1 | tee $HOME/sheetpedia_build.log
# OPUS_COUNT=0 (the default) skips the reviewer-model step. Steps already completed are skipped
# on a rerun, so an interrupted run can simply be started again.
set -euo pipefail

REPO=${REPO:-https://github.com/Abhisek12378/sheettruth.git}
WORK=${WORK:-$HOME/work}
PROJECT=$WORK/sheettruth
VENV=$WORK/.venv
TEST_DIR=${TEST_DIR:-$HOME/enron_errors_xlsx}
ARCHIVE_URL=${ARCHIVE_URL:-https://huggingface.co/datasets/tianzl66/Sheetpedia_xlsx/resolve/main/pii_processed_xlsx_0929.tar.gz}
SAMPLE=${SAMPLE:-11000}
MIXED_WORKBOOKS=${MIXED_WORKBOOKS:-8000}
HN_WORKBOOKS=${HN_WORKBOOKS:-3000}
WORKERS=${WORKERS:-6}
OPUS_COUNT=${OPUS_COUNT:-0}
OPUS_MODEL=${OPUS_MODEL:-claude-opus-5-5}
OPUS_PREFERRED=${OPUS_PREFERRED:-extra_rows, skipped_rows, missing_term, wrong_operator, missing_factor, wrong_reference}
RESULT=${RESULT:-$HOME/sheetpedia_dataset.tar.gz}

stamp() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

stamp "== step 1: system packages, repository, virtual environment"
if ! command -v soffice >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libreoffice-calc python3-venv python3-pip git rsync
fi
mkdir -p "$WORK"
if [ ! -d "$PROJECT/.git" ]; then
  git clone --quiet "$REPO" "$PROJECT"
fi
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r "$PROJECT/requirements.txt"
cd "$PROJECT"
source "$VENV/bin/activate"
if [ ! -d "$TEST_DIR" ]; then
  stamp "test workbooks not found at $TEST_DIR; copy data/test/enron_errors_xlsx there and rerun"
  exit 1
fi
mkdir -p data/test
if [ ! -d data/test/enron_errors_xlsx ]; then
  cp -r "$TEST_DIR" data/test/enron_errors_xlsx
fi

stamp "== step 2: download and unpack Sheetpedia"
mkdir -p data/raw/sheetpedia/extract
if [ ! -f data/raw/sheetpedia/sheetpedia.tar.gz ]; then
  curl -L --retry 5 -o data/raw/sheetpedia/sheetpedia.tar.gz "$ARCHIVE_URL"
fi
if [ ! -f data/raw/sheetpedia/extract/.done ]; then
  tar -xzf data/raw/sheetpedia/sheetpedia.tar.gz -C data/raw/sheetpedia/extract
  touch data/raw/sheetpedia/extract/.done
fi
stamp "unpacked $(find data/raw/sheetpedia/extract -name '*.xlsx' | wc -l) workbooks"

stamp "== step 3: sample $SAMPLE workbooks, index, leakage filter"
mkdir -p data/xlsx/sheetpedia data/index/sheetpedia
if [ ! -f data/xlsx/sheetpedia/.done ]; then
  find data/raw/sheetpedia/extract -name '*.xlsx' -size +4k -size -3M -printf '%P\n' \
    | shuf -n "$SAMPLE" --random-source=<(yes 20261103) > data/raw/sheetpedia/sample.txt
  rsync -a --files-from=data/raw/sheetpedia/sample.txt data/raw/sheetpedia/extract/ data/xlsx/sheetpedia/
  touch data/xlsx/sheetpedia/.done
fi
if [ ! -f data/index/sheetpedia/cells.jsonl ]; then
  python scripts/index_corpus.py data/xlsx/sheetpedia data/index/sheetpedia --workers "$WORKERS"
fi
if [ ! -f data/index/sheetpedia/allowed.json ]; then
  python scripts/filter_leakage.py data/index/sheetpedia/workbooks.jsonl data/test/enron_errors_xlsx \
    data/index/sheetpedia/allowed.json --threshold 0.6
fi

stamp "== step 4: mixed examples, then hard negatives"
if [ ! -f data/dataset/sheetpedia/report.json ]; then
  python scripts/build_dataset.py --config configs/v3.yaml --source sheetpedia --index data/index/sheetpedia \
    --xlsx data/xlsx/sheetpedia --out data/dataset/sheetpedia --max-workbooks "$MIXED_WORKBOOKS" --workers "$WORKERS"
fi
if [ ! -f data/dataset/sheetpedia_hn/report.json ]; then
  python scripts/build_dataset.py --config configs/v3.yaml --source sheetpedia_hn --index data/index/sheetpedia \
    --xlsx data/xlsx/sheetpedia --out data/dataset/sheetpedia_hn --mode hard_negatives \
    --exclude-workbooks data/dataset/sheetpedia/examples.jsonl --max-workbooks "$HN_WORKBOOKS" --workers "$WORKERS"
fi

if [ "$OPUS_COUNT" -gt 0 ]; then
  stamp "== step 5: reviewer-model proposals, $OPUS_COUNT seeds, one Message Batch"
  mkdir -p data/dataset/sheetpedia_opus
  if [ ! -f data/dataset/sheetpedia_opus/batch_web.json ]; then
    python scripts/assisted_mutate_batch.py submit data/dataset/sheetpedia/examples.jsonl --xlsx data/xlsx/sheetpedia \
      --out data/dataset/sheetpedia_opus --name web --count "$OPUS_COUNT" --seed 13 --model "$OPUS_MODEL" \
      --preferred "$OPUS_PREFERRED"
  fi
  OUT=data/dataset/sheetpedia_opus XLSX=data/xlsx/sheetpedia bash scripts/collect_batches.sh web
fi

stamp "== step 6: pack the results"
tar -czf "$RESULT" -C data/dataset sheetpedia sheetpedia_hn $( [ -d data/dataset/sheetpedia_opus ] && echo sheetpedia_opus )
stamp "== done: $RESULT ($(du -h "$RESULT" | cut -f1))"
