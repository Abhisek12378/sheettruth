# SheetTruth web application

- `backend/`: FastAPI service. `server.py` is the API and serves the built front end; `jobs.py`
  runs audits one at a time in a background worker and keeps each one in its own folder.
- `frontend/`: React + TypeScript (Vite). `npm run build` writes `backend/static`.
- `deploy/`: the systemd unit and the scripts the deployment pipeline runs on the server.

Run locally:

    pip install -r requirements.txt
    cd webapp/frontend && npm ci && npm run build && cd ../..
    uvicorn webapp.backend.server:app --host 0.0.0.0 --port 8000

API:

    POST /api/audits                 multipart: file (.xlsx), threshold (0 to 1); returns the job
    GET  /api/audits                 all jobs, newest first
    GET  /api/audits/{id}            job status, finished steps and, when done, the full result
    GET  /api/audits/{id}/report.md
    GET  /api/audits/{id}/report.json
    GET  /api/audits/{id}/corrected.xlsx   the workbook with confirmed fixes applied
    GET  /api/health
