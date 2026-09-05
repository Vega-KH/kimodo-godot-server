# Development goals and session log

Last updated: 2026-09-05

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
  report and celebrate the result, and end the turn. Do not start the next
  goal until the user explicitly requests it.

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

Status: **Planned**

Outcome sought: recorded, sanitized fixtures and automated parsers describe
the inherited server before its SOMA output behavior changes.

- [x] Create `tests/contract/fixtures/` and fixture-recording guidance.
- [ ] Define fixture metadata containing dependency commits and schema version.
- [ ] Record `/capabilities` for the pinned SOMA-RP model.
- [ ] Record one valid fixed-seed generation response.
- [ ] Record representative validation/error responses.
- [ ] Add tests that load and validate every fixture without model weights.
- [ ] Document fields that are deliberately preserved versus scheduled to
  change.

Completion test:

- Contract tests pass offline with network and model loading disabled.
- Every fixture identifies its source commits and contains no credentials,
  absolute personal paths, or licensed model weights.

Stop condition: mark Goal 2 Complete, commit the fixtures/tests, report the
result, and end the turn without starting Goal 3.

## Goal 3 — Expose SOMA-77 at the service boundary

Status: **Planned**

Outcome sought: the service advertises and returns the authoritative SOMA-77
presentation skeleton while preserving SOMA-30 as the internal generation and
constraint representation.

- [ ] Add golden assertions for the current 30-to-77 skeleton relationship.
- [ ] Separate input/constraint skeleton handling from output skeleton handling.
- [ ] Remove the inherited SOMA-77-to-SOMA-30 response slice.
- [ ] Advertise the correct output skeleton and contact channels.
- [ ] Validate joint order, hierarchy, rotations, root translation, and array
  dimensions before encoding.
- [ ] Update contract fixtures and document the intentional protocol change.

Completion test:

- Unit and contract tests prove 77 output joints in canonical order.
- A fixed live generation returns structurally valid SOMA-77 animation data.
- The same request remains accepted using the internally supported SOMA-30
  constraint representation.

Stop condition: mark Goal 3 Complete, commit the boundary change, report the
result, and end the turn before planning Godot editor work.

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

- The inherited MMCP capability response advertises 30 canonical joints and
  slices the model's 77-joint result down to 30. Goal 3 changes this.
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
  key summaries plus a multiple-adapter warning. Text-conditioned generation
  succeeds deterministically, but adapter-version compatibility should be
  investigated before quality benchmarking.

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
