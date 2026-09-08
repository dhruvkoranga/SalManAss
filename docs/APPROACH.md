# Approach & Decision Log

A running log of decisions made while building this project, and the reasoning behind them. Newest entries at the top. This is where the "why" lives, since git history only shows the "what."

Each entry should be short: what was decided, why, and what alternative was considered (if any).

---

## Format for new entries

```
## YYYY-MM-DD — <short title>
**Decision:** what we chose to do.
**Why:** the reasoning / constraint that drove it.
**Alternative considered:** what else was on the table, if anything, and why it was rejected.
```

---

## 2026-09-08 — Project scaffolding: CLAUDE.md + docs structure

**Decision:** Set up [CLAUDE.md](../CLAUDE.md) with four core rules (think before coding, simplicity first, surgical changes, TDD/goal-driven execution), plus separate `docs/ARCHITECTURE.md`, `docs/DESIGN_PATTERNS.md`, and this file, kept apart from CLAUDE.md itself.

**Why:** Keeps the *behavioral rules* for how Claude should work (CLAUDE.md) separate from *project knowledge* that accumulates over time (the docs/ files) — CLAUDE.md should stay stable and short, while the docs grow with the project. This is also the user's first Python project coming from Java, so CLAUDE.md includes a note to keep explanations Java-relative and beginner-friendly.

**Alternative considered:** A single monolithic CLAUDE.md with everything inline — rejected because it would grow unbounded and mix stable rules with fast-changing project details.
