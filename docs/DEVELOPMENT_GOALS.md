# Development goals and project ledger

Last reviewed: **2026-10-01**

Current product stage: **basic workflow**

Current goal: **Goal 20 complete — Goal 21 planning, approval pending**

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
persistent-authoring vertical slice. Goals 14–17 completed the intended
session/take/save/accept spine of the basic workflow:

1. create or reopen a project-owned session before authoring controls appear;
2. select the character and autosave every meaningful session transition;
3. generate and compare several takes on that character;
4. validate full-skeleton retargeting, including fingers;
5. retain every generated take in durable session history until the artist
   explicitly deletes it;
6. explicitly accept one take into native animation data.

Before Stage 2, Goals 18–20 generalize target setup from Jenny to reviewable,
saved rig profiles across mainstream and incomplete humanoid rigs, improve
matching on diverse exports, and define explicit unsupported-topology limits;
Goal 21 then performs final basic-workflow hardening and release validation.

`MotionDraft` was the Goal 13 implementation name. The product concept is now
**session**: a persistent, conversation-like workspace containing target and
intent history, exact generation records, take references, and saved artifact
references. A **take** is one motion variation returned by a generation. A
session, generation, take, saved artifact, and accepted animation are distinct
states and must remain distinct in code and UI.

SOMA-77, the synthetic Godot humanoid, and their preview scenes remain valuable
diagnostic layers, but they must not define the artist-facing workflow. Saving
has two independent dimensions: the rig the artifact is **for** (SOMA-77,
Humanoid, or Selected Character) and the form it is saved **as** (lightweight
Animation Library or complete Preview Scene).

## Repository checkpoints

| Repository | Current reviewed checkpoint | Notes |
| --- | --- | --- |
| `kimodo-godot-server` | `d69ca22` | Goal 20 acceptance and verification on `codex/milestone-0-bootstrap`; server code unchanged |
| `godot-kimodo` | `f4d667e` | Goal 20 bounded rig matching, review preservation and common-parent feasibility on `main` |

The user authorized pushes after each completed and tested goal. Goal 20 passed
its final manual gate on 2026-10-01; this completion record accompanies the
verified extension checkpoint. Goal 21 is proposed for approval.

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
| 15 | 2026-09-26 | Completed 77-joint transfer, anatomical hand-frame correction, profile-driven character retargeting, and four compact rig/form export choices. | Godot `ad5d23b`; server `fd1b2b9` |
| 16 | 2026-09-27 | Archived every generated take with its versioned source rig, added recoverable batch persistence, chronological offline History, lazy previews, and confirmed source deletion. | Godot `6860e9b`; server `d53af66` |

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

## Goal 15 — Full-skeleton retarget fidelity and rig-aware export

Status: **Complete — automated, rendered, and manual acceptance passed 2026-09-26**

### Why this goal

Goal 14 completed the session and multiple-take workflow, but two connected
correctness gaps remained before a generated take could be accepted as useful
character animation:

1. The earlier SOMA-77→humanoid map transferred only the body subset and
   deliberately dropped all 48 SOMA finger joints. Jenny therefore kept her
   fingers at rest even when the source motion animated them.
2. **Character take** previously packed the entire instantiated Jenny scene into
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
to a compatible player. Therefore Goal 15 saves the already-baked Jenny
tracks as a small target-specific `.res` whose paths resolve on Jenny, without
duplicating Jenny's model or textures.

### Outcome sought

Every deliberately supported animated SOMA-77 joint has an explicit,
documented disposition: transferred to the humanoid/character, intentionally
collapsed into another joint, or excluded for a measured reason. Finger motion
visibly and numerically survives through SOMA-77, the canonical humanoid, and
Jenny.

The save UI remains one compact dropdown plus one Save button. Its options are
**Character animation** (default), **Humanoid animation**, **SOMA-77
animation**, and **Character Preview**. The three animation choices save
lightweight reusable `.res` libraries. Character Preview saves the complete
playable `.tscn`, intentionally including the character, meshes, materials,
textures, skin, and animation, and may be around 15 MB. That large result is
valid when explicitly requested. Existing SOMA-77/humanoid preview-scene code
may remain as internal diagnostic/test support, but it does not need another
artist-facing save option.

A Selected Character Animation Library can be attached to the canonical Jenny
`AnimationPlayer` in the editor and plays without unresolved-track warnings.
It contains animation data, not another copy of the character.

This goal validates lightweight animation libraries for all three rig layers
and the retained complete Character Preview artifact. Automatically
archiving every generated take into session history remains Goal 16. Choosing
an existing production `AnimationLibrary`, naming an accepted animation inside
it, and replacing/merging with UndoRedo remain Goal 17.

### Compatibility contract

- A humanoid library is compatible with the canonical humanoid preview rig,
  not automatically with Jenny.
- A selected-character library is baked for one recorded target skeleton signature,
  rest pose, hierarchy, and track namespace. Goal 15 proves this contract for
  Jenny and must not claim arbitrary-humanoid portability. The transfer core
  must nevertheless consume explicit rig/profile data and target paths rather
  than branch on Jenny names, so another imported character can use the same
  machinery once it has a validated profile.
- Track paths are resolved from a documented `AnimationPlayer.root_node`.
  Saving and reload tests must use the same contract an artist uses in the
  editor, not a test-only path rewrite.
- Existing imported character resources, scenes, skins, materials, and prior
  animation libraries remain unmodified.
- An explicitly saved Preview Scene is a durable user artifact and is never
  treated as disposable cache. Automatically constructed preview nodes remain
  ephemeral and are freed on take/session changes.
- Old Goal 12–14 packed character scenes and session artifact records remain
  readable. No migration may relabel a packed scene as a lightweight library.

### Scope

- [x] Inventory all 77 SOMA joints, every source animation track, the canonical
  56-bone humanoid, and Jenny's 61-bone hierarchy. Record for each source joint
  its target, collapse rule, or explicit exclusion.
- [x] Replace the body-only hardcoded map with declarative retarget-profile data
  that includes supported finger chains and keeps source/target names,
  hierarchy assumptions, root-motion ownership, and target signature explicit.
  Transfer and sampling functions operate on profile/skeleton inputs rather
  than Jenny-specific constants or branches; Jenny remains the acceptance
  fixture, not the architecture.
- [x] Map the meaningful left/right thumb, index, middle, ring, and little-
  finger rotations into the canonical Godot humanoid and Jenny. Treat end/tip
  joints and any differing chain lengths deliberately rather than guessing or
  copying rotations by index.
- [x] Preserve the corrected rest-aware model-space transfer for the body and
  extend it to fingers. Do not regress Root/Hips translation, shoulder/neck
  direction, loop state, duration, or source immutability.
- [x] Add a full-skeleton audit fixture with non-identity rotations on every
  supported chain. At representative frames, compare source intent,
  humanoid-local results, and Jenny model-space deltas with documented numeric
  tolerances; fail on missing, duplicate, non-finite, or unresolved tracks.
- [x] Keep one save dropdown and one Save button with exactly four choices:
  Character animation (default), Humanoid animation, SOMA-77 animation, and
  Character Preview.
- [x] Save each Animation Library as a standalone `.res` containing a deep copy
  of the selected rig's animation. A Selected Character library must not pack
  meshes, skins, materials, textures, or the character scene.
- [x] Retain the existing complete selected-character scene exporter as
  Character Preview. Do not silently create any preview scene for the three
  animation choices.
- [x] Make the save dialog's extension, filename suggestion, size warning, and
  collision checks follow the selected option. `.res` is used for all three
  animations; `.tscn` is used only for Character Preview. Clearly warn that
  Character Preview embeds the complete character and can be large.
- [x] Prove the saved character library can be loaded onto a canonical Jenny
  scene/player in the Godot editor and plays every track without
  `couldn't resolve track` warnings. Verify that the generic humanoid library is
  still rejected or clearly described as incompatible rather than pretending
  it is character-ready.
- [x] Record the target skeleton signature, rig layer, artifact form, and path
  with the saved session artifact so later history/acceptance can diagnose
  incompatible targets without guessing from extensions.
- [x] Add save/reload, dependency, size, path-resolution, target-signature,
  finger-transfer, whole-skeleton numeric, legacy-artifact, source-immutability,
  and node-lifecycle regression coverage.
- [x] Measure representative output size. The character `.res` must contain no
  dependency on Jenny's mesh/texture payload and should remain in the animation-
  data scale (expected hundreds of KB, not tens of MB). Record the intentionally
  large Selected Character Preview Scene separately rather than treating its
  size as a failure.
- [x] Update README, plan, repair ledger, and artifact terminology with the
  exact compatibility boundary and editor instructions.
- [x] Manually inspect a generated finger-rich take on SOMA-77, the canonical
  humanoid, and Jenny from several angles; then load the saved character `.res`
  into Jenny in the editor and verify body, fingers, root motion, looping, and
  track resolution.

### Out of scope

- Automatically retaining every generated take and presenting chronological
  session history (Goal 16).
- Accepting or merging into an artist-selected existing `AnimationLibrary`,
  conflict policy, UndoRedo, and Accept/Reject state (Goal 17).
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
3. Each of the four save choices produces only its requested artifact.
   Character animation creates a lightweight `.res` with no embedded Jenny
   mesh, texture, material, or skin; Character Preview deliberately creates the
   complete self-contained character `.tscn`.
4. Loading the selected-character `.res` into the documented Jenny
   `AnimationPlayer` setup works
   in the editor without unresolved-track warnings and reproduces the previewed
   body, finger, root-motion, duration, and loop behavior.
5. The session records the correct selected take, character-library artifact
   kind, target signature, and existing/missing status; legacy artifacts remain
   truthful and readable.
6. All automated Godot/backend checks, rendered checks, and the manual multi-
   angle/library-load gate pass without leaks, partial files, or source changes.

Stop condition passed: the user confirmed that the regenerated Jenny wrist and
finger motion matches the SOMA-77 source and described the transfer as perfect.
Goal 15 is complete. Its implementation and completion record are committed and
pushed before Goal 16 work begins.

## Goal 16 — Durable generated-take history and preview-cache lifecycle

Status: **Complete**

Completed: **2026-09-27**

### Why this goal

Goal 14 records exact generation provenance but labels unsaved take payloads as
transient. Closing Godot or switching sessions frees those motions, leaving a
record of what was generated but no animation to reopen. That was an honest
intermediate policy, but it conflicts with the intended conversation-like
session: every successfully generated take is valuable and should remain
available until the artist explicitly deletes it.

Saving every derived character preview would solve the wrong problem. Preview
scenes duplicate meshes and textures and can exceed 15 MB; humanoid and
character animations can also be regenerated as retargeting improves. The
smallest lossless source is the validated SOMA-77 animation plus the exact
source-rig rest/hierarchy data required to interpret it.

### Outcome sought

Every validated generation becomes a durable chronological entry before the UI
reports success. Each take owns a lightweight SOMA-77 `AnimationLibrary`; each
distinct source skeleton owns a deduplicated, versioned rig snapshot containing
bone names, parents, local rest transforms, skeleton transform, and its hash.
Together those resources are sufficient to reconstruct the original source
motion without the backend, response glTF, selected character, or the plugin
version that created it.

A **History** workspace lists generations by prompt and creation time, with
their takes in response order. Selecting any available take lazily reconstructs
the SOMA-77 source, retargets it through the current humanoid/character code,
and makes it the active Preview & Save take. Derived previews remain disposable;
only explicit Save actions create durable humanoid, character, or preview-scene
artifacts.

