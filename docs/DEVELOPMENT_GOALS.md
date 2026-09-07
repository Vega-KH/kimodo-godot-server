# Development goals and session log

Last updated: 2026-09-07

This is the authoritative living record for near-term development. It keeps
completed work visible while limiting planning to the active goal and the next
one or two goals.

## How we use this document

- Exactly one goal is **Active**, unless it is **Blocked** while awaiting the
  user or an external system.
- Goals should fit a focused session of roughly 20–60 minutes of active work.
- Every goal ends with an explicit test or manual acceptance check.
- A goal is **Complete** only after its completion test passes and evidence is
  recorded here.
- Completed goals and tasks are never deleted. Corrections are appended as
  notes so the project history remains understandable.
- When a goal becomes complete, update this document, commit the checkpoint,
  report and celebrate the result, and end the turn. When no major blocker
  makes planning premature, also lay out the next goal for review. Do not
  start that proposed goal until the user explicitly approves it.

Checkboxes mean:

- `[x]` complete
- `[ ]` pending
- `[!]` blocked

## Goal 0 — Bootstrap the backend and Windows CUDA environment

Status: **Complete**
Completed: 2026-09-04

Outcome: a history-preserving, independently versioned backend fork and a
reproducible Windows CUDA development environment are running on the reference
machine.

- [x] Clone Animatica `motionmcp-kimodo` with its Git history intact.
- [x] Create the public GitHub fork at
  `https://github.com/Vega-KH/kimodo-godot-server`.
- [x] Keep Animatica as `upstream` and the Vega-KH fork as `origin`.
- [x] Rename the distribution and preferred CLI to `kimodo-godot-server` while
  preserving the legacy import namespace and executable alias.
- [x] Change the default bind address from all interfaces to `127.0.0.1`.
- [x] Create the Python 3.10.16 virtual environment and install `uv`.
- [x] Verify Visual Studio 2022 MSVC, CMake, and MotionCorrection.
- [x] Lock MMCP SDK, the candidate Kimodo fork, and PyTorch 2.12.1+cu130.
- [x] Verify PyTorch CUDA access to the RTX 4070 Laptop GPU.
- [x] Authenticate GitHub CLI as `Vega-KH` and Hugging Face CLI as `VegaKH`.
- [x] Download and load NVIDIA Kimodo-SOMA-RP-v1.1.
- [x] Confirm the model uses SOMA-30 input and SOMA-77 output skeletons.
- [x] Run two short dummy-encoder generations with identical inputs and seed;
  all output arrays matched exactly.
- [x] Start the live MMCP server on loopback and receive HTTP 200 from
  `/capabilities`.

Completion test and evidence:

- `pytest`: 10 passed, 7 hardware-specific tests skipped.
- `ruff check .`: passed.
- `torch.cuda.is_available()`: true; CUDA build 13.0.
- MotionCorrection import: passed.
- Five-step, 30-frame dummy generation: about 9.4 seconds including process
  startup and cached model load.
- Generated arrays included 77-joint local/global rotations, posed joints,
  root motion, and six foot-contact channels.
- Git checkpoints: `c90cf82` and `688ea8b` on
  `codex/milestone-0-bootstrap`.

## Goal 1 — Run MMCP with the full CPU-offloaded text encoder

Status: **Complete**
Completed: 2026-09-05

Outcome sought: a text prompt travels through the live MMCP service and returns
a structurally valid motion while the text encoder remains on CPU and the
motion model remains within the 8 GB GPU budget.

- [x] Install and authenticate the Hugging Face CLI as `VegaKH`.
- [x] Verify access to `nvidia/Kimodo-SOMA-RP-v1.1`.
- [x] Identify the two McGill LLM2Vec adapter repositories.
- [x] Confirm from adapter metadata that the required base is exactly
  `meta-llama/Meta-Llama-3-8B-Instruct`.
- [x] Obtain gated access to `meta-llama/Meta-Llama-3-8B-Instruct` for the
  `VegaKH` account.
- [x] Confirm access with an authenticated Hugging Face metadata request.
- [x] Record the expected download size and available disk space.
- [x] Restore and test explicit CPU device placement in the maintained
  `Vega-KH/kimodo` fork after the inherited quantization patch regressed it.
- [x] Load with `TEXT_ENCODER_MODE=local` and `TEXT_ENCODER_DEVICE=cpu`.
- [x] Run one short, fixed-seed text-conditioned generation.
- [x] Start `kimodo-godot-server` on loopback with the full encoder.
- [x] Submit the same prompt through MMCP and validate the returned animation.
- [x] Record cold/warm load time, generation latency, peak VRAM, peak system
  RAM, model identifiers, and warnings.
- [x] Update ADR 0002 with the result; keep it Proposed because its remaining
  constraint-generation gate is still open.

Completion test:

1. The service becomes ready at `127.0.0.1` without OOM.
2. `/capabilities` returns HTTP 200.
3. A fixed text prompt produces a valid MMCP animation response.
4. The result contains finite rotations/root translations at the advertised
   30 fps and can be decoded without schema or glTF errors.
