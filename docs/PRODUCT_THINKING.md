# Product Thinking & Problem Breakdown

Living notebook for this project. Unlike [APPROACH.md](APPROACH.md) (a log of *decisions already made*), this file captures the *thinking in progress* — how we're breaking the problem down, what's still open, and why we're leaning one way or another. It gets messier and more honest than the polished deliverables; that's the point.

The polished, one-page requirements doc required by the assignment will live separately at `docs/REQUIREMENTS.md`, written once the scope decisions below are settled — per the assignment's own instruction to write it *before* building.

---

## 1. The Assignment, Restated

**What's being assessed:** not "can you build a CRUD app" but *how you think* — problem framing, scoping judgment, architecture calls, test discipline, and how deliberately you use AI tooling. The commit history itself is a graded artifact — it needs to read as a real, incremental build, not a single dump.

**Goal:** salary management software for ACME, an org with 10,000 employees across multiple countries.

**Persona:** HR Manager. One persona, not many — so every feature should be justifiable in terms of *what does the HR Manager need to do or know?* If a feature doesn't trace back to an HR Manager task or question, it's probably out of scope.

**Problem statement, decoded:** today this lives in spreadsheets. The pain of spreadsheets isn't "no UI" — it's:
- No structured querying ("how do we pay people?" is hard to answer from a flat sheet across multiple files/tabs)
- No validation (typos, inconsistent currency formats, duplicate rows)
- No audit trail (who changed what salary, when, why)
- No access control (anyone with the file can edit anything)
- Multi-country data (currencies, maybe different pay structures) mixed together

So "web-based software" is the delivery mechanism; the actual value is **structured data + the ability to answer questions about pay** ("how does the org pay people" is explicitly called out — this is an analytics/reporting need, not just a data-entry replacement).

## 2. Deliverables Checklist (from the assignment)

- [ ] One-page requirements doc (`docs/REQUIREMENTS.md`) — written before building
- [ ] End-to-end functional software: backend + UI
- [ ] Backend: language/framework (JD-preferred, or free choice) + relational DB
- [ ] UI: React/Next.js (or Angular+Java) + a component library
- [ ] Seed script generating 10,000 employees
- [ ] Deployed, working instance
- [ ] Video demo
- [ ] Unit tests: meaningful coverage of core functionality, fast/deterministic/readable
- [ ] Clean code structure, readability, maintainability
- [ ] Incremental commit history showing evolution
- [ ] Artifacts: requirements doc, design notes, architecture diagrams, AI prompts/instructions used, trade-off explanations, performance considerations

This file plus [APPROACH.md](APPROACH.md), [ARCHITECTURE.md](ARCHITECTURE.md), and [DESIGN_PATTERNS.md](DESIGN_PATTERNS.md) together are meant to satisfy the "artifacts" ask — rather than one giant doc, the thinking is split by concern.

## 3. Scope Thinking (draft — not final until REQUIREMENTS.md is written)

### Almost certainly in scope
- Employee records: name, ID, country, currency, salary, department/title, manager/reporting line (useful for "how do we pay people" cuts), start date.
- List/search/filter employees (10,000 rows — needs real pagination + server-side filtering, not a client-side dump).
- View + edit a single employee's salary record.
- Some form of aggregate/analytics view answering "how does the org pay people": e.g. average/median salary by country, department, role; salary bands; distribution. This is the feature that directly answers the problem statement's explicit question — it shouldn't be an afterthought.
- Basic validation (no negative salaries, valid currency codes, required fields).
- Seed script for 10,000 synthetic employees across multiple countries/currencies.

### Leaning out of scope (needs to be justified explicitly in REQUIREMENTS.md, not just silently dropped)
- Authentication/multi-user RBAC — single HR Manager persona is explicit in the brief. A real product would need this, but building full auth is a lot of surface area that doesn't demonstrate the core ask. **Open question below.**
- Payroll processing / actually paying anyone (tax, disbursement, compliance per country) — out of scope; this is a *system of record + insight*, not a payroll engine.
- Full audit-log UI (though an audit trail *field/table* might be cheap to include and worth it for "production quality" signaling — separate from building a full history UI).
- Import from Excel (nice-to-have, not core — the seed script replaces the need for it in this exercise).
- Org chart / manager hierarchy visualization beyond simple filtering.