### Durability and storage contract

- The canonical archive layer is SOMA-77. Humanoid and selected-character
  outputs are derived and may improve when retargeting changes.
- Stable UUIDs, not prompts or take names, identify directories and files.
  Human-readable prompts remain metadata and UI titles.
- Session-owned data lives under
  `res://animations/kimodo/session_data/<session_id>/`. A proposed layout is:
  `rigs/<skeleton_signature>.tres` and
  `generations/<record_id>/take_<sample_index>.res`, plus a compact generation
  manifest used for verification and crash recovery.
- A take record stores archive path, decoded-motion content hash, saved-file
  hash, byte size, duration, sample index/name, SOMA contract version, source
  rig signature, and availability/deletion state. Existing request,
  capability, response, model, seed, target, and timestamp provenance remains.
- A generation is committed as a batch. Write all take libraries and the
  manifest into a same-parent staging directory, reload and validate every
  resource, then promote the complete directory and atomically save the session
  reference. Controlled failures roll back new files and leave the prior
  session byte-identical.
- Cross-file operations cannot be perfectly transactional across a process or
  power loss. The generation manifest makes the narrow promotion/save window
  recoverable: opening a session scans only its own data directory, completes or
  reports a fully verified orphan generation, and removes an incomplete staging
  directory only when its state proves it contains no committed take.
- Archived source takes are immutable. Explicit Save creates a separate user
  artifact and never moves, renames, or repurposes the archive copy.
- Derived SOMA scene instances, humanoid motions, character motions, and render
  resources are an in-memory preview cache. They are freed on take, target, or
  session changes and rebuilt on demand. No automatic `.tscn` preview is written
  to disk. An explicitly saved Character Preview remains a durable user artifact
  and is never cache-cleaned.
- Deleting an archived take always requires confirmation. It removes only the
  automatic SOMA source archive, never explicit exports or future accepted
  animations. The session retains a small tombstone and truthful descendant
  references so provenance is not rewritten.

### Session schema boundary and compatibility

- `KimodoSession` advances to schema v2. The user explicitly classified every
  pre-Goal-16 session and animation as disposable test data, so v1 sessions and
  Goal 13 drafts are rejected unchanged instead of migrated.
- No archive is invented for a legacy transient record and no separately saved
  artifact is relabeled as its generated source. Goal 16 begins durable history
  with the first generation made by a v2 session.
- If an archived file is later moved, corrupted, or deleted outside the add-on,
  the UI reports missing or hash-mismatched state without crashing,
  regenerating, or rewriting history.
- A rig snapshot is keyed by the full rest/hierarchy signature, not merely the
  name SOMA-77. Future compatible contracts may coexist without silently
  interpreting old animation against a new rest pose.

### Scope

- [x] Define the versioned source-rig snapshot and prove that snapshot plus a
  SOMA-77 `.res` library reconstructs source transforms exactly at sampled
  frames. Keep one snapshot per distinct rig signature within session storage.
- [x] Add a dedicated take-archive service responsible for deterministic paths,
  staging, deep-copy library creation, reload validation, hashing, promotion,
  rollback, orphan recovery, and explicit deletion. Keep filesystem transaction
  logic out of the dock UI.
- [x] Change generation completion order so every returned take is archived and
  verified before its generation record becomes durable or the UI reports the
  batch ready. If any take fails, preserve all returned motions in memory when
  safe, report the failure, and commit none of the batch.
- [x] Extend take summaries and session validation with durable archive metadata
  and clear `available`, `missing`, `corrupt`, and `deleted`
  states. Validate paths remain under the owning session data directory.
- [x] Enforce the v2 schema boundary, reject disposable v1/draft resources
  unchanged, and load new durable history offline.
- [x] Add a focused History workspace without broad dock redesign. Group entries
  by generation, title each group with its prompt, show timestamp/take order and
  concise availability, and keep the selected historical take synchronized with
  Preview & Save.
- [x] Lazily rehydrate a selected source take from its rig snapshot and library,
  then run the existing humanoid and selected-character bakers. Preserve play,
  pause, scrub, loop, camera, take switching, and the four Goal 15 save choices.
- [x] Rebuild only derived previews when the selected character changes. Never
  modify the archived source or require the backend for history playback.
- [x] Add confirmed per-take deletion with safe active-selection fallback,
  tombstone metadata, descendant warnings, and a guarantee that explicit saved
  artifacts are untouched. Do not add automatic age, quota, or session-close
  deletion of source takes.
- [x] Release all preview/cache nodes and resources during repeated history,
  target, and session switching. Keep explicit preview scenes outside cache
  ownership.
- [x] Update README, development plan, session details, status language, and
  recovery messages so no generated take is described as transient after a
  successful Goal 16 generation.

### Out of scope

- Accepting, merging, naming, or replacing animation inside an artist-selected
  production `AnimationLibrary`, and UndoRedo integration (Goal 17).
- Automatically converting legacy transient records into source archives when
  their original payload no longer exists.
- Persisting humanoid/character derived previews merely to make history switch
  faster, or deleting explicit user saves as cache.
- Cloud synchronization, repository-independent media storage, compression or
  quota policy, and whole-session deletion UX.
- Server job cancellation/progress changes, arbitrary-rig discovery, a Rig
  Wizard, or a broad visual redesign.

### Decision gates

- If a SOMA-77 library plus the proposed rig snapshot cannot reproduce the
  imported source exactly, stop and choose a measured lightweight self-contained
  source format rather than archiving incomplete data.
- If Godot import behavior makes directory promotion unsafe, stop and adopt an
  explicit manifest state/recovery protocol; do not describe a merely ordered
  sequence of writes as atomic.
- If failure injection finds a state that can lose a completed take or make the
  session claim a missing take, repair the archive transaction before building
  History UI.
- If History materially overloads the current dock, stop with a small wireframe
  and choose navigation with the user instead of folding more controls into the
  Preview & Save panel.
- If archive loading depends on a mutable editor fixture, test asset, or current
  target character, move that dependency into the versioned source archive
  contract before continuing.

### Completion test

1. Generate two batches of two takes. Four immutable SOMA-77 libraries and the
   required rig snapshot exist before both generation records report complete;
   paths, hashes, sizes, order, prompts, and provenance survive restart.
2. With the backend stopped and response glTF absent, reopen the session,
   select every historical take, and reproduce its SOMA-77 sampled transforms
   exactly. Humanoid and Jenny previews rebuild and remain synchronized.
3. Inject failure at every archive step, including the second take, validation,
   promotion, and session save. No session claims a partial generation, prior
   history remains byte-identical, and staged/orphan data is either safely
   rolled back or deterministically recovered.
4. Open a v1 session and a Goal 13 draft. Both are rejected unchanged; no
   archive, generation record, or migrated session is invented.
5. Corrupt or externally remove one archived take. Other history remains usable,
   and the affected entry reports its exact state without regeneration or data
   loss. Repeated switching does not leak nodes or retain stale character data.
6. Delete one archived take with explicit confirmation. Its source file is gone,
   its tombstone remains, sibling takes and explicit exports remain byte-identical,
   and reopening the session produces the same truthful history.
7. The complete Godot/backend suites and rendered History layout pass. The
   user completed the real-editor workflow and reported that all tests passed,
   everything looked good, and Jenny celebrated with a successful dance.

Stop condition passed: the user completed the manual
generate→restart→offline-History→retarget→save→delete gate on 2026-09-27. Goal
16 is complete. Its implementation and completion record are committed and
pushed before Goal 17 begins.

## Goal 17 — Accept one take into native Godot animation data

Status: **Complete — automated, rendered, and real-editor gates passed**

### Why this goal

Goal 15 can export a lightweight character animation, but export still creates
a standalone file and does not place the selected take into an artist's chosen
production library. The governing basic workflow ends with an explicit,
non-destructive **Accept** operation. Previewing, automatic archival, and Save
exports must remain distinct from acceptance.

Godot's `AnimationLibrary` stores named `Animation` resources, while editor
plugins integrate mutations with `EditorUndoRedoManager`. Goal 17 combines
those APIs behind one transaction boundary so adding or deliberately replacing
an animation is undoable from Godot's normal editor history.

### Outcome sought

From the active Preview & Save take, the artist chooses an existing project
`.res` `AnimationLibrary` or creates a new one, enters a valid animation name,
and presses **Accept**. The add-on bakes the current target-character animation
into that target's track namespace, validates it against the selected character,
and performs one editor undo action. The accepted animation is immediately
editable/playable in Godot and remains usable without the add-on, backend,
model, source glTF, archived take, or Jenny fixture.

An existing animation is never replaced implicitly. A name collision presents
an explicit Replace choice and summarizes what will change. Undo restores the
previous library and session acceptance state; redo reapplies the same accepted
animation without regenerating or retargeting it again.

### Acceptance and destination contract

- **Accept** uses only a character-compatible derived animation from an
  available archived take. SOMA-77 and generic humanoid diagnostic layers stay
  Save/export choices, not production acceptance targets.
- The destination is a project-contained `.res` `AnimationLibrary`. It may
  already exist or be created by the acceptance operation. Imported model-owned
  or otherwise non-editable library resources are rejected with guidance to
  create a project-owned library.
- The artist supplies the animation key. Normalize only characters Godot cannot
  store safely; do not silently rename a collision.
- Preflight validates the current target signature, `AnimationPlayer.root_node`
  basis, every track path, finite values, duration, and reload behavior before
  registering the undo action.
- A new animation is a deep copy of the preview result; neither the automatic
  SOMA archive nor the disposable preview is moved or mutated.
- No-collision Add and explicit Replace are separate transaction modes. Replace
  captures the previous animation so Undo restores it exactly in memory and on
  disk. Undo of a newly created destination removes the animation but retains a
  valid empty artist-owned library; undo of an Add removes only the new key.
- The do/undo helpers atomically persist the library through same-directory
  staging and update the session's acceptance record in the same editor action.
  Redo reuses the captured animation and destination identity; it never calls
  the backend or reruns retargeting.
- An acceptance record stores take/generation IDs, target signature, destination
  path, animation key, add/replace mode, prior/replacement hashes, timestamp,
  and `accepted` state. Undo restores the exact prior acceptance dictionary—
  normally absence—while Redo restores the same record identity. It is
  provenance, not ownership of the production library.
- Current Save choices remain available and unchanged. Delete source continues
  to affect only the automatic archive and cannot remove accepted animation.

### Scope

- [x] Add a focused acceptance service that owns destination validation, deep
  copying, collision policy, atomic library persistence, rollback, and semantic
  hashing. Keep filesystem and undo details out of the dock.
- [x] Inject the editor's `EditorUndoRedoManager` into the workflow and register
  exactly one named action for Add or Replace, with tested do/undo/redo helpers
  and an explicit external-resource history context.
- [x] Extend Preview & Save with a visually separate **Accept** section:
  destination library, animation name, one Accept button, and concise current
  accepted/undone state. Reuse Godot file dialogs; do not restore path text
  boxes or overload the four-choice Save control.
- [x] Support choosing an existing project-owned `.res` library and creating a
  new one. Reject directories outside `res://`, wrong resource types, imported
  read-only resources, invalid names, stale target signatures, unresolved
  tracks, and corrupt destinations before mutation.
- [x] Block collisions by default. Require an explicit Replace confirmation
  that names the destination and existing animation; capture the replaced
  animation before committing.
- [x] Validate the accepted character animation on a clean instance of the
  selected target, reload the destination from disk, and prove it matches the
  preview at sampled frames before reporting success.
