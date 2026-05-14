# AudioFix Project Memory

Shared memory for coding agents. Keep this file concise and durable: architecture, ownership, defaults, workflow rules, and hard-won debugging notes only.

## Workflow
- Treat this file as the project source of truth before non-trivial edits.
- Update it when architecture, defaults, APIs, or debugging lessons change.
- Do not store secrets, personal data, machine-local scratch notes, or session logs.
- Format ToDo plans with numbered sections (`### 1. file/topic`) and lettered checkbox substeps (`- [ ] a) ...`).
- After significant changes, provide a concise git commit message.

## Utility Summary
the initial tool will be used as a one to many audio file converter such that a single audio file can be converted to multiple files of different volumes / amplitudes.

## Design Principles
- **Single source of truth:** Defaults, parameters, constants etc should have one owner.

- **Single-path behavior:** Prefer one deterministic runtime path. Centralize unavoidable branching and route callers through it.

- **Readability:** Small functions are fine when they clarify real work. Avoid abstractions that hide API, timing, or hot-path state.

- **Efficiency:** optimize code to avoid unecessary loops abd big O complexity.

- Treat what I say as a hypothesis, not a fact, unless we have proof. If I am wrong, then correct me directly.


## File Map


## Core Architecture Rules
keep things modular and organized

## GUI/Layout Rules
gui elements should have a clear and consistent placement system

