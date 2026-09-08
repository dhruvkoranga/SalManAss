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
│   ├── main.py          FastAPI app, route registration
│   ├── base.py           SQLAlchemy DeclarativeBase (own module to avoid a
│   │                      circular import between models.py and db.py)
│   ├── models.py        SQLAlchemy models (Currency, Employee)
│   ├── schemas.py       Pydantic request/response schemas
│   ├── exceptions.py     domain exceptions (EmployeeNotFoundError, etc.),
│   │                      framework-agnostic, translated to HTTP by routers
│   ├── db.py             engine/session setup + data-access functions
│   ├── routers/
│   │   ├── employees.py
│   │   └── analytics.py
│   └── seed.py            generates Currency rows + 10,000 employees
└── tests/
    ├── test_models.py
    ├── test_schemas.py
    ├── test_db.py
    ├── test_employees.py     (routers, once built)
    ├── test_analytics.py
    └── test_seed.py
```

## Frontend Structure

```
frontend/
└── src/
    ├── api/client.ts        fetch wrappers for the endpoints above
    ├── pages/
    │   ├── EmployeeList.tsx     MUI DataGrid, server-side pagination/filter
    │   ├── EmployeeDetail.tsx   view/edit salary
    │   └── Analytics.tsx        the "how do we pay people" view
    └── components/            shared pieces (filters, charts)
```

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
- The seed script has one dedicated test asserting it produces exactly 10,000 valid
  employee rows. This test is slower by nature and is kept separate from the fast
  unit suite. Faker is seeded with a fixed random value so the seed script's output
  is still deterministic, not just fast.

## Performance Considerations

- Indexes on `country`, `department`, `job_title`, and `currency_id` — cheap to add,
  meaningful once filtering is in active use, even though 10,000 rows would still be
  fast unindexed.
- The employee list endpoint always paginates server-side; the frontend never
  fetches all 10,000 rows at once.
- SQLite is adequate at this scale for a single-instance demo; a real multi-writer
  production deployment would move to Postgres (see REQUIREMENTS.md).

## External Dependencies

- **FastAPI** — web framework, chosen for async support, built-in OpenAPI docs, and
  strong pairing with Pydantic for validation.
- **SQLAlchemy** — ORM, chosen over raw SQL for a real migrations story (Alembic)
  and to keep the codebase idiomatic for a typical FastAPI project.
- **Pydantic** — request/response validation, ships with FastAPI.
- **Faker** — generates realistic seed data (names, emails) instead of hand-rolled
  random strings.
- **pytest** — test runner.
- **React (Vite) + MUI** — frontend framework and component library; MUI's DataGrid
  has strong built-in support for the 10,000-row list, filtering, and pagination.
