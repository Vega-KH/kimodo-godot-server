# Repository guidance

This repository is the local Python backend for Kimodo Motion Studio for
Godot. Keep it independently versioned from the Godot editor extension.

## Current phase

Goals 0–13 established the backend/extension vertical slice and persistent
target-first authoring state. Goal 13 passed its manual editor acceptance check.
Goal 14 implementation is complete and awaiting its final manual editor gate.
It replaces the draft metaphor with a session-first workspace and validates
two-take generation end to end. Unsaved take payloads remain transient until
the user explicitly saves one. The project is finishing the basic workflow
before advanced constraint authoring. Prefer small changes with tests
and record consequential decisions in `docs/adr/`.

## Goal-oriented sessions

Read `docs/DEVELOPMENT_GOALS.md` before choosing work. It is the authoritative
current-goal and progress ledger; the product workflows in the root development
plan take precedence if a historical note conflicts with them.

- Work on only the active goal unless the user explicitly changes the goal.
- Keep goals small enough for a focused session of roughly 20–60 minutes.
- Update task checkboxes, evidence, blockers, and the session log as work lands.
- Preserve the outcome, consequential corrections, acceptance evidence, and
  checkpoint commit for every completed goal. Older task lists and session notes
  may be summarized once they are more than three goals behind the current goal;
  Git remains the detailed historical record.
- Remove obsolete notes only when their useful decision/evidence has been
  retained elsewhere in the ledger, an ADR, or version history.
- Run the goal's completion test before marking it complete.
- When a goal passes, mark it complete, commit the record, report the result,
  and, unless a major blocker makes planning premature, lay out the next goal
  for user review. Commit the checkpoint and end the turn.
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