5. Recorded peak VRAM stays within the reference 8 GB GPU.

Stop condition: mark Goal 1 Complete, commit the measurements, report the
result, and end the turn without starting Goal 2.

Completion test and evidence:

- Full-encoder environment: `TEXT_ENCODER_MODE=local`,
  `TEXT_ENCODER_DEVICE=cpu`, and no quantization.
- Exact model revisions: Meta Llama 3 `8afb486c1db24fe5011ec46dfbe5b5dccdb575c2`,
  McGill MNTP adapter `31474e395ada192e8ed1586db6be79fb3b70c9c0`, and
  McGill supervised adapter `baa8ebf04a1c2500e61288e7dad65e8ae42601a7`.
- Hugging Face repository metadata totals 32.13 GB across all formats. The
  files selected by Transformers occupy 14.958 GiB for the base, 0.165 GiB
  for the MNTP adapter, and 0.156 GiB for the supervised adapter locally.
- Download-inclusive cold setup: 3,218.4 seconds. Cached setup: 24.1 seconds.
- Five-step, 30-frame generation: 6.10 seconds direct and 7.09 seconds over
  live loopback HTTP, using seed 1234.
- `/capabilities`: HTTP 200. `/generate`: HTTP 200 with
  `model/gltf+json`.
- Both responses decoded as one 30-joint, 30-frame animation at 30 fps;
  all 3,720 accessor floats were finite. The direct and HTTP glTF documents
  matched exactly by SHA-256.
- Peak process RSS: 16.01 GiB. Peak system memory used across the cold and
  cached runs: 28.52 GiB of 31.52 GiB.
- Peak CUDA memory: 1.12 GiB allocated and 1.29 GiB reserved on the 8 GB
  RTX 4070 Laptop GPU.
- Kimodo dependency patch: `Vega-KH/kimodo` commit
  `3362b92c37faa100fb697972f0fc5485dd94dd4f`; focused tests: 2 passed.
- Backend tests: 11 passed, 7 hardware-specific tests skipped. Ruff passed.

## Goal 2 — Freeze the current upstream MMCP contract

Status: **Complete**
Completed: 2026-09-06

Outcome sought: recorded, sanitized fixtures and automated parsers describe
the inherited server before its SOMA output behavior changes.

- [x] Create `tests/contract/fixtures/` and fixture-recording guidance.
- [x] Define fixture metadata containing dependency commits and schema version.
- [x] Record `/capabilities` for the pinned SOMA-RP model.
- [x] Record one valid fixed-seed generation response.
- [x] Record representative validation/error responses.
- [x] Add tests that load and validate every fixture without model weights.
- [x] Document fields that are deliberately preserved versus scheduled to
  change.

Completion test:

- Contract tests pass offline with network and model loading disabled.
- Every fixture identifies its source commits and contains no credentials,
  absolute personal paths, or licensed model weights.

Stop condition: mark Goal 2 Complete, commit the fixtures/tests, report the
result, and end the turn without starting Goal 3.

Completion test and evidence:

- Recorded a live loopback MMCP 1.0 fixture set at
  `tests/contract/fixtures/pre_soma77_mmcp_1_0/`.
- Metadata pins backend `d3c2d43`, MMCP SDK `a298338`, Kimodo `3362b92`, and
  Kimodo-SOMA-RP-v1.1 model revision `6c9233a`; every payload has a SHA-256.
- Captured HTTP 200 capability and generation responses, including the exact
  seed-1234 request and self-contained glTF animation.
- Captured actual schema-validation (HTTP 422), unsupported-version (HTTP
  400), and unknown-model (HTTP 400) envelopes.
- Offline validation proves the historical response contains 30 nodes, 30
  rotation channels, one root-translation channel, four contact channels,
  30 frames at 30 fps, and 3,720 finite accessor floats.
- Five contract tests pass with `HF_HUB_OFFLINE=1` and
  `TRANSFORMERS_OFFLINE=1`. Fixtures contain no credentials or personal
  absolute paths and are each under 250 KB, excluding model weights.

## Goal 3 — Expose SOMA-77 at the service boundary

Status: **Complete**
Completed: 2026-09-06

Outcome sought: the service advertises and returns the authoritative SOMA-77
presentation skeleton while preserving SOMA-30 as the internal generation and
constraint representation.

- [x] Add golden assertions for the current 30-to-77 skeleton relationship.
- [x] Separate input/constraint skeleton handling from output skeleton handling.
- [x] Remove the inherited SOMA-77-to-SOMA-30 response slice.
- [x] Advertise the correct output skeleton and contact channels.
- [x] Validate joint order, hierarchy, rotations, root translation, and array
  dimensions before encoding.
- [x] Update contract fixtures and document the intentional protocol change.

Completion test:

- Unit and contract tests prove 77 output joints in canonical order.
- A fixed live generation returns structurally valid SOMA-77 animation data.
- The same request remains accepted using the internally supported SOMA-30
  constraint representation.

Stop condition: mark Goal 3 Complete, commit the boundary change, add only the
Goal 4 plan for review, report the result, and end the turn before Godot work.

