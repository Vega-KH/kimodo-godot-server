# SPDX-License-Identifier: Apache-2.0
"""Golden tests for the SOMA-30 constraint / SOMA-77 presentation boundary."""

from __future__ import annotations

import asyncio

import numpy as np
import pytest
from kimodo.skeleton import SOMASkeleton30, SOMASkeleton77
from motionmcp import GenerateRequest
from motionmcp.errors import ProtocolError

from motionmcp_kimodo import backbone as backbone_module
from motionmcp_kimodo.skeleton import skeleton_to_mmcp

SOMA30_NAMES = (
    "Hips", "Spine1", "Spine2", "Chest", "Neck1", "Neck2", "Head", "Jaw",
    "LeftEye", "RightEye", "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
    "LeftHandThumbEnd", "LeftHandMiddleEnd", "RightShoulder", "RightArm",
    "RightForeArm", "RightHand", "RightHandThumbEnd", "RightHandMiddleEnd", "LeftLeg",
    "LeftShin", "LeftFoot", "LeftToeBase", "RightLeg", "RightShin", "RightFoot",
    "RightToeBase",
)

SOMA77_NAMES = (
    "Hips", "Spine1", "Spine2", "Chest", "Neck1", "Neck2", "Head", "HeadEnd", "Jaw",
    "LeftEye", "RightEye", "LeftShoulder", "LeftArm", "LeftForeArm", "LeftHand",
    "LeftHandThumb1", "LeftHandThumb2", "LeftHandThumb3", "LeftHandThumbEnd",
    "LeftHandIndex1", "LeftHandIndex2", "LeftHandIndex3", "LeftHandIndex4",
    "LeftHandIndexEnd", "LeftHandMiddle1", "LeftHandMiddle2", "LeftHandMiddle3",
    "LeftHandMiddle4", "LeftHandMiddleEnd", "LeftHandRing1", "LeftHandRing2",
    "LeftHandRing3", "LeftHandRing4", "LeftHandRingEnd", "LeftHandPinky1",
    "LeftHandPinky2", "LeftHandPinky3", "LeftHandPinky4", "LeftHandPinkyEnd",
    "RightShoulder", "RightArm", "RightForeArm", "RightHand", "RightHandThumb1",
    "RightHandThumb2", "RightHandThumb3", "RightHandThumbEnd", "RightHandIndex1",
    "RightHandIndex2", "RightHandIndex3", "RightHandIndex4", "RightHandIndexEnd",
    "RightHandMiddle1", "RightHandMiddle2", "RightHandMiddle3", "RightHandMiddle4",
    "RightHandMiddleEnd", "RightHandRing1", "RightHandRing2", "RightHandRing3",
    "RightHandRing4", "RightHandRingEnd", "RightHandPinky1", "RightHandPinky2",
    "RightHandPinky3", "RightHandPinky4", "RightHandPinkyEnd", "LeftLeg", "LeftShin",
    "LeftFoot", "LeftToeBase", "LeftToeEnd", "RightLeg", "RightShin", "RightFoot",
    "RightToeBase", "RightToeEnd",
)

SOMA77_CONTACT_NAMES = (
    "LeftFoot", "LeftToeBase", "LeftToeEnd",
    "RightFoot", "RightToeBase", "RightToeEnd",
)


def test_golden_soma30_to_soma77_relationship_and_hierarchy():
    input_skeleton = SOMASkeleton30()
    output_skeleton = SOMASkeleton77()

    assert tuple(input_skeleton.bone_order_names) == SOMA30_NAMES
    assert tuple(output_skeleton.bone_order_names) == SOMA77_NAMES
    assert set(SOMA30_NAMES) < set(SOMA77_NAMES)
    assert tuple(SOMA77_NAMES[index] for index in input_skeleton.get_skel_slice(output_skeleton)) == (
        SOMA30_NAMES
    )

    wire = skeleton_to_mmcp(output_skeleton)
    assert tuple(joint["name"] for joint in wire["joints"]) == SOMA77_NAMES
    assert wire["joints"][0]["parent"] is None
    seen: set[str] = set()
    for joint in wire["joints"]:
        if joint["parent"] is not None:
            assert joint["parent"] in seen
        assert np.isfinite(joint["rest_translation"]).all()
        seen.add(joint["name"])


