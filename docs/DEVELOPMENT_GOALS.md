# Development goals and project ledger

Last reviewed: **2026-09-25**

Current product stage: **basic workflow**

Current goal: **Goal 15 — Proposed; awaiting approval**

## How to use this document

The basic and advanced workflows at the beginning of
`../../Kimodo_Godot_Bridge_Research_and_Development_Plan.md` are the highest
project authority. This ledger translates that product intent into small,
reviewable implementation goals.

- Work on exactly one user-approved goal at a time.
- A goal is complete only after its stated acceptance test passes and evidence
  is recorded here.
- Completed goals may be summarized once they are more than three goals behind
  the current goal. Preserve their outcome, important corrections, verification
  evidence, and checkpoint commit; Git retains the detailed historical text.
- Record newly discovered code defects in the repair ledger instead of
  silently expanding the active goal.
- After completing a goal, update this ledger, commit the affected repository
  or repositories, propose the next goal, and stop until the user approves it.
- Do not treat a preview or a saved diagnostic artifact as artist acceptance.

## Current direction

Goals 0–13 established a working transport, playback, retargeting, and
persistent-authoring vertical slice. The next phase must turn it into the
intended basic workflow:

1. create or reopen a project-owned session before authoring controls appear;
2. select the character and autosave every meaningful session transition;
3. generate and compare several takes on that character;
4. validate full-skeleton retargeting, including fingers;
5. explicitly accept one take into native animation data.

`MotionDraft` was the Goal 13 implementation name. The product concept is now
**session**: a persistent, conversation-like workspace containing target and
intent history, exact generation records, take references, and saved artifact
references. A **take** is one motion variation returned by a generation. A
session, generation, take, saved artifact, and accepted animation are distinct
states and must remain distinct in code and UI.

SOMA-77, the synthetic Godot humanoid, and their save buttons remain valuable
diagnostic layers, but they must not define the artist-facing workflow.

## Repository checkpoints

| Repository | Current reviewed checkpoint | Notes |
| --- | --- | --- |
| `kimodo-godot-server` | `c79c9df` | Goal 14 implementation evidence on `codex/milestone-0-bootstrap` |
| `godot-kimodo` | `fb16d7b` | Goal 14 implementation and UI refactor on `main` |

The user authorized pushes after each completed and tested goal. Goal 14's
completion record and implementation checkpoints are pushed before Goal 15
begins.

The repositories remain independently versioned. The server keeps the
`motionmcp_kimodo` namespace and MMCP surface until a deliberate migration.

## Completed goals

| Goal | Date | Durable outcome | Checkpoint evidence |
| --- | --- | --- | --- |
| 0 | 2026-09-04 | Forked and locked the Windows/CUDA backend; verified model load, MotionCorrection, deterministic dummy generation, and MMCP capability service. | Server `c90cf82`, `688ea8b` |
| 1 | 2026-09-05 | Loaded the full Meta-Llama-3/LLM2Vec encoder on CPU, generated through live loopback MMCP, and stayed below 8 GB VRAM. | Server `d3c2d43`; Kimodo patch `3362b92` |
| 2 | 2026-09-06 | Froze the inherited pre-SOMA-77 contract with hashed capability, response, glTF, and error fixtures. | Server `4fc31b6` |
| 3 | 2026-09-06 | Removed the inherited 77-to-30 response slice; kept SOMA-30 constraints internal and exposed SOMA-77 plus six contacts. | Server `06a5f8c`, `def4acf`; ADR 0003 |
| 4 | 2026-09-06 | Created the Godot repository, imported the recorded glTF in memory, and played the canonical 77-bone fixture. | Godot `f1f9982`; server ledger `b1ddd16` |
| 5 | 2026-09-06 | Baked deterministic, self-contained native SOMA-77 Godot animation and verified save/reload/playback. | Godot `986306a`; server ledger `6011277`; ADR 0001 |
| 6 | 2026-09-06 | Added the loopback-only asynchronous capability client and the first functional AI Motion dock. | Godot `b358606`; server ledger `98815f3` |
| 7 | 2026-09-07 | Added typed one-sample generation, strict glTF validation, cancellation-safe client state, and embedded source preview. | Godot `5680fa1`; server ledger `c755141`; ADR 0002 |
| 8 | 2026-09-07/08 | Added backend launcher, 100-step default, unique native-take saving, backend-independent reload, and a scrollable dock. | Godot `aa0a675`, `a6f1f0f`; server ledger `188543e`, `7a66730` |
| 9 | 2026-09-08 | Added deterministic SOMA-77→56-bone humanoid retargeting; corrected planar locomotion ownership from `Hips` to `Root`. | Godot `f40fc5d`, `5327522`; server ledger `ff1422c`, `7d98484`; ADR 0003 |
| 10 | 2026-09-23 | Added dock humanoid preview/save, synchronized scrub/playback, orbit/zoom/root-follow, and a 200-step ceiling. | Godot `ddd1e07`, `961218b`; server ledger `02a8f0f`, `418d86c` |
| 11 | 2026-09-24 | Drove the rooted Jenny Auto-Rig Pro fixture; corrected rest-direction transfer after a holding-walk exposed shoulder/neck defects; added CC BY 4.0 attribution. | Godot `3466190`, `71346ad`; server ledger `0642202`, `ae973ca` |
| 12 | 2026-09-24 | Added a `PackedScene` target picker, validated exact-name compatible rigs, synchronized skinned preview, and unique self-contained character-scene saving. | Godot `d985782`; server ledger `8e379dd` |
| 13 | 2026-09-25 | Added target-first persistent authoring state, exact generation provenance, atomic project-contained save/load, and successful-save-only artifact tracking. | Godot `3e415b2`; server ledger `bb5b57f` |
| 14 | 2026-09-25 | Replaced drafts with autosaved sessions, added strict two-take generation and transient payload ownership, split the dock into focused components, and simplified preview/save into a selected-take workflow. | Godot `0898724`–`fb16d7b`; server `f5cb0a5`, `c79c9df` |

