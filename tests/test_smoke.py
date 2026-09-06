# SPDX-License-Identifier: Apache-2.0
"""Smoke tests that don't require loading model weights.

Anything that needs an actual Kimodo model (FK, generation) is excluded
from CI; those run as integration tests against a GPU-equipped runner.
"""

from __future__ import annotations

import pytest


def test_imports_clean():
    import motionmcp_kimodo
    from motionmcp_kimodo import KimodoBackbone
    from motionmcp_kimodo.cli import main  # noqa: F401
    from motionmcp_kimodo.skeleton import (  # noqa: F401
        resolve_foot_contact_joints,
        skeleton_to_mmcp,
        standing_root_position,
    )
    from motionmcp_kimodo.translate import translate_request  # noqa: F401

    assert motionmcp_kimodo.__version__ == "0.1.0.dev0"
    assert KimodoBackbone


def test_resolve_foot_contact_joints_full_set():
    from motionmcp_kimodo.skeleton import resolve_foot_contact_joints

    bones = ["Hips", "LeftFoot", "LeftToeBase", "RightFoot", "RightToeBase"]
    resolved = resolve_foot_contact_joints(bones)
    assert resolved == ["LeftFoot", "LeftToeBase", "RightFoot", "RightToeBase"]


def test_resolve_foot_contact_joints_missing_returns_empty():
    from motionmcp_kimodo.skeleton import resolve_foot_contact_joints

    bones = ["Hips", "LeftFoot"]   # no right side at all
    assert resolve_foot_contact_joints(bones) == []


def test_resolve_expanded_soma77_foot_contact_joints():
    from motionmcp_kimodo.skeleton import resolve_foot_contact_joints

    bones = [
        "Hips", "LeftFoot", "LeftToeBase", "LeftToeEnd",
        "RightFoot", "RightToeBase", "RightToeEnd",
    ]
    assert resolve_foot_contact_joints(bones, expanded_soma77=True) == bones[1:]


def test_backbone_does_not_load_until_setup():
    """KimodoBackbone() must not try to load the model on construction —
    setup() is the lifecycle hook for that."""
    from motionmcp_kimodo import KimodoBackbone

    b = KimodoBackbone(model_id="some-model", device="cpu")
    assert b.model is None
    assert b._spec is None


def test_cli_passes_text_encoder_mode(monkeypatch):
    import sys

    captured: dict = {}

    def fake_serve(backbone, **kwargs):
        captured["backbone"] = backbone

    monkeypatch.setattr("motionmcp_kimodo.cli.serve", fake_serve)
    monkeypatch.setattr(
        sys,
        "argv",
        ["motionmcp-kimodo", "--text-encoder-mode", "local", "--port", "9000"],
    )

    from motionmcp_kimodo.cli import main

    main()
    assert captured["backbone"].text_encoder_mode == "local"


def test_cli_binds_to_loopback_by_default(monkeypatch):
    import sys

    captured: dict = {}

    def fake_serve(backbone, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr("motionmcp_kimodo.cli.serve", fake_serve)
    monkeypatch.setattr(sys, "argv", ["kimodo-godot-server"])

    from motionmcp_kimodo.cli import main

    main()
    assert captured["host"] == "127.0.0.1"


def test_capabilities_before_setup_raises():
    from motionmcp.errors import ProtocolError

    from motionmcp_kimodo import KimodoBackbone

    b = KimodoBackbone(model_id="x", device="cpu")
    with pytest.raises(ProtocolError) as ei:
        b.capabilities()
    assert ei.value.code == "model_unavailable"


def test_request_seed_is_applied(monkeypatch):
    import asyncio

    import numpy as np
    from motionmcp import GenerateRequest, Options

    from motionmcp_kimodo import backbone as backbone_module

    class FakeModel:
        skeleton = type(
            "Skeleton",
            (),
            {"bone_order_names": ["Hips"], "root_idx": 0, "hip_joint_idx": None},
        )()

        def __call__(self, **_kwargs):
            return {
                "local_rot_mats": np.eye(3, dtype=np.float32)[None, None, None],
                "root_positions": np.zeros((1, 1, 3), dtype=np.float32),
            }

    seeded = []
    monkeypatch.setattr(backbone_module, "seed_everything", seeded.append)
    monkeypatch.setattr(backbone_module, "translate_request", lambda *_args: {})

    instance = backbone_module.KimodoBackbone(model_id="test", device="cpu")
    instance.model = FakeModel()
    instance._output_joint_names = ("Hips",)
    request = GenerateRequest.model_construct(options=Options(seed=1234), constraints=[])

    asyncio.run(instance.generate(request))

    assert seeded == [1234]
