# Architecture

This document describes the system's structure: modules, how they depend on each other, and how data flows through them. It's a living document — update it whenever a structural decision is made, not after the fact.

See [REQUIREMENTS.md](REQUIREMENTS.md) for scope and [PRODUCT_THINKING.md](PRODUCT_THINKING.md) for the reasoning behind these choices.

## Overview

Employees span two countries, each tied to one currency: **United States (USD)** and
**India (INR)**. Salaries are stored in the employee's local currency; cross-currency
aggregates (by department, by role) convert to **INR** at query time using an exchange
rate stored on the `Currency` table, rather than storing a duplicated/snapshotted
INR value on every employee row.

## Data Model

```
Currency
  id                      PK
  code                    "USD" | "INR", unique
  symbol                  "$" | "₹"
  exchange_rate_to_inr    value of 1 unit of this currency, in INR (INR = 1.0)

Employee
  id                      PK
  first_name, last_name
  email                   unique
  country                 "United States" | "India"
  department              e.g. Engineering, Sales, HR, Finance
  job_title               e.g. Software Engineer, Sales Manager
  salary_amount           numeric, in the employee's local currency
  currency_id             FK -> Currency
  hire_date
  created_at, updated_at  basic audit trail
```

No manager/reporting-line field — REQUIREMENTS.md's in-scope list is name, country,
department, and role; org-chart visualization is explicitly out of scope, so adding
a hierarchy field now would be scope creep.

## API (FastAPI, REST)

```
GET  /api/employees?search=&country=&department=&role=&page=&page_size=
GET  /api/employees/{id}
PUT  /api/employees/{id}          edit salary (+ department/role/currency)
GET  /api/currencies              for the edit form's currency dropdown
GET  /api/analytics/summary       avg/median by country, department, role + distribution
```

Cross-currency aggregates convert each row to INR via
`salary_amount * currency.exchange_rate_to_inr` inside the SQL query — computed at
query time via a join, not a stored column. At 10,000 rows this join has no
meaningful performance cost, so there is no need to denormalize.

## Backend Structure

Flat structure: routers call data-access functions directly. No separate service or
repository layer — the app is a CRUD + aggregation system, and a full layered
architecture would be abstraction the app doesn't need yet (see CLAUDE.md's
"Simplicity First"). Data-access functions are still plain, independently testable
functions.

```
backend/
├── app/
│   ├── main.py          FastAPI app, route registration, exception handlers
│   ├── deps.py            real (file-based) DB wiring + get_db dependency;
│   │                      own module so main.py and routers/ don't import
│   │                      each other
│   ├── base.py           SQLAlchemy DeclarativeBase (own module to avoid a
│   │                      circular import between models.py and db.py)
│   ├── models.py        SQLAlchemy models (Currency, Employee)
│   ├── schemas.py       Pydantic request/response schemas
│   ├── exceptions.py     domain exceptions (EmployeeNotFoundError, etc.),
│   │                      framework-agnostic, translated to HTTP by routers
│   ├── db.py             engine/session setup + data-access functions
│   ├── routers/
│   │   ├── employees.py
│   │   ├── analytics.py
│   │   └── currencies.py  read-only list, backs the edit form's currency
│   │                      dropdown and the list view's salary display
│   └── seed_data.py       pure data/generation logic for the seed script
│                          (kept out of scripts/ so it's unit-testable without
│                          touching a real database)
├── scripts/
│   └── seed.py            CLI: clears + repopulates Currency/Employee rows
│                          in app.db via seed_data.build_employees()
├── alembic.ini            points at sqlite:///./app.db, same hardcoded path
│                          as app/deps.py
├── alembic/
│   ├── env.py             target_metadata = Base.metadata (imports app.models
│   │                      so tables are registered before autogenerate)
│   └── versions/          one migration so far: initial schema (Currency,
│                          Employee) — the existing 10,000-row app.db was
│                          `alembic stamp head`-ed onto it, not re-migrated
└── tests/
    ├── test_models.py
    ├── test_schemas.py
    ├── test_db.py
    ├── test_employees_router.py
    ├── test_analytics.py
    ├── test_analytics_router.py
    ├── test_currencies_router.py
    ├── test_seed_data.py
    └── test_migrations.py    runs `alembic upgrade head` against a temp
                               SQLite file, asserts the expected tables/columns
```

Schema is owned by Alembic for the real database (`alembic upgrade head` before
running the app); `tests/conftest.py` still uses `Base.metadata.create_all()` /
`drop_all()` directly against a temporary SQLite file per test — migrations
would only slow the fast, isolated unit-test setup down for no benefit there.

## Frontend Structure

```
frontend/
└── src/
    ├── api/client.ts        fetch wrappers + types for the endpoints above
    ├── utils/format.ts      formatMoney() — fixed-locale currency formatting,
    │                        shared so the locale bug below can't recur per-page
    ├── pages/
    │   ├── EmployeeList.tsx     MUI DataGrid, server-side pagination/filter
    │   ├── EmployeeDetail.tsx   view/edit salary
    │   └── Analytics.tsx        the "how do we pay people" view
    └── components/
        ├── SalaryByCategoryChart.tsx    avg-vs-median grouped bar (by
        │                                 country/department/role)
        └── SalaryDistributionSummary.tsx  five-number-summary range bar
```

