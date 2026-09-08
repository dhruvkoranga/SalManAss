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

## 5. Open Questions (still blocking REQUIREMENTS.md)

1. **Auth** — build a minimal single-user login (even a hardcoded HR Manager account) to signal awareness of the concern, or explicitly state it's out of scope in REQUIREMENTS.md and skip entirely? Leaning toward stating it out of scope explicitly, since building real auth doesn't showcase anything the assignment is grading, but a one-line stub is cheap if it reads as more "production."
2. **Deployment target** — needs to be free/simple and support a FastAPI backend + static/SPA frontend + SQLite. Candidates: Render, Railway, Fly.io. Still needs a decision.
3. **"How the org pays people" — which specific questions does the analytics view need to answer?** E.g. avg/median by country, by department, by role, pay equity gaps, salary distribution histograms, top/bottom percentiles. Worth deciding 3-5 concrete questions rather than building an open-ended BI tool.

## 6. Working Log

Dated entries as thinking evolves — append, don't rewrite history.

### 2026-09-08 — Initial problem breakdown
Read the assignment brief, broke down goal/persona/problem statement, drafted a scope split (in/out), and surfaced 8 open questions. Nothing built yet.

### 2026-09-08 — Stack decided
Resolved the 5 blocking stack questions with the user: **Python/FastAPI + SQLite + React (Vite)/MUI**. Remaining open questions (auth stance, deployment target, exact analytics questions) don't block writing `docs/REQUIREMENTS.md` — they can be stated as explicit decisions/scope calls within it. Next step: write `docs/REQUIREMENTS.md`.
