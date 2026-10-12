# SPDX-License-Identifier: Apache-2.0
"""Scene-guide requests must normalize positions and headings together."""

import json
from pathlib import Path

import numpy as np
from motionmcp import schemas

from motionmcp_kimodo.backbone import _normalize_origin, _unnormalize_output


def test_pose_and_root_path_heading_share_origin_rotation():
    payload = json.loads((Path(__file__).parent / "contract/fixtures/soma77_mmcp_1_0/generate_request.json").read_text())
    heading = 0.8
    payload["constraints"] = [
        {"type": "pose_keyframe", "frame": 0, "root_position": [2.0, 1.0, -3.0],
         "joint_rotations": {"Hips": [0.0, float(np.sin(heading / 2)), 0.0, float(np.cos(heading / 2))]}, "fill_mode": "rest"},
        {"type": "root_path", "frames": [0, 15], "positions_xz": [[2.0, -3.0], [3.0, -1.0]], "heading_radians": [heading, heading + 0.4]},
    ]
    request = schemas.GenerateRequest.model_validate(payload)
    original = request.model_dump(mode="json")
    normalized = request.model_copy(deep=True)
    origin = _normalize_origin(normalized, root_joint_name="Hips")
    assert origin is not None
    path = normalized.constraints[1]
    np.testing.assert_allclose(path.heading_radians, [0.0, 0.4], atol=1e-6)
    np.testing.assert_allclose(path.positions_xz[0], [0.0, 0.0], atol=1e-6)
    roots = np.array([[[p[0], 1.0, p[1]] for p in path.positions_xz]])
    rotations = np.tile(np.eye(3), (1, 2, 1, 1, 1))
    _, restored = _unnormalize_output(rotations, roots, 0, origin)
    np.testing.assert_allclose(restored[0, :, [0, 2]].T, original["constraints"][1]["positions_xz"], atol=1e-6)
    assert request.model_dump(mode="json") == original


def test_earlier_path_pin_takes_precedence_over_later_pose():
    payload = json.loads((Path(__file__).parent / "contract/fixtures/soma77_mmcp_1_0/generate_request.json").read_text())
    payload["constraints"] = [
        {"type": "pose_keyframe", "frame": 15, "root_position": [5.0, 1.0, -1.0],
         "joint_rotations": {"Hips": [0.0, 0.0, 0.0, 1.0]}, "fill_mode": "rest"},
        {"type": "root_path", "frames": [0, 15], "positions_xz": [[3.0, -2.0], [5.0, -1.0]], "heading_radians": [0.7, 0.9]},
    ]
    request = schemas.GenerateRequest.model_validate(payload)
    origin = _normalize_origin(request, root_joint_name="Hips")
    assert origin == {"ox": 3.0, "oz": -2.0, "heading": 0.7}
    np.testing.assert_allclose(request.constraints[1].positions_xz[0], [0.0, 0.0], atol=1e-6)
    np.testing.assert_allclose(request.constraints[1].heading_radians, [0.0, 0.2], atol=1e-6)