### Corrections that remain architecturally binding

- Service responses preserve all 77 SOMA joints; never restore the inherited
  30-joint response slice.
- Planar locomotion belongs to the profile `Root`; `Hips` retains vertical
  pelvis motion.
- Retargeting uses semantic rest-direction normalization. Directly transferring
  target rest offsets reproduced visible arm/neck defects and must not return.
- The rooted `Jenny03.glb` is the current acceptance asset. Its success proves
  this rig convention only; it does not certify arbitrary Godot humanoids.

## Goal 13 — Persist a target-first motion draft with provenance

Status: **Complete**

Completed: **2026-09-25**

### Why this goal changed

The earlier proposal persisted the current generation form and described saved
artifact references as accepted output. That would preserve the existing
source-first engineering workflow and create an acceptance concept before the
product has an Accept action. The revised goal makes the selected character
and draft the basic-workflow entry point, separates editable intent from an
immutable generation record, and reserves acceptance for Goal 15.

### Outcome sought

An artist can select a compatible character, create or open a project-owned
`MotionDraft`, edit generation intent, generate one current candidate, save the
draft, restart Godot with the backend stopped, and recover the target, intent,
provenance, and valid artifact references without mutation or regeneration.

### Scope

- [x] Define a versioned `MotionDraft` `Resource` with a stable draft ID and
  UTC creation/update times.
- [x] Store target state as project-relative data: character scene path,
  deterministic skeleton signature, optional future rig-profile reference,
  and intended animation destination. Do not serialize live nodes.
- [x] Store editable intent separately: prompt, frame count, seed, denoising
  steps, and fields reserved for later candidate count/presets.
- [x] Store an immutable generation record when a validated response enters
  the dock: exact request JSON and hash, capability snapshot and hash,
  protocol/model/fps/skeleton identity, response hash, and generation time.
  Requested settings and returned/negotiated data must remain distinguishable.
- [x] Store artifact references by type and save status. Update a reference
  only after its corresponding save succeeds. A preview is not an artifact and
  a saved artifact is not yet an accepted candidate.
- [x] Add one centralized project-path validator used by draft and existing
  save flows. Resolve/canonicalize paths and prove the result remains under the
  project root; a `res://` string prefix alone is insufficient.
- [x] Keep draft serialization, hashing, and path handling outside
  `ai_motion_dock.gd`. Extract enough state/controller code that adding
  persistence does not further entangle the current 1,073-line UI class.
- [x] Present draft and target selection before generation in the dock. Loading
  a draft restores the compatible target and editable inputs; the diagnostic
  source-only path may remain available but must be visually secondary.
- [x] Add explicit New, Save, Save As, and Load behavior. New/Save As choose a
  unique project-relative path; Save updates the explicitly loaded draft;
  unsupported schema versions and invalid paths fail without partial writes.
- [x] On offline load, report missing target/artifact paths individually and
  keep the remaining draft usable. Never contact the backend or regenerate as
  a side effect of loading.
- [x] Add round-trip, schema-version, deterministic-hash, path-containment,
  missing-artifact, unique-save, source-immutability, and plugin-lifecycle
  tests.
- [x] Save a Jenny draft after one known generation, restart the editor with
  the backend stopped, reload it, and manually verify target, inputs,
  provenance, and artifact status.

### Implementation evidence — 2026-09-25

- `KimodoMotionDraft`, `KimodoMotionDraftStore`, and `KimodoProjectPaths` keep
  the versioned resource, state transitions, canonical hashing, atomic save,
  and project-containment rules outside the dock.
- The dock now starts with draft/target controls before prompt generation,
  retains the exact MMCP request, capability response, and returned bytes as
  hashed provenance, and attaches only successfully saved artifacts.
- Native and humanoid multi-file bakers remove partial output if a later save
  stage fails. All existing save flows use the centralized canonical path
  validator.
- New and Load clear transient source/humanoid/character previews, disable
  stale save actions, and reset their status text before the next generation.
- A clean automated dock destruction/recreation with disconnected clients
  restored Jenny, editable intent, provenance, and artifact links without a
  connection or generation side effect. The Jenny source hash was unchanged.
- The real Windows OpenGL renderer produced a 480×1000 narrow-dock capture;
  target-first ordering, status text, provenance summary, and scrolling were
  visually sound.
- The user completed the real Godot editor check: after a known Jenny
  generation and restart with the backend stopped, the draft restored its
  target, inputs, provenance, and artifact state correctly. The user also
  reported that the dock has become confusing and cluttered; that finding
  directly motivates Goal 14's session-first UI boundary.

### Completion test

1. Jenny can be selected before generation and is represented in a new draft
   by a project-relative path plus a repeatable skeleton signature.
2. A generated result produces an exact, immutable generation record; changing
   editable inputs afterward does not rewrite that record.
3. Only successful native/humanoid/character saves update their artifact
   entries, and none is labeled accepted.
4. After a clean Godot 4.7.2 restart with the backend stopped, loading the
   draft restores target and inputs and reports available/missing artifacts
   without touching the target or starting generation.
