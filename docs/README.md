# Backend documentation

Stage 1 basic workflow is complete and user-tested (2026-10-01).
This folder covers the independently versioned **server**, not the shared roadmap.

| Guide | Purpose |
| --- | --- |
| [Installation](INSTALL.md) | Windows reference setup, prerequisites and troubleshooting |
| [Usage](USAGE.md) | Launcher, CLI flags, environment and SOMA constraint boundary |
| [MotionCorrection](MOTION_CORRECTION.md) | Retained C++ build/platform troubleshooting |
| [Server architecture](SERVER_ARCHITECTURE.md) | Adapter modules, embedding and tests |
| [Architecture decisions](adr/README.md) | Durable dependency/protocol/rig/ownership decisions |

Shared planning and fresh-session context live in
[godot-kimodo/docs](https://github.com/Vega-KH/godot-kimodo/tree/main/docs).
In the combined workspace, read `../../godot-kimodo/docs/README.md`;
then its product plan, DEVELOPMENT_GOALS, AGENT_HANDOFF and STAGE1_COMPLETION.

The obsolete bootstrap baseline, long duplicated ledger and Goal 21 walkthrough
were distilled into that handoff/completion record. Their complete historical
text remains in server Git checkpoint `0f1d347`.
DEVELOPMENT.md was replaced by SERVER_ARCHITECTURE.md; no runtime code changed.

Artist steps: [add-on guide](https://github.com/Vega-KH/godot-kimodo/blob/main/addons/kimodo_motion/README.md).
Upstream protocol/model references: [MMCP](https://animatica.ai/mmcp),
[official Kimodo](https://github.com/nv-tlabs/kimodo).
