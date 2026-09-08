# CLAUDE.md

Guidance for Claude Code when working in this repository. This is a **Python** project.

For project-specific context, see:
- [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) — one-page requirements: goal, scope, what's deliberately out
- [docs/PRODUCT_THINKING.md](docs/PRODUCT_THINKING.md) — problem breakdown, scope thinking, open questions
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system structure, modules, data flow
- [docs/DESIGN_PATTERNS.md](docs/DESIGN_PATTERNS.md) — patterns and idioms used, and why
- [docs/APPROACH.md](docs/APPROACH.md) — decisions made along the way and their rationale

---

## Guiding Principles

- Think deeply before coding — surface tradeoffs, don't default to the first idea.
- Make thoughtful, pragmatic architecture and design decisions.
- Build systems that are maintainable and understandable, not just functional.
- Use tools — including AI — intentionally, to raise quality and speed, not as a substitute for thinking.
- Write production-quality code and tests.
- Show product thinking, not just implementation — trace decisions back to the actual problem and persona, not just the ticket.

---

## The 4 Core Principles

### 1. Think Before Coding

Don't make silent assumptions. If a request has more than one reasonable interpretation, or key details are missing, **stop and ask before writing code**.

- State assumptions explicitly rather than burying them in the implementation.
- If uncertain about intent, ask — don't guess.
- If multiple valid approaches exist, present the tradeoffs and let the user pick. Don't silently choose one.
- If a simpler approach exists than the one implied by the request, say so before building the complicated version.

### 2. Simplicity First

Build the minimum code required to solve the problem in front of us. Nothing speculative.

- No abstractions, config options, or "flexibility" for use cases that don't exist yet.
- No premature optimization.
- If a function/class is only used once, don't generalize it "just in case."
- Rule of thumb: if it could be written in a quarter of the lines, rewrite it. Ask: *would a senior engineer call this overcomplicated?*
- Prefer Python's standard library and built-ins over adding a dependency, unless the dependency clearly earns its place.

### 3. Surgical Changes

Diffs should be tightly scoped to the request.

- Only touch files/lines directly relevant to the task.
- Don't "improve" adjacent code, comments, or formatting while passing through.
- Don't refactor things that aren't broken, even if they look messy — that's a separate, explicitly-requested task.
- Match the existing style of the file (naming, quote style, import ordering) rather than imposing new conventions mid-file.
- Test: every changed line should trace directly back to the user's request.

### 4. Goal-Driven Execution (TDD)

This project follows **Test-Driven Development**. For any new behavior:

1. **Red** — write a failing test first that describes the desired behavior.
2. **Green** — write the minimum code to make it pass.
3. **Refactor** — clean up only what you just wrote, with tests still green.

Rules that follow from this:

- Don't write implementation code before there's a failing test for it, unless the user explicitly says otherwise (e.g. a throwaway script).
- Define done as "tests pass," not "looks right." Run the test suite before declaring a task complete.
- Tests live alongside the code they cover, in a `tests/` directory mirroring the source layout (standard `pytest` convention).
- Use `pytest` as the test runner unless the user says otherwise.
- A bug fix gets a regression test first, reproducing the bug, before the fix goes in.

---

## Code Style

- No emoji anywhere in the codebase — code, comments, commit messages, docs, UI copy — unless explicitly asked for.
- Comments: plain, simple English. Explain only the non-obvious *why* (a hidden constraint, a workaround, a subtle invariant) — never restate *what* the code already says.

---

## Environment

- OS: Windows (PowerShell primary shell).
- Repo layout: `backend/` (FastAPI + pytest + SQLite) and `frontend/` (React/Vite/MUI), each with its own dependency management.
- Backend: `venv` for dependency isolation, `pytest` for testing.
- Frontend: `npm` for dependency management, its own test runner (Vitest, once frontend is scaffolded).

---

## Working With Me (Process)

- **Plan before execute.** No file write — code, tests, docs, config, anything — happens without a proposed plan first and explicit approval from the user. This applies to every change, not just large ones.
- **Grill at junctions.** At any real decision point — scope, architecture, tech stack, implementation-level choices, product calls — don't silently pick the reasonable-sounding option and move on. Push back, surface the tradeoffs, and make the user commit to a direction before proceeding.
- **Commits are yours to make.** After a change is reviewed and any grilling is
  done, the user runs `git commit`/`git push` themselves — not me. I prepare and
  stage changes (or leave them unstaged for review) and stop there.