Completion test and evidence:

- Golden tests pin all 30 internal and 77 presentation joint names, their
  subset mapping, canonical order, and parent-before-child hierarchy.
- A SOMA-77 MMCP request containing a root-path constraint compiles to a real
  Kimodo constraint whose skeleton is the internal SOMA-30 object.
- Runtime guards reject invalid skeleton relationships, output joint counts,
  dimensions, non-finite rotation/root values, and mismatched contact counts
  before glTF encoding.
- The inherited response slice is removed. `MotionResult.joint_names` now
  explicitly identifies all 77 ordered output rotations.
- The expanded contacts are correctly labeled as left foot/toe/toe-end,
  followed by right foot/toe/toe-end. This also fixes a previously hidden
  channel-to-name misalignment.
- A full CPU-offloaded text-encoder run on CUDA returned HTTP 200 and recorded
  a 30-frame, seed-1234 live fixture at
  `tests/contract/fixtures/soma77_mmcp_1_0/`.
- The live glTF has 77 named nodes in canonical order, 77 rotation channels,
  one root-translation channel, six contacts, and 9,360 finite accessor
  floats. The 111.3 KiB response contains no weights or private paths.
- ADR 0003 records the boundary decision and its 30-joint constraint-name
  limitation. Implementation checkpoint: `06a5f8c`.

## Goal 4 — Bootstrap the Godot SOMA-77 playback fixture

Status: **Complete**
Completed: 2026-09-06

Outcome sought: an independently versioned Godot 4.7 extension repository can
load the recorded SOMA-77 MMCP animation and prove the source skeleton and
animation survive Godot import before networking or retargeting is added.

- [x] Create the `godot-kimodo` repository locally and on GitHub under
  `Vega-KH`, with license, attribution, Godot ignore rules, and initial docs.
- [x] Record the reference engine as Godot 4.7.2 using
  `C:\Godot-472\Godot_v4.7.2-stable_win64_console.exe` for automated checks.
- [x] Scaffold a minimal Godot project and `addons/kimodo_motion` editor plugin
  that enables without parse errors.
- [x] Copy the Goal 3 SOMA-77 glTF fixture into the Godot test assets with its
  source commit, license/provenance note, and SHA-256.
- [x] Implement a small GDScript fixture loader using `GLTFDocument` and an
  in-memory byte buffer rather than backend-specific parsing shortcuts.
- [x] Add a headless test that verifies the 77 bone names/order and hierarchy,
  one 30 fps animation, all 77 source rotation channels, one root-translation
  channel, and finite native-animation samples.
- [x] Record the Godot 4.7.2 importer behavior that removes nine identity-only
  tracks while retaining their bones' rest rotations; verify the resulting 68
  varying rotation tracks and one translation track.
- [x] Add a minimal editor-openable fixture scene for visual inspection of the
  imported skeleton animation; no humanoid retargeting or live server call yet.
- [x] Document the exact headless command and short manual playback check.

Completion test:

1. The addon enables and the project imports with no Godot errors.
2. The automated fixture test exits zero under the Godot 4.7.2 console build
   and proves the SOMA-77 hierarchy/animation invariants.
3. Opening the fixture scene permits scrubbing or playing the one-second
   recorded animation without altering source assets.

Stop condition: mark Goal 4 Complete, commit and push the new repository,
add the Goal 5 plan for review, report and celebrate, then end the turn before
starting native animation persistence.

Completion test and evidence:

- Created the public MIT-licensed repository at
  `https://github.com/Vega-KH/godot-kimodo`; initial commit `f1f9982` is on
  `main` with a clean worktree.
- Confirmed Godot `4.7.2.stable.official.ed1daf0bf` and recorded the console
  executable used by `scripts/test.ps1`.
- The enabled `addons/kimodo_motion` plugin loads during a headless editor
  startup without parser, plugin, or engine errors.
- The fixture loader passes the recorded JSON glTF bytes directly through
  `GLTFDocument.append_from_buffer` and generates a Godot scene.
- The copied fixture remains byte-identical to Goal 3 at SHA-256
  `54a7a63a326149d4573005be29df49142345bec43240f4cc2451db6bd70461b0`;
  Git line-ending normalization is explicitly disabled for glTF artifacts.
- The headless contract test proves 77 canonical bones in order, one root,
  parent-before-child hierarchy, finite rest transforms, 77 source rotation
  channels, one source translation channel, 30 samples, and finite native
  animation interpolation at the start, midpoint, and end.
- Godot generates 68 varying rotation tracks plus one root-translation track;
  nine source rotations are constant identity and are safely represented by
  the corresponding bones' rest rotations.
- The playback scene ran without errors and rendered 15 GPU-backed frames.
  Visual inspection of the first, middle, and final sampled images showed the
  cyan SOMA-77 line rig progressing from its initial pose into a walking pose
  with root motion.

## Goal 5 — Persist a native Godot animation without runtime dependencies

Status: **Complete**
Completed: 2026-09-06

