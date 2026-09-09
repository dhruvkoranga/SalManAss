# SalManAss — Employee Salary Management

Web-based salary management software for ACME's HR team — 10,000 employees across
multiple countries, currently managed via spreadsheets. Built for the HR Manager
persona to view, edit, and answer questions about org-wide pay.

> **Status: backend is scaffolded and runnable** (FastAPI app, SQLite, 31 passing
> tests) — the Backend setup steps below are verified. **Frontend is not yet
> scaffolded**; its setup steps are still aspirational. This banner will be
> removed once both sides are built and verified.

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

## TODO

### Backend
- [x] Scaffold backend (FastAPI app, SQLite schema, pytest setup)
- [x] Employee/Currency data models (SQLAlchemy)
- [ ] Database migrations (Alembic) — currently using `Base.metadata.create_all()`,
      no real migration tooling yet
- [x] Employee list/search/filter/paginate (`GET /api/employees`)
- [x] Single employee view/edit (`GET`/`PUT /api/employees/{id}`)
- [x] Analytics endpoint answering "how does the org pay people" (`GET /api/analytics/summary`)
- [x] Input validation (salary, currency, required fields)
- [x] Unit tests — backend core logic (31 tests passing)
- [x] Seed script — 10,000 employees across multiple countries (`python -m scripts.seed`)

### Frontend
- [ ] Scaffold frontend (Vite + React + MUI)
- [ ] Employee list view (paginated, filterable, searchable)
- [ ] Single employee view/edit
- [ ] Analytics view
- [ ] Unit tests — frontend components

### Other
- [ ] Deploy to a hosting target (TBD — Render/Railway/Fly.io)
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
