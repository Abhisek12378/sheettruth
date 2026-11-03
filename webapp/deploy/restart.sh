#!/usr/bin/env bash
# Restart the systemd service and fail unless the health endpoint answers within 30 seconds.
# Run on the server by the deployment pipeline: bash webapp/deploy/restart.sh
set -euo pipefail

SERVICE="${SHEETTRUTH_SERVICE:-sheettruth}"
HEALTH_URL="${SHEETTRUTH_HEALTH_URL:-http://127.0.0.1:8000/api/health}"

sudo systemctl restart "$SERVICE"
for _ in $(seq 1 30); do
  if curl -sf "$HEALTH_URL"; then
    echo
    echo "$SERVICE is up"
    exit 0
  fi
  sleep 1
done
echo "$SERVICE did not answer at $HEALTH_URL" >&2
sudo systemctl status "$SERVICE" --no-pager >&2 || true
exit 1
