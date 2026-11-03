# SheetTruth front end

React + TypeScript, built with Vite. The build output goes to `webapp/backend/static`, which the
FastAPI server serves at `/`. The deployment pipeline builds it; it is not committed.

Develop (with the API running on port 8000):

    npm install
    npm run dev

Build for the server:

    npm run build
