# Repository guidance

This repository is the local Python backend for Kimodo Motion Studio for
Godot. Keep it independently versioned from the Godot editor extension.

## Current phase

Milestone 0 establishes a reproducible upstream baseline before Studio API or
UI feature work. Prefer small changes with tests and record consequential
decisions in `docs/adr/`.

## Goal-oriented sessions

Read `docs/DEVELOPMENT_GOALS.md` before choosing work. It is the authoritative,
append-only progress record.

- Work on only the active goal unless the user explicitly changes the goal.
- Keep goals small enough for a focused session of roughly 20–60 minutes.
- Update task checkboxes, evidence, blockers, and the session log as work lands.
- Never delete completed goals or tasks; add a correction or superseding note.
- Run the goal's completion test before marking it complete.
- When a goal passes, mark it complete, commit the record, report the result,
  celebrate briefly, and end the turn. Do not begin the next goal until the
  user explicitly asks.
- If work exposes a blocker, record it and stop at a useful checkpoint rather
  than silently switching to another planned goal.

## Compatibility boundaries

- Preserve the standard MMCP capability and generation surface.
- Keep the `motionmcp_kimodo` namespace until an explicit migration decision.
- Return SOMA-77 at the service boundary; SOMA-30 is an internal model and
  constraint representation. The upstream code does not meet this invariant
  yet, so do not treat its current slicing behavior as the target design.
- Bind only to `127.0.0.1` by default. Remote access must be opt-in and must not
  weaken path, command, or token boundaries.
- Never run model loading or inference in the Godot editor process.
- Preserve upstream copyright, history, notices, and Apache-2.0 licensing.

## Verification

Run lightweight checks before GPU tests:

```powershell
python -m pytest
python -m ruff check .
```

Tests requiring weights, CUDA, or network access belong in explicitly marked
integration suites. Record GPU, driver, dependency commits, model hash, and
resolved settings for every benchmark.
