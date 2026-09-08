# Requirements — Employee Salary Management System

## Goal
Give ACME's HR Manager a web-based system to manage and understand salary
data for 10,000 employees across multiple countries, replacing spreadsheets
as the source of truth.

## Persona
HR Manager — single user of this system for the scope of this exercise.

## In Scope
- Employee directory: search, filter, and paginate across 10,000 employees
  (by name, email, country, department, role).
- View and edit an individual employee's salary record, with validation
  (no negative salary, valid currency, required fields).
- Analytics view answering "how does the org pay people": average and
  median salary by country, by department, by role, and overall salary
  distribution.
- Seed script generating 10,000 synthetic employees across multiple
  countries and currencies.

## Deliberately Out of Scope
- **Auth / multi-user access control** — the brief specifies a single HR
  Manager persona; building real auth adds surface area without
  demonstrating the skills this exercise assesses.
- **Payroll processing / disbursement / tax compliance** — this is a
  system of record and insight, not a payroll engine.
- **Excel import** — the seed script covers the need for populated data
  in this exercise; import tooling is a separate, later concern.
- **Full audit-log UI** — a lightweight audit trail at the data layer may
  be included cheaply, but a full history UI is not.
- **Pay-equity / demographic analytics** — kept to the four core cuts
  above to avoid scope creep and the extra care sensitive attributes
  require; a real product would revisit this deliberately, not as an
  afterthought.

## Tech Stack
- Backend: Python, FastAPI, SQLite, pytest
- Frontend: React (Vite), MUI
- Deployment: Render (backend as a web service, frontend as a static site)

## Performance Considerations
- 10,000 rows requires server-side pagination and filtering; the list
  view must never load the full table client-side.
- SQLite is sufficient for this scale and a single-instance demo; a
  real multi-writer production deployment would move to Postgres.

## Success Criteria
- HR Manager can find any of the 10,000 employees via search/filter.
- HR Manager can edit a salary and see the change persisted and validated.
- HR Manager can answer "how do we pay people" from the analytics view
  alone, without a spreadsheet.
- Seed script produces exactly 10,000 valid employee records.
- Core business logic (validation, aggregation) is covered by fast,
  deterministic unit tests.
