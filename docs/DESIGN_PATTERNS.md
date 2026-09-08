# Design Patterns & Coding Conventions

This document tracks the patterns and idioms used in this codebase, and why — so choices stay consistent as the project grows, and so a Java developer new to Python has a reference for "why does this look different from Java."

> Status: project not yet started. This file will be filled in as real patterns emerge — don't pre-populate it with patterns we aren't using yet (see Simplicity First in [CLAUDE.md](../CLAUDE.md)).

## Conventions

- **Style**: follow [PEP 8](https://peps.python.org/pep-0008/) (Python's standard style guide — think of it as the Java equivalent of Google's Java Style Guide).
- **Type hints**: used on function signatures for clarity, not enforced at runtime (Python's type hints are documentation + tooling support, not a compiler check like Java's).
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes — same idea as Java's class naming, different casing for methods/variables (Java uses `camelCase`).

## Patterns in Use

_None yet. Each entry below should say: what the pattern is, where it's used, and why it was chosen over the alternative — added only once actually adopted, not speculatively._

<!-- Example entry format:
### Repository Pattern
Used in: `src/data/`
Why: isolates data access so storage can change without touching business logic.
-->

## Java → Python Quick Reference

| Java | Python | Note |
|---|---|---|
| Interface | `abc.ABC` / duck typing | Python often skips formal interfaces; duck typing is idiomatic |
| `HashMap` | `dict` | |
| `ArrayList` | `list` | |
| Method overloading | default args / `*args`, `**kwargs` | Python has no overloading |
| `static` method | `@staticmethod` / module-level function | Module-level functions are often preferred |
| Checked exceptions | (none) | All Python exceptions are unchecked |
| Maven/Gradle | `pip` + `requirements.txt` / `pyproject.toml` | |
| JUnit | `pytest` | |