Outcome sought: convert the imported SOMA-77 fixture into native Godot
animation resources that survive save/reload and play without the extension,
backend, or source glTF being present at runtime.

- [x] Define the minimal native source-motion representation and stable track
  paths used between transport decoding and later retargeting.
- [x] Extract the imported SOMA-77 `Animation` into a new `AnimationLibrary`
  without modifying the imported fixture or its generated resources.
- [x] Save the library and skeleton playback scene as native Godot resources
  using unique output paths and explicit replacement refusal by default.
- [x] Reload the saved resources in a fresh headless scene and verify all 77
  bones, animation duration, root motion, and expected optimized track counts.
- [x] Compare sampled root positions and bone rotations before and after the
  save/reload round trip within recorded numerical tolerances.
- [x] Prove the native playback artifact loads outside the editor process and
  with source-fixture loading excluded from the test path.
- [x] Add a native playback scene for visual comparison with the Goal 4
  in-memory fixture scene.
- [x] Document ownership, unique naming, non-destructive output behavior, and
  the exact automated/manual acceptance commands.

Completion test:

1. A headless bake creates a uniquely named native animation artifact without
   changing the fixture or an existing destination.
2. A clean reload reproduces the recorded poses/root trajectory within the
   declared tolerance and succeeds with the addon disabled.
3. The native visual scene plays the same one-second motion after source glTF
   access is removed from the playback path.

Stop condition: mark Goal 5 Complete, commit and push, propose Goal 6 for
review, report and celebrate, then end the turn before networking work.

Completion test and evidence:

- ADR 0001 defines a native `Soma77Motion` scene, `Soma77Skeleton` node,
  `AnimationPlayer`, external binary `AnimationLibrary`, animation name
  `motion`, and stable track paths of
  `Soma77Skeleton:<SOMA-77 bone name>`.
- `NativeAnimationBaker` creates new skeleton, animation, library, and scene
  objects without taking ownership of or modifying the imported glTF scene.
- The baker uses unique suffixes rather than replacement. Its automated test
  bakes `walk`, then `walk_2`, and verifies the first scene and library remain
  byte-identical after the second bake.
- The committed native fixture is a 24.1 KiB reviewable `.tscn` skeleton scene
  plus a 66.9 KiB binary `.res` animation library. Its complete runtime
  dependency closure contains exactly those two files and rejects any
  reference to `.gltf` or `addons/`.
- Fresh-process runtime validation proves all 77 ordered bones, stable track
  targets, 69 optimized native tracks, unchanged 29/30-second duration,
  finite sampled global poses, and more than one meter of vertical bone span
  so a collapsed skeleton cannot pass.
- Save/reload comparisons cover the start, quarter, midpoint, and final sample
  at tolerances of 0.001 radians (about 0.057 degrees) for rotations and one
  micrometer for root positions. All comparisons pass.
- The full `scripts/test.ps1` gate passes editor-plugin startup, source glTF
  import, unique/non-destructive native round trip, runtime independence, and
  both playback scenes without Godot or script errors.
- The initial orange-rig render exposed missing copied bone pose offsets even
  though structural tests passed. The baker now copies rest and initial pose
  transforms, the runtime test guards against recurrence, and a corrected
  15-frame GPU render visibly matches the Goal 4 cyan rig's movement.
- Godot implementation checkpoint: `986306a` on `Vega-KH/godot-kimodo`.

## Goal 6 — Connect a minimal Godot dock to MMCP capabilities

Status: **Complete**
Completed: 2026-09-06

Outcome sought: an editor dock connects asynchronously to the local backend,
shows trustworthy readiness/model information, and remains responsive and
recoverable when the service is absent or returns incompatible data.

- [x] Add a small transport client for `GET /capabilities` with an explicit
  loopback URL, bounded timeout, cancellation, and no synchronous editor wait.
- [x] Parse and validate MMCP version, model id, fps, SOMA-77 skeleton order,
  supported constraints, contact joints, and response formats into typed
  Godot-side data rather than passing raw dictionaries through the UI.
- [x] Replace the placeholder plugin with a minimal AI Motion dock containing
  connection state, backend URL, Connect/Refresh action, model summary, and
  expandable technical error text.
- [x] Represent at least `Disconnected`, `Connecting`, `Ready`, and `Error`
  states and prevent stale or concurrent responses from overwriting newer
  connection attempts.
- [x] Add deterministic tests for a valid recorded capability response,
  connection refusal, timeout/cancellation, malformed JSON, unsupported MMCP
  version, and a non-SOMA-77 model response.
- [x] Verify plugin disable/re-enable and project restart do not leak HTTP
  nodes, retain stale readiness, or freeze the editor.
- [x] Run one live capability handshake against `kimodo-godot-server` on
  loopback and confirm the dock reports the pinned model, 30 fps, 77 joints,
  three supported constraint types, and six contact channels.
- [x] Document the manual dock check and whether a Godot MCP/editor bridge now
  provides enough benefit to adopt for later interactive viewport work.

Completion test:

1. Automated transport/state tests pass for success, failure, cancellation,
   stale-response, schema, and compatibility cases without external network.
