# Development baseline

Status: Milestone 0 bootstrap

## Fork point

- Upstream: `https://github.com/animatica-ai/motionmcp-kimodo.git`
- Upstream commit: `99a88e6ceae89bdc9734503dd06cd61d9d82ed1b`
- Upstream branch: `main`
- License: Apache-2.0 (retained in `LICENSE`)
- Local fork name: `kimodo-godot-server`
- Hosted fork: `https://github.com/Vega-KH/kimodo-godot-server`

The local Git remote named `upstream` tracks Animatica. `origin` tracks the
hosted Vega-KH fork.

## Verified development machine

- OS: Windows
- Godot: 4.7.2 stable at `C:\Godot-472`
- GPU: NVIDIA GeForce RTX 4070 Laptop GPU, 8188 MiB
- NVIDIA driver: 616.64
- Git: 2.49.0.windows.1
- Python: 3.10.16 in `.venv`
- `uv`: 0.12.9
- PyTorch: 2.12.1+cu130; CUDA 13.0; GPU detected
- CMake: 3.31.6 from Visual Studio Community 2022
- MSVC: 19.44.35209 x64
- GitHub CLI: 2.100.0 portable workspace install

Some tools are installed outside the process `PATH`; use `.venv` and
`scripts/check-system.ps1` rather than relying on global command discovery.

## Initial validation

- `torch.cuda.is_available()`: `true`
- CUDA device: NVIDIA GeForce RTX 4070 Laptop GPU
- MotionCorrection import: passed
- Unit tests: 10 passed, 7 hardware-specific tests skipped
- Ruff: passed
- Kimodo-SOMA-RP-v1.1 model access, download, and CUDA load: passed
- Loaded skeletons: SOMA-30 input and SOMA-77 output
- Dummy-encoder fixed-seed generation: passed and exactly reproducible
- Live loopback `/capabilities`: HTTP 200; currently advertises SOMA-30
- Full text encoder: blocked on gated base-model approval

## Immediate gates

1. Obtain gated access to `meta-llama/Meta-Llama-3-8B-Instruct` and run the
   CPU-text-encoder baseline.
2. Capture the upstream MMCP behavior as contract fixtures.
3. Run a constraint-only baseline.
4. Change the service output boundary from the upstream SOMA-30 slice to
   structurally validated SOMA-77 output.
5. Reconcile the Windows/low-memory patches with NVIDIA's newer upstream and
   benchmark fixes.

## Bootstrap decisions

- The distribution and preferred executable are named
  `kimodo-godot-server`.
- The existing Python import namespace and legacy executable remain available
  during the adapter refactor.
- The server listens on loopback by default.
- No Godot MCP bridge is required for backend development. Godot can be driven
  headlessly for extension tests; an editor bridge can be evaluated when
  interactive dock and viewport work begins.
- Detailed progress and the next goals are maintained in
  `docs/DEVELOPMENT_GOALS.md`.
