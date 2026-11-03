#!/usr/bin/env bash
# Bring the server's checkout to the given commit (or origin/main) and install Python dependencies.
# Run on the server by the deployment pipeline: bash webapp/deploy/update.sh <commit>
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV="${SHEETTRUTH_VENV:-$HOME/work/.venv}"
COMMIT="${1:-origin/main}"

cd "$APP_DIR"
git fetch --prune origin
git checkout --quiet --force "$COMMIT"
echo "checked out $(git rev-parse --short HEAD)"

if [ ! -x "$VENV/bin/pip" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r requirements.txt
echo "dependencies installed in $VENV"