- [x] Record acceptance separately from Save artifacts and automatic source
  archives. Update that record through undo/redo without rewriting generation
  provenance.
- [x] Keep preview, History selection, generation, session switching, and source
  deletion non-mutating with respect to the production library.
- [x] Add failure injection for preflight, staging, promotion, session update,
  undo, and redo. A failed operation must restore the prior library and session
  state and leave no staging/backup debris.
- [x] Update README, architecture notes, workflow plan, recovery language, and
  the repair ledger with the acceptance boundary and observed limitations.

### Out of scope

- Automatic rig discovery or a general mapping UI; that is Goal 18.
- Editing animation curves, blending clips, trimming, transitions,
  `AnimationTree` state machines, timeline placement, or advanced constraint
  authoring.
- Accepting SOMA-77 or generic humanoid tracks into a character library.
- Silently resolving name collisions, modifying imported model source files,
  attaching a library to every scene instance, or accepting several takes in
  one action.
- Changing archive retention, History deletion, backend generation, or the four
  Goal 15 Save formats.

### Decision gates

- If `EditorUndoRedoManager` cannot safely coordinate an external resource and
  session update, stop and choose a smaller explicit transaction boundary with
  the user; do not present two independent mutations as one undoable action.
- If new-file creation cannot be undone without cache/resource divergence,
  limit the first implementation to a pre-created empty library only after
  discussion; do not leave a falsely undoable file operation.
- If an existing library is embedded in an imported or scene-owned resource,
  reject it and explain how to create a project-owned `.res`; do not mutate an
  import artifact that Godot may overwrite.
- If reloaded accepted tracks do not resolve against a clean target instance,
  stop before committing and repair path/root-node ownership.
- If replace Undo cannot restore the prior animation numerically and preserve
  unrelated entries, Replace does not ship in this goal.

### Completion test

1. Generate or reopen an archived take, create a new production library, accept
   it under an artist-chosen name, reload it, attach it to a clean Jenny player,
   and match the Preview & Save animation at sampled frames.
2. Undo once: the newly created destination remains as an empty reusable
   library and the session acceptance state returns to its exact prior absence.
   Redo once: the same animation, hashes, name, target identity, and provenance
   return without backend or retarget work.
3. Accept a second take into an existing library. Undo removes only that key;
   unrelated animations remain numerically and structurally unchanged. Redo
   restores it.
4. Attempt a collision and verify the default operation changes nothing. Then
   explicitly Replace, verify the chosen take, Undo to recover the previous
   animation, and Redo to restore the replacement.
5. Inject failure at every persistence and session-update boundary. Library and
   session remain mutually truthful, prior bytes/semantic hashes are restored,
   and no temporary files remain.
6. Stop the backend, delete the accepted take's automatic source archive, and
   restart Godot. The accepted animation remains editable and playable; History
   truthfully shows the deleted source and retains its descendant provenance.
7. The complete Godot/backend suites, a rendered narrow-dock acceptance layout,
   and a manual create/add/collision/replace/undo/redo/restart walkthrough pass.

### Completion evidence

- `KimodoAcceptanceService` owns preflight, semantic hashing, staged reload,
  exact before/after bytes, compensating rollback, and session provenance. The
  dock coordinates the user gesture but contains no library persistence logic.
- Initial Add/Replace is executed and verified before its single named action is
  registered with `EditorUndoRedoManager`. This prevents a failed disk/session
  update from leaving a dead entry in Godot's Undo history. Redo reuses captured
  bytes and never invokes generation or retargeting.
- Existing/new-library selection uses Godot file dialogs. The compact rendered
  480×1000 Preview & Save tab contains no path or directory text boxes; Save and
  Accept remain visibly separate operations.
- A staged accepted library reloads without dependencies, attaches to a clean
  Jenny instance, and matches preview bone poses at start/middle/end samples.
  Add preserves an unrelated animation; Replace Undo restores its exact prior
  bytes; new-file Undo retains a valid empty library container.
- Collision, import-cache, read-only, invalid-name/type/path, stale target,
  player-root, track, finite-value, and duration checks occur before production
  mutation. Explicit Replace is the only overwrite route.
- Controlled staging, promotion, post-library, session-save, undo, and redo
  failures restore prior library/session state. Tests assert no staging or
  backup debris remains. As ADR 0005 records, this is compensating rollback
  across two files, not a claim of cross-file filesystem atomicity.
- The user completed the real-editor
  create→Add→collision→Replace→Undo→Redo→restart/source-deletion walkthrough on
  2026-09-29 and reported that all tests passed. Godot retained an empty library
  after undoing its first accepted animation; the user selected that as the
  intended behavior, leaving deletion of the artist-owned container explicit.

Stop condition passed: Goal 17 is complete. Record and push both affected
repositories, propose Goal 18 in detail, and stop before building general rig
discovery.

## Planned goals after Goal 17

### Goal 18 — Rig-profile foundation and Mixamo onboarding (complete)

#### Why split the work here

“General retargeting” combines three distinct risks: authoring and persisting a
mapping, handling incomplete/variant anatomy, and separating a complex control
rig from the deform skeleton that should receive motion. Shipping all three in
one goal would make failures hard to diagnose. Goal 18 establishes the reusable
profile and mapping workflow against a mainstream, regular Mixamo rig; Goals 19
and 20 then widen structural difficulty without redesigning that foundation.

The local-only `Models/Remy-with-taunt-animation.fbx` is a strong first target.
A read-only binary audit found 68 raw `mixamorig` names. Godot's supported FBX
import produces one 67-bone `Skeleton3D` using `mixamorig_` names, including a conventional
five-digit hand set, eyes, `Hips`, three spine levels, and a bundled `Take 001`.
The model is for internal validation only and must not be committed. Goal 18
will establish a gitignored project-local fixture location so Godot can import
private test models under `res://`; bundled target animations are ignored and
must remain unmodified.

#### Outcome sought

Selecting an unsupported character opens a focused **Rig Setup** workspace.
The add-on suggests a Godot-humanoid-to-target mapping, shows why and how
confidently each suggestion was made, lets the artist correct every row, and
saves a versioned project-owned `KimodoRigProfile`. Reopening the session reuses
the profile only when its exact target skeleton signature still matches.

The first certified non-Jenny profile is Remy/Mixamo. Once mapped, an archived
take must preview, Save, and Goal 17 Accept on Remy without changing or playing
the bundled taunt animation.

#### Mapping and profile contract

- Store schema version, target scene/skeleton signatures, skeleton node path,
  canonical semantic role → target bone map, root-motion policy, reference/rest
  measurements, ignored/optional roles, and certification results. Store no
  absolute machine path or private model data.
- Generate transparent suggestions in deterministic tiers: exact names,
  normalized names and namespace/prefix stripping (including `mixamorig:`),
  curated aliases, then side/hierarchy/chain/rest-axis evidence. Do not call a
  low-confidence suggestion “matched.”
- Present one reviewable row per canonical role with target choice, confidence,
  evidence, required/optional state, conflict indicator, and explicit unmapped
  choice. Manual selection always wins over a suggestion.
- Detect duplicate targets, wrong-side assignments, broken parent/child order,
  implausible chain geometry, degenerate hand frames, stale signatures, and
  missing required body roles before certification.
- Treat root motion separately from skeletal rotation mapping. Mixamo's `Hips`
  without a distinct deform `Root` requires an explicit, tested policy rather
  than an invented bone.
- Map only the target skeleton used for deformation. Existing target
  `AnimationPlayer` libraries and bundled clips are not profile inputs and are
  never deleted, renamed, played, or rewritten.
- Keep Jenny's exact-name profile working through the same public profile
  contract; no Mixamo branch may enter the transfer mathematics.

#### Scope

- [x] Define and validate the versioned `KimodoRigProfile` resource and atomic
  project-owned save/load service.
- [x] Add deterministic candidate generation with normalized Mixamo prefixes,
  curated aliases, side semantics, hierarchy, and geometric evidence.
- [x] Add the focused Rig Setup table, confidence/evidence display, editable
  target selection, conflict/missing diagnostics, Reset Suggestions, and Save
  Profile action without broad dock redesign.
- [x] Gate generation/preview on a certified current-signature profile and give
  a useful route back to setup when the target changes.
- [x] Route Jenny and Remy through the same profile-driven transfer API,
  including body, five-digit hands, rest-aware wrist frames, scale, and root
  travel.
- [x] Establish a documented gitignored private-fixture staging location; keep
  Remy and every other licensed test model out of commits and release packages.
- [x] Ignore and preserve the target's bundled taunt animation while adding the
  disposable Kimodo preview player.
- [x] Add deterministic mapping/profile round-trip, stale-signature,
  ambiguity/conflict, body/hand/root numeric, extra-branch, History, Save, and
  Goal 17 Accept regressions.
- [x] Render the narrow Rig Setup workspace and run a manual Remy walkthrough
  from target selection through profile reuse, offline History, Save, and
  Accept.

#### Out of scope

- Missing canonical digits or anatomy, four-finger policy, and substantially
  different hierarchy semantics (Goal 19).
- Face, IK/control-rig interpretation, twist distribution authoring, or
  advanced deform/control separation (Goal 20).
- Runtime universal retargeting, constraint baking, animation editing, or
  copying private model files into either repository.
- Broad UI overhaul and release packaging (Goal 21).

#### Decision gates

- If Remy does not import through Godot's supported FBX path without an external
  conversion step, stop and choose a reproducible local conversion/import
  contract before building profile UI around an unstable asset representation.
- If the target contains multiple plausible skeletons, require explicit
  skeleton selection; do not silently use the first `Skeleton3D`.
- If a Mixamo rest/root convention cannot preserve both grounded feet and
  intended root travel with one explicit policy, stop for a root-motion design
  decision rather than hiding offsets in per-model corrections.
- If a saved profile cannot be invalidated reliably after rig changes, do not
  auto-reuse it.

#### Completion test

1. Stage Remy locally under the ignored private-fixture directory, import it in
   Godot, and prove its bundled taunt remains intact and uninvolved.
2. Review deterministic suggestions, manually change at least one mapping,
   resolve/reset it, certify, save, reopen, and reproduce the exact mapping.
3. Change or simulate one target signature and prove the stale profile is
   rejected with a direct route back to Rig Setup.
4. Retarget a deterministic body/hand/root fixture to Jenny and Remy; quantify
   mapped chain/orientation/root agreement and confirm unmapped extras receive
   no Kimodo tracks.
5. Generate or reopen a real archived take, preview it on Remy, switch History
   takes offline, Save a character animation, and Accept it into a production
   library with Undo/Redo.
6. Restart Godot and reuse the profile/session without the backend. Jenny's
   complete existing workflow and all Goal 17 behavior remain green.
7. Complete Godot/backend suites, rendered narrow-dock setup review, and manual
   Remy acceptance pass.

Stop condition: implement only after user approval. When every gate passes,
mark Goal 18 complete, push both affected repositories, propose Goal 19 in
detail, and stop.

#### Implementation evidence — 2026-09-29

- `KimodoRigProfile` schema 1 records exact target identity, skeleton path,
  reviewed semantic mapping, root/scale policy, rest measurements, optional
  roles, and certification. `KimodoRigProfileStore` atomically saves a stable
  project-owned profile and rejects stale skeleton signatures on load.
- Deterministic candidate rows distinguish exact, normalized-prefix, curated
  Mixamo, manual, and unmatched states. Certification rejects duplicate target
  use, wrong sides, broken body hierarchy, degenerate chains/hand frames, and
  missing required anatomy. The narrow Rig Setup UI exposes Unmapped, visible
  confidence/evidence, Reset Suggestions, and Save Profile.
