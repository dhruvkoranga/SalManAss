# Design Patterns & Coding Conventions

This document tracks the patterns and idioms used in this codebase, and why — so choices stay consistent as the project grows and future readers understand the reasoning, not just the result.

> This file is filled in as real patterns emerge — don't pre-populate it with patterns we aren't using yet (see Simplicity First in [CLAUDE.md](../CLAUDE.md)).

## Conventions

- **Style**: follow [PEP 8](https://peps.python.org/pep-0008/), Python's standard style guide.
- **Type hints**: used on function signatures for clarity; Python's type hints are documentation and tooling support, not an enforced compile-time check.
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes.

## Patterns in Use

Each entry says: what the pattern is, where it's used, and why it was chosen over
the alternative — added only once actually adopted, not speculatively.

### DTO / Schema Separation
Used in: `app/models.py` (persistence) vs. `app/schemas.py` (API contract).
Why: decouples what's stored from what's exposed over the API — either can
change without forcing a change in the other.

### Data Mapper
Used in: `app/models.py`, via SQLAlchemy's declarative ORM.
Why: `Employee`/`Currency` are plain objects with no built-in save/load
methods; a separate `Session` (see `app/db.py`) handles all persistence.
Keeps the model classes trivially testable without a database.

### Factory Function for Session Creation
Used in: `app/db.py`, `create_session_factory()`.
Why: tests and the real app get differently-configured database connections
(in-memory SQLite vs. a real file) from the same function, without
duplicating engine/session setup logic.

### Domain Exceptions
Used in: `app/exceptions.py` (`EmployeeNotFoundError`, `InvalidCurrencyError`),
raised from `app/db.py`'s data-access functions.
Why: `app/db.py` has no reason to know HTTP exists. Plain Python exceptions
keep the data-access layer usable outside a web context (e.g. from the seed
script or a test) and let the future router layer decide how to translate
"not found" into a 404 — the failure and its HTTP representation are
different concerns.