2. The Godot editor remains responsive while the backend is stopped and while
   a live loopback capability request is in flight.
3. With the backend ready, the dock displays the exact Goal 3 SOMA-77
   capability summary and recovers cleanly after disconnect/reconnect.

Stop condition: mark Goal 6 Complete, commit and push both affected
repositories, propose Goal 7 for review, report and celebrate, then end the
turn before live motion generation from Godot.

Completion test and evidence:

- `MmcpCapabilitiesClient` performs a frame-asynchronous loopback-only HTTP
  request, applies a deterministic client deadline, cancels in-flight work,
  and uses monotonic attempt tokens so late responses cannot replace newer
  connection state.
- Typed parsing accepts the byte-identical Goal 3 capability fixture and
  rejects malformed JSON, unsupported MMCP versions, incompatible skeletons,
  missing constraint support, incorrect contacts, formats, coordinates,
  rotations, units, and frame rate before data reaches the dock.
- The right-side **AI Motion** dock presents Disconnected, Connecting, Ready,
  and Error states; Connect/Cancel/Refresh actions; the loopback URL; an exact
  model summary; and expandable technical details.
- Offline transport tests pass actual TCP success, malformed response,
  cancellation, deterministic timeout, connection refusal, and a simulated
  stale completion. The event loop advances throughout each case.
- Three create/state/free dock cycles leave no nodes behind. Two clean
  headless editor startups in the full suite enable the plugin without parser,
  orphan-node, lifecycle, or engine errors.
- The complete Godot suite passes capability, editor restart, SOMA-77 fixture,
  native round-trip, runtime-independence, and both playback checks.
- A live dummy-encoder backend handshake at `127.0.0.1:8769` returned HTTP 200;
  Godot reported exactly `kimodo-soma-rp`, 30 fps, 77 joints, three constraint
  types, and six contact channels. Dummy mode is valid here because
  `/capabilities` is independent of text embeddings.
- The README records the manual dock check, live command, and loopback safety
  boundary. A Godot MCP bridge remains deferred: direct editor startup,
  GDScript integration tests, and rendered project scenes provide the needed
  control today. Reassess when Goal 7 adds interactive viewport preview.
- Godot implementation checkpoint: `b358606` on
  `Vega-KH/godot-kimodo`.

## Goal 7 — Generate and preview live SOMA-77 motion from the dock

Status: **Complete**
Completed: 2026-09-07

Outcome sought: an artist enters a prompt in Godot, receives a live MMCP
SOMA-77 animation without freezing the editor, and immediately previews the
same line-skeleton motion used by the proven fixture pipeline.

- [x] Define typed Godot-side generation options for the initial vertical
  slice: prompt, duration, seed, selected connected model, and glTF response.
- [x] Add an asynchronous, cancellable `POST /generate` client that reuses the
  Goal 6 loopback and attempt-token rules and reports useful server errors.
- [x] Extend the AI Motion dock with prompt/options, Generate/Cancel actions,
  generation status, and clear separation between connection and job state.
- [x] Validate every response against the negotiated MMCP/SOMA-77 contract and
  decode its self-contained glTF bytes in memory without altering fixtures or
  existing native animation resources.
- [x] Preview successful results in a plugin-owned, replaceable line-skeleton
  scene with play/pause and looping controls; clean it up on replacement or
  plugin disable.
- [x] Add deterministic offline tests for request encoding, success, protocol
  errors, cancellation, stale results, invalid glTF, and preview lifecycle.
- [x] Run one live full-text-encoder prompt through the dock path and visually
  compare the generated line skeleton with the recorded fixture behavior.
- [x] Reassess a Godot MCP/editor bridge based on whether direct viewport
  automation is materially limiting interactive preview verification.

Completion test:

1. With the full local encoder running, “A person walks forward.” generates a
   valid 77-joint motion from the Godot dock while the editor remains usable.
2. The result can be played, paused, looped, replaced, and canceled without
   stale state, leaked preview nodes, or modified source/native resources.
3. Offline tests cover the complete request-to-preview path, and a manual
   viewport check confirms visible articulated motion and root travel.

Stop condition: mark Goal 7 Complete, commit and push both affected
repositories, propose Goal 8 for review, report and celebrate, then end the
turn before humanoid retargeting.

Completion test and evidence:

- `KimodoGenerationOptions` owns prompt, duration, seed, and diffusion-step
  validation. Request encoding uses the connected model/version/fps and a deep
  copy of the exact canonical skeleton validated from `/capabilities`.
- `MmcpGenerationClient` performs frame-asynchronous `POST /generate` with an
  explicit 8 MiB response bound, 120-second default deadline, cancellation,
  artist-readable protocol errors, and monotonic attempt tokens. Connection
  and generation remain independent state machines.
- Responses must be glTF 2.0 JSON with the negotiated SOMA-77 names and exact
  hierarchy, all 77 unique rotation channels, one root-translation channel,
  one finite animation, and the requested duration before Godot previews them.