- Jenny continues through the same public profile API. Remy's 67-bone Godot
  import certifies without a model-specific transfer branch. Its Hips-only root
  convention emits one scaled position track and no invented Root. Numeric
  regression checks cover root/pelvis displacement, floor penetration, limb
  directions, wrist frames, and digit compensation.
- The real private Remy fixture completes target selection, artist override and
  reset, certification/save, exact-signature reuse, preview, character-library
  Save, production-library Accept, Undo, and Redo. Both bundled imported clips
  remain present, unchanged, and unplayed; preview explicitly selects Kimodo's
  separate disposable player.
- The first manual Remy pass exposed and repaired three integration gaps:
  Follow Root now tracks mapped Hips on Hips-as-root rigs; certified profiles
  reconstruct the complete editable Rig Setup after session reopen; and a saved
  Character Preview contains only Kimodo's selected motion player. Regression
  coverage proves the detached preview cleanup does not mutate Remy's imported
  clips, the live preview, or the source FBX.
- `tests/private_models/` is documented and gitignored except for its guide.
  Clean checkouts skip private-fixture checks while deterministic synthetic
  mapping/profile tests remain mandatory.
- The complete 28-check Godot 4.7.2 suite passes, including both staged Remy
  checks. A GPU-backed 480×1000 render exposed and then verified the repaired
  stacked Rig Setup rows. The unchanged backend passes `24 passed, 7 skipped`;
  Ruff passes, with the same 18 pinned-dependency deprecation warnings. Final
  manual real-editor Remy acceptance passed on 2026-09-30, including all three
  final repairs: mapped-Hips camera follow, complete reopened Rig Setup, and
  saved-preview animation cleanup. Goal 18 is complete at extension checkpoint
  `ded4aef`.

### Goal 19 — Variant anatomy and hierarchy (complete)

Make reviewed profiles support regular humanoids with fewer torso segments or
digits, different naming/rest conventions, and extra branches through a generic
semantic transfer contract. Synthetic skeleton families define acceptance;
Jenny04 and Remy are independent imported compatibility examples,
not rigs whose quirks define the algorithm or characters the product targets.
Mannequiny is an explicit bind/rest incompatibility example. The user approved
requiring matching skin bind and skeleton rest poses rather than spending this
goal on alternate saved reference poses. [ADR 0004](adr/0004-matching-bind-rest-partial-profiles.md)
records the contract.

#### Generality contract and synthetic coverage

- Transfer and certification consume reviewed semantic mappings, hierarchy,
  rest geometry, and explicit policies. No character filename, identity, or
  fixture-specific offset may select transfer mathematics.
- Separate name suggestions from transfer. Curated convention aliases may
  improve onboarding, but an equivalent manually mapped rig with arbitrary
  names must produce the same motion. Ambiguous suggestions remain reviewable.
- Build deterministic synthetic families using canonical Godot names, Mixamo
  names/prefixes, common sided `.L`/`.R` and numbered-chain conventions, plus
  opaque names requiring manual mapping. These are convention examples, not a
  claim to support every rig produced by a particular DCC or auto-rigger.
- Vary naming independently from anatomy: one/two/three torso segments,
  separate Root versus Hips-as-root, five/four/no digit chains, shortened digit
  chains, optional eyes/jaw, and extra hair/accessory/twist branches. Cover
  different rest bases, proportions, scale, and valid non-parent-first bone
  indexing. Use a focused pairwise matrix plus targeted edge cases rather than
  a costly Cartesian product.
- Prove invariance under renaming and valid reindexing, and test an unseen
  combination of conventions after the transfer rules are established. Use an
  independent expected-pose oracle rather than reproducing the transfer code.
  Anatomies with insufficient frame evidence must fail with an actionable
  diagnostic unless an explicitly reviewed frame policy has been validated.

#### Fixture evidence and boundaries

The read-only glTF audit confirms one skin, 45 skin joints, and ten bundled
animations. Mannequiny uses `pelvis`, `spine_01`, `spine_02`, `neck_01`, sided
names such as `upperarm.l`, and four three-joint digits per hand: thumb, index,
middle, and ring. It has no little-finger, eye, jaw, or third spine skin joint.
Godot's imported hierarchy and rest transforms must still be audited before
choosing the final profile; glTF skin membership alone is not that proof.

Jenny04 is now available. A read-only export audit finds one skin, 64 uniquely
named skin joints, 64 inverse-bind matrices, and no animations. `Hair`, `Eye_L`,
and `Eye_R` are weighted skin joints parented to `Head`; left/right eye weights
affect separate vertex sets. All inspected JOINTS_0/WEIGHTS_0 data has valid
joint indices, finite nonnegative weights, and no zero-total-weight vertices.
The GLB is self-contained. Small near-unit scale deviations exist in the export;
import/rest consistency and visible deformation still require Godot checks.
The user's Blender round trip must be audited, not assumed lossless.

Use Jenny04 as the real hair/eye compatibility example alongside mandatory
synthetic branches. Do not replace the existing repository Jenny fixture until
the new import, skin/rest behavior, and regressions pass and its intended
repository inclusion is confirmed. Local Jenny03 variants remain useful root
and twist examples. Stage all new models only in the ignored project-local
directory during this goal; their source files remain unchanged.

#### Intended mapping policy

- Keep pelvis, head, hands, feet, and the major arm/leg chains mandatory.
  Require a usable torso path, with at least one mapped spine/chest role;
  evaluate neck, shoulder, toes, and additional torso segments explicitly
  rather than treating every canonical role as mandatory.
- Make digit chains, eyes, and jaw optional. Distinguish an intentionally
  omitted role from a required unresolved role in the UI and certification.
  Validate the order of every mapped subset; missing anatomy must not excuse
  duplicate targets, wrong sides, stale signatures, or invalid geometry.
- Do not assign several canonical roles to one target bone. For an omitted
  intermediate source role, transfer the mapped descendant's complete motion
  relative to its actual target parent so torso motion is not silently lost.
- Hands must use one shared anatomical palm frame for wrist and all mapped
  digits. Choose explicit, recorded frame landmarks from available geometry;
  middle-forward and index-to-ring lateral is one four-finger example to test,
  not a model-specific rule. Also validate missing/shortened digit subsets and
  the diagnostic for insufficient landmarks. Never invent a
  little-finger bone or independently align thumb phalanges. If no trustworthy
  non-degenerate hand frame exists, stop and discuss the supported fallback.
- Extra target branches receive no Kimodo tracks and retain their local rest
  transforms while inheriting the mapped parent's animation. This preserves
  hierarchy; it does not add hair physics or active twist distribution.

#### Import audit and approved decision — 2026-09-30

- Staged Jenny04 and Mannequiny only in the ignored project-local area. No
  source model, existing session or animation was modified. The reproducible
  private import check is now in the passing suite, accepting Jenny04 and
  asserting Mannequiny's detailed rejection.
- Jenny04 imports as one 64-bone skeleton at `jennyrig/Skeleton3D`; Hair and
  Eye_L/Eye_R remain Head children. Across nine skinned mesh nodes / 576 bind
  entries, the maximum discrepancy between rest × skin bind and mesh-relative
  transform is 0.00001248. No material bind/rest mismatch was detected. Direct
  inspection confirms that the GLB has no animations property; the preliminary
  PowerShell audit mistakenly counted an absent property as one entry. Godot's
  lack of an AnimationPlayer therefore represents no lost source animation.
  Weighted-vertex stress checks and a GPU-rendered walking preview pass;
  multi-angle real-editor acceptance remains pending. No bind/rest export
  problem was found in Jenny04. This does not certify every artistic skin weight.
- Mannequiny imports as one 45-bone skeleton at `root/Skeleton3D` with all ten
  animations. Its skin matrices describe a different reference pose from the
  imported bone defaults: maximum rest × bind discrepancy is 3.33283734 across
  position and basis-vector distances. The raw GLB already stores the posed
  pelvis default (translation approximately -0.00276, 0.96641, 0.21429 and
  quaternion -0.25439, 0.11986, -0.06610, 0.95737); Godot preserves that default.
  This is not established to be invalid glTF or an importer failure.
- The existing transfer uses imported bone rests as its sole reference. A
  posed default with a different skin bind reference requires a deliberate
  generic policy, not a per-Mannequiny offset or silently rewritten asset.
  Implementation stopped for discussion; the user chose matching bind/rest
  poses as an asset requirement. No alternate-reference selector, per-model
  offset, or source modification was implemented. The rejection names mesh
  `body_001` and bone `pelvis`, reports position/axis differences, explains the
  requirement, and recommends a modeling-tool repair and re-export. Selection,
  baking and Accept preflight share validation; editing the map is explicitly
  not presented as a repair for this incompatibility.
- Godette's control/IK/face interpretation and the Skeleton model remain
  optional Goal 20 checks. Goal 19's synthetic matrix provides sufficient
  independent anatomy, naming, rest-axis, proportion and indexing coverage;
  no additional download or character-specific exception was necessary.

#### Ordered task list

- [x] **19.1 — Define the generic test matrix and audit imports.** Build the
  synthetic convention/anatomy matrix and independent expected-pose cases
  first. Stage Mannequiny and Jenny04; record imported skeleton paths,
  hierarchy, rest bases, units, root convention, skins, and bundled clips.
  Audit Jenny04's round-trip bind/rest consistency and hair/eye deformation.
  Notify the user of asset issues before changing or replacing any fixture.
- [x] **19.2 — Define partial-profile certification.** Separate required body
  roles, required chain structure, optional anatomy, and intentional omissions.
  Record effective torso/hand landmarks and unsupported cases in profile data.
  Version the schema if the persisted contract changes; preserve or explicitly
  recertify Goal 18 profiles without losing sessions or archived takes.
- [x] **19.3 — Extend transparent suggestions and Rig Setup.** Recognize sided
  prefix/suffix and numbered-chain conventions with visible evidence; use the
  synthetic naming families rather than an alias list designed for one model.
  Keep manual overrides authoritative. Show missing optional chains, required
  unresolved roles, and the recorded hand-frame choice clearly. Reopen/reset
  behavior must preserve the reviewed profile and remain usable in a narrow
  dock; do not infer control/deform classification here.
- [x] **19.4 — Transfer supported partial anatomy.** Handle omitted torso roles
  and mapped descendants through the existing rest-aware transfer path. Build
  a shared frame from recorded available hand landmarks and apply it through
  each mapped digit. Emit tracks only for mapped bones, preserving root travel,
  scale, thumb roll, and unmapped branches without fixture-specific math.
- [x] **19.5 — Verify root, scale, and branches.** Test synthetic partial rigs,
  Remy and Jenny04's root conventions and effective camera-follow bones. Run the
  synthetic matrix, renaming/reindexing invariance, and held-out combination.
  Verify parent inheritance and unchanged local transforms for hair/accessory
  branches, and map optional eyes through the same semantic contract. Preserve
  unmapped twist branches without claiming active twist distribution.
- [x] **19.6 — Exercise the complete session workflow.** Certify/save/reopen a
  profile for Jenny04 and retain Remy's complete regression, reload History
  offline, preview/switch takes, Save a
  lightweight character library and clean Character Preview, and Accept into
  a production library with exact Undo/Redo and restart. Preserve all ten
  Mannequiny bundled clips and all original model files. Mannequiny only enters
  the rejection path, not the supported workflow. Jenny04 has no source
  animations; add a synthetic authored clip to test preservation on that path.
