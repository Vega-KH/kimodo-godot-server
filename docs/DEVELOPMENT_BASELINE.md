# Development baseline

Status: Milestone 0 bootstrap

## Fork point

- Upstream: `https://github.com/animatica-ai/motionmcp-kimodo.git`
- Upstream commit: `99a88e6ceae89bdc9734503dd06cd61d9d82ed1b`
- Upstream branch: `main`
- License: Apache-2.0 (retained in `LICENSE`)
- Local fork name: `kimodo-godot-server`

The local Git remote named `upstream` tracks Animatica. A hosted fork remote
named `origin` will be added after the GitHub destination is known.

## Verified development machine

- OS: Windows
- Godot: 4.7.2 stable at `C:\Godot-472`
- GPU: NVIDIA GeForce RTX 4070 Laptop GPU, 8188 MiB
- NVIDIA driver: 616.64
- Git: 2.49.0.windows.1

Not yet installed or not on `PATH` at bootstrap time:

- Python
- `uv`
- CMake
- GitHub CLI (`gh`)
- A verified Visual Studio C++ build environment

## Immediate gates

1. Provision a Python 3.10 environment and Windows C++/CMake prerequisites.
2. Resolve and lock CUDA-compatible PyTorch, MMCP SDK, Kimodo, and transitive
   dependencies without downloading model weights as part of normal tests.
3. Capture the upstream MMCP behavior as contract fixtures.
4. Compare the Animatica Kimodo fork with NVIDIA upstream and record the
   dependency choice.
5. Change the service output boundary from the upstream SOMA-30 slice to
   structurally validated SOMA-77 output.
6. Only then run the first CPU-text-encoder/CUDA-motion-model benchmark.

## Bootstrap decisions

- The distribution and preferred executable are named
  `kimodo-godot-server`.
- The existing Python import namespace and legacy executable remain available
  during the adapter refactor.
- The server listens on loopback by default.
- No Godot MCP bridge is required for backend development. Godot can be driven
  headlessly for extension tests; an editor bridge can be evaluated when
  interactive dock and viewport work begins.