- The dock now provides prompt, frame, and seed controls; Generate/Cancel;
  independent job status/details; and an embedded green line-skeleton preview
  with Play/Pause and Loop controls. A newer successful take frees and replaces
  only the temporary preview scene.
- Deterministic offline tests cover request encoding/validation, real TCP
  success, server errors, invalid glTF, incompatible names and hierarchy,
  cancellation, timeout, stale completion, play/pause/loop, replacement, and
  node cleanup. The complete Goal 4–7 regression suite and two editor startups
  pass without Godot or script errors.
- With the cached full Llama 3/LLM2Vec encoder on CPU and Kimodo on CUDA, the
  automated dock connected, submitted “A person walks forward.” at 30 frames,
  five diffusion steps, and seed 1234, then received HTTP 200 in a 5.73-second
  Godot run. The validated 79,483-byte response has SHA-256
  `f5e939a32e406d75c53aeaa08dbcb6c104c4dd78df211b71a658ed5729a129dc`,
  77 bones, and began playing immediately.
- Three GPU-rendered samples at approximately 0.13, 0.53, and 0.93 seconds
  visibly progress from the initial pose through a lifted-leg stride to a
  distinct late walking pose with root travel.
- ADR 0002 records validation-before-preview and ephemeral ownership. Native
  Windows window control was unavailable during the visual check, but direct
  Godot integration tests and GPU frame capture remained deterministic and
  sufficient. A Godot MCP bridge is still deferred; retargeting may provide a
  stronger interactive-editor use case.
- Godot implementation checkpoint: `5680fa1` on
  `Vega-KH/godot-kimodo`.

## Goal 8 — Save a generated take as a native Godot asset

Status: **Complete**
Completed: 2026-09-07

Outcome sought: an artist can promote the currently previewed generated take
into the self-contained, non-destructive native artifact format proven in
Goal 5, directly from the AI Motion dock.

- [x] Add a Save Native Take action that is enabled only for a validated
  generated preview and asks for a project-relative destination/name.
- [x] Add a repository-root `start.bat` that starts the server with the local
  CPU-offloaded text encoder in one click, independent of the inherited PATH.
- [x] Expose the request's denoising-step count as a manual Godot dock control;
  retain the current MMCP range and use a quality-oriented default rather than
  the five-step integration-test setting.
- [x] Feed the generated imported scene into `NativeAnimationBaker` without
  mutating or transferring ownership of the active preview.
- [x] Preserve Goal 5 unique-name/refuse-overwrite behavior and clearly report
  the actual `.tscn` and `.res` paths created.
- [x] Keep save state separate from connection and generation state so a
  backend disconnect cannot invalidate an already generated take.
- [x] Refresh/select the created resource in the Godot FileSystem dock where
  supported, while keeping the core save path testable without editor UI.
- [x] Add offline tests proving preview-to-native pose equivalence, duplicate
  naming, failure recovery, preview survival, and no glTF/addon dependency in
  the saved resource closure.
- [x] Manually generate, save, reopen, and play one take with the backend
  stopped, confirming the preview and saved copy remain visually equivalent.

Completion test:

1. Saving a live generated take creates unique native `.tscn` and `.res`
   assets without overwriting an existing take or interrupting preview.
2. The saved scene reloads and plays with the backend stopped and has no glTF,
   addon, Python, model, or temporary-preview dependency.
3. Automated samples match preview poses/root motion within Goal 5 tolerances,
   followed by a successful manual reopen/playback check.

Stop condition: mark Goal 8 Complete, commit and push both affected
repositories, propose Goal 9 for review, report and celebrate, then end the
turn before humanoid retargeting.

Completion test and evidence:

- The dock exposes `Denoising steps` from 1–100 and encodes the selected value
  into MMCP; its normal default is now 100 rather than the five-step Goal 7
  integration shortcut.
- `Save Native Take` accepts a `res://` directory and sanitized take name only
  after a validated preview exists. It reports both created paths, refreshes
  and selects the scene in the editor FileSystem dock, and uses Goal 5's
  numeric-suffix behavior for duplicates.
- Offline coverage saves directly from the owned preview scene, proves that
  the preview survives success and failure, reloads the native scene, compares
  animation samples within 0.001 radians / one micrometer, and verifies the
  scene has no glTF or addon dependency.
- The repository-root `start.bat` resolves `.venv` from its own location, sets
  local LLM2Vec and CPU placement explicitly, accepts optional CLI arguments,
  and successfully reached the real CLI help path without relying on PATH.
- Full regression gates passed: backend 23 passed / 7 hardware tests skipped,
  Ruff clean, and every Godot 4.7.2 editor, transport, fixture, native, preview,
  lifecycle, and playback check passed without engine or script errors.
- Live acceptance used the batch launcher and full CPU text encoder to generate
  “A person walks forward.” at 30 frames, 100 denoising steps, and seed 1234 in
  7.41 seconds. The dock received 79,474 bytes and saved a 77-bone native take
  while its preview remained playing. After terminating the complete server
  process tree and confirming loopback refusal, Godot reloaded and played the
  saved `.tscn`; temporary acceptance assets were then removed.
