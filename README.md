# kimodo-godot-server

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/animatica-ai/motionmcp-kimodo)

Local Kimodo motion-generation service for the Godot editor, built as a
history-preserving fork of Animatica's Apache-2.0
[`motionmcp-kimodo`](https://github.com/animatica-ai/motionmcp-kimodo).

The fork supports the completed, user-tested Godot Stage 1 basic workflow.
It intentionally retains the
`motionmcp_kimodo` Python namespace and the `motionmcp-kimodo` command while
the reusable MMCP adapter is separated from Godot Studio services. The new
preferred command is `kimodo-godot-server`.

See [the development baseline](docs/DEVELOPMENT_BASELINE.md) and
[architecture decisions](docs/adr/README.md) for current status.

The primary client is [Kimodo Motion Studio for Godot](https://github.com/Vega-KH/godot-kimodo).
Its session-first workflow generates one or two SOMA-77 takes, retargets them
through reviewed character profiles, and keeps durable source history in the
Godot project. The server owns inference, not editor sessions or exported files.
It binds to loopback by default; remote deployment is not the validated workflow.

## Who this is for

**This repo is for developers** who are comfortable with Python environments, CUDA, and self-hosting ML services. The install assumes you can debug `pip`, virtualenvs, CUDA drivers, and Hugging Face authentication on your own. See [Installation](docs/INSTALL.md) and [MotionCorrection](docs/MOTION_CORRECTION.md) for what that involves.

For the artist-facing steps, use the add-on's
[basic workflow guide](https://github.com/Vega-KH/godot-kimodo/blob/main/addons/kimodo_motion/README.md).
The supported reference environment is Windows, Godot 4.7.2, CUDA motion
generation and a local CPU text encoder. This is not a universal installer.

> **Development build** — dependencies are pinned in `pyproject.toml`.
> The validated service contract is MMCP 1.0 with SOMA-77 presentation;
> SOMA-30 remains an internal model/constraint representation.

## Features

- **MMCP-native** — implements [`motionmcp.Backbone`](https://animatica.ai/mmcp/docs/sdk/backbone); capabilities, `/generate`, glTF responses
- **Kimodo SOMA models** — loads Kimodo checkpoints; maps MMCP requests to Kimodo inference
- **Constraint-aware** — root paths, effector targets, pose keyframes (see [MMCP concepts](https://animatica.ai/mmcp/docs/concepts/skeleton))
- **Local CLI** — `kimodo-godot-server --port 8000`; root `start.bat` launches the verified Windows environment
- **Embeddable** — mount `KimodoBackbone` in your own FastAPI / ASGI app ([Development](docs/DEVELOPMENT.md))

## Requirements

| | |
|---|---|
| **Python** | 3.10+ |
| **GPU** | NVIDIA GPU strongly recommended (CUDA-capable PyTorch) |
| **Build tools** | CMake + C++ compiler — Kimodo builds **MotionCorrection** during install ([guide](docs/MOTION_CORRECTION.md)) |
| **Git** | Required for `pip` install (Kimodo is not on PyPI) |

Dependency/build troubleshooting: **[Installation](docs/INSTALL.md)**.
That inherited guide also discusses Blender; use the Godot workflow linked above
for this fork's client setup. The [development baseline](docs/DEVELOPMENT_BASELINE.md)
records the original installation and machine, not current workflow acceptance.

## Quick start (self-hosted)

After completing this fork's development installation and model-access setup:

```powershell
.\start.bat
```

Wait for model/text-encoder loading, then enable the Godot add-on, start/open a
session, select/review a character rig, and connect to `http://127.0.0.1:8000`.
Generate at the default 100 steps; the add-on supports one or two takes and
caps steps at 200. Save exports, Accept into a production library, and offline
History/reopen/delete are handled by the Godot project. **Stop waiting** only
stops the client from receiving that response; active inference may continue.
Do not launch a second server on the same port. Ctrl+C stops the existing server.

Install can take **30+ minutes** on first run (PyTorch, Kimodo, MotionCorrection compile). Use `pip install -v ...` to see progress.

### Windows development checkout

After completing the development install in this repository, double-click
`start.bat` to start the loopback server with Kimodo on CUDA and the full local
LLM2Vec text encoder offloaded to CPU. The launcher resolves `.venv` relative to
itself, so neither Python nor `kimodo-godot-server` needs to be on `PATH`.

## Documentation

| Guide | Description |
|---|---|
| [Installation](docs/INSTALL.md) | Inherited dependency/build setup and troubleshooting |
| [MotionCorrection](docs/MOTION_CORRECTION.md) | C++ build step (common install blocker) |
| [Usage](docs/USAGE.md) | CLI, ports, models, environment variables |
| [Development](docs/DEVELOPMENT.md) | Architecture and programmatic use |
| [Docs index](docs/README.md) | All guides and external links |

## Related projects

| Project | Role |
|---|---|
| [MMCP](https://animatica.ai/mmcp) | Motion Model Communication Protocol |
| [motionmcp](https://github.com/animatica-ai/motionmcp) | Python SDK (`Backbone`, server helpers) |
| [Kimodo](https://github.com/animatica-ai/kimodo) | Motion diffusion model (dependency) |
| [Proscenium](https://github.com/animatica-ai/proscenium-blender) | Official Blender client |
| [Implementations](https://animatica.ai/mmcp/docs/get-started/implementations) | All official servers & clients |

## Contributing

Contributions are welcome.

1. Check [open issues](https://github.com/animatica-ai/motionmcp-kimodo/issues) or open one to discuss larger changes.
2. Clone, install dev deps, and run tests — see [Development](docs/DEVELOPMENT.md).
3. Open a pull request with a clear description and test plan.

Bug reports for install failures: include OS, Python version, and the full `pip install -v` log (especially the MotionCorrection build).

## Community

**[Animatica AI Discord](https://discord.com/invite/A8CrURBewz)** — questions, install help, Proscenium, and MMCP/Kimodo discussion.

## License

[Apache License 2.0](LICENSE). Kimodo model weights and third-party deps have separate licenses — see [Kimodo](https://github.com/animatica-ai/kimodo) and Hugging Face model cards.