### Genuinely undecided — see Open Questions

## 4. Stack Decisions (resolved 2026-09-08)

Decided with the user rather than assumed, per the project's "Think Before Coding" principle:

1. **Backend**: Python + **FastAPI**. Matches the repo's existing Python/pytest setup; async, fast to scaffold, built-in OpenAPI docs, plays well with TDD.
2. **Database**: **SQLite**. Zero-ops, file-based, matches the assignment's own example, plenty for 10k rows and a single-user demo.
3. **Frontend**: **React (Vite) + MUI**. No SSR/routing overhead we don't need for a single-persona data app; MUI's DataGrid gives strong built-in support for the 10k-row list + filtering + analytics views.

These will be stated (with brief rationale) in `docs/REQUIREMENTS.md` and `docs/ARCHITECTURE.md` once those are written.

## 5. Remaining Decisions (resolved 2026-09-08)

1. **Auth**: explicitly **out of scope**, stated with reasoning in `docs/REQUIREMENTS.md`. The brief specifies a single HR Manager persona; real auth adds surface area without demonstrating anything this exercise is grading.
2. **Deployment target**: **Render**. Free tier supports a FastAPI web service plus a static site for the React build; simple git-push deploy; SQLite file persists fine for a low-traffic single-instance demo.
3. **Analytics scope**: **Core 4** — average/median salary by country, by department, by role, plus overall salary distribution. Directly answers "how do we pay people" without scope-creeping into an open-ended BI tool; demographic/pay-equity cuts deliberately deferred (see REQUIREMENTS.md for reasoning).

## 6. Working Log

Dated entries as thinking evolves — append, don't rewrite history.

### 2026-09-08 — Initial problem breakdown
Read the assignment brief, broke down goal/persona/problem statement, drafted a scope split (in/out), and surfaced 8 open questions. Nothing built yet.

### 2026-09-08 — Stack decided
Resolved the 5 blocking stack questions with the user: **Python/FastAPI + SQLite + React (Vite)/MUI**. Remaining open questions (auth stance, deployment target, exact analytics questions) don't block writing `docs/REQUIREMENTS.md` — they can be stated as explicit decisions/scope calls within it. Next step: write `docs/REQUIREMENTS.md`.

### 2026-09-08 — Requirements finalized
Resolved the 3 remaining open questions: auth is explicitly out of scope, deployment target is Render, analytics scope is the "core 4" (country/department/role/distribution). Wrote `docs/REQUIREMENTS.md` — the one-page requirements doc is now complete. Next step: architecture (`docs/ARCHITECTURE.md`) and then scaffolding the backend under TDD.

### 2026-09-08 — Architecture decided
Resolved 3 architecture-level questions: a normalized `Currency` table (USD/INR, exchange rate to USD) instead of a snapshotted per-employee value; SQLAlchemy ORM + Pydantic over raw SQL; a flat backend structure (routers + a data-access module) over a layered services/repository split. Scope narrowed to two countries — United States (USD) and India (INR). Wrote `docs/ARCHITECTURE.md`. Next step: scaffold the backend under TDD, starting with the data model and seed script.

### 2026-09-08 — Correction: base currency for cross-currency aggregation is INR
User specified INR, not USD, as the pivot currency for org-wide aggregates
(department/role cuts). Updated `docs/ARCHITECTURE.md`: `Currency.exchange_rate_to_usd`
(divisive, local units per 1 USD) became `exchange_rate_to_inr` (multiplicative, value
of 1 unit of that currency in INR; INR row = 1.0). No code existed yet, so this was a
docs-only fix. Also fixed a leftover issue in `docs/DESIGN_PATTERNS.md`, which still had
Java-background framing and a Java-comparison table from before CLAUDE.md was split into
public/local versions — moved that content into the gitignored `CLAUDE.local.md`.

### 2026-09-09 — First backend TDD slices: models, schemas, FK enforcement
Wrote `Currency`/`Employee` SQLAlchemy models and their first persistence test
(Red confirmed via a hidden-implementation run, then Green). Added `EmployeeUpdate`
Pydantic schema with syntactic validation (salary must be greater than zero, not
just non-negative; required fields) — deliberately separate from semantic
validation (does a given currency actually exist), which needs the database and
belongs with the future CRUD layer.