- Godot implementation checkpoint: `aa0a675` on `Vega-KH/godot-kimodo`.

## Goal 9 — Retarget a saved SOMA-77 take to a Godot humanoid skeleton

Status: **Planned — awaiting user review**

Outcome sought: a saved native SOMA-77 take can drive a separate Godot humanoid
test skeleton through an explicit, inspectable bone map without modifying the
source take.

- [ ] Define and document the SOMA-77-to-Godot-humanoid bone mapping, including
  deliberately ignored face, finger, toe-end, and contact-only joints.
- [ ] Add a repository-owned humanoid target fixture with a distinct rest pose
  so the test proves actual retargeting rather than identical-skeleton playback.
- [ ] Implement rest-pose-aware local rotation transfer and preserve intentional
  root translation/heading in a new target `AnimationLibrary`.
- [ ] Keep source, mapping, retargeted animation, and saved target scene as
  separate non-destructive artifacts with unique output naming.
- [ ] Add offline tests for mapped-bone coverage, hierarchy, finite transforms,
  duration, source immutability, save/reload stability, and unmapped-bone rest
  preservation.
- [ ] Compare source and target line-skeleton playback visually at several
  frames, then save/reopen one retargeted take and confirm recognizable motion.

Completion test:

1. A native SOMA-77 take retargets to the distinct humanoid fixture and saves
   without changing either source asset or an existing destination.
2. Automated checks prove all required humanoid bones receive finite,
   rest-pose-corrected animation with preserved duration and root travel.
3. A manual side-by-side playback confirms the target performs the same
   recognizable action after a clean reload.

Stop condition: mark Goal 9 Complete, commit and push, propose Goal 10 for
review, report and celebrate, then end the turn before production-character
mapping or automatic rig detection.

## Current blockers

### Gated Meta Llama 3 access

Resolved 2026-09-05: gated access was granted and verified for `VegaKH`. The
required repository is:

`https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct`

Do not choose Llama 3.1 or 3.2 as a substitute: the pinned McGill adapter
configuration and weights name the original Llama 3 checkpoint.

No active external blocker is known. The full text-encoder load is proven, but
its 28.52 GiB peak system usage leaves limited headroom on this 31.52 GiB
machine; close other memory-heavy applications before cold startup.

## Known issues and risks

- Resolved in Goal 3: the inherited adapter advertised 30 canonical joints and
  sliced 77-joint output to 30. Current capabilities and responses preserve
  authoritative SOMA-77 output; the old behavior remains in historical
  fixtures only.
- Hugging Face reports degraded caching because Windows symlinks are disabled;
  downloads still work but may consume more disk space. Do not enable Windows
  Developer Mode solely for this project without a separate decision.
- PyTorch emits deprecation warnings for Kimodo's `torch.jit` usage. They do
  not currently fail tests or inference.
- Python, CMake, and GitHub CLI are not all on the inherited process `PATH`.
  Use `.venv` and `scripts/check-system.ps1`.
- The Animatica Kimodo fork contains useful Windows/low-memory patches but is
  behind NVIDIA on benchmark fixes. ADR 0002 remains Proposed.
- Animatica commit `390fadb` accidentally removed explicit text-encoder
  placement while adding quantization. The backend now pins the tested
  `Vega-KH/kimodo` repair at `3362b92`; upstream reconciliation remains due.
- Transformers/PEFT emit adapter load reports containing missing/unexpected
  key summaries plus a multiple-adapter warning. NVIDIA's Kimodo quick-start
  explicitly identifies these LLM2Vec reports as expected and safe to ignore.
- Early five-step previews sometimes collapsed more complex prompts, including
  a roundhouse kick, toward idle motion. Goal 8 restored the normal 100-step
  default. Defer a controlled multi-seed combat-vocabulary quality comparison
  until qualitative motion evaluation is in scope.

## Design decisions and questions to track

- Keep the growing progress history here; keep only durable working rules in
  `AGENTS.md`.
- Keep the Godot extension and Python backend independently versioned.
- Preserve MMCP compatibility and add Studio endpoints separately.
- Bind locally by default and make remote access an explicit advanced mode.
- Evaluate a Godot MCP/editor bridge only when interactive editor work begins;
  backend and headless Godot tests do not require it.
- Decide how to maintain the Windows/low-memory Kimodo patches on top of
  NVIDIA upstream after the baseline is complete.
- Decide whether recorded binary glTF fixtures live directly in Git or use a
  separate fixture-release mechanism after their sizes are known.
- Explore a quantized or smaller compatible text encoder after the MMCP
  boundary work. Measure semantic quality as well as download size, RAM,
  startup latency, and GPU impact; this is independent of exposing SOMA-77.
- If no suitable checkpoint exists, investigate producing an exact
  base-plus-LLM2Vec-adapter quantized checkpoint on rented GPU hardware. Before
  publishing it on Hugging Face, review the Meta Llama 3 Community License,
  acceptable-use terms, adapter licenses, attribution, and weight-
  redistribution requirements; the existence of other community conversions
  is not by itself permission.