- [x] **19.7 — Document and accept.** Record supported anatomy limits, profile
  compatibility rules, chosen hand landmarks, and numeric evidence. Run the
  complete extension suite, inspect the narrow UI, and perform the manual
  multi-angle imported-model gate before marking complete or pushing.

#### Numeric and workflow acceptance

1. Deterministic profile fixtures prove missing optional roles certify while
   missing required body roles, duplicates, reversed sides, invalid mapped
   chain order, degenerate frames, and stale signatures fail clearly.
   Equivalent mappings across naming families and valid reindexings produce
   identical results within numerical tolerance. An unseen naming/anatomy/rest
   combination passes without adding a fixture-specific alias or correction.
2. Synthetic motion exercises all mapped body and digit rotations, including
   non-rest omitted torso segments. Compared with an independent expected pose,
   corresponding anatomical directions/frame axes agree within 0.1 degrees,
   and scaled root/pelvis positions agree within 0.0001 target units. Unmapped
   branches retain their local rest transforms and receive zero tracks.
3. Jenny and Remy's existing numerical gates continue to pass. For imported
   Jenny04, record frame/chain/root errors across sampled poses, and inspect
   ground contact manually; anatomical/proportion differences must not be hidden by
   relaxing the synthetic transfer tests. Discuss material discrepancies.
   On Jenny04, verify bind/rest consistency, head-following hair, and separately
   mapped eyes with synthetic motion; generated Kimodo eye movement is not
   assumed. Distinguish bad skin weights from transfer errors using bone poses
   and deformed-mesh checks.
4. Profile save/reopen reproduces omissions, landmark choices, and mapping.
   Preview and saved-library reload contain no unresolved tracks or invalid
   transforms; lightweight libraries carry no character meshes/textures.
5. The imported source hash and all bundled animation names/data remain
   unchanged. Saved Character Preview contains only Kimodo's selected player.
   Accept/Undo/Redo and source-archive deletion retain Goal 17 guarantees.
6. Clean checkouts without private fixtures pass the deterministic suite and
   skip only model-dependent checks. The staged private workflow passes too.
7. Manual gate: restart Godot, reopen the profile/session offline, inspect a
   walking/body take plus a synthetic wrist/digit stress take from several
   angles, confirm root-follow and optional-role UI, Save/load on a fresh
   character instance, and Accept/Undo/Redo. Kimodo's subtle generated finger
   motion is not the sole test of digit fidelity.

#### Implementation and verification evidence — 2026-09-30

- Profile schema 2 separates required body anatomy from optional roles, requires
  at least one torso segment, validates every mapped chain subset, and stores
  explicit source/target palm-landmark pairs. Four-finger and shortened chains
  certify; insufficient/fingerless palm geometry produces a clear diagnostic.
  Existing certified schema-1 profiles upgrade in memory only for an exact
  signature and are rewritten only when Save Profile is clicked.
- Six synthetic families cover canonical, Mixamo, sided/numbered, prefixed and
  opaque names; 1/2/3 torso segments; 4/5 digits and missing-digit rejection;
  short chains; optional neck/shoulders/toes/eyes/jaw; separate Root/Hips-as-root;
  different rest axes, independently changed limb/torso proportions and scale;
  reverse bone numbering; head accessories and limb twist branches. A held-out
  combined recipe passes without production fixture-specific branches.
- Independent body/palm axis oracles pass the 0.1° bound; scaled pelvis/root
  position checks pass the 0.0001-unit bound. Renaming/reindexing invariance and
  actual baked-library playback on newly built rigs pass. Unmapped branches
  preserve local rests, inherit parent poses and receive no tracks.
- Shared compatibility validation accounts for scene transforms and every
  mesh skin binding. Detailed checks cover missing skins/bones, invalid rests,
  mismatched bind/rest matrices and unsafe reflected/sheared/non-uniform bone
  bases. Accept repeats skin checks even when the skeleton signature is unchanged.
- Jenny04's private full workflow passes reviewed sided-eye mapping,
  profile/session reopen, offline History, lightweight library playback on a
  fresh target, clean Character Preview, Accept and exact Undo/Redo. A synthetic
  authored target clip remains untouched in live/source data and is stripped
  only from the detached saved preview. Original hashes remain unchanged.
- Synthetic head/eye/wrist/all-digit motion tests imported Jenny04 without
  relying on Kimodo's weak finger generation. Optional-eye maximum angular error
  is 0.055953° (within 0.1°); hair local rest and inherited Head pose match;
  CPU weighted skin samples for Hair/Eye_L/Eye_R move and remain finite.
- All **31 Godot checks** pass with staged private fixtures. The same complete
  suite passes in a fresh temporary project without private models: only the
  explicitly model-dependent sections skip. No unexpected engine/script errors
  or orphan warnings. A GPU-rendered 480-pixel dock inspection passes optional
  roles, palm controls, full incompatibility text and Jenny04 preview. Backend
  code is unchanged; prior backend evidence remains applicable.
- Repairs addressed: stale Rig Setup rows are cleared before rejected selection;
  generation availability is recomputed on target errors; duplicate structural
  validators were consolidated behind the shared compatibility check; bone
  traversal no longer assumes parent-first indexing. The renamed-skeleton test
  now also renames its Skin bindings, rather than relying on an invalid asset.
- **Preservation incident — resolved with user confirmation:** the inherited
  `test_private_remy_workflow.gd` saved a profile at the real staged-Remy target's
  shared path and deleted it during cleanup. It was run before this defect was
  identified. `remy_2.tres`, `remy_3.tres` and `kyle's_test_session.tres` still
  referenced `remy_with_taunt_animation_867509c6_rig.tres`, which was absent.
  The session files, takes, saved animations and source models remain intact;
  original custom mapping choices were not assumed to match suggestions.
  Both the Remy workflow test and existing capture helper now save per-process
  isolated target scenes/profiles; the isolated Remy workflow passes. Work
  stopped for discussion before writing a guessed replacement. The user then
  confirmed that every Remy profile used unchanged suggestions, and permitted
  removal of unrecoverable test sessions if necessary. Recreated and certified
  the suggested schema-2 profile at the original path (54 roles, Hips-is-root,
  leg-height scaling, recorded palm pairs). All three affected sessions reopen
  with that mapping and remain byte-identical. No session or animation was
  deleted. The recovery blocker is resolved; the final manual gate subsequently
  passed on 2026-10-01.
- **2026-10-01 manual feedback:** the user passed Jenny04 plus additional
  Auto Rig Pro spine/neck variants, Godot universal and Unity-exported rigs;
  manual mapping and actionable validation messages worked. Their corrected
  Godette export exposed a harmless common bind-space scale from a parent
  empty. Added the approved shared positive-uniform-scale exception, without
  changing skins, rests or transfer math; inconsistent scales and genuine
  pose mismatches remain rejected. See [ADR 0005](adr/0005-common-uniform-bind-space-scale.md).
  The full 31-check Godot suite passes; Godette's corrected export reports
  scale 1.07826213 and normalized axis error 0.00000074. Original Godette and
  Mannequiny still reject. Source models remain byte-identical.
- **Final acceptance, 2026-10-01:** the user confirmed corrected Godette loads
  without compatibility errors and explicitly marked Goal 19 complete. Its
  flattened torso hierarchy is a separate Goal 20 scope discussion, not a
  failed bind/rest correction. All 31 automated checks passed. Existing sessions/animations and source models
  were not cleaned, migrated or replaced. Jenny04 remains private, not substituted
  for the repository's licensed Jenny03 fixture.

#### Final manual checklist

The Remy preservation checkpoint above is resolved. The editor can be restarted;
the affected existing sessions now have their original suggested mapping available.

1. Restart Godot. Open/create a Jenny04 session using
   `res://tests/private_models/Jenny04.glb`. In Rig Setup, Reset Suggestions to
   include `LeftEye → Eye_L` and `RightEye → Eye_R`, review the map and Save Profile.
   Generate/reopen a body take; inspect hair/head motion, wrists and ground
   contact from several angles. No new hair physics or foot-contact solver is
   claimed here.
2. Close/reopen the session offline. Confirm Rig Setup retains optional eye
   mappings and both palm frames; select the archived take from History. Save
   a character library, play it on a fresh Jenny04 instance, and test
   Accept/Undo/Redo in a production library.
3. Select staged Mannequiny after a valid target. Confirm the bind/rest message
   explains the affected mesh/bone and remedy, generation is disabled, and stale
   map rows are cleared. Select Jenny04 again and confirm recovery.
4. For the strong finger/eye test, open
   `res://tests/private_models/goal19_manual/jenny04_stress_2.tscn` and inspect
   `KimodoAnimationPlayer/motion` at 0.0, 0.25 and 0.5 seconds. Compare with the
   humanoid source in `goal19_manual/humanoid_stress.tscn`. All finger joints,
   wrists, eyes and head deliberately move. The matching `_2.res` library can
   also be loaded on a fresh Jenny04 instance. These local-only manual fixtures
   were generated with `test_private_jenny04_workflow.gd -- --keep-stress`;
   rerunning prints collision-safe new output paths.

#### Decision gates and exclusions

Stop for discussion if import produces multiple plausible skeletons, a usable
torso/hand frame requires invented anatomy, or the rest/root convention needs a
per-model offset or substantially different solver. Fix nearby code concerns
only when necessary for these tasks and record them in the repair ledger.

Goal 20's revised proposal below focuses on reviewable matching and a bounded
complex-hierarchy feasibility check, not general face/control/IK interpretation,
active twist distribution or multiple-skeleton selection. Goal 21 retains broad
UI overhaul, performance/release work, and server cancellation. Goal 19 changes
neither generation nor the authoritative SOMA-77 archive format; no private
fixture is committed or packaged.

Stop condition: obtain user approval before implementation. After all automated
and manual gates pass, mark complete, commit/push, propose Goal 20, and stop.

### Goal 20 — Faster, evidence-based rig setup (complete)

**Outcome:** make common exported naming variations substantially faster to map
without sacrificing manual review, hierarchy validation or certified-profile
stability. Replace the earlier broad complex-control-rig milestone with a
bounded matching improvement and one explicit structural feasibility gate.
General constraint reconstruction is not a prerequisite for Stage 1.

Approved on 2026-10-01 with the user's modifier: make rig setup good, not perfect.
Assist recognizable conventions and explain uncertainty; do not chase every
possible naming scheme, infer anonymous digits, or silently expand solver scope.

#### Evidence and scope

The corrected private Godette now passes bind/rest validation. Its actual chain
is Root_225 → Body_220, branching to Hip_218 and Spine_1_199; the spine continues
through Spine_2_198 → Ribcage_197. Spine_Control_219 is another Body child.
Hip and Body are effectively colocated. Hip and spine bones carry mesh weights;
Body, Spine_Control, Root and the GLTF-created wrapper have no direct weights.
This is not evidence of a universal Character Creator convention or a corrupt
rig. Mapping semantic Hips to Hip_218 violates the current torso ancestor
contract; mapping Hips to Body_220 is a plausible existing-profile alternative,
not yet a verified solution. No filename-specific transfer branch is justified.

Private universal Remy has root.x → spine_01.x and both thigh branches, with
c_traj above root.x. Thus root.x is a pelvis candidate, not automatically the
root-motion bone. Numeric suffixes also have different meanings: Hip_218 may
carry an exporter ID, whereas spine_01 and index2 encode anatomical sequence.
GLTF_created_0_rootJoint is a wrapper candidate, not necessarily the artist's
intended root. These cases motivate semantic evidence, not substring guessing.