User then asked whether `test_employee_persists_with_its_currency` actually proved
`currency_id` was validated. It didn't: SQLite does not enforce foreign key
constraints by default, so an `Employee` could reference a nonexistent
`currency_id` and SQLite would silently accept it. Proved the gap with a failing
test first (`DID NOT RAISE IntegrityError`), then fixed it by enabling
`PRAGMA foreign_keys=ON` via a connection event listener in `app/db.py`, and the
same test now passes. A good example of the "grill at junctions" rule catching a
real correctness gap, not just a hypothetical one.

### 2026-09-09 — update_employee_salary(): validation loop closed
Added `update_employee_salary()` to `app/db.py` — the deferred semantic
"valid currency" check from the schema slice is now implemented (raises
`InvalidCurrencyError` for an unknown currency_id, `EmployeeNotFoundError` for
an unknown employee id; see the new Domain Exceptions pattern in
`docs/DESIGN_PATTERNS.md`). REQUIREMENTS.md's validation criteria (no negative
salary, valid currency, required fields) are now fully covered end to end:
Pydantic for syntax, this function for DB-existence checks.

Hit and fixed a circular import while implementing it: `app/db.py` needed to
import `Employee`/`Currency` from `app/models.py`, which already imported
`Base` from `app/db.py`. Extracted `Base` into its own `app/base.py` — the
standard fix for this exact situation. Caught immediately by actually running
the test suite, not by inspection.

### 2026-09-09 — list_employees(): the read side (search, filter, paginate)
Added `list_employees()` to `app/db.py` — search (name + email, case-insensitive
via `ilike`), exact-match filters (country, department, job_title), and
offset/limit pagination with a total count for pagination metadata. Uses a
stable `ORDER BY` (last_name, first_name, id), since LIMIT/OFFSET pagination is
only reliable with one.

User asked for email to be included in search, which REQUIREMENTS.md didn't
originally list — updated its in-scope line to "by name, email, country,
department, role" rather than letting the doc silently drift from what's
actually built. 10 tests in `test_db.py` now (3 update, 7 list/search/paginate),
16 passing overall.

### 2026-09-09 — First running server: FastAPI router for employees
Added `app/main.py`, `app/deps.py`, and `app/routers/employees.py` — the app
is now an actual running server for the first time (`GET /api/employees`,
`GET /api/employees/{id}`, `PUT /api/employees/{id}`), not just tested
functions. Caught a second circular import before writing any code, this time
between `main.py` (needs the router) and `routers/employees.py` (needs
`get_db` from main) — fixed with the same pattern as the models/db.py cycle:
extract the shared piece (`get_db` and the real database wiring) into a new
leaf module, `app/deps.py`, that neither `main.py` nor the router depends on
the other for.

`app/db.py` gained `get_employee()`, and `update_employee_salary()` was
refactored to reuse it instead of duplicating the not-found check.

21 tests passing. Two deprecation warnings surfaced from inside the
fastapi/starlette libraries themselves (not our code) — noted, not chased,
since fixing them would mean guessing at dependency changes rather than
fixing a line we actually wrote.

### 2026-09-09 — Analytics endpoint: the backend API surface is complete
Added `get_analytics_summary()` (`app/db.py`) and `GET /api/analytics/summary`.
Chose a five-number summary (min/p25/median/p75/max) for "overall salary
distribution" since REQUIREMENTS.md didn't specify a shape and a histogram
would need arbitrary bucket-width decisions the requirements don't call for.

Real technical constraint: SQLite has no median/percentile aggregate, so
median and percentiles are computed in Python via the `statistics` module
after pulling matching rows out of SQL (`AVG()` alone would not have needed
this — only median does). User asked whether this holds up well beyond 10,000
rows; answered honestly: it would still be correct but would get memory- and
transfer-heavy well before it got CPU-heavy, and the real fix at large scale
is a database with native percentile support (Postgres) or an approximation
algorithm, not a smarter Python loop. Documented as a deliberate, stated scale
limit in `docs/ARCHITECTURE.md`'s Performance Considerations, not a hidden one.

27 tests passing. The backend API surface (employees + analytics) is now
functionally complete; next is the seed script for real data, then the
frontend.