### Future text-encoder investigation

- Runtime BitsAndBytes 4-bit/8-bit quantization should reduce resident model
  memory, but it still starts from the full-precision Hugging Face checkpoint
  and therefore is not expected to reduce the initial ~15.3 GiB selected-file
  download. Verify this rather than assuming otherwise.
- A pre-quantized checkpoint could reduce both transfer and storage, but must
  preserve the exact LLM2Vec base/adapters and licensing provenance.
- GPU 4-bit inference may fit beside the ~1.3 GiB Kimodo workload on an 8 GB
  GPU, but leaves narrow headroom. CPU quantization, an encoder-only service,
  and persistent embedding caches are separate candidates.
- Replacing Llama 3 with a smaller encoder is not plug-compatible merely
  because it can emit 4,096 values; semantic alignment with Kimodo training
  matters. Evaluate motion quality using a fixed prompt suite before adopting
  any replacement.
- Benchmark encoder-only latency separately from diffusion generation, plus
  cold/cached download, startup, system RAM, VRAM, and prompt quality.

## Session log

### 2026-09-04 — Backend bootstrap and CUDA baseline

Completed Goal 0. Created and pushed the fork, locked the environment, verified
CUDA and MotionCorrection, authenticated GitHub/Hugging Face, loaded the
SOMA-RP model, proved dummy-generation determinism, and exercised the live
MMCP capability endpoint.

### 2026-09-05 — Adopt goal-oriented development

Created this living goal document and linked it from `AGENTS.md`. Goal 1 is
blocked only on access to the exact gated Meta Llama 3 base model.

### 2026-09-05 — Full CPU text encoder and live MMCP generation

Completed Goal 1. Repaired the inherited text-encoder device regression in a
maintained Kimodo fork, applied MMCP request-level seeds, loaded the full
Llama 3/LLM2Vec stack on CPU, and generated matching finite glTF animation
both directly and through the live loopback service while staying below the
8 GB GPU budget.

### 2026-09-06 — Freeze the pre-SOMA-77 MMCP contract

Completed Goal 2. Recorded and hashed the live MMCP 1.0 capability, seeded
generation, glTF, and representative error envelopes. Added offline parsers
that validate structure, finite animation data, provenance, size, and
sanitization. Documented which 30-joint fields are historical and deliberately
scheduled to change in Goal 3.

### 2026-09-06 — Expose the complete SOMA-77 service boundary

Completed Goal 3. Removed the inherited 77-to-30 output slice, advertised the
authoritative 77-joint skeleton, corrected the expanded six-contact mapping,
and retained native SOMA-30 constraint translation. Added golden/runtime
validation, ADR 0003, and a separate fixed-seed live contract fixture. Planned
Goal 4 for user review without beginning its Godot work.

### 2026-09-06 — Bootstrap Godot SOMA-77 fixture playback

Completed Goal 4. Created and published the independent Godot extension
repository, enabled its first editor plugin, decoded the live MMCP fixture from
memory, and proved its 77-bone hierarchy and animation data under Godot 4.7.2.
Added a visible looping line-skeleton scene, automated plugin/fixture/playback
checks, provenance safeguards, and the proposed Goal 5 plan without beginning
native animation persistence.

### 2026-09-06 — Persist self-contained native Godot motion

Completed Goal 5. Added a non-destructive native animation baker, stable
source-motion paths, binary AnimationLibrary output, clean save/reload and
dependency-closure tests, and an orange native-only playback scene. A visual
gate caught and drove a fix for missing initial bone pose offsets. Accepted
ADR 0001 and proposed Goal 6 without beginning networking work.

### 2026-09-06 — Connect the editor dock to MMCP capabilities

Completed Goal 6. Added an asynchronous, cancellable, loopback-only capability
client; strict typed validation of the MMCP 1.0 SOMA-77 contract; and the first
functional AI Motion editor dock. Offline tests cover success, compatibility,
transport failures, stale responses, UI states, and lifecycle cleanup. A live
backend handshake reported the exact expected model summary. Deferred a Godot
MCP bridge until interactive preview work demonstrates a concrete need, and
proposed Goal 7 without beginning live generation.

### 2026-09-07 — Generate and preview live motion in Godot

Completed Goal 7. Added typed request construction, a cancellable/stale-safe
generation transport, strict generated glTF/SOMA-77 validation, and an embedded
playable line-skeleton preview. The full encoder produced “A person walks
forward.” through the real dock workflow, and three rendered frames visibly
confirmed an articulated walking progression. Accepted ADR 0002, kept the
Godot bridge deferred after reassessment, and proposed Goal 8 without beginning
native take saving.

### 2026-09-07 — Save generated takes as native Godot assets

Completed Goal 8. Added the one-click Windows backend launcher, restored a
quality-oriented 100-step generation default with an explicit dock control,
and connected live preview ownership to the proven non-destructive native
baker. Offline and live tests proved unique save paths, pose-equivalent native
reloads, preview survival, and playback after the full backend was stopped.
Proposed Goal 9 without beginning humanoid retargeting.
