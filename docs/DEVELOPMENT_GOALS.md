# Development goals and project ledger

Last reviewed: **2026-09-25**

Current product stage: **basic workflow**

Current goal: **Goal 14 — Proposed; awaiting user approval**

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
| `kimodo-godot-server` | `bb5b57f` | Goal 13 completion and Goal 14 proposal on `codex/milestone-0-bootstrap` |
| `godot-kimodo` | `3e415b2` | Goal 13 implementation on `main` |

The Godot and server checkpoints are local until explicit push authorization
is received for each source/document payload and remote.

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

Status: **Proposed; awaiting user approval**

Do not implement this goal until the user approves it.

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
character, generates a tested number of takes in one request, switches between
those takes on the selected character, and closes/reopens Godot with the
backend stopped without losing session state or generated take data.

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
- **Session-managed source:** the exact validated MMCP response saved under the
  session directory so takes remain previewable offline. This is not an
  accepted animation.
- **Saved artifact:** an explicit native/humanoid/character export linked to a
  take. It is not accepted merely because it exists.
- **Accepted animation:** remains absent until the later acceptance goal.

### Scope

- [ ] Introduce a versioned `KimodoSession` model and session store. Rename the
  product/UI terminology from draft to session; do not merely relabel widgets
  while keeping draft-shaped ownership.
- [ ] Add a lossless schema migration from Goal 13 `MotionDraft` resources.
  Preserve IDs, target signatures, editable intent, exact generation records,
  and artifact links. Loading an old draft must never overwrite it in place.
- [ ] Start in a session landing state that exposes only New Session, Open
  Session, and a small recent-session list. Backend, prompt, generation,
  preview, retarget, and export controls remain unconstructed or hidden until
  a session is active.
- [ ] Require a validated project-owned character before Generate is enabled.
  Keep diagnostic SOMA/humanoid layers available inside the session but
  secondary to the selected-character workflow.
- [ ] Break the 1,400-line dock into focused session shell, generation/take,
  preview, and output components with one explicit session controller. Avoid a
  visual-only rearrangement that leaves state transitions in the widget class.
- [ ] Replace manual draft Save/Save As with atomic autosave and a visible
  `Saving…` / `Saved` / actionable-error indicator. Mark state dirty on edits,
  debounce ordinary field changes, and force a save at session creation,
  validated target change, immediately before Generate, after a validated
  response is durably stored, after artifact save, before session switch, and
  on editor shutdown.
- [ ] Never update the session manifest before its referenced response or
  artifact exists. Use temporary files plus atomic rename/rollback so a crash
  cannot leave a manifest pointing at partial data.
- [ ] Persist each exact validated MMCP response in a project-contained session
  directory and record its SHA-256. Create one take record per response
  animation with sample index/name and a deterministic decoded-motion hash.
- [ ] Add backend contract tests for `num_samples == 2` proving Kimodo-style
  `(B,T,J,...)` arrays survive `MotionResult` validation and serialize as two
  ordered glTF animations plus two matching metadata entries.
- [ ] Run one short fixed-request live loopback generation with
  `num_samples == 2`. Verify both takes are structurally valid and distinct,
  record latency/RAM/VRAM relative to one sample, and reduce the exposed limit
  to tested behavior rather than trusting `max_num_samples: 16`.
- [ ] Extend the Godot response layer to parse all response animations and
  correlate them one-to-one with `MMCP_motion.samples[]`. Reject duplicate
  names, count/order mismatches, invalid tracks, or cross-sample metadata.
- [ ] Let the artist request the tested take count and switch quickly between
  takes on the selected character while preserving playback time, loop state,
  camera, and root-follow state. Use the term **take**, not candidate or sample,
  in artist-facing UI.
- [ ] Keep every take non-destructive. Switching, regenerating, changing the
  target, closing the editor, and reopening offline must not alter the source
  character or existing project animation.
- [ ] Autosave the old target state before changing character. Retain prior
  generations/takes with their target snapshot and rebuild previews lazily for
  the new current target.
- [ ] Add migration, session-gating, autosave/coalescing, atomic-failure,
  response/take round-trip, multi-animation parsing, offline reopen, target
  switch, preview synchronization, source-immutability, and node-lifecycle
  tests.
- [ ] Update the plan, README, and repair ledger, including measured
  multi-take behavior and the exact tested maximum exposed by the UI.
- [ ] Manually verify the complete session-first workflow with Jenny: launch to
  the session chooser, create a session, choose Jenny, generate multiple takes,
  switch takes, restart with the backend stopped, reopen the session, and
  preview the same takes without mutation or regeneration.

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
   playback/camera state and does not mutate Jenny or existing animation.
5. After a clean restart with the backend stopped, reopening the session
   restores target, intent, provenance, take list, selected take, and artifact
   status; the persisted takes remain previewable without regeneration.
6. A Goal 13 draft migrates losslessly to a new session while the original file
   remains byte-identical.
7. All backend and Godot suites pass without unexpected engine errors, leaked
   nodes, partial files, or writes outside the project.

Stop condition: mark Goal 14 Complete only after the live and manual gates pass,
record evidence, commit and push the affected repositories, add a detailed Goal
15 proposal for approval, and stop before full-skeleton repair or animation
acceptance.

## Planned goals after Goal 14

### Goal 15 — Full-skeleton retarget fidelity

Audit every animated SOMA-77 joint against the humanoid and character outputs,
implement a tested finger-chain mapping, quantify rotation transfer across the
whole mapped skeleton, and replace exact-name assumptions with the first
explicit rig-profile data where necessary. This must pass before generated
takes are treated as acceptance-ready.

### Goal 16 — Accept one take as native Godot animation

Choose an animation destination, explicitly accept the selected take in one
undoable editor operation, and preserve existing animation unless the user
chooses replacement. Reject/regenerate must restore the exact prior state.
This goal completes the core six-step basic workflow.

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
2. **Partially resolved in Goal 13 — cancellation remains client-side.** Cancel
   and timeout messages now say that Godot stopped waiting while the local
   backend may still be finishing inference. Actual CUDA cancellation still
   requires a server job/cancel mechanism. **Owner: Goal 14 if measured
   multi-take latency makes it material; otherwise Goal 17.**
3. **The multi-take protocol path is documented but not verified end to end.**
   Kimodo and the pinned MMCP SDK represent `num_samples` as a batch and the SDK
   serializes one animation/metadata entry per sample. The extension still
   hardcodes one sample and requires exactly one animation, and no repository
   or live test yet proves the two-take path. Do not expose the advertised
   maximum of 16 until the complete path is tested and measured. **Owner: Goal
   14.**
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

### Priority 2 — structural risks to address while nearby code changes

1. **Partially addressed in Goal 13 — `ai_motion_dock.gd` remains large.** The
   new resource model, draft store, canonical hashing, atomic persistence, and
   path validation live in domain services rather than the dock. The dock still
   owns substantial widget construction and workflow orchestration and is now
   roughly 1,400 lines. Goal 14 must split session, generation/take, preview,
   and output responsibilities while introducing the session controller; avoid
   an unrelated rewrite beyond those boundaries. **Owner: Goal 14.**
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
