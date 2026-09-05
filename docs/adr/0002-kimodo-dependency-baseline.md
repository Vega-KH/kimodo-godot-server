# ADR 0002: Maintain the patched Kimodo fork for the Windows baseline

- Status: Proposed
- Date: 2026-09-04

## Context

At the initial comparison point, NVIDIA `main` was four commits ahead of the
common ancestor and Animatica `main` had two unique commits. Animatica adds Windows
MotionCorrection build changes, a dummy text encoder, explicit text-encoder
placement, and optional 4/8-bit quantization. NVIDIA adds later documentation
and benchmark-metric corrections.

During Goal 1, inspection found that Animatica's quantization commit
`390fadb` had accidentally overwritten the earlier explicit
`TEXT_ENCODER_DEVICE` behavior. The encoder loaded on CPU but LLM2Vec would
move it to CUDA on the first prompt, which cannot fit the reference 8 GB GPU.

The first reference machine is Windows with 8 GB VRAM, so the Animatica
changes directly support the initial compatibility experiment. Using a moving
branch would make that experiment irreproducible.

## Candidate decision

Pin Vega-KH Kimodo commit
`3362b92c37faa100fb697972f0fc5485dd94dd4f`, based on Animatica `390fadb`,
for the first installation and hardware baseline. This repair preserves the
quantization support while restoring explicit device placement during both
model load and encode. Pin MMCP SDK commit
`a298338bb3684a506ec313dce6d5cb12a6dc5167` and PyTorch 2.12.1 alongside it.

Do not mark this ADR Accepted until all of the following pass:

- [x] MotionCorrection builds and imports on Windows.
- [x] PyTorch detects CUDA and the reference GPU.
- [ ] A constraint-only smoke generation succeeds.
- [x] CPU text-encoder generation succeeds within the 8 GB VRAM budget.

Goal 1 evidence (2026-09-05): the full unquantized Llama 3/LLM2Vec encoder
remained on CPU before and after generation. A five-step, 30-frame prompt
completed directly and through live loopback MMCP; both glTF documents matched
exactly and decoded to finite data. Peak CUDA memory was 1.12 GiB allocated /
1.29 GiB reserved; peak process RSS was 16.01 GiB. Cached setup took 24.1
seconds, excluding the one-time 53.6-minute gated-model download.

After the baseline, create a maintained Kimodo patch branch based on NVIDIA
upstream or contribute the required changes upstream. Carry NVIDIA's benchmark
fixes into that branch before benchmark results are used as quality gates.

## Consequences

- The first experiment prioritizes known Windows and low-memory support.
- The backend temporarily depends on an unmerged branch in the Vega-KH fork.
- The device-placement repair has focused tests and an immutable commit pin.
- Benchmark results from this candidate must be treated as provisional.
- Adapter loading currently emits missing/unexpected-key summaries and a
  multiple-adapter warning. Successful deterministic generation makes this
  non-blocking for the runtime gate, but quality benchmarks require a separate
  compatibility investigation.
