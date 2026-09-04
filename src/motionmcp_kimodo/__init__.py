# SPDX-License-Identifier: Apache-2.0
"""kimodo-godot-server — Godot service and MMCP Kimodo adapter.

A drop-in :class:`motionmcp.Backbone` that runs a Kimodo SOMA model under
the MMCP protocol. Clients send the canonical skeleton served at
``/capabilities`` verbatim.

Run a server::

    kimodo-godot-server --port 8000
    # or:
    python -m motionmcp_kimodo --model soma30 --device cuda:0
"""

from .backbone import KimodoBackbone

__all__ = ["KimodoBackbone"]
__version__ = "0.1.0.dev0"
