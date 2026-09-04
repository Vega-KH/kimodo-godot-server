# Repository guidance

This repository is the local Python backend for Kimodo Motion Studio for
Godot. Keep it independently versioned from the Godot editor extension.

## Current phase

Milestone 0 establishes a reproducible upstream baseline before Studio API or
UI feature work. Prefer small changes with tests and record consequential
decisions in `docs/adr/`.

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
