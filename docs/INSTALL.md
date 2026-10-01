# Backend installation — Windows reference workflow

[Documentation index](README.md). The primary client is
[Kimodo Motion Studio for Godot](https://github.com/Vega-KH/godot-kimodo).
Blender/Proscenium is a separate upstream client, not required for this fork.

## Prerequisites

- Python 3.10+, Git, and a CUDA-capable PyTorch installation/NVIDIA GPU.
  Verified machine: Python 3.10.16, RTX 4070 Laptop (8 GB VRAM), 32 GB RAM.
- CMake and MSVC C++ build tools. Kimodo builds MotionCorrection locally;
  use a Visual Studio developer shell if the compiler is not discoverable.
  Read [MotionCorrection](MOTION_CORRECTION.md) before retrying failed builds.
- Model access/downloads for Kimodo-SOMA-RP-v1.1 and the gated
  Meta-Llama-3-8B-Instruct encoder base. Authenticate locally; never commit tokens.
- Enough disk for model caches and enough RAM for CPU text encoding:
  cold startup has used about 28.52 GiB of total system memory.

## Development checkout

Use this fork, not an unpinned upstream installation:

```powershell
git clone --branch codex/milestone-0-bootstrap https://github.com/Vega-KH/kimodo-godot-server.git
cd kimodo-godot-server
uv sync --locked --extra dev --python 3.10
```

The reference dependency declarations and CUDA package index are in
`pyproject.toml` and `uv.lock`; the Kimodo fork includes Windows/low-VRAM placement repairs.
See [uv's sync documentation](https://docs.astral.sh/uv/concepts/projects/sync/)
for locked installation and extras. This command is for a new checkout;
do not sync or upgrade the established environment during ordinary feature work.
Install uv if needed and complete C++/model access prerequisites first.
This is checkout setup guidance, **not** a new-machine provisioning guarantee:
Stage 1's clean-project acceptance reused the established backend environment.
Build/downloads can take many minutes. Do not recreate a working `.venv`
merely because a restricted agent identity cannot launch it.

## Launch and connect

```powershell
.\start.bat
```

The launcher resolves the checkout's `.venv`, sets local text encoding on CPU
and uses automatic motion-device selection (CUDA on the reference machine).
Wait for `ready`, then connect the Godot dock to `http://127.0.0.1:8000`.
Do not run a second service on the same port. Ctrl+C stops the service.
For add-on installation, sessions and rig setup, follow the
[artist guide](https://github.com/Vega-KH/godot-kimodo/blob/main/addons/kimodo_motion/README.md).

## Troubleshooting

- Build failure: inspect the C++ error and follow the MotionCorrection guide;
  do not blame Python or replace pinned dependencies without evidence.
- Model access failure: verify local Hugging Face authorization and gated
  approvals. Preserve tokens outside the repository and logs.
- Out of memory: close other heavy applications, retain CPU text encoding,
  shorten the clip and inspect the actual backend traceback.
- Cannot connect: verify the ready message, loopback URL and port/process;
  an encoder/model still loading is not a ready service.
- Sandbox permission error: the working owner-created venv may require execution
  in the owner's context; this is not evidence of dependency corruption.

[Usage](USAGE.md) documents flags and the canonical skeleton/constraint limits.
Remote/LAN deployment, other GPU vendors and automatic provisioning remain unvalidated.
