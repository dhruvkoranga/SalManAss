# SalManAss — Employee Salary Management

Web-based salary management software for ACME's HR team — 10,000 employees across
multiple countries, currently managed via spreadsheets. Built for the HR Manager
persona to view, edit, and answer questions about org-wide pay.

> **Status: deployed and live** — employee directory, salary editing, and
> analytics all work end-to-end against the real 10,000-row seeded dataset,
> both locally and at https://salmanass-frontend.onrender.com (FastAPI +
> SQLite backend, 33 passing tests; React + MUI frontend, 8 passing tests).
> Remaining work is the video demo — see TODO below.

See [docs/PRODUCT_THINKING.md](docs/PRODUCT_THINKING.md) for the problem breakdown
and [docs/APPROACH.md](docs/APPROACH.md) for the decision log.

## Tech Stack

**Backend:** Python, FastAPI, SQLite, pytest
**Frontend:** React (Vite), MUI (Material UI)

## Repo Layout

    SalManAss/
    ├── backend/     FastAPI app, SQLite DB, pytest tests
    ├── frontend/    React (Vite) app, MUI components
    ├── docs/        Requirements, architecture, product thinking, decision log
    └── CLAUDE.md    AI working rules for this repo

## Getting Started — Backend

    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    alembic upgrade head
    uvicorn app.main:app --reload

API docs (once running): http://localhost:8000/docs

## Getting Started — Frontend

    cd frontend
    npm install
    npm run dev

App (once running): http://localhost:5173

## Running Tests

    cd backend
    pytest

    cd frontend
    npm test

## Deployment

Live at:
- Frontend: https://salmanass-frontend.onrender.com
- Backend API: https://salmanass-backend.onrender.com/docs

[render.yaml](render.yaml) is the Render Blueprint defining both services on
the free tier: `salmanass-backend` (FastAPI) and `salmanass-frontend` (static
site). To redeploy elsewhere: push this repo to GitHub, then in the Render
dashboard use **New > Blueprint** and point it at the repo.

The two services' URLs are hardcoded to each other as
`https://salmanass-<backend|frontend>.onrender.com` (`FRONTEND_ORIGIN` for
CORS, `VITE_API_BASE_URL` for the frontend's API calls). If Render assigns
different actual hostnames (e.g. a name collision), update those two env vars
in the dashboard.

**Data does not persist across restarts on the free tier** — the backend's
start command reseeds all 10,000 employees on every boot since Render's free
tier has no persistent disk, and free services spin down after 15 minutes
idle (the first request after that takes ~30-60s to wake back up). See
`docs/APPROACH.md`'s 2026-09-09 entry for the full trade-off.

## TODO

### Backend
- [x] Scaffold backend (FastAPI app, SQLite schema, pytest setup)
- [x] Employee/Currency data models (SQLAlchemy)
- [x] Database migrations (Alembic) — `alembic upgrade head` before running the app
- [x] Employee list/search/filter/paginate (`GET /api/employees`)
- [x] Single employee view/edit (`GET`/`PUT /api/employees/{id}`)
- [x] Analytics endpoint answering "how does the org pay people" (`GET /api/analytics/summary`)
- [x] Currency list endpoint (`GET /api/currencies`) — backs the frontend's salary display and edit dropdown
- [x] Input validation (salary, currency, required fields)
- [x] Unit tests — backend core logic (33 tests passing)
- [x] Seed script — 10,000 employees across multiple countries (`python -m scripts.seed`)

### Frontend
- [x] Scaffold frontend (Vite + React + MUI, routing via react-router-dom)
- [x] Employee list view (paginated, filterable, searchable, currency-aware salary display)
- [x] Single employee view/edit
- [x] Analytics view (avg/median by country/department/role, salary distribution)
- [x] Unit tests — frontend components (8 tests passing)

### Other
- [x] Deploy to Render — live at https://salmanass-frontend.onrender.com (see Deployment above)
- [ ] Record video demo

### Deliberately deferred / out of scope (see docs/PRODUCT_THINKING.md)
- [ ] Multi-user auth / RBAC
- [ ] Payroll processing / disbursement
- [ ] Excel import
- [ ] Full audit-log UI

### Done (project setup)
- [x] Git repo initialized, remote configured
- [x] CLAUDE.md — working rules for AI-assisted development
- [x] docs/ scaffolding — architecture, design patterns, approach, product thinking
- [x] Problem breakdown and stack decisions (Python/FastAPI, SQLite, React/Vite/MUI)
- [x] Write one-page requirements doc (docs/REQUIREMENTS.md)
