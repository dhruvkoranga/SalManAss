# SalManAss — Employee Salary Management

Web-based salary management software for ACME's HR team — 10,000 employees across
multiple countries, currently managed via spreadsheets. Built for the HR Manager
persona to view, edit, and answer questions about org-wide pay.

> **Status: scaffolding not yet built.** The commands below describe the target
> setup once the backend/frontend are scaffolded — they are not runnable yet.
> This banner will be removed once the steps are verified against a working repo.

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

### Not started
- [ ] Scaffold backend (FastAPI app, SQLite schema, pytest setup)
- [ ] Scaffold frontend (Vite + React + MUI)
- [ ] Employee data model + migrations
- [ ] Seed script — 10,000 employees across multiple countries
- [ ] Employee list view — paginated, filterable, searchable
- [ ] Single employee view/edit
- [ ] Analytics view — answer "how does the org pay people"
- [ ] Input validation (salary, currency, required fields)
- [ ] Unit tests — backend core logic
- [ ] Unit tests — frontend components
- [ ] Deploy to a hosting target (TBD — Render/Railway/Fly.io)
- [ ] Record video demo

### Deliberately deferred / out of scope (see docs/PRODUCT_THINKING.md)
- [ ] Multi-user auth / RBAC
- [ ] Payroll processing / disbursement
- [ ] Excel import
- [ ] Full audit-log UI

### Done
- [x] Git repo initialized, remote configured
- [x] CLAUDE.md — working rules for AI-assisted development
- [x] docs/ scaffolding — architecture, design patterns, approach, product thinking
- [x] Problem breakdown and stack decisions (Python/FastAPI, SQLite, React/Vite/MUI)
- [x] Write one-page requirements doc (docs/REQUIREMENTS.md)
