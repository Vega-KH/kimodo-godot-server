# 0006 — Session deletion ownership and recoverable staging

Date: 2026-10-01
Status: accepted and implemented; Goal 21 manual acceptance passed 2026-10-01

## Decision

Session deletion belongs to a Godot domain service, not the backend or UI.
Read-only preflight validates the selected current-schema resource, UUID,
exclusive archive ownership and file inventory. It includes orphan generation
manifests in the count, honors later session take-deletion tombstones, and
separately reports missing source files. Duplicate IDs, shared archives, protected
outputs placed inside the managed tree, unknown files, traversal and links block
the operation with an explanation. Unsupported legacy/corrupt ownership is not
inferred from a filename.

The confirmation fingerprint includes the session, managed file inventory and
other project session resources. Execution repeats preflight. The only primary
targets are that exact session file and `session_data/<UUID>`, never arbitrary
artifact paths or the general animations directory. Export, acceptance and
profile-save destinations reject reserved managed storage.

Godot's [DirAccess.is_link](https://docs.godotengine.org/en/4.7/classes/class_diraccess.html#class-diraccess-method-is-link)
supports Windows junction/reparse detection. Validate every ancestor and managed
descendant before traversing/removing it; real junction and exclusive-file-lock
regressions exercise the supported Windows environment. This is not a claim of
race-proof deletion against a malicious concurrent filesystem actor.

Files are renamed into `session_deletions/<UUID>` beside a durable staging
receipt. Before commit, failure/restart restores the originals; after commit,
cleanup is retried until complete. Remaining files must match the recorded owned
inventory; changed/unrecognized staged content pauses cleanup. Do not describe
cross-file operations as atomic or promise OS Trash/Undo support.

A small committed identity receipt remains after payload purge. It prevents
retained autosave/archive/Accept resources from recreating deleted sessions.
Normal production-library Undo/Redo remains available without re-saving deleted
source data or clearing global editor undo. For nondeleted sessions, Accept Undo
updates acceptance fields on the latest saved resource, preserving newer history,
artifacts and intent. The active dock merges those fields without clearing
pending intent autosave.

## Consequences and evidence

- Exported/accepted libraries, saved Character Previews, imported models and
  shared certified rig profiles remain independent. Back up sessions and their
  managed source data together, and keep identity receipts while old editor
  actions/resources may still exist.
- An unrecognized incomplete staging directory blocks preflight; normal session
  archive recovery must resolve it before ownership can be claimed. No broad
  garbage-collection sweep is introduced.
- Automated tests cover empty/multi-take/multi-generation counts, missing and
  deleted archives, orphan manifests, duplicate/shared ownership, protected
  outputs, stale confirmation, real Windows junctions/locks, injected failure
  and both interruption phases. Dock tests cover cancel, active/inactive delete,
  more than eight entries, generation gating, late callbacks and actual retained
  Undo/Redo. Existing Add/Replace compensation tests remain in the full suite.
- Stage 1 completion still requires the owner's manual workflow gate.
