# Repository guidance

This repository is the independently versioned Python backend for Kimodo Motion
Studio for Godot. Inference never runs inside the editor.

## Start of a development session

Read the shared product documents in the sibling extension repository:
`../godot-kimodo/docs/README.md`, then its product plan, DEVELOPMENT_GOALS.md
and AGENT_HANDOFF.md. Product workflows supersede historical task lists.
If that checkout is absent, use
https://github.com/Vega-KH/godot-kimodo/tree/main/docs rather than recreating a
second roadmap in this repository.

Goals 0–21 and Stage 1 are complete and user-accepted (2026-10-01).
Stage 2 starts with poses; propose the next detailed goal for review before
implementation. Aim for useful, generic assistance, not exhaustive rig coverage.

## Goal-oriented work

- Work on one explicitly approved goal; stop for discussion on major blockers
  or architectural changes instead of applying a suboptimal workaround.
- Record concrete defects and repair nearby ones with regressions when in scope.
- Keep the current goal/proposal concise in the shared DEVELOPMENT_GOALS.md.
  Preserve completed outcomes, important corrections, evidence and commits in
  compact history; Git retains detailed obsolete lists.
- Complete automated, relevant rendered/live and user manual gates before marking
  a goal complete. User has authorized commit/push after completed, tested goals.
- Record completion, commit/push affected repositories, then propose the next
  goal for approval. Do not implement that proposal without approval.
- Permanent compatibility/security decisions belong in `docs/adr/`; supersede
  accepted ADRs rather than rewriting their historical decisions.

## Compatibility and preservation boundaries

- Preserve MMCP capability/generation endpoints and `motionmcp_kimodo` namespace.
- SOMA-77 is the canonical/output rig; SOMA-30 is internal model/constraint data.
  Never restore the inherited 77→30 output slice. Preserve six contact channels.
- Bind only to `127.0.0.1` by default. Remote deployment needs explicit
  authentication, error/path hardening and approval.
- Keep Python/CUDA/model weights outside the editor and add-on distribution.
- Preserve upstream history, copyright, notices and Apache-2.0 licensing.
- Never clean, stage or modify user animation archives, independent exports,
  private model originals or shared artist profiles as incidental test work.

## Verification

Use the existing checkout environment, lightweight checks before GPU work:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
```

Hardware/network tests are explicit integration checks. Record actual GPU,
dependency/model identity and resolved settings for benchmarks. The project-owned
venv can require owner-context execution under the agent sandbox; this is not
proof of a broken Python installation. See the shared handoff and
`docs/SERVER_ARCHITECTURE.md` for current code/test notes.