5. All existing offline tests plus the new draft/path/lifecycle suite pass
   without script errors, engine errors, stale nodes, or partial files.

Stop condition: mark Goal 13 Complete, record evidence in this ledger, commit
and push the affected repository or repositories, propose Goal 14, and stop
before multi-candidate generation, comparison, server job orchestration, or
native animation acceptance.

## Goal 14 — Session-first workspace and multiple takes

Status: **Complete — 2026-09-25**

Approved: **2026-09-25**

### Why this goal changed

Goal 13 proved persistence but exposed the wrong product metaphor and an
overgrown dock. The resource called `MotionDraft` does not contain a draft
animation; it contains authoring state, generation history, and references to
saved data. The user wants the ChatGPT-like model instead: open or create a
session first, then work inside it, with automatic persistence at every
meaningful boundary. Generation controls should not exist outside an active
session.

This restructure must happen before adding several takes; otherwise take
comparison would deepen the current UI/state entanglement and make migration
more painful.

### `num_samples` research result

The user's interpretation is correct, with one important seed caveat:

- NVIDIA's [Kimodo CLI documentation](https://research.nvidia.com/labs/sil/projects/kimodo/docs/user_guide/cli.html)
  defines `num_samples` as the number of motion variations and writes one file
  per sample for values greater than one.
- Kimodo's [model implementation](https://github.com/nv-tlabs/kimodo/blob/main/kimodo/model/kimodo_model.py)
  uses `num_samples` as batch dimension `B`; output arrays have one motion per
  batch entry.