#### Ordered tasks

- [x] **20.1 — Establish matching baselines.** Capture current correct,
  unmatched, ambiguous and wrong suggestions on generic synthetic conventions
  and staged Remy/Jenny variants. Create held-out suffix/prefix/chain/control
  combinations. Imported models remain optional private examples; no fixture
  filename, bone count or model-specific offset enters production matching.
- [x] **20.2 — Token-aware normalization and aliases.** Preserve exact-name
  precedence. Recognize neutral `.x` markers, namespaces, exporter wrappers,
  singular Hip/pelvis synonyms and common stretch/deform naming conventions.
  Separate exporter numeric IDs from anatomical chain/digit numbers using
  patterns and whole-rig evidence. Retain original names and normalization
  evidence; do not globally strip all digits or blindly truncate prefixes.
- [x] **20.3 — Rank candidates using structure.** Combine semantic tokens,
  side, ancestry, descendant limb/torso branches and rest geometry. Treat skin
  weighting and control/IK/pole/twist/end markers as supporting evidence, not
  definitive deform/control labels: valid root/helper bones may be unweighted.
  Specifically distinguish pelvis-like root.x from trajectory/root wrappers.
  Deterministic ties remain unresolved; prevent duplicate-role and wrong-side
  suggestions. Do not relax certification to make a guessed map pass.
- [x] **20.4 — Explain and preserve review.** Show ranked alternatives and
  concise confidence/evidence for ambiguous or weak rows in the existing Rig
  Setup surface. Keep manual choices and certified maps authoritative; rerun
  suggestions only through an explicit action, without overwriting reviewed
  rows. Preserve the profile schema unless concrete evidence requires a change.
  Explain structural failures with actual bone names/parent relationships and
  an honest remedy when remapping cannot solve them. Avoid a broad UI overhaul.
- [x] **20.5 — Bounded Godette/common-parent feasibility gate.** Use a generic
  synthetic colocated pelvis-helper/weighted-hip topology and corrected private
  Godette to evaluate mapping Hips to the common parent while leaving the hip
  helper unmapped. Check pelvis translation/rotation, leg and torso response,
  root ownership, skin deformation and saved playback against independent
  expectations. This is a read-only asset experiment using existing transfer,
  not automatic reparenting. If independent hip articulation, missing exported
  constraints or per-branch translation requires a different solver, stop and
  discuss; document the unsupported topology instead of weakening validation.
  Full Godette support is conditional, not the goal's completion requirement.
- [x] **20.6 — Regress and accept.** Prove greater correct automatic coverage
  on the declared naming suite than the recorded baseline, with zero newly
  incorrect high-confidence mappings. Test misleading names, numeric collisions,
  duplicate aliases, multiple root wrappers, twist/control decoys, wrong sides,
  renaming/reindexing invariance and a held-out combination. Demonstrate manual
  correction, profile save/reopen and unchanged archived take playback. Run all
  Godot checks, render the affected setup UI, and obtain the manual gate below.

#### Acceptance and stop conditions

1. On private universal Remy, suggestions identify the pelvis structurally,
   handle `.x` names, and reduce manual setup compared with the baseline. Root
   selection remains reviewable. Certify, preview, save a character library,
   reopen the session and play the library on a fresh target.
2. On a synthetic exporter-ID/control-decoy rig, see useful candidates and
   reasons without silently selecting a conflicting control or opposite side.
   Manually resolve a deliberate ambiguity and verify saved choices persist.
3. On Godette, either validate the common-parent mapping through preview/save
   or receive a precise topology limitation explaining why full transfer is
   deferred. Report the experimental result, not just successful certification.
4. Existing Jenny, Mixamo and Goal 19 partial-profile workflows and their
   preservation gates remain green. No user profiles, sessions, models or
   animation libraries are overwritten by diagnostics.

Explicit exclusions: rebuilding Blender constraints/IK, automatic reparenting,
new multi-branch translation solvers, facial animation synthesis, active twist
distribution, multiple-skeleton selection, and model-specific remapping hacks.
Unsupported control-driven rigs may need an exported game/deform skeleton or a
future solver; these capabilities are not required to close Stage 1. Goal 21
will document the support contract and harden the basic workflow.

Stop for discussion before expanding beyond this scope. After approval and
successful automated/manual gates, commit/push, propose Goal 21, and stop.

#### Implementation evidence and final manual gate

- Before/after synthetic correct suggestions: canonical 56→56, exporter IDs
  0→56, neutral .x 48→56, held-out combined prefix/.x/IDs 0→56; no incorrect
  suggestions in these declared families. Private universal Remy improves
  from 12 to 53 suggested roles, with c_traj as Root and root.x as Hips. The
  map certifies and passes the full isolated dock History/Save/Accept/Undo/Redo,
  exact-profile reuse, session reopening and fresh-character library playback.
  Jenny04 remains at 55 suggestions. Godette gains 17 suggestions, not a claim
  of 17 independently verified anatomical matches or complete automatic setup.
- Name interpretation lives in a separate bounded module. Keep primary numeric
  keys; add weaker exporter-ID keys only after whole-rig suffix evidence.
  Exact valid names win; close alternatives remain unresolved. Actual ancestor
  chains and zero-length rest geometry veto unsafe suggestions. Positive
  sampled skin influence is informational only (bounded scan), not evidence
  that other bones are controls. No private names enter production matching.
- Alternatives lead the existing dropdown and have per-candidate explanations.
  Suggest Unmapped fills only unreviewed empty rows from the current suggestion
  set, avoiding used targets. Manual choices, explicit omissions, root policy
  and certified palm frames survive; Reset Suggestions remains the explicit
  discard/restart action. Fixed an adjacent preservation issue where editing
  an unrelated certified row could re-derive saved palm landmarks.
- Generic colocated pelvis-helper topology passes independent body/palm/digit
  axes, translation, extra-branch inheritance and saved skin-space playback.
  Corrected private Godette also passes a bounded body-motion experiment with
  Hips=Body_220, Chest=Spine_2_198 and UpperChest=Ribcage_197. Its first spine
  joint is colocated with Body; leave the optional Spine role unmapped rather
  than weakening validation. Hip_218 keeps its local rest and inherits Body.
  Worst body/limb axis discrepancy: 0.000045 degrees. An actual hip-weighted
  vertex moves 0.184708 skeleton-space units; all 227 saved-playback bone poses
  agree with the live preview on a fresh import. Anonymous fingers remain
  unmapped; test-only palm landmarks are geometry inputs, not certified digit
  semantics. Blender constraints, independent hip controls and full Godette
  articulation remain outside this result.
- All 34 headless Godot checks pass on 4.7.2. Two 480×1100 OpenGL screenshots
  verify ordinary and ambiguous rows plus the compact action row. Adversarial
  checks cover meaningful spine numbers amid exporter IDs, exact-vs-normalized
  duplicates, tied aliases, misleading parent chains, control/IK/twist names,
  bone-index invariance, reviewed omissions and certified landmark preservation.
  Original model hashes are unchanged. Failed-run scratch output was removed;
  existing user animations, profiles and sessions were neither migrated nor
  deleted. Server code is unchanged.

Manual acceptance:

1. Start a test session with private universal Remy. If an existing certified
   profile appears, use Reset Suggestions explicitly to inspect the new matcher.
   Confirm Root=c_traj, Hips=root.x and substantially fewer empty rows. Review,
   save the profile, generate/open a take, save a character animation, reopen
   the session and play that library on a fresh target.
2. Change one mapping or intentionally unmap an optional role; click Suggest
   Unmapped and confirm your choice survives. On an ambiguous custom rig,
   review alternatives/tooltips and resolve one manually. Confirm Save Profile
   and reopen preserve the decision and palm landmarks.
3. Optionally inspect the body-only feasibility preview at
   res://tests/private_models/goal20_manual/godette_common_parent_9176.tscn,
   KimodoAnimationPlayer/motion, especially 0.0 and 0.5 seconds. Its first
   colocated spine and anonymous digits intentionally receive no tracks.
   Compare body/legs, not unimplemented facial/control/finger semantics. The
   automated feasibility gate is already passed; full Godette setup is not
   required for completion.

The user accepted the current retargeting state on 2026-10-01, closing the manual
gate and authorizing the Goal 20 push. No Goal 21 implementation before approval.

### Goal 21 — Final Stage 1 workflow polish and acceptance (proposed)

**Outcome:** close the basic-workflow stage with a manageable, safe session
lifecycle, a useful preview, truthful diagnostics and an owner-validated
clean-project installation. This is the final Stage 1 goal, not an opportunity
to expand retargeting or build Stage 2 infrastructure. Implementation requires
user approval. Work through the following ordered checkpoints within this goal;
stop for discussion if a checkpoint needs a substantially different architecture.

#### Requested changes and ownership contract

- Add session deletion from the session chooser, including old entries beyond
  the current eight-session recent limit. Allow deletion of the active session
  through the same explicit, confirmed path; return safely to the chooser.
- The warning names the session and gives the number of remaining archived
  animation drafts to be deleted, with Cancel as the safe default. Count source
  takes, not generations, rig snapshots, exported files or already deleted
  tombstones. Account for recoverable generation manifests and explain missing
  archive files rather than silently inventing a zero count.
- Delete only the selected session resource and its verified managed
  session_data/<session UUID> tree: retained SOMA-77 takes, rig snapshots,
  manifests, owned staging/recovery debris and any derived disposable cache.
  Never sweep the animations directory or follow arbitrary artifact paths.
  Explicitly saved/accepted libraries, explicitly saved Character Previews,
  imported models and shared certified rig profiles remain independent and
  must survive. The confirmation says so.
- Make Preview & Save's viewport approximately square, following available
  width instead of imposing a huge fixed size. The existing preview component
  has a 320×250 minimum; the new layout must also consider how its parent
  container stretches it. Preserve camera synchronization, take switching and
  access to playback/save controls at narrow and wider dock sizes.

Suggested warning: “Delete ‘Walking studies’ and its 12 archived animation
drafts? This removes this session and its managed source data. Saved/accepted
animation libraries, saved previews, character models and shared rig profiles
will be kept. This deletion cannot be undone.” Final wording must match the
actual recovery/undo behavior; do not claim operating-system Trash support.

#### Ordered task list

- [ ] **21.1 — Safe session deletion service.** Introduce a focused domain
  service with read-only deletion preflight/count and explicit execution, not
  filesystem logic inside the UI. Verify the exact session file, UUID and owned
  directory, reject traversal and linked/junction targets, and block duplicate
  IDs/shared ownership or unprovable archive ownership. Revalidate a stale
  confirmation before deleting. If explicit saved output was placed inside the
  managed tree, stop with an actionable conflict rather than deleting it under
  a misleading preservation promise; prevent new exports/Accept destinations
  from using reserved managed storage.
  Handle missing data and file locks honestly. Use bounded staging/rollback or
  a recoverable deletion marker so interrupted/partially failed cleanup can be
  retried without pretending cross-file atomicity. Never delete another session.
  Corrupt/unsupported resources receive an explanatory limitation; do not infer
  their ownership from a filename or migrate legacy sessions.
- [ ] **21.2 — Session chooser and lifecycle integration.** Show a browsable
  session list (not only eight recent entries) with clear titles, update times
  and selection-specific Delete. Add confirmation/cancel/result states and
  refresh the list after successful deletion. Disable destructive actions
  during generation or a Save/Accept transaction. Stop/detach active autosave,
  clear owned preview state, and return to the chooser only after a safe result.
  Old timers, deferred callbacks and acceptance Undo/Redo must not recreate a
  deleted session. Preserve ordinary production-library Undo/Redo and unrelated
  editor undo history; do not clear the editor's global stack as a shortcut.
