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

## 2026-09-10 — Deferred: natural-language employee query

**Decision:** Don't build a free-form/natural-language query feature for fetching employee records (e.g. asking "list all engineers in Germany earning over ₹20L" and having it answered directly) in this iteration.

**Why:** Answering an open-ended query well means passing a non-trivial slice of the 10,000-row dataset to an LLM as context, and the token cost isn't fixed — it scales with how broad or vague the query is. A narrow query might stay cheap; a broad one ("show everyone above median pay") could need most of the dataset in context, making per-request cost unpredictable. The structured filter/sort/search UI already covers the day-to-day query patterns an HR manager needs, at a small, predictable cost (a plain SQL query, not an LLM call).

**Alternative considered:** None evaluated in depth — this is deferred, not rejected. Worth revisiting later with a scoped approach (e.g. querying only pre-aggregated summary data, or capping how many rows can be pulled into context) rather than open-ended free-form querying over the full dataset.

---

## 2026-09-09 — Render deploy: free tier, SQLite reseeded on every boot

**Decision:** Deploy both services on Render's free tier (`render.yaml` at repo root: `salmanass-backend` as a Python web service, `salmanass-frontend` as a static site). The backend's start command runs `alembic upgrade head && python -m scripts.seed` before `uvicorn` on every boot, so the app always comes up with a full 10,000-row dataset.

**Why:** Render's free web-service tier has an ephemeral filesystem — any local file, including the SQLite `app.db`, is wiped on every restart or 15-minute-idle spin-down. Since there's no persistent disk on the free tier, "the data survives" isn't actually on the table without paying; auto-reseeding on boot means a grader/viewer always sees a working, populated app rather than an empty database after the first idle timeout. The trade-off is real and accepted: any salary edits made during a live session are lost the next time the service spins down and back up. That's a fine trade for a graded demo, not for real use — matches `REQUIREMENTS.md`'s existing framing of this as "a single-instance demo," not a production deployment.

**Alternative considered:** Render's free Postgres tier (real persistence, but expires 30 days after creation) and a paid plan with a persistent disk (real persistence, no expiry, but costs money and wasn't something to commit the user to without asking). Both were offered explicitly; free-tier SQLite with reseeding was the chosen trade-off. Service-to-service URLs (`FRONTEND_ORIGIN`, `VITE_API_BASE_URL`) are hardcoded to the `<service-name>.onrender.com` pattern rather than wired automatically, because Render Blueprints' `fromService` only exposes a service's *private*-network host/port, not its public URL — there's no Blueprint-native way to reference another service's public address. If Render assigns different actual hostnames (name collision), those two env vars need a manual update after first deploy.

---

## 2026-09-08 — Project scaffolding: CLAUDE.md + docs structure

**Decision:** Set up [CLAUDE.md](../CLAUDE.md) with four core rules (think before coding, simplicity first, surgical changes, TDD/goal-driven execution), plus separate `docs/ARCHITECTURE.md`, `docs/DESIGN_PATTERNS.md`, and this file, kept apart from CLAUDE.md itself.

**Why:** Keeps the *behavioral rules* for how Claude should work (CLAUDE.md) separate from *project knowledge* that accumulates over time (the docs/ files) — CLAUDE.md should stay stable and short, while the docs grow with the project. This is also the user's first Python project coming from Java, so CLAUDE.md includes a note to keep explanations Java-relative and beginner-friendly.

**Alternative considered:** A single monolithic CLAUDE.md with everything inline — rejected because it would grow unbounded and mix stable rules with fast-changing project details.
