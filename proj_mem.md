# AudioFix Project Memory
Shared memory for coding agents. Keep this file concise and durable: architecture, ownership, defaults, workflow rules, and hard-won debugging notes only.

## Workflow
- Treat this file as the project source of truth before non-trivial edits.
- Update it when architecture, defaults, APIs, or debugging lessons change.
- Do not store secrets, personal data, machine-local scratch notes, or session logs.
- Format ToDo plans with numbered sections (`### 1. file/topic`) and lettered checkbox substeps (`- [ ] a) ...`).
- After significant changes, provide a concise git commit message.

## Project Summary
- The initial tool is a one-to-many batch loudness converter.
- The user manually analyzes the source audio in a separate program, then enters a dB offset into AudioFix.
- AudioFix generates multiple quieter output files from one source file.
- The user controls the number of output files / steps and the dB interval between files.
- Output files must have unique numbered names: `filename_0.ogg`, `filename_1.ogg`, `filename_2.ogg`, etc.
- Each conversion run must generate a log file that records the source file, output file names, and dB levels used.

## Design Principles
- **Single source of truth:** Defaults, parameters, constants etc should have one owner.

- **Single-path behavior:** Prefer one deterministic runtime path. Centralize unavoidable branching and route callers through it.

- **Readability:** Small functions are fine when they clarify real work. Avoid abstractions that hide API, timing, or hot-path state.

- **Efficiency:** Avoid unnecessary decode/encode passes and redundant file processing.

- **Skepticism:** Treat what I say as a hypothesis, not a fact, unless we have proof. If I am wrong, then correct me directly.


## File Map
- `README.md`: public project summary and MVP scope.
- `proj_mem.md`: durable agent/project memory and architecture rules.
- `docs/ideas.md`: future ideas, restoration references, and non-MVP notes.
- `src/audiofix/gui/`: Tkinter GUI. Keep it thin; route behavior through `audiofix.core`.
- `src/audiofix/core/`: conversion planning, naming, defaults, ffmpeg command construction, and log generation.
- `src/audiofix/resources/`: package resources, if needed later.
- `vendor/ffmpeg/`: bundled ffmpeg/ffprobe runtime resources.
- `tools/`: maintenance scripts for dependency/resource updates and release prep.
- `docs/`: supporting technical notes.
- `tests/`: focused tests for deterministic core behavior.

## Core Architecture Rules
- Keep things modular and organized.
- Keep conversion defaults, naming rules, and dB step calculations in one owner module.
- Prefer one deterministic conversion path for GUI-triggered and future CLI-triggered runs.
- Avoid third-party Python runtime libraries for the MVP unless the standard library becomes a real blocker.
- Prefer bundled `ffmpeg`/`ffprobe` binaries for user-facing builds; system ffmpeg fallback is acceptable for development.
- Runtime resource updates should be explicit maintenance actions, not silent downloads during conversion.

## GUI/Layout Rules
- GUI elements should have a clear and consistent placement system.
- MVP controls should include source file, output folder, dB offset, number of files / steps, dB interval, run action, progress/status, and log location.
- Maintain basic light and dark themes with standard-library `ttk`; default to dark while keeping light available.
- Use a traditional top menu bar for global app actions. Current pattern: `View > Theme` for theme selection and `Help > About AudioFix` for app information.
