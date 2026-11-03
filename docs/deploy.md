# Deployment

The application is one Python process (`webapp/backend`) that serves the built front end
(`webapp/frontend`). It needs LibreOffice for recalculation, a Modal account for the model
server, and optionally a reviewer endpoint. Node is only needed where the front end is built,
which the pipeline does.

## Pipeline

`.github/workflows/deploy.yml` runs on every push and pull request:

1. `test`: installs the Python dependencies and runs `pytest`.
2. `build-frontend`: `npm ci` and `npm run build` in `webapp/frontend`; the output
   (`webapp/backend/static`) is kept as a build artifact.
3. `deploy` (pushes to `main` only, after 1 and 2 pass): over SSH, runs
   `webapp/deploy/update.sh` on the server (checks out the pushed commit, installs
   dependencies), uploads the built front end with rsync, then runs
   `webapp/deploy/restart.sh` (restarts the systemd service and waits for `/api/health`).
   A failed health check fails the pipeline.

Repository secrets: `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY` (the private key as text). The job
uses the `production` environment, so a reviewer can be required before each deploy.

## Model server (once)

```
python -m modal token set --token-id <id> --token-secret <secret>
python -m modal deploy training/predict_glimmer_modal.py
```

The deployment starts GPU containers on demand and stops them after two minutes of inactivity,
so the first audit after a pause waits for the model to load (several minutes for a 30B model).
To keep one container warm during a live session, deploy with `SHEETTRUTH_MIN_CONTAINERS=1`.

## Server setup (Ubuntu, once)

```
sudo apt-get install -y libreoffice-calc rsync
git clone https://github.com/Abhisek12378/sheettruth.git ~/work/sheettruth
cd ~/work/sheettruth
python3 -m venv ~/work/.venv && ~/work/.venv/bin/pip install -r requirements.txt
python -m modal token set --token-id <id> --token-secret <secret>     # as the service user
sudo cp webapp/deploy/sheettruth.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now sheettruth
```

Settings in `/etc/sheettruth.env`, one `KEY=value` per line:

```
SHEETTRUTH_ADAPTER=/models/glimmer-sheettruth-v2/adapter
SHEETTRUTH_REVIEWER_BASE_URL=...
SHEETTRUTH_REVIEWER_MODEL=...
SHEETTRUTH_REVIEWER_API_KEY=...
```

Useful commands:

```
sudo systemctl status sheettruth
journalctl -u sheettruth -f
curl http://127.0.0.1:8000/api/health
```

Open port 8000 in the instance's security group. Uploads and results are kept under
`data/uploads/<job id>/`; delete a folder to remove an audit from the history.

## Manual deploy

The same steps the pipeline runs:

```
bash webapp/deploy/update.sh origin/main
cd webapp/frontend && npm ci && npm run build && cd ../..
bash webapp/deploy/restart.sh
```
