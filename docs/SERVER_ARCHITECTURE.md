# Server architecture and development

[Documentation index](README.md). Shared product intent/current work lives in
the [extension development docs](https://github.com/Vega-KH/godot-kimodo/tree/main/docs),
not in a second server roadmap.

This Apache-2.0 fork preserves Animatica history and the `motionmcp_kimodo`
Python namespace. `kimodo-godot-server` is the preferred executable;
`motionmcp-kimodo` remains an alias. See `pyproject.toml` for exact pins.

| Module | Responsibility |
| --- | --- |
| [cli.py](../src/motionmcp_kimodo/cli.py) | CLI/options and loopback launch |
| [backbone.py](../src/motionmcp_kimodo/backbone.py) | Model load, capabilities, request-copy/origin normalization, inference, validated result |
| [translate.py](../src/motionmcp_kimodo/translate.py) | Prompt ranges, options and supported constraints → Kimodo objects/tensors |
| [skeleton.py](../src/motionmcp_kimodo/skeleton.py) | Canonical skeleton and contact contract |

The pinned MMCP SDK supplies HTTP validation, error envelopes and glTF encoding.
Return the exact SOMA-77 presentation rig and six contacts; constraints use the
internal SOMA-30 shared subset. Never restore the inherited 77→30 response slice.
The server does not own Godot sessions, profiles, previews or animation exports.

## Embedded use

The adapter can be embedded using the existing SDK surface:

```python
from motionmcp import serve
from motionmcp_kimodo import KimodoBackbone

serve(KimodoBackbone(text_encoder_mode="local"))
```

Set `TEXT_ENCODER_DEVICE=cpu` for the reference low-VRAM setup.
Prefer the checkout's `start.bat` for normal development. Do not launch multiple
workers/model copies casually on an 8 GB GPU; multi-worker deployment is unvalidated.

## Verification and decisions

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
```

Hardware/network tests remain explicitly separate. Stage 1: 24 passed,
7 hardware-specific skips, Ruff passed; detailed acceptance and local-machine
notes are in the shared handoff/completion record.

Permanent compatibility decisions: [ADRs](adr/README.md). Preserve accepted
decisions; supersede with a new ADR. Dependency reconciliation, remote-mode
error sanitization and a real job/cancellation API are future decisions,
not requirements to implement during pose storage work.