class _FakeSomaModel:
    fps = 30.0

    def __init__(self) -> None:
        self.skeleton = SOMASkeleton30()
        self.output_skeleton = SOMASkeleton77()
        self.received_constraints = None

    def __call__(self, **kwargs):
        self.received_constraints = kwargs["constraint_lst"]
        frames = sum(kwargs["num_frames"])
        rotations = np.broadcast_to(
            np.eye(3, dtype=np.float32), (1, frames, len(SOMA77_NAMES), 3, 3),
        ).copy()
        return {
            "local_rot_mats": rotations,
            "root_positions": np.zeros((1, frames, 3), dtype=np.float32),
            "foot_contacts": np.zeros((1, frames, 6), dtype=bool),
        }


def test_soma77_request_generates_soma77_using_soma30_constraints(monkeypatch):
    model = _FakeSomaModel()
    monkeypatch.setattr(backbone_module, "load_model", lambda *_args, **_kwargs: model)
    backend = backbone_module.KimodoBackbone(model_id="test", device="cpu")
    backend.setup()

    spec = backend.capabilities()
    assert tuple(joint.name for joint in spec.canonical_skeleton.joints) == SOMA77_NAMES
    assert tuple(spec.predicted_contact_joints) == SOMA77_CONTACT_NAMES

    request = GenerateRequest.model_validate({
        "protocol_version": "1.0",
        "model": "test",
        "skeleton": spec.canonical_skeleton.model_dump(),
        "segments": [{"type": "text", "prompt": "walk", "duration_frames": 5}],
        "constraints": [{
            "type": "root_path",
            "frames": [0, 4],
            "positions_xz": [[0.0, 0.0], [1.0, 0.0]],
        }],
        "timing": {"fps": 30.0},
        "options": {"diffusion_steps": 1, "num_samples": 1, "seed": 7},
    })
    result = asyncio.run(backend.generate(request))

    assert model.received_constraints[0].skeleton is model.skeleton
    assert result.rotations.shape == (1, 5, 77, 4)
    assert result.root_translations.shape == (1, 5, 3)
    assert tuple(result.joint_names or ()) == SOMA77_NAMES
    assert tuple(result.foot_contacts) == SOMA77_CONTACT_NAMES


def test_output_validation_rejects_wrong_joint_count_and_nonfinite_root():
    rotations = np.broadcast_to(np.eye(3), (1, 2, 76, 3, 3))
    roots = np.zeros((1, 2, 3))
    with pytest.raises(ProtocolError, match="76 joints"):
        backbone_module._validate_output_arrays(
            rotations,
            roots,
            joint_names=SOMA77_NAMES,
            contacts=np.zeros((1, 2, 6)),
            contact_joint_names=list(SOMA77_CONTACT_NAMES),
        )

    rotations = np.broadcast_to(np.eye(3), (1, 2, 77, 3, 3))
    roots[0, 0, 0] = np.nan
    with pytest.raises(ProtocolError, match="non-finite"):
        backbone_module._validate_output_arrays(
            rotations,
            roots,
            joint_names=SOMA77_NAMES,
            contacts=np.zeros((1, 2, 6)),
            contact_joint_names=list(SOMA77_CONTACT_NAMES),
        )


def test_output_validation_rejects_misaligned_contact_channels():
    rotations = np.broadcast_to(np.eye(3), (1, 2, 77, 3, 3))
    roots = np.zeros((1, 2, 3))
    with pytest.raises(ProtocolError, match="foot-contact shape"):
        backbone_module._validate_output_arrays(
            rotations,
            roots,
            joint_names=SOMA77_NAMES,
            contacts=np.zeros((1, 2, 4)),
            contact_joint_names=list(SOMA77_CONTACT_NAMES),
        )
