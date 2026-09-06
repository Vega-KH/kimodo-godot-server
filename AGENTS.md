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
  and, unless a major blocker makes planning premature, lay out the next goal
  for user review. Commit the checkpoint, celebrate briefly, and end the turn.
  Do not begin the proposed goal until the user explicitly approves it.
- If work exposes a blocker, record it and stop at a useful checkpoint rather
  than silently switching to another planned goal.

## Compatibility boundaries

- Preserve the standard MMCP capability and generation surface.
- Keep the `motionmcp_kimodo` namespace until an explicit migration decision.
- Return SOMA-77 at the service boundary; SOMA-30 is an internal model and
  constraint representation. Goal 3 established this invariant and its golden
  fixtures; do not restore the inherited 77-to-30 response slice.
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