- [ ] **21.3 — Responsive square preview and targeted UI polish.** Give the
  preview enough vertical room at approximately 1:1 aspect ratio, including
  resized/split docks. Render/check narrow and wider layouts. Keep take
  selection, transport, Save and Accept compact and accessible; reduce redundant
  status text and ensure disabled controls explain what is missing. Preserve
  existing tabs and Rig Setup rather than redesigning the entire dock.
- [ ] **21.4 — Close nearby correctness issues.** Make backend origin
  normalization operate on a copy so the validated request, retry inputs and
  retained provenance are unchanged. Separate advanced-constraint support flags
  from basic-generation eligibility while retaining strict actual SOMA-77 rig,
  response and required generation-option validation. Add focused regression
  fixtures before touching either boundary. Audit save-state errors, missing or
  changed character/profile references, corrupt/missing archives, disconnects,
  late responses and session-switch recovery; repair only concrete failures.
  Large baker consolidation and matcher/control-rig expansion are deferred.
- [ ] **21.5 — Honest operation and setup guidance.** Retain client-side
  cancellation for Stage 1; make the action/message clearly “stop waiting,”
  not a promise to stop CUDA inference. Do not add a server job queue/cancel
  protocol here. Verify one/two-take and diffusion-step bounds; retain the
  current conservative defaults unless a small reproducible live check justifies
  a change, rather than launching a broad quality/performance benchmark.
  Give actionable backend-unreachable, loading, GPU-memory, archive/disk and
  stale-rig messages where the current interface can distinguish them.
- [ ] **21.6 — Documentation and clean-project handoff.** Refresh stale
  “Milestone 0,” exact-name-only, obsolete map/count and unfinished-rig-setup
  claims. Provide one concise Windows/Godot 4.7.2 quick start covering backend
  prerequisites/start.bat, enable add-on, session → character/profile → generate
  → compare/history → Save/Accept → reopen/delete. Document matching bind/rest
  requirements, common uniform bind-space scale, optional anatomy, manual
  mapping, limited generated finger articulation and unsupported control rigs.
  Separate session-owned data from independent exports and explain backup/
  version-control responsibilities. Specify an add-on-only distribution/copy
  manifest with license notices, excluding private fixtures, user animations,
  credentials, model weights, .venv and development artifacts. Validate a clean
  Godot project against the existing verified backend; a new cross-platform
  installer or full machine re-provision is not part of this goal.
- [ ] **21.7 — Final Stage 1 acceptance.** Run the full Godot suite, backend
  pytest and Ruff (new backend tests must actually execute, not be skipped),
  rendered narrow/wide UI checks, and the clean-project/basic-workflow matrix.
  Include a live one/two-take smoke check when the user starts the backend.
  Obtain the manual gate below. Resolve remaining Stage 1 defects or explicitly
  discuss any new blocker; do not silently defer data-loss or broken workflow
  issues. Then mark Stage 1 complete, commit/push both affected repositories,
  propose the first small Stage 2 goal for approval, and stop.

#### Mandatory regression cases

- Empty, single- and multi-generation sessions; multi-take count accuracy;
  some already-deleted/missing drafts; recovered manifests; unrelated sessions.
- Cancel confirmation leaves session/data/output hashes unchanged. Deleting an
  active session does not trigger resurrection through autosave, a late response
  or an old Accept undo action. Deleting an inactive one preserves the active
  session. Save/Accept output and shared rig/profile hashes survive deletion.
- Traversal, project/root paths, links/junctions, duplicate session IDs,
  conflicting output placement, stale confirmation, locked files and injected
  failures/interruption. Partial cleanup is reported and recoverable, not hidden.
- Square preview across narrow/wide dock sizes without clipping controls,
  camera regressions or take-selection/save mismatch.
- Origin normalization leaves the input request deeply unchanged; basic
  capability fixtures do not require unused advanced constraints, while
  malformed required rig/response data still rejects.
- Full offline History/reopen, new/existing library Add/Replace/Undo/Redo,
  disconnect/error recovery, imported character and profile preservation, and
  a clean-project install with no private fixtures.

#### Manual final-stage gate

1. In a clean Godot project, install/enable only the add-on, connect to the
   supported local backend, create a session, import/map a character and generate
   one or two takes. Confirm the larger preview and direct take switching.
2. Save a character animation and optionally a preview, Accept into an existing
   library, exercise Undo/Redo, and verify exported animation on a fresh target.
3. Restart with the backend stopped; reopen the session and its History offline.
   Check one helpful missing/changed-reference case and recover without losing
   the archived sources.
4. Create more than eight disposable sessions. Select one with several drafts;
   verify the warning count and preservation text. Cancel once (nothing changes),
   then confirm deletion. Its owned data is gone, other sessions/exports/shared
   profiles still work, and it stays deleted after editor restart/Undo.
5. Delete an empty and the active disposable session. Confirm safe return to
   the chooser and disabled authoring controls until another session is opened.

The Stage 1 completion claim is the owner-validated Windows/Godot 4.7.2 basic
workflow, not universal rigs, marketplace readiness or every operating system.
Deferred: full CUDA cancellation/retained server jobs, remote/LAN deployment,
automated Python provisioning, broad inference-quality tuning, comprehensive
UI redesign, large refactors, alternate reference poses and control-rig solvers.
These exclusions must be visible in the completion record, not advertised as
implemented. No Stage 2 pose/path/constraint/timeline UI begins before approval.

## Code-review repair ledger

These are implementation findings and their current disposition.

### Priority 1 — before the affected workflow is claimed complete

0. **Goal 21 session-deletion integration hazards — not yet repaired.**
   ProjectPaths currently checks lexical containment, not linked/junction
   traversal. Session save_as can retain an existing session UUID, so shared
   ownership must not be assumed away. Export/Accept destinations currently
   allow project paths inside managed archive storage. Acceptance Undo/Redo
   unconditionally saves its retained session resource, which could recreate
   a session after the new deletion feature. Address these narrowly with
   ownership/link checks, reserved-output containment and lifecycle guards
   before claiming safe session deletion; preserve normal library undo behavior.
1. **Resolved in Goal 13 — save-path containment and partial saves.** Draft and
   all three existing output flows now canonicalize `res://` paths, compare
   their absolute result with the project root, reject traversal and `user://`,
   and clean up earlier files when a later multi-file save stage fails.
2. **Measured in Goal 14 — cancellation remains client-side.** Cancel
   and timeout messages now say that Godot stopped waiting while the local
   backend may still be finishing inference. Actual CUDA cancellation still
   requires a server job/cancel mechanism. The measured two-take path remained
   responsive enough for the tested limit, so this is not a Goal 14 blocker.
   **Owner: Goal 21.**
3. **Resolved in Goal 14 — two-take protocol path.** Backend and Godot contract
   tests plus a live generation prove two ordered animations and metadata
   entries, distinct decoded hashes, selected-character retargeting, switching,
   and cleanup. The artist-facing maximum is deliberately two, not the
   backend-advertised 16.
4. **Resolved in Goal 15 — finger rotations were dropped during retargeting.**
   The audited map now accounts for all 77 SOMA joints: 55 mapped rotations,
   nine deliberately collapsed intermediate joints, and 13 terminal joints.
   A synthetic non-rest fixture numerically exercises all 30 mapped humanoid
   finger rotations.
5. **Resolved for regular complete humanoids in Goal 18 — rig compatibility
   was overclaimed.**
   Character transfer now consumes an explicit canonical-to-target rig profile
   and a renamed-bone regression proves the mathematics is not Jenny-specific.
   Goal 18 adds reviewed exact/normalized/alias matching, hierarchy/rest
   certification, signature invalidation, scale/root policy, and persistent
   Rig Setup for Jenny and Mixamo. Goal 19 adds generic partial anatomy and
   compatible rest/skin validation. Completed Goal 20 improves evidence-based
   matching and bounds common-parent feasibility; general control-rig solvers
   are deferred rather than implied by the Stage 1 compatibility claim.
6. **Resolved in Goal 15 — character saves duplicated the target scene.** The
   default Character animation output is now a dependency-free target-specific
   `AnimationLibrary`; the large self-contained character scene remains only
   as the explicit Character Preview choice.
7. **Resolved in Goal 17 — production acceptance could not safely accumulate
   named animation.** Accept now adds to a new or existing project-owned
   `AnimationLibrary`, blocks collisions until explicit Replace, and captures
   exact before/after library bytes plus session provenance in one Godot editor
   action. Controlled persistence, Undo, and Redo failures compensate back to
   the prior state without transaction debris. Cross-file filesystem atomicity
   is not claimed; see Goal 17's recorded compensation/rollback evidence.

### Priority 2 — structural risks to address while nearby code changes

1. **Materially addressed in Goal 14 — dock responsibilities extracted.**
   Session persistence/state transitions and transient take ownership now live
   in domain controllers; generation and combined Preview & Save UI are real
   components rather than empty containers. `ai_motion_dock.gd` still
   coordinates the cross-component editor workflow but fell from 1,643 to about
   1,036 lines. Further visual redesign can now proceed without first untangling
   local widget construction and state. **Owner: future UI overhaul.**
2. **Reduced in Goal 15 — retarget/save logic is duplicated.** The SOMA→humanoid and
   humanoid→character bakers duplicate global-rest sampling, direction
   correction, track indexing, unique naming, and save behavior. Their baseline
   assumptions already differ. Consolidate only with regression fixtures in
   place and where the full-skeleton audit makes the shared behavior explicit.
   Profile-driven semantics now remove character-name assumptions, but shared
   sampling/save helpers are still a safe future cleanup. **Owner: deferred
   post-Stage-1 maintenance; do not force a broad refactor into final hardening.**
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

Goal 19's local Remy rig-profile preservation issue is resolved with user
confirmation and verified recovery. Goal 20 passed manual acceptance; Goal 21
is proposed and has not started.
No external service blocker is active. Gated access to
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

## Verification snapshot — 2026-09-26 Goal 16 implementation

- A versioned SOMA-77 rig snapshot plus each archived `.res` animation library
  reconstructs all 77 bone names, hierarchy/rest transforms, animation tracks,
  and sampled values exactly. Two takes share one deduplicated rig snapshot;
  their libraries have no external resource dependencies.
- Failure injection after rig persistence, either take, manifest staging, and
  session save leaves the prior session byte-identical and no partial final
  generation. A simulated interruption after directory promotion is recovered
  from its verified manifest on the next session open.
- External file corruption is reported and a restored file becomes available
  again. An interrupted delete is repaired on open; a confirmed delete removes
  only its source archive, retains a tombstone, and leaves its sibling and
  explicit exports intact.
- The complete 25-check Godot suite passes under Godot 4.7.2. A GPU-backed
  480×1000 Windows OpenGL capture verifies the narrow three-tab dock and grouped
  History layout.
- The unchanged backend passes `24 passed, 7 skipped`; Ruff passes. Its 18
  warnings remain known pinned-dependency `torch.jit` deprecations.
- The user completed the real-editor
  generate→restart→offline-History→retarget→save→delete acceptance on
  2026-09-27 and reported that all tests passed and everything looked good.

## Verification snapshot — 2026-09-28 Goal 17 implementation