**Locale gotcha:** `Number(x).toLocaleString(undefined, ...)` uses the
*runtime's* default locale — on this dev machine that produced Indian-style
digit grouping (`1,20,000.00`) instead of the intended `120,000.00`, which
would make salary display depend on the deployed server's OS locale. Fixed by
pinning `'en-US'` explicitly in `formatMoney()` rather than passing `undefined`.

The frontend reads the backend's URL from `VITE_API_BASE_URL` (default
`http://localhost:8000` for local dev). The backend allows that origin via
`CORSMiddleware`, configurable through `FRONTEND_ORIGIN` — required because
Render deploys the frontend and backend as separate services (different
origins), not just a local-dev convenience.

## Data Flow

1. Frontend requests a page of employees with filters as query params.
2. `employees` router validates params (Pydantic), calls a data-access function in
   `db.py`, which runs a filtered, paginated SQL query via SQLAlchemy.
3. Results are serialized through a Pydantic response schema and returned as JSON.
4. Editing a salary: frontend sends a `PUT`, the router validates the payload
   (no negative salary, valid currency), the data-access layer updates the row.
5. The analytics endpoint runs aggregate SQL queries (`GROUP BY` country/department/
   role, with the INR-conversion join described above) and returns precomputed
   summary numbers — no client-side aggregation of raw rows.

## Testing Strategy

- Unit/integration tests run against a temporary SQLite database created fresh per
  test (SQLAlchemy `create_all` / `drop_all`), seeded with a handful of deterministic
  rows — not the full 10,000. This keeps the suite fast and isolated, per CLAUDE.md's
  TDD rule (fast, deterministic tests).
- `test_seed_data.py` exercises `build_employees()` at a small n (200), not the
  full 10,000 — enough to assert correctness (unique emails, valid currency
  refs, positive salaries, known country/department/role values) while staying
  fast. Each test passes a seeded `random.Random` instance so results are
  deterministic. The actual 10,000-row run only happens via `scripts/seed.py`
  against the real database, not in the test suite.

## Performance Considerations

- Indexes on `country`, `department`, `job_title`, and `currency_id` — cheap to add,
  meaningful once filtering is in active use, even though 10,000 rows would still be
  fast unindexed.
- The employee list endpoint always paginates server-side; the frontend never
  fetches all 10,000 rows at once.
- SQLite is adequate at this scale for a single-instance demo; a real multi-writer
  production deployment would move to Postgres (see REQUIREMENTS.md).
- **Analytics median/percentiles are computed in Python (`statistics` module),
  not SQL.** SQLite has no built-in median/percentile function (unlike Postgres'
  `percentile_cont`). At 10,000 rows, pulling matching rows into Python and
  computing average/median/percentiles there is instant and simple — but this
  is a deliberate scale limit, not a free lunch. `AVG()` alone would be fine to
  push into SQL at any size; it's specifically the median calculation that
  requires this workaround. At a much larger scale (roughly 1M+ employees),
  this would need to change — either move to Postgres for a native
  `percentile_cont()`, or use an approximation algorithm (e.g. t-digest) rather
  than sorting the full dataset. Not built now, since the app is scoped at
  10,000 employees and building for a scale that doesn't exist yet would be
  premature (see CLAUDE.md's "Simplicity First").

## External Dependencies

- **FastAPI** — web framework, chosen for async support, built-in OpenAPI docs, and
  strong pairing with Pydantic for validation.
- **SQLAlchemy** — ORM, chosen over raw SQL for a real migrations story and to
  keep the codebase idiomatic for a typical FastAPI project.
- **Alembic** — schema migrations against `app.db`. `target_metadata` points at
  `Base.metadata`, so new migrations are autogenerated from model changes
  rather than hand-written.
- **Pydantic** — request/response validation, ships with FastAPI.
- No new dependency for seed data — the seed script (`backend/scripts/seed.py`)
  builds names/emails from small hand-rolled lists in `app/seed_data.py` rather
  than adding Faker, since the volume of names needed doesn't earn a dependency.
- **pytest** — test runner.
- **React (Vite) + MUI** — frontend framework and component library; MUI's DataGrid
  has strong built-in support for the 10,000-row list, filtering, and pagination.
- **react-router-dom** — routes between the three pages (employee list, employee
  detail, analytics); the standard routing choice for a multi-page React app.
- **@mui/x-charts** — same vendor family as the DataGrid already in use; gives
  the Analytics page accessible SVG bar charts (tooltips, responsive sizing,
  MUI theme integration) without hand-rolling scaling/hover/accessibility
  logic. Chart colors follow the categorical/sequential palette from the
  project's dataviz skill (fixed hue order, not generated per-series).
