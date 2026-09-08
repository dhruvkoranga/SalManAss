# CLAUDE.md

Guidance for Claude Code when working in this repository. This is a **Python** project, and it's the user's **first Python project** — they come from a Java background. Explain Python idioms in terms of Java equivalents when it helps (e.g. "a Python `dict` is like a Java `HashMap`", "no static typing by default, but we use type hints — think of them as lightweight Java-style declarations").

For project-specific context, see:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system structure, modules, data flow
- [docs/DESIGN_PATTERNS.md](docs/DESIGN_PATTERNS.md) — patterns and idioms used, and why
- [docs/APPROACH.md](docs/APPROACH.md) — decisions made along the way and their rationale

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

## Beginner-Friendly Python Notes (for a Java developer)

Since this is a first Python project, favor clarity over cleverness, and briefly call out Python-specific gotchas when they come up — things that don't map cleanly from Java, e.g.:

- Indentation is syntactic (no braces).
- Duck typing / no mandatory interfaces — but we still use type hints (`def foo(x: int) -> str:`) for clarity, similar in spirit to Java method signatures.
- No method overloading — use default arguments or `*args`/`**kwargs` instead.
- `__init__.py`, modules, and packages vs. Java's package/class file structure.
- Virtual environments (`venv`) are Python's answer to per-project dependency isolation (loosely: Maven/Gradle's dependency scoping, but for the interpreter environment itself).

Keep explanations short — a sentence or two — not a lecture. Only explain what's relevant to the code being touched.

## Environment

- OS: Windows (PowerShell primary shell).
- Use `venv` for dependency isolation.
- Use `pytest` for testing, `pip` + `requirements.txt` (or `pyproject.toml`, once we decide) for dependencies.
