# ADR 0002: Use the patched Kimodo fork for the first Windows baseline

- Status: Proposed
- Date: 2026-09-04

## Context

At the comparison point, NVIDIA `main` is four commits ahead of the common
ancestor and Animatica `main` has two unique commits. Animatica adds Windows
MotionCorrection build changes, a dummy text encoder, explicit text-encoder
placement, and optional 4/8-bit quantization. NVIDIA adds later documentation
and benchmark-metric corrections.

The first reference machine is Windows with 8 GB VRAM, so the Animatica
changes directly support the initial compatibility experiment. Using a moving
branch would make that experiment irreproducible.

## Candidate decision

Pin Animatica Kimodo commit
`390fadb57a188fb97b8c3af5d5fb693a72ff03c3` for the first installation and
hardware baseline. Pin MMCP SDK commit
`a298338bb3684a506ec313dce6d5cb12a6dc5167` and PyTorch 2.12.1 alongside it.

Do not mark this ADR Accepted until all of the following pass:

- [x] MotionCorrection builds and imports on Windows.
- [x] PyTorch detects CUDA and the reference GPU.
- [ ] A constraint-only smoke generation succeeds.
- [ ] CPU text-encoder generation succeeds within the 8 GB VRAM budget.

After the baseline, create a maintained Kimodo patch branch based on NVIDIA
upstream or contribute the required changes upstream. Carry NVIDIA's benchmark
fixes into that branch before benchmark results are used as quality gates.

## Consequences

- The first experiment prioritizes known Windows and low-memory support.
- Production does not depend indefinitely on an unmerged third-party branch.
- Benchmark results from this candidate must be treated as provisional.
