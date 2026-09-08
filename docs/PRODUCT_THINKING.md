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

Decided with the user rather than assumed, per [CLAUDE.md](../CLAUDE.md)'s "Think Before Coding" principle:

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

### 2026-09-08 — Stack decided
Resolved the 5 blocking stack questions with the user: **Python/FastAPI + SQLite + React (Vite)/MUI**. Remaining open questions (auth stance, deployment target, exact analytics questions) don't block writing `docs/REQUIREMENTS.md` — they can be stated as explicit decisions/scope calls within it. Next step: write `docs/REQUIREMENTS.md`.
