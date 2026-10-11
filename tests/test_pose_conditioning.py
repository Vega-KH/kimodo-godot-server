# SPDX-License-Identifier: Apache-2.0
"""Pinned pose conditioning semantics; CPU skeletons only, no diffusion weights."""

from collections import defaultdict
from types import SimpleNamespace

import numpy as np
import pytest
import torch
from kimodo.constraints import EndEffectorConstraintSet, FullBodyConstraintSet
from kimodo.skeleton import SOMASkeleton30
from motionmcp import schemas
from motionmcp.errors import ProtocolError

from motionmcp_kimodo.translate import _pose_keyframe


@pytest.fixture
def model():
    return SimpleNamespace(skeleton=SOMASkeleton30(), fps=30.0)


def test_complete_edited_pose_changes_fk_positions_and_preserves_input(model):
    rotations = {name: [0.0, 0.0, 0.0, 1.0] for name in model.skeleton.bone_order_names}
    angle = 0.65
    rotations["LeftForeArm"] = [0.0, 0.0, float(np.sin(angle / 2)), float(np.cos(angle / 2))]
    pose = schemas.PoseKeyframeConstraint(
        type="pose_keyframe", frame=5, joint_rotations=rotations,
        root_position=[1.5, 0.8, -2.0], fill_mode="rest",
    )
    before = pose.model_dump(mode="json")
    constraint = _pose_keyframe(pose, model, "cpu", 30)
    assert isinstance(constraint, FullBodyConstraintSet)
    assert constraint.frame_indices.tolist() == [5]
    np.testing.assert_allclose(constraint.smooth_root_2d.numpy(), [[1.5, -2.0]])
    np.testing.assert_allclose(constraint.root_y_pos.numpy(), [0.8])
    neutral = schemas.PoseKeyframeConstraint(
        type="pose_keyframe", frame=5,
        joint_rotations={name: [0.0, 0.0, 0.0, 1.0] for name in rotations},
        root_position=[1.5, 0.8, -2.0], fill_mode="rest",
    )
    neutral_constraint = _pose_keyframe(neutral, model, "cpu", 30)
    hand = model.skeleton.bone_index["LeftHand"]
    assert torch.linalg.vector_norm(
        constraint.global_joints_positions[0, hand]
        - neutral_constraint.global_joints_positions[0, hand]
    ).item() > 0.1
    # Conditioning containers need empty lists for each consumed quantity.
    data, indices = defaultdict(list), defaultdict(list)
    constraint.update_constraints(data, indices)
    assert data["global_joints_positions"]
    assert not data["global_joints_rots"]  # Full-body rotations drive FK, not a rotation mask.
    assert pose.model_dump(mode="json") == before


def test_generate_fill_is_effector_group_conditioning_not_a_joint_mask(model):
    pose = schemas.PoseKeyframeConstraint(
        type="pose_keyframe", frame=3,
        joint_rotations={"Spine1": [0, 0, 0, 1], "LeftHand": [0, 0, 0, 1]},
        fill_mode="generate",
    )
    constraint = _pose_keyframe(pose, model, "cpu", 30)
    assert isinstance(constraint, EndEffectorConstraintSet)
    assert constraint.joint_names == ["LeftHand"]
    assert model.skeleton.bone_index["Spine1"] not in constraint.rot_indices.tolist()
    assert constraint.rot_indices.tolist() == [model.skeleton.bone_index["LeftHand"]]


def test_torso_only_generate_fill_falls_back_to_full_body(model):
    pose = schemas.PoseKeyframeConstraint(
        type="pose_keyframe", frame=3,
        joint_rotations={"Spine1": [0, 0, 0, 1]}, fill_mode="generate",
    )
    assert isinstance(_pose_keyframe(pose, model, "cpu", 30), FullBodyConstraintSet)


def test_presentation_finger_channels_are_not_model_constraints(model):
    pose = schemas.PoseKeyframeConstraint(
        type="pose_keyframe", frame=3,
        joint_rotations={"LeftHandIndex2": [0, 0, 0, 1]}, fill_mode="rest",
    )
    with pytest.raises(ProtocolError, match="unknown joints"):
        _pose_keyframe(pose, model, "cpu", 30)


def test_shared_neutral_positions_match_the_output_reference(model):
    skeleton = model.skeleton
    output = skeleton.somaskel77
    for index, name in enumerate(skeleton.bone_order_names):
        np.testing.assert_allclose(
            skeleton.neutral_joints[index].numpy(),
            output.neutral_joints[output.bone_index[name]].numpy(),
            atol=1e-6, rtol=0,
        )