- The pinned MMCP SDK's
  [`MotionResult`](https://github.com/animatica-ai/motionmcp/blob/a298338bb3684a506ec313dce6d5cb12a6dc5167/motionmcp/backbone.py)
  defines rotations as `(B,T,J,4)`; its
  [glTF encoder](https://github.com/animatica-ai/motionmcp/blob/a298338bb3684a506ec313dce6d5cb12a6dc5167/motionmcp/gltf.py)
  writes one animation named `sample_0`, `sample_1`, and so on and creates one
  matching `MMCP_motion.samples[]` entry per animation. The request schema
  accepts 1–16, and the advertised default limit is 16.
- The current Kimodo adapter already passes `options.num_samples` to the model
  and returns the full batch. However, this repository has only tested
  `num_samples == 1`, and the Godot parser currently requires exactly one
  source animation. The advertised limit is therefore not yet a product claim.
- A request has one seed. Kimodo seeds once and samples a batch; it does not
  return an independent seed for each variation. Changing batch size can also
  change deterministic results. A take must therefore be identified by its
  generation record plus sample index and content hash, never by an invented
  per-take seed.

### Outcome sought

Opening the plugin shows a quiet session chooser, not generation controls. An
artist creates or opens a project-owned session, chooses a compatible
character, generates a tested number of takes in one request, and switches
between those takes on the selected character. Unsaved take payloads are
transient; closing/reopening Godot restores durable session state and saved
artifact references without preserving every discarded motion.

The session autosaves. There is no manual session Save button and no hidden
dirty state that can be lost at Generate, target change, artifact save, editor
shutdown, or session switch.

### State model

- **Session:** project-owned workspace, title/identity, current target and
  settings, generation/take history, artifact references, and timestamps.
- **Generation:** one exact request/capability/response provenance event. It
  owns the request seed shared by its returned batch.
- **Take:** one variation within a generation, identified by stable take ID,
  generation ID, sample index/name, and decoded-motion content hash.
- **Transient take payload:** validated response bytes and decoded previews
  retained in memory, with an optional disposable project cache. They are not
  session history and may be removed when the editor or session closes.
- **Saved artifact:** an explicit native/humanoid/character export linked to a
  take. It is not accepted merely because it exists.
- **Accepted animation:** remains absent until the later acceptance goal.

### Scope

- [x] Introduce a versioned `KimodoSession` model and session store. Rename the
  product/UI terminology from draft to session; do not merely relabel widgets
  while keeping draft-shaped ownership.
- [x] Add a lossless schema migration from Goal 13 `MotionDraft` resources.
  Preserve IDs, target signatures, editable intent, exact generation records,
  and artifact links. Loading an old draft must never overwrite it in place.
- [x] Start in a session landing state that exposes only New Session, Open
  Session, and a small recent-session list. Backend, prompt, generation,
  preview, retarget, and export controls remain unconstructed or hidden until
  a session is active.
- [x] Require a validated project-owned character before Generate is enabled.
  Keep diagnostic SOMA/humanoid layers available inside the session but
  secondary to the selected-character workflow.
- [x] Break the 1,400-line dock into a focused session shell, generation/take
  component, combined Preview & Save component, and explicit session
  controller. Avoid a visual-only rearrangement that leaves state transitions
  in the widget class.
- [x] Replace manual draft Save/Save As with atomic autosave and a visible
  `Saving…` / `Saved` / actionable-error indicator. Mark state dirty on edits,
  debounce ordinary field changes, and force a save at session creation,
  validated target change, immediately before Generate, after a validated
  response provenance is recorded, after artifact save, before session switch, and
  on editor shutdown.
- [x] Append generation provenance only after the complete response validates,
  and never add an artifact reference before its file exists. Use temporary
  files plus atomic rename/rollback so a crash cannot leave a partial session
  manifest.
- [x] Keep validated response bytes and decoded takes in memory or an explicitly
  disposable cache until the user saves a take. Persist provenance and take
  summaries/hashes in the session, not every generated animation payload.
- [x] Add backend contract tests for `num_samples == 2` proving Kimodo-style
  `(B,T,J,...)` arrays survive `MotionResult` validation and serialize as two
  ordered glTF animations plus two matching metadata entries.
- [x] Run one short fixed-request live loopback generation with
  `num_samples == 2`. Verify both takes are structurally valid and distinct,
  record latency/RAM/VRAM relative to one sample, and reduce the exposed limit
  to tested behavior rather than trusting `max_num_samples: 16`.
- [x] Extend the Godot response layer to parse all response animations and
  correlate them one-to-one with `MMCP_motion.samples[]`. Reject duplicate
  names, count/order mismatches, invalid tracks, or cross-sample metadata.
- [x] Let the artist request the tested take count and switch quickly between
  takes on the selected character while preserving playback time, loop state,
  camera, and root-follow state. Use the term **take**, not candidate or sample,
  in artist-facing UI.
- [x] Keep take selection beside the preview and make that selected take the
  save source. Convert SOMA-77 to humanoid and character previews automatically
  after generation instead of exposing redundant retarget/preview actions.
- [x] Replace output directory/name fields and three save buttons with one
  output-type selector (default Character), one Save action, and Godot's native
  project save dialog. Reject existing scene or companion-resource paths rather
  than silently overwriting or renaming the artist's requested output.
- [x] Keep every take non-destructive. Switching, regenerating, changing the
  target, closing the editor, and reopening offline must not alter the source
  character or existing project animation. Unsaved take previews need not
  survive a restart and must be reported honestly as unavailable.
- [x] Autosave the old target state before changing character. Retain prior
  generations/takes with their target snapshot and rebuild previews lazily for
  the new current target.
- [x] Add migration, session-gating, autosave/coalescing, atomic-failure,
  provenance/take-summary round-trip, multi-animation parsing, offline reopen, target
  switch, preview synchronization, source-immutability, and node-lifecycle
  tests.
- [x] Update the plan, README, and repair ledger, including measured
  multi-take behavior and the exact tested maximum exposed by the UI.
- [x] Manually verify the complete session-first workflow with Jenny: launch to
  the session chooser, create a session, choose Jenny, generate multiple takes,
  switch takes, save one selected take, restart with the backend stopped,
  reopen the session, and verify that session state plus the saved artifact
  remain while unsaved take payloads are not presented as durable.

### Implementation evidence — 2026-09-25

- Added schema-versioned `KimodoSession`, atomic session store, explicit
  session controller, and lossless `MotionDraft` migration. The original draft
  is hash-checked and remains byte-identical; autosave covers debounced edits
  plus every forced workflow boundary.
- The dock now launches to a quiet chooser and constructs an active workspace
  around focused session, generation/take, and combined Preview & Save
  components. Generate requires both an active session and a validated
  character target. Successful generation automatically creates all three
  preview layers; the preview-local take selector controls both viewing and
  saving.
- The former directory/name matrix and three save buttons are replaced by an
  output-type selector plus one Godot project save dialog. Character is the
  default output, and explicit collision rejection prevents accidental
  overwrites. The orchestration shell fell from 1,643 to about 1,036 lines.
- The typed request permits the tested one- or two-take range. The response
  parser enforces exact ordered animation/metadata correspondence, isolates
  each animation into an independent scene, hashes decoded motion content,
  and rejects duplicate names, count/order mismatches, and cross-sample data.
- Take payloads are owned by a transient in-memory set. The durable session
  records provenance and take summaries; only an explicitly saved selected
  take becomes an artifact. Reopening offline does not pretend discarded
  payloads are playable.
- Backend boundary coverage proves a two-item `(B,T,77,4)` batch survives
  `MotionResult` validation and serializes as ordered `sample_0`/`sample_1`
  glTF animations with matching metadata.
- A final live 20-step, two-take run completed in 5.85 seconds inference / 6.59
  seconds wall time with a 147,763-byte response, 13.23 GiB peak server working
  set, and 1,708 MiB baseline/peak total GPU allocation. Both decoded motions
  had distinct hashes, retargeted to Jenny, switched cleanly, and leaked no
  nodes. The exposed maximum remains two despite the backend advertising 16.
- Comparative measurements are workload/cache sensitive. A same-session
  back-to-back reference measured one take at 3.69 seconds generation / 4.45
  seconds wall and two at 6.46 / 7.42 seconds; server working set and reported
  total GPU allocation were effectively unchanged. This latency did not make
  the editor materially unresponsive, so server job cancellation remains a
  later hardening item rather than a Goal 14 blocker.
- The post-refactor live two-take regression also passed: 7.23 seconds reported
  generation / 7.41 seconds wall, the same 147,763-byte response, 15.57 GiB
  peak server working set, and 1,411/1,483 MiB baseline/peak total GPU
  allocation. Both automatic retarget stages, preview selection, and typed save
  path completed through the simplified UI orchestration.
- Final automated verification: all 24 Godot checks pass under Godot 4.7.2;
  the backend reports 24 passed and 7 device-gated skips; Ruff passes. The only
  warnings are 18 known `torch.jit` deprecations in pinned dependencies.
- GPU-rendered dock captures verified the quiet landing state and the active
  Generate and Preview & Save workspace.
- The user completed the final real-editor walkthrough after the Preview &
  Save refactor: session gating, two-take generation and switching, selected-
  take saving through Godot's file dialog, collision handling, and offline
  session/artifact recovery all passed.

### Decision gates

- If the real backend does not return one valid animation and metadata entry
  per requested sample, stop and discuss the contract instead of inventing a
  client workaround.
- If batch latency, memory use, or client-only cancellation makes the editor
  materially unresponsive, stop and decide on a versioned server job/progress/
  cancel API before shipping multi-take UI.
- If lossless migration would require silently changing old provenance or
  artifact meaning, keep the old resource read-only and discuss the migration
  boundary rather than rewriting history.

### Completion test

1. A fresh editor shows no generation controls until a new or existing session
   is active; Generate remains disabled until that session has a valid target.
2. One fixed, live `num_samples == 2` request returns two ordered, distinct
   takes in a single response. Each take has a stable ID, sample index/name,
   and content hash; both correctly share the request seed.
3. Generate, target change, artifact save, and session switch each leave an
   atomically saved session with no manual Save action or stale dirty state.
4. Take switching previews the selected variation on Jenny at the same
   playback/camera state, controls which take is saved, and does not mutate
   Jenny or existing animation. The Save action uses Godot's project file dialog
   and never silently overwrites an existing scene or companion resource.
5. After a clean restart with the backend stopped, reopening the session
   restores target, intent, provenance/take summaries, selection metadata, and
   artifact status. Saved artifacts remain usable; unsaved take payloads are
   clearly unavailable and were not silently retained as permanent history.
6. A Goal 13 draft migrates losslessly to a new session while the original file
   remains byte-identical.
7. All backend and Godot suites pass without unexpected engine errors, leaked
   nodes, partial files, or writes outside the project.

Stop condition: mark Goal 14 Complete only after the live and manual gates pass,
record evidence, commit and push the affected repositories, add a detailed Goal
15 proposal for approval, and stop before full-skeleton repair or animation
acceptance.

## Goal 15 — Full-skeleton retarget fidelity and lightweight character libraries

Status: **Proposed; awaiting approval**

### Why this goal

Goal 14 completed the session and multiple-take workflow, but two connected
correctness gaps remain before a generated take can be accepted as useful
character animation:

1. The current SOMA-77→humanoid map transfers only the body subset and
   deliberately drops all 48 SOMA finger joints. Jenny therefore keeps her
   fingers at rest even when the source motion animates them.
2. **Character take** currently packs the entire instantiated Jenny scene into
   every `.tscn`. This produces files above 15 MB because meshes, materials,
   textures, skin data, and the animation are saved together. It is a useful
   diagnostic preview but the wrong durable form for a library of motions.

The generic humanoid `.res` is not a substitute for a character-specific
library. Its tracks intentionally target paths such as
`HumanoidSkeleton:RightLowerLeg`, while Jenny's animation uses the actual path
from its `AnimationPlayer.root_node` to Jenny's `Skeleton3D`. Bone names alone
also do not make two skeletons interchangeable: Godot 4 animation values
include bone-rest orientation. The existing character baker already performs
that rest-aware conversion; it simply embeds the result in a packed scene
instead of saving the resulting `AnimationLibrary` independently.

Godot's documented model supports the intended fix: animation transform tracks
store exact node/bone `NodePath`s, `AnimationMixer.root_node` defines where
those paths resolve from, and a standalone `AnimationLibrary` can be attached
to a compatible player. Therefore Goal 15 will save the already-baked Jenny
tracks as a small target-specific `.res` whose paths resolve on Jenny, without
duplicating Jenny's model or textures.

### Outcome sought

Every deliberately supported animated SOMA-77 joint has an explicit,
documented disposition: transferred to the humanoid/character, intentionally
collapsed into another joint, or excluded for a measured reason. Finger motion
visibly and numerically survives through SOMA-77, the canonical humanoid, and
Jenny.

The default **Character animation** output is a lightweight target-specific
`AnimationLibrary` that can be attached to the canonical Jenny
`AnimationPlayer` in the editor and plays without unresolved-track warnings.
It contains animation data, not another copy of the character. Diagnostic
humanoid/SOMA preview scenes may remain available, but a packed character scene
is no longer the primary saved character artifact.

This goal validates and saves a standalone character library. Choosing an
existing production `AnimationLibrary`, naming an accepted animation inside
it, and replacing/merging with UndoRedo remain Goal 16.

### Compatibility contract

- A humanoid library is compatible with the canonical humanoid preview rig,
  not automatically with Jenny.
- A character library is baked for one recorded target skeleton signature,
  rest pose, hierarchy, and track namespace. Goal 15 proves this contract for
  Jenny and must not claim arbitrary-humanoid portability.
- Track paths are resolved from a documented `AnimationPlayer.root_node`.
  Saving and reload tests must use the same contract an artist uses in the
  editor, not a test-only path rewrite.
- Existing imported character resources, scenes, skins, materials, and prior
  animation libraries remain unmodified.
- Old Goal 12–14 packed character scenes and session artifact records remain
  readable. No migration may relabel a packed scene as a lightweight library.

### Scope

- [ ] Inventory all 77 SOMA joints, every source animation track, the canonical
  56-bone humanoid, and Jenny's 61-bone hierarchy. Record for each source joint
  its target, collapse rule, or explicit exclusion.
- [ ] Replace the body-only hardcoded map with declarative retarget-profile data
  that includes supported finger chains and keeps source/target names,
  hierarchy assumptions, root-motion ownership, and target signature explicit.
- [ ] Map the meaningful left/right thumb, index, middle, ring, and little-
  finger rotations into the canonical Godot humanoid and Jenny. Treat end/tip
  joints and any differing chain lengths deliberately rather than guessing or
  copying rotations by index.
- [ ] Preserve the corrected rest-aware model-space transfer for the body and
  extend it to fingers. Do not regress Root/Hips translation, shoulder/neck
  direction, loop state, duration, or source immutability.
- [ ] Add a full-skeleton audit fixture with non-identity rotations on every
  supported chain. At representative frames, compare source intent,
  humanoid-local results, and Jenny model-space deltas with documented numeric
  tolerances; fail on missing, duplicate, non-finite, or unresolved tracks.
- [ ] Change the default save type label from **Character take** to
  **Character animation** and save a standalone `.res` `AnimationLibrary`
  containing a deep copy of the selected character-baked animation. Do not pack
  meshes, skins, materials, textures, or the character scene into that file.
- [ ] Make the save dialog's extension and collision checks follow the selected
  artifact type. Character animation defaults to `.res`; diagnostic preview
  scenes, if retained, remain explicit rather than silently accompanying every
  character save.
- [ ] Prove the saved character library can be loaded onto a canonical Jenny
  scene/player in the Godot editor and plays every track without
  `couldn't resolve track` warnings. Verify that the generic humanoid library is
  still rejected or clearly described as incompatible rather than pretending
  it is character-ready.
- [ ] Record the target skeleton signature and artifact kind with the saved
  session artifact so later acceptance can diagnose incompatible targets.
- [ ] Add save/reload, dependency, size, path-resolution, target-signature,
  finger-transfer, whole-skeleton numeric, legacy-artifact, source-immutability,
  and node-lifecycle regression coverage.
- [ ] Measure representative output size. The character `.res` must contain no
  dependency on Jenny's mesh/texture payload and should remain in the animation-
  data scale (expected hundreds of KB, not tens of MB).
- [ ] Update README, plan, repair ledger, and artifact terminology with the
  exact compatibility boundary and editor instructions.
- [ ] Manually inspect a generated finger-rich take on SOMA-77, the canonical
  humanoid, and Jenny from several angles; then load the saved character `.res`
  into Jenny in the editor and verify body, fingers, root motion, looping, and
  track resolution.

### Out of scope

- Accepting or merging into an artist-selected existing `AnimationLibrary`,
  conflict policy, UndoRedo, and Accept/Reject state (Goal 16).
- Claiming support for arbitrary humanoid rigs or building the later Rig Wizard.
- Runtime universal retargeting between unrelated skeletons.
- A broad visual redesign of the dock.
- Server job/progress/cancellation protocol changes.

### Decision gates

- If SOMA and Godot finger chains cannot be mapped without an ambiguous
  twist/distribution policy, stop with the measured joint evidence and choose
  that policy explicitly rather than hiding the mismatch.
- If a lightweight library only works by mutating Jenny's imported scene,
  renaming its skeleton, or changing its rest pose, stop and choose a stable
  wrapper/root-node contract instead.
- If full-skeleton validation exposes a body regression beyond the current
  rest-direction model, fix the shared retarget mathematics before adding
  per-bone exceptions.
- If a second rig is required to distinguish Jenny-specific behavior from the
  first reusable profile abstraction, discuss and license that fixture before
  making a general compatibility claim.

### Completion test

1. A finger-rich SOMA-77 fixture produces non-rest, finite, directionally
   correct motion on every supported humanoid and Jenny finger chain, with all
   77 source joints accounted for by the audit.
2. Existing body/root retarget fixtures and multi-take preview behavior remain
   numerically stable and non-destructive.
3. Saving **Character animation** creates a lightweight `.res` with no embedded
   Jenny mesh, texture, material, or skin payload and no unintended companion
   character scene.
4. Loading that `.res` into the documented Jenny `AnimationPlayer` setup works
   in the editor without unresolved-track warnings and reproduces the previewed
   body, finger, root-motion, duration, and loop behavior.
5. The session records the correct selected take, character-library artifact
   kind, target signature, and existing/missing status; legacy artifacts remain
   truthful and readable.
6. All automated Godot/backend checks, rendered checks, and the manual multi-
   angle/library-load gate pass without leaks, partial files, or source changes.

Stop condition: after the user approves this proposal, implement only this
scope. When all gates pass, mark Goal 15 complete, commit and push the affected
repositories, propose detailed Goal 16 for approval, and stop before accepting
or merging animation into production libraries.

## Planned goals after Goal 15

### Goal 16 — Accept one take into native Godot animation data

Choose an existing or new character-compatible `AnimationLibrary`, explicitly
accept the selected take under an artist-chosen animation name in one undoable
editor operation, and preserve existing animation unless the user chooses
replacement. Reject/regenerate must restore the exact prior state. This goal
completes the core six-step basic workflow.

### Goal 17 — Basic-workflow hardening and release gate

Exercise at least one additional redistributable humanoid with different
proportions/hierarchy, finish setup and recovery diagnostics, measure defaults,
and resolve remaining basic-workflow repair items before advanced pose,
effector, waypoint, path, and timeline authoring begins.

## Code-review repair ledger

These are implementation findings and their current disposition.

### Priority 1 — before the affected workflow is claimed complete

1. **Resolved in Goal 13 — save-path containment and partial saves.** Draft and
   all three existing output flows now canonicalize `res://` paths, compare
   their absolute result with the project root, reject traversal and `user://`,
   and clean up earlier files when a later multi-file save stage fails.
2. **Measured in Goal 14 — cancellation remains client-side.** Cancel
   and timeout messages now say that Godot stopped waiting while the local
   backend may still be finishing inference. Actual CUDA cancellation still
   requires a server job/cancel mechanism. The measured two-take path remained
   responsive enough for the tested limit, so this is not a Goal 14 blocker.
   **Owner: Goal 17.**
3. **Resolved in Goal 14 — two-take protocol path.** Backend and Godot contract
   tests plus a live generation prove two ordered animations and metadata
   entries, distinct decoded hashes, selected-character retargeting, switching,
   and cleanup. The artist-facing maximum is deliberately two, not the
   backend-advertised 16.
4. **Finger rotations are deliberately dropped during retargeting.** The
   SOMA-77 humanoid map contains only 22 body targets and explicitly ignores 48
   finger joints; its regression test currently enforces that omission. The
   user's observation that Jenny's humanoid fingers remain in rest pose is
   therefore a confirmed implementation gap, not merely a visual suspicion.
   Audit every animated joint and add tested finger-chain transfer before any
   take is acceptance-ready. **Owner: Goal 15.**
5. **General rig compatibility is overclaimed.** Validation checks exact bone
   names, finite rests, and the existence of a non-empty skin, but not a full
   semantic `BoneMap`, hierarchy/reference-pose correctness, skin-to-skeleton
   binding, or scale policy. Character root/hips travel is transferred without
   an explicit proportional scale. Jenny is valid evidence for Jenny, not for
   arbitrary humanoids. **Owner: Goal 15 and the later Rig Wizard.**
6. **Character saves duplicate the entire target scene.** The Goal 12 baker
   packs the instantiated character, embedded animation player, meshes,
   materials, textures, and skin into each character-take `.tscn`. A Jenny take
   can therefore exceed 15 MB while an animation library is roughly 100 KB.
   Save the already rest-corrected, Jenny-path animation as a target-specific
   standalone `AnimationLibrary`; keep preview scenes diagnostic. **Owner: Goal
   15.**

### Priority 2 — structural risks to address while nearby code changes

1. **Materially addressed in Goal 14 — dock responsibilities extracted.**
   Session persistence/state transitions and transient take ownership now live
   in domain controllers; generation and combined Preview & Save UI are real
   components rather than empty containers. `ai_motion_dock.gd` still
   coordinates the cross-component editor workflow but fell from 1,643 to about
   1,036 lines. Further visual redesign can now proceed without first untangling
   local widget construction and state. **Owner: future UI overhaul.**
2. **Retarget/save logic is duplicated.** The SOMA→humanoid and
   humanoid→character bakers duplicate global-rest sampling, direction
   correction, track indexing, unique naming, and save behavior. Their baseline
   assumptions already differ. Consolidate only with regression fixtures in
   place and where the full-skeleton audit makes the shared behavior explicit.
   **Owner: Goal 15.**
3. **Backend origin normalization mutates the validated request.** That is
   currently hidden from the client, but it complicates retries, hashes, and
   server-side provenance. Preserve the original request and normalize a copy
   before introducing retained jobs or server audit records.
4. **Capability parsing is stricter than the basic workflow needs.** The Godot
   client rejects a model unless all three advanced constraint types and the
   exact contact layout are present, even though basic text generation does
   not use them. Keep strict SOMA-77 validation, but capability-gate optional
   advanced UI instead of rejecting an otherwise usable basic model.

### Priority 3 — before remote access or broader distribution

1. The backend converts arbitrary model exceptions into `internal_error` text
   containing the exception message. Keep detailed local logs, but sanitize
   client responses before any remote/LAN mode.
2. The generated glTF validator intentionally assumes a skeleton-only,
   exactly-77-node response. That is correct for the pinned server fixture but
   should be described as a contract constraint and revisited before accepting
   output from other MMCP backends.

## Current blockers and operational risks

No external blocker is active. Gated access to
`meta-llama/Meta-Llama-3-8B-Instruct` was granted and verified on 2026-09-05.

- The full text encoder peaked near 28.52 GiB of system memory on the 31.52 GiB
  reference machine. Close other memory-heavy applications before cold start.
- Windows Hugging Face caching works without symlinks but can use more disk.
- PyTorch emits known `torch.jit` deprecation warnings from pinned Kimodo code.
- The owner-created Python `.venv` cannot be launched directly by Codex's
  restricted sandbox identity. Running the same environment in the project
  owner's context passes; this is host isolation, not a broken project venv.
- The maintained `Vega-KH/kimodo` pin includes the required Windows/low-memory
  text-encoder placement repair. Reconciliation with newer NVIDIA fixes is
  still a separate decision.
- Low-step generations can collapse complex prompts toward idle motion. The
  dock default remains 100 steps; qualitative prompt/seed benchmarking belongs
  in a later quality goal.
- The Godot working tree currently contains an untracked `animations/`
  directory. Treat it as user-owned output; do not delete or rewrite it during
  implementation.

## Verification snapshot — 2026-09-25 Goal 13 implementation

- Backend: `23 passed, 7 skipped`; skips are device-specific; Ruff passed.
- Backend warnings: 18 pinned-dependency `torch.jit` deprecations; no test
  failure.
- Godot: all 15 substantive offline scripts passed under Godot 4.7.2, including
  the new draft domain and target-first offline dock-reopen tests, plus
  transport, generation, native round-trip, humanoid retarget, Jenny retarget,
  and character dock coverage.
- Two clean editor startups loaded the plugin without product errors.
- All four short playback scene smoke checks also exited cleanly: SOMA-77
  fixture, native take, humanoid retarget, and Jenny character playback.
- `scripts/test.ps1` now suppresses only Godot's exact sandboxed-Windows root
  certificate-store diagnostic and continues to fail on every other engine or
  script error. Its complete 21-check run passed.
- A GPU-backed Windows OpenGL capture verified the revised narrow dock layout.
- An auxiliary `--editor --script` run exercised the actual
  `EditorResourcePicker` branch and passed the draft lifecycle assertions. It
  is not counted as a clean suite check because Godot reports editor-owned RID
  leaks when that test harness terminates the editor process abruptly.
- No new live model generation was needed: exact provenance used the recorded
  known generation fixture, while Goals 1, 7, 8, 10, 11, and 12 retain their
  live/manual evidence.
- The user completed the final real-editor Jenny workflow: after a known
  generation and restart with the backend stopped, the draft reopened with its
  target and authoring state intact. Goal 13's manual gate passed. The user also
  reported that the accumulated dock controls are becoming confusing and
  cluttered; that finding directly shaped Goal 14's session-first shell and
  component split.

## Verification snapshot — 2026-09-25 Goal 14 implementation

- Godot: the complete 24-check suite passes under Godot 4.7.2, covering session
  migration/autosave, atomic failure behavior, chooser gating, two-take parsing,
  direct component ownership, take switching, offline reopen, source
  immutability, retargeting, saving, and all four playback smoke scenes.
- Backend: `24 passed, 7 skipped`; skips are device-specific. Ruff passes. The
  18 warnings are known `torch.jit` deprecations from pinned dependencies.
- Live: a final two-take run returned 147,763 bytes, completed inference in
  5.85 seconds (6.59 seconds wall), peaked at 13.23 GiB server working set, and
  did not increase the 1,708 MiB reported total GPU allocation. Both takes were
  distinct, retargeted, switchable, and cleaned up without ObjectDB leaks.
- Live refactor regression: 7.23 seconds reported generation / 7.41 seconds
  wall, 15.57 GiB peak server working set, and 1,411/1,483 MiB baseline/peak
  total GPU allocation. The simplified automatic-conversion and selected-take
  save path passed without leaks.
- Rendered UI checks pass. The user subsequently passed the real-editor session
  creation, two-take switching, selected-take save, collision, restart, and
  offline-reopen walkthrough. Goal 14 is complete.

## Durable design decisions

- Keep backend and extension independently versioned.
- Bind locally by default; remote access remains explicit and deferred.
- Keep MMCP compatibility and add Studio endpoints only for demonstrated
  product needs.
- Preserve SOMA-77 at the service boundary and SOMA-30 internally.
- Keep generated animations usable without the extension or backend.
- Use the rooted Jenny fixture for current visual acceptance, with its CC BY
  4.0 attribution; add other rigs before general compatibility claims.
- Evaluate a smaller or quantized text encoder only with a fixed prompt suite
  and measurements of download, RAM, VRAM, latency, and motion quality.

## Compact session log

- **2026-09-04–09-07:** Goals 0–8 established the backend baseline, full CPU
  text encoder, SOMA-77 MMCP contract, Godot playback, native save, capability
  dock, live generation, and native take saving.
- **2026-09-08:** Goal 9 added humanoid retargeting and corrected root-motion
  ownership.
- **2026-09-23:** Goal 10 integrated humanoid preview/save and navigation into
  the dock.
- **2026-09-24:** Goals 11–12 added and corrected Jenny retargeting, then added
  selectable skinned-character preview/save to the dock.
- **2026-09-25:** Documentation-only review re-centered the roadmap on the
  authoritative basic/advanced workflows, condensed completed history,
  recorded the repair ledger, and revised proposed Goal 13. No product code was
  modified.
- **2026-09-25:** Implemented Goal 13's target-first persistent `MotionDraft`,
  exact generation provenance, atomic project-owned persistence, artifact
  tracking, offline reload, centralized save containment, partial-save cleanup,
  honest cancellation text, and regression coverage. Automated and rendered
  checks pass. A follow-up audit fixed stale New/Load save-state presentation
  and exercised the real editor resource-picker branch. The user then passed
  the manual Jenny restart/offline-reload gate, closing Goal 13, and requested
  that drafts become autosaved conversation-like sessions before any authoring
  controls appear.
- **2026-09-25:** Researched `num_samples`: NVIDIA defines it as the number of
  motion variations, Kimodo generates them as one batch sharing the request
  seed, and the pinned MMCP SDK serializes one animation and metadata entry per
  sample. Confirmed that the current retarget map intentionally drops all 48
  SOMA finger joints. Added the detailed, approval-gated Goal 14 session/multiple-
  take proposal and assigned full-skeleton/finger repair to Goal 15.
- **2026-09-25:** Implemented Goal 14's session-first chooser and workspace,
  atomic autosave, lossless draft migration, focused UI/domain controllers,
  typed two-take request/response path, transient payload ownership, take
  switching on Jenny, and durable selected-take artifacts. A follow-up
  separation-of-concerns pass combined Preview & Save, removed redundant manual
  conversion actions and six path/name fields, added preview-local take
  switching, and delegated output naming/location to Godot's save dialog.
  Automated, rendered, live two-take, and final real-editor gates passed; Goal
  14 is complete.
- **2026-09-25:** Investigated oversized character takes and humanoid-library
  track failures. Confirmed that packed character scenes duplicate Jenny's
  heavy resources, while generic humanoid tracks target
  `HumanoidSkeleton:<bone>` and cannot resolve on Jenny. Proposed Goal 15 to
  combine the full-skeleton/finger audit with lightweight, target-specific
  character `AnimationLibrary` export; acceptance into an existing production
  library remains Goal 16.
