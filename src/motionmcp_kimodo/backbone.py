# SPDX-License-Identifier: Apache-2.0
"""KimodoBackbone — wraps a Kimodo SOMA model in the MMCP protocol.

The request must use the model's canonical skeleton (the one served at
``/capabilities``).
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import torch

from kimodo import DEFAULT_MODEL, load_model
from motionmcp import (
    Backbone,
    GenerateRequest,
    ModelSpec,
    MotionResult,
    Skeleton,
)
from motionmcp.errors import ProtocolError
from motionmcp.gltf import matrices_to_quats
from motionmcp.schemas import (
    EffectorTargetConstraint,
    PoseKeyframeConstraint,
    RootPathConstraint,
)

from .skeleton import resolve_foot_contact_joints, skeleton_to_mmcp
from .translate import translate_request


class KimodoBackbone(Backbone):
    """Run a Kimodo SOMA model under the MMCP protocol.

    Parameters
    ----------
    model_id
        Kimodo model id (e.g. ``"soma30"``). Defaults to env
        ``KIMODO_MODEL`` if set, otherwise :data:`kimodo.DEFAULT_MODEL`.
    device
        Torch device (e.g. ``"cuda:0"``). Defaults to CUDA if available,
        otherwise CPU.
    text_encoder_mode
        Kimodo ``TEXT_ENCODER_MODE`` (``dummy``, ``local``, ``api``, ``auto``).
        When omitted, uses the env var if set, otherwise ``dummy``.
    """

    def __init__(
        self,
        model_id: str | None = None,
        device: str | None = None,
        text_encoder_mode: str | None = None,
    ) -> None:
        self.model_id = model_id or os.environ.get("KIMODO_MODEL", DEFAULT_MODEL)
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.text_encoder_mode = text_encoder_mode
        self.model: Any = None
        self._spec: ModelSpec | None = None
        self._slice_indices: np.ndarray | None = None

    # ----- lifecycle -------------------------------------------------------

    def setup(self) -> None:
        if self.text_encoder_mode is not None:
            os.environ["TEXT_ENCODER_MODE"] = self.text_encoder_mode.lower()
        else:
            os.environ.setdefault("TEXT_ENCODER_MODE", "dummy")
        print(
            f"[motionmcp-kimodo] loading {self.model_id} on {self.device} "
            f"(TEXT_ENCODER_MODE={os.environ['TEXT_ENCODER_MODE']})",
            flush=True,
        )
        self.model = load_model(self.model_id, device=self.device)

        input_skel = self.model.skeleton
        output_skel = getattr(self.model, "output_skeleton", input_skel)

        # Foot contacts are reported in the OUTPUT frame. Resolve against
        # the input joint list (what we serve as the canonical) so clients
        # only see joints they sent.
        contact_joints = resolve_foot_contact_joints(
            list(input_skel.bone_order_names)
        )

        self._spec = ModelSpec(
            id=self.model_id,
            fps=float(self.model.fps),
            canonical_skeleton=Skeleton.model_validate(skeleton_to_mmcp(input_skel)),
            supports_retargeting=False,
            supported_constraints=["root_path", "effector_target", "pose_keyframe"],
            predicted_contact_joints=contact_joints,
            native_clip_seconds=10.0,
            chunking="none",
            recommended_max_duration_seconds=12.0,
        )

        # Cache the slice indices used to project SOMA77 → SOMA30 (or
        # equivalent) on every request. None when input == output.
        if input_skel is not output_skel:
            output_names = list(output_skel.bone_order_names)
            input_names = list(input_skel.bone_order_names)
            self._slice_indices = np.array(
                [output_names.index(n) for n in input_names], dtype=np.int64,
            )
        else:
            self._slice_indices = None

        print(
            f"[motionmcp-kimodo] ready. fps={self.model.fps} "
            f"canonical_joints={len(input_skel.bone_order_names)}",
            flush=True,
        )

    # ----- protocol --------------------------------------------------------

    def capabilities(self) -> ModelSpec:
        if self._spec is None:
            raise ProtocolError(
                "model_unavailable",
                "model has not finished loading",
            )
        return self._spec

    async def generate(self, req: GenerateRequest) -> MotionResult:
        # Canonicalize the request so the earliest root pin sits at xz=(0,0)
        # facing +Z — Kimodo was trained on motions starting at world origin,
        # so non-canonical inputs degrade generation. The inverse transform
        # is reapplied to the model output below.
        skel = self.model.skeleton
        root_name = skel.bone_order_names[int(skel.root_idx)]
        hip_idx = getattr(skel, "hip_joint_idx", None)
        hip_names = (
            tuple(skel.bone_order_names[int(i)] for i in hip_idx) if hip_idx else None
        )
        origin_transform = _normalize_origin(
            req, root_joint_name=root_name, hip_joint_names=hip_names,
        )

        kwargs = translate_request(req, self.model, self.device)

        try:
            output = self.model(**kwargs)
        except torch.cuda.OutOfMemoryError as exc:
            raise ProtocolError(
                "resource_exhausted",
                "GPU out of memory; retry with a smaller request",
                details={"device": self.device, "reason": str(exc)},
            ) from exc
        except Exception as exc:
            raise ProtocolError(
                "internal_error",
                f"backbone raised {type(exc).__name__}: {exc}",
            ) from exc

        local_rot_mats = _to_numpy(output["local_rot_mats"])    # (B, T, J_out, 3, 3)
        root_positions = _to_numpy(output["root_positions"])    # (B, T, 3)

        # Un-canonicalize before slicing — the un-normalize indexes joints
        # in the OUTPUT-skeleton layout (root_idx is on the unsliced array).
        if origin_transform is not None:
            output_skel = getattr(self.model, "output_skeleton", skel)
            out_root_idx = int(getattr(output_skel, "root_idx", 0))
            local_rot_mats, root_positions = _unnormalize_output(
                local_rot_mats, root_positions, out_root_idx, origin_transform,
            )

        # Slice the wider output skeleton down to the input subset, so the
        # wire response uses only joints the client sent.
        if self._slice_indices is not None:
            local_rot_mats = np.take(local_rot_mats, self._slice_indices, axis=2)

        rotations_quat = matrices_to_quats(local_rot_mats)      # (B, T, J_in, 4)

        foot_contacts: dict[str, np.ndarray] = {}
        contact_joints = self._spec.predicted_contact_joints if self._spec else []
        if contact_joints and "foot_contacts" in output:
            contacts = _to_numpy(output["foot_contacts"]).astype(bool)
            for ch, name in enumerate(contact_joints):
                foot_contacts[name] = contacts[..., ch]

        return MotionResult(
            rotations=rotations_quat.astype(np.float32),
            root_translations=root_positions.astype(np.float32),
            foot_contacts=foot_contacts,
        )


def _to_numpy(x: Any) -> np.ndarray:
    if isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()
    return np.asarray(x)


# ---- Origin canonicalization ---------------------------------------------
#
# Kimodo's training distribution starts each motion at world origin facing
# +Z. Requests that pin the root somewhere else (or with a non-zero heading)
# fall outside that distribution and the model produces degraded motion. We
# work around it by translating + rotating every constraint into the
# canonical frame before generation, then inverting the transform on the
# output trajectory and root local rotation.


def _normalize_origin(
    body: GenerateRequest,
    *,
    root_joint_name: str,
    hip_joint_names: tuple[str, str] | None = None,
) -> dict[str, Any] | None:
    """Canonicalize the request so the earliest-frame root pin sits at
    ``(x=0, z=0)`` with heading=0 (character faces MMCP +Z). Mutates
    ``body.constraints`` in place. Returns ``{"ox","oz","heading"}``,
    or ``None`` when no root-pinning constraint was found.
    """
    anchor_frame: int | None = None
    ox = oz = 0.0
    heading = 0.0

    for c in body.constraints:
        if isinstance(c, PoseKeyframeConstraint):
            if c.root_position is not None and (anchor_frame is None or c.frame < anchor_frame):
                anchor_frame = c.frame
                ox = c.root_position[0]
                oz = c.root_position[2]

    if anchor_frame is None:
        for c in body.constraints:
            if isinstance(c, RootPathConstraint):
                for f, (x, z) in zip(c.frames, c.positions_xz):
                    if anchor_frame is None or f < anchor_frame:
                        anchor_frame, ox, oz = f, x, z

    if anchor_frame is None:
        return None

    earliest_pk: PoseKeyframeConstraint | None = None
    for c in body.constraints:
        if isinstance(c, PoseKeyframeConstraint) and root_joint_name in c.joint_rotations:
            if earliest_pk is None or c.frame < earliest_pk.frame:
                earliest_pk = c
    if earliest_pk is not None:
        x, y, z, w = earliest_pk.joint_rotations[root_joint_name]
        rest_by_name = {j.name: j.rest_translation for j in body.skeleton.joints}
        r_hip = hip_joint_names[0] if hip_joint_names else None
        l_hip = hip_joint_names[1] if hip_joint_names else None
        if r_hip in rest_by_name and l_hip in rest_by_name:
            r_off = np.asarray(rest_by_name[r_hip], dtype=np.float64)
            l_off = np.asarray(rest_by_name[l_hip], dtype=np.float64)
            hip_rest = r_off - l_off
            hip_world = _rotate_vec_xyzw(x, y, z, w, hip_rest)
            heading = float(np.arctan2(hip_world[2], -hip_world[0]))
        else:
            fx = 2.0 * (x * z + w * y)
            fz = 1.0 - 2.0 * (x * x + y * y)
            heading = float(np.arctan2(fx, fz))

    cos_t = float(np.cos(-heading))
    sin_t = float(np.sin(-heading))

    def rot_xz(x: float, z: float) -> tuple[float, float]:
        return (x * cos_t + z * sin_t, -x * sin_t + z * cos_t)

    half = -heading * 0.5
    qy = float(np.sin(half))
    qw = float(np.cos(half))
    q_inv_heading_xyzw = (0.0, qy, 0.0, qw)

    def qmul_xyzw(a, b):
        ax, ay, az, aw = a
        bx, by, bz, bw = b
        return (
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz,
        )

    for c in body.constraints:
        if isinstance(c, RootPathConstraint):
            new_xz: list[list[float]] = []
            for p in c.positions_xz:
                rx, rz = rot_xz(p[0] - ox, p[1] - oz)
                new_xz.append([rx, rz])
            c.positions_xz = new_xz
        elif isinstance(c, EffectorTargetConstraint):
            new_pos: list[list[float]] = []
            for p in c.positions:
                rx, rz = rot_xz(p[0] - ox, p[2] - oz)
                new_pos.append([rx, p[1], rz])
            c.positions = new_pos
        elif isinstance(c, PoseKeyframeConstraint):
            if c.root_position is not None:
                rx, rz = rot_xz(c.root_position[0] - ox, c.root_position[2] - oz)
                c.root_position = [rx, c.root_position[1], rz]
            if root_joint_name in c.joint_rotations:
                q_old = tuple(c.joint_rotations[root_joint_name])
                q_new = qmul_xyzw(q_inv_heading_xyzw, q_old)
                c.joint_rotations = {
                    **c.joint_rotations,
                    root_joint_name: [float(q_new[0]), float(q_new[1]),
                                      float(q_new[2]), float(q_new[3])],
                }
    return {"ox": float(ox), "oz": float(oz), "heading": heading}


def _unnormalize_output(
    local_rot_mats: np.ndarray,
    root_positions: np.ndarray,
    root_idx: int,
    norm: dict[str, float],
) -> tuple[np.ndarray, np.ndarray]:
    """Inverse of :func:`_normalize_origin`: rotate root traj + root local
    rot by ``+heading``, translate xz by ``(ox, oz)``."""
    heading = float(norm["heading"])
    ox = float(norm["ox"])
    oz = float(norm["oz"])

    cos_t, sin_t = float(np.cos(heading)), float(np.sin(heading))
    R_y = np.array([
        [cos_t,  0.0, sin_t],
        [0.0,    1.0, 0.0  ],
        [-sin_t, 0.0, cos_t],
    ], dtype=root_positions.dtype)

    root_positions = root_positions.copy()
    x_old = root_positions[..., 0].copy()
    z_old = root_positions[..., 2].copy()
    root_positions[..., 0] = x_old * cos_t + z_old * sin_t + ox
    root_positions[..., 2] = -x_old * sin_t + z_old * cos_t + oz

    local_rot_mats = local_rot_mats.copy()
    local_rot_mats[..., root_idx, :, :] = R_y @ local_rot_mats[..., root_idx, :, :]
    return local_rot_mats, root_positions


def _rotate_vec_xyzw(x: float, y: float, z: float, w: float, v: np.ndarray) -> np.ndarray:
    """Apply an xyzw quaternion to a 3-vector via Rodrigues' formula."""
    qv = np.array([float(x), float(y), float(z)], dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    cross1 = np.cross(qv, v)
    cross2 = np.cross(qv, cross1)
    return v + 2.0 * (float(w) * cross1 + cross2)
