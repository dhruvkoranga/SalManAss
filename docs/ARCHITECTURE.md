# Architecture

This document describes the system's structure: modules, how they depend on each other, and how data flows through them. It's a living document — update it whenever a structural decision is made, not after the fact.

> Status: project not yet started. This file will be filled in as the first modules are built.

## Overview

_TBD — one paragraph on what the system does and its major moving parts, once they exist._

## Module Layout

```
SalManAss/
├── CLAUDE.md
├── docs/
│   ├── ARCHITECTURE.md      (this file)
│   ├── DESIGN_PATTERNS.md
│   └── APPROACH.md
├── src/                     (source modules — TBD)
├── tests/                   (pytest tests, mirrors src/ layout)
└── requirements.txt / pyproject.toml
```

## Data Flow

_TBD — describe how data/requests move through the system once there's more than one module._

## External Dependencies

_TBD — list any third-party libraries and why each was chosen, once added._