- The complete 26-check Godot suite passes under Godot 4.7.2, including editor
  startup/restart, focused acceptance transactions, full dock Undo/Redo,
  archive deletion independence, all retarget/save regressions, and four
  playback smoke scenes.
- New/existing Add, collision, explicit Replace, exact library-byte Undo/Redo,
  stable acceptance identity, clean Jenny sampled playback, dependency
  independence, offline restart, and post-acceptance source deletion pass.
- Injected staging, promotion, post-library, session-save, Undo, and Redo
  failures restore prior production/session state and leave no temporary files.
- A GPU-backed 480×1000 Windows OpenGL capture verifies the distinct compact
  Save and Accept controls in Preview & Save.
- The unchanged backend passes `24 passed, 7 skipped`; Ruff passes. Its 18
  warnings remain known pinned-dependency `torch.jit` deprecations.
- The user passed the real-editor create/add/collision/replace/undo/redo/restart
  walkthrough on 2026-09-29. The observed empty-library result after first-add
  Undo was accepted and made the explicit, tested contract.

## Verification snapshot — 2026-09-26 Goal 15 implementation

- The SOMA-77 audit accounts for all 77 joints: 55 mapped rotations, nine
  collapsed intermediates, and 13 terminal joints. The canonical humanoid
  output contains 55 rotation tracks plus Root/Hips positions; Jenny honestly
  contains 52 supported rotations because its fixture omits eye and jaw bones.
- A deterministic finger-rich regression inserts non-rest motion into all 30
  mapped finger joints and verifies model-space transfer numerically. Existing
  body, root-motion, multi-take, ownership, reload, and smoke tests remain green.
- A read-only acceptance pass over the user's original untracked
  `closed_fists.tscn` confirmed 30 non-rest source finger rotations, 30 in the
  converted humanoid animation, and 30 in the Jenny animation. This directly
  reproduces and repairs the motion that originally exposed the omission.
- A later `fistpump` manual comparison exposed compounded wrist dorsiflexion:
  the old transfer preserved world-space hand rotation but not the anatomical
  hand frame. Goal 15 now constructs each hand frame from wrist-to-middle
  forward and index-to-little lateral axes, validates degeneracy, and transfers
  both flexion and palm roll. On the real saved fixture, worst directional error
  fell from about 59° to 1.8°, while humanoid and Jenny agree within 0.0001°.
- Applying that correction only at the wrist exposed a thumb-roll regression:
  independently aligning each phalanx constrained its direction but left its
  roll ambiguous, producing roughly 84–86° distal compensation on Jenny. All
  30 mapped digit joints now share their hand's complete anatomical frame. A
  31-sample pass over the saved `Soma77_Fistpump2_animation.res` measured a
  worst local thumb-bend difference of 0.009° through both conversion stages;
  focused digit-compensation guards and the complete suite pass.
- A synthetic 62-bone Jenny fixture confirms an unmapped ponytail branch is
  accepted, receives no authored track, and inherits animated Head motion.
- `KimodoHumanoidRigProfile` separates canonical semantics from target bone
  names. A renamed-bone fixture proves character retargeting consumes the
  profile instead of branching on Jenny.
- The dock exposes exactly one dropdown and one Save button with Character
  animation, Humanoid animation, SOMA-77 animation, and Character Preview.
  The first three produce only `.res`; the last produces only `.tscn`.
- A saved character library reloads without external dependencies, attaches to
  a fresh Jenny instance, reproduces the preview animation, and is more than
  ten times smaller than the self-contained preview scene in the automated
  fixture.
- The complete Godot suite passed on Godot 4.7.2. A GPU-backed Windows OpenGL
  render at 480×1000 verified the compact Preview & Save layout. The user then
  regenerated the corrected motion and confirmed that Jenny's wrist and finger
  bends match the SOMA-77 source, describing the transfer as perfect. Goal 15's
  manual gate passed.

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
  library remains Goal 17.
- **2026-09-26:** Clarified Goal 15's export model as one compact dropdown:
  Character/Humanoid/SOMA-77 animation libraries plus an explicit complete
  Character Preview. Retained the working character preview-scene path,
  required profile-driven transfer code reusable beyond Jenny, and added
  proposed Goal 16 for durable chronological session take history. The user
  approved Goal 15 with this final save-control simplification.
  Goal 16 will archive authoritative SOMA-77 libraries and regenerate bulky
  previews on demand; explicit preview-scene saves remain durable artifacts.
- **2026-09-26:** Implemented Goal 15's full 77-joint audit, 30 mapped finger
  rotations, profile-driven character transfer, three lightweight rig-specific
  AnimationLibrary exports, retained explicit Character Preview export, compact
  save control, and richer session artifact metadata. Automated and rendered
  gates pass; manual editor acceptance is pending before completion/push.
- **2026-09-26:** Diagnosed the user's `fistpump` screenshots as a real
  anatomical wrist-frame error rather than weight painting. Replaced the
  underconstrained hand transfer with a validated two-axis palm frame, added
  full-frame and extra-bone regressions, and reduced the measured visual-axis
  error from roughly 59° to 1.8°. The complete suite and GPU render pass;
  corrected manual acceptance remains pending.
- **2026-09-26:** Reproduced the follow-up backward-thumb regression and found
  that the digit bones still used independent one-vector alignments after the
  wrist adopted the full palm frame. Assigned the shared palm frame to every
  mapped finger and thumb joint, added bounded local-compensation regressions,
  and measured only 0.009° worst thumb-bend drift across 31 samples of the real
  `Fistpump2` fixture. The complete Godot suite passes. The user confirmed the
  regenerated Jenny preview matches SOMA-77 at the wrists and fingers, closing
  Goal 15. Goal 16 is now proposed for approval with durable SOMA source
  archives, versioned rig snapshots, recoverable batch persistence, offline
  History, explicit deletion, and disposable derived previews.
- **2026-09-26:** Implemented approved Goal 16 with session schema v2,
  automatically archived SOMA-77 takes, versioned/deduplicated rest-rig
  snapshots, recoverable generation manifests, offline chronological History,
  lazy retargeting, explicit source deletion, and disposable derived previews.
  At the user's direction, disposable pre-Goal-16 sessions are rejected rather
  than migrated. Automated and rendered gates pass; manual acceptance remains.
- **2026-09-27:** The user passed Goal 16's full real-editor acceptance and
  reported successful durable History playback, retargeting, saving, deletion,
  and restart behavior. Closed Goal 16 and proposed Goal 17 for an undoable
  Accept operation into a project-owned production `AnimationLibrary`. Added a
  dedicated pre-Stage-2 Goal 18 for reviewable general rig profiles validated
  on Jenny, Mixamo, and a structurally different redistributable humanoid;
  moved final hardening and release readiness to Goal 19.
- **2026-09-28:** Implemented Goal 17's explicit production-library acceptance:
  compact new/existing destination controls, artist naming, collision-safe Add
  and confirmed Replace, exact Undo/Redo, clean-target staged reload, durable
  acceptance provenance, source-deletion independence, and injected rollback
  coverage. The complete Godot suite and GPU-rendered narrow dock pass. Manual
  real-editor acceptance remains before completion and push.
- **2026-09-29:** The user passed Goal 17's complete real-editor walkthrough and
  approved push. Made the observed first-add Undo behavior intentional: remove
  the animation and provenance while retaining an empty reusable library.
  Audited the private local test models and split general retargeting into
  Goal 18 (profile/mapping foundation plus Mixamo Remy), Goal 19 (variant or
  missing anatomy with Mannequiny and hair-bone Jenny), and Goal 20 (Godette's
  complex face/control/IK rig); moved Stage 1 hardening to Goal 21.
- **2026-09-30:** Closed Goal 18 after the user passed the final mapped-Hips
  camera, reopened Rig Setup, and clean saved-preview tests. All 28 Godot checks
  and the rendered certified-profile UI passed; backend code is unchanged and
  its previously recorded checks passed. Extension checkpoint `ded4aef`.
  Prepared Goal 19's seven ordered tasks for optional anatomy, omitted torso
  roles, four-finger shared hand frames, profile compatibility, extra-branch
  preservation, and full offline Save/Accept acceptance. Confirmed Jenny03 has
  twist branches but no hair joints, so synthetic hair coverage is mandatory
  and an updated private Jenny is optional. Goal 19 awaits approval.
- **2026-09-30:** Revised the Goal 19 proposal at the user's direction to make
  generic synthetic convention/anatomy families the acceptance contract and
  imported models compatibility examples. Added naming/reindexing invariance,
  a held-out combination, and the newly supplied Jenny04 hair/eye audit.
  Preliminary GLB structure/weight checks pass; imported bind/rest and visual
  deformation remain implementation-time checks. No Goal 19 code work begun.
- **2026-09-30:** Implemented approved Goal 19 using generic partial schema-2
  profiles, paired hand landmarks, hierarchy-order-independent transfer and
  shared actionable asset compatibility checks. The user chose matching
  bind/rest poses instead of alternate references; Mannequiny is a rejection
  fixture. All 31 Godot checks pass with private fixtures and in a temporary
  project without them; numerical and rendered Jenny04 checks pass. Found and
  repaired an inherited test/capture cleanup defect that targeted the shared
  Remy profile. The profile is absent after earlier test runs, while sessions,
  archives, saved animations and models remain intact. Stopped for user review
  of mapping recovery/recertification; no guessed replacement, completion or push.
- **2026-09-30:** The user confirmed unchanged suggested Remy mappings. Recreated
  the certified profile at its original shared path and verified all three
  affected sessions reopen with that map without changing their file bytes.
  No sessions or animations needed removal. The preservation discussion is
  resolved; Goal 19 awaits its real-editor manual acceptance before completion
  and push.
- **2026-10-01:** The user accepted Goal 19 and confirmed corrected Godette
  loads without compatibility errors. Pushed extension `4719722` and completion
  documentation `886201e`. Audited Godette's sibling pelvis/torso branches and
  universal Remy's misleading pelvis name `root.x`. Proposed a narrower Goal
  20 for evidence-based matching, explicit ambiguity review and a bounded
  common-parent feasibility check, leaving new control-rig solvers deferred.
  No Goal 20 implementation has begun.
- **2026-10-01:** Implemented approved Goal 20 with the good-not-perfect scope
  modifier. Bounded token/alias evidence, ranked alternatives and structural
  vetoes improve universal Remy from 12 to 53 suggestions. Preserved manual
  omissions and saved palm choices. Generic/common-parent and private Godette
  body experiments pass without a new solver or rest/bind edits; anonymous
  finger/control semantics are not inferred. All 34 Godot checks and rendered
  UI checks pass. Manual acceptance is pending; no checkpoint push yet.
- **2026-10-01:** The user accepted Goal 20's retargeting state and authorized
  push. Closed the goal with 34 passing automated checks and rendered evidence;
  extension checkpoint `f4d667e`. Goal 21 will be the final Stage 1 goal,
  explicitly including confirmed session-owned-data deletion and a taller
  square preview. Preparation is documentation-only until approval.
- **2026-10-01:** Prepared the detailed final Stage 1 Goal 21 proposal after
  pushing Goal 20 (extension `f4d667e`, documentation `d69ca22`). Added the
  requested counted/confirmed session deletion and responsive square preview,
  bounded correctness repairs, truthful cancellation/setup guidance and a
  clean-project/manual release gate. Read-only audit identified deletion
  hazards in linked paths, shared IDs, outputs inside managed storage and old
  acceptance callbacks re-saving session resources; tests for these are explicit
  tasks, not implemented fixes. No Goal 21 product code has changed.
