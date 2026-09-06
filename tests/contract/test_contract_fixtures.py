"""Offline validation for the recorded pre-SOMA-77 MMCP contract."""

from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
from motionmcp import GenerateRequest, ModelSpec

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "pre_soma77_mmcp_1_0"


def _load(name: str) -> Any:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


def _decode_accessor(document: dict[str, Any], index: int) -> np.ndarray:
    accessor = document["accessors"][index]
    assert accessor["componentType"] == 5126
    widths = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}
    width = widths[accessor["type"]]
    view = document["bufferViews"][accessor["bufferView"]]
    uri = document["buffers"][view.get("buffer", 0)]["uri"]
    prefix = "data:application/octet-stream;base64,"
    assert uri.startswith(prefix)
    raw = base64.b64decode(uri[len(prefix) :], validate=True)
    offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    return np.frombuffer(raw, dtype="<f4", count=accessor["count"] * width, offset=offset)


def test_metadata_identifies_immutable_sources_and_file_hashes():
    metadata = _load("metadata.json")
    assert metadata["fixture_schema_version"] == 1
    assert metadata["recording_method"] == "live_loopback"
    assert metadata["historical_boundary"] == "pre_soma77_mmcp_1_0"
    assert metadata["protocol"] == {
        "version": "1.0",
        "response_format": "gltf_2.0_json",
    }
    assert metadata["http"] == {
        "capabilities": {"status": 200, "content_type": "application/json"},
        "generate": {"status": 200, "content_type": "model/gltf+json"},
    }
    for commit in metadata["source_commits"].values():
        assert re.fullmatch(r"[0-9a-f]{40}", commit)
    assert re.fullmatch(r"[0-9a-f]{40}", metadata["model"]["revision"])

    for descriptor in metadata["files"].values():
        fixture = FIXTURE_DIR / descriptor["path"]
        assert fixture.is_file()
        assert hashlib.sha256(fixture.read_bytes()).hexdigest() == descriptor["sha256"]


def test_capabilities_fixture_matches_pre_soma77_boundary():
    capabilities = _load("capabilities.json")
    assert capabilities["protocol_version"] == "1.0"
    assert capabilities["rotation_format"] == "quaternion_xyzw"
    assert capabilities["coordinate_system"] == "right_handed_y_up"
    assert capabilities["units"] == "meters"
    assert capabilities["response_formats"] == ["gltf_2.0_json"]
    assert len(capabilities["models"]) == 1

    model = ModelSpec.model_validate(capabilities["models"][0])
    assert model.id == "kimodo-soma-rp"
    assert model.fps == 30.0
    assert len(model.canonical_skeleton.joints) == 30
    assert model.supports_retargeting is False
    assert model.predicted_contact_joints == [
        "LeftFoot",
        "LeftToeBase",
        "RightFoot",
        "RightToeBase",
    ]


def test_generation_request_and_gltf_response_are_structurally_valid():
    request = GenerateRequest.model_validate(_load("generate_request.json"))
    document = _load("generate_response.gltf")
    assert request.options is not None and request.options.seed == 1234
    assert request.total_frames == 30
    assert document["asset"] == {"version": "2.0", "generator": "motionmcp"}
    assert document["extensionsUsed"] == ["MMCP_motion"]
    assert len(document["nodes"]) == 30
    assert len(document["skins"][0]["joints"]) == 30
    assert len(document["animations"]) == 1
    channels = document["animations"][0]["channels"]
    assert len(channels) == 31
    assert sum(channel["target"]["path"] == "rotation" for channel in channels) == 30
    assert sum(channel["target"]["path"] == "translation" for channel in channels) == 1

    extension = document["extensions"]["MMCP_motion"]
    assert extension["version"] == "1.0"
    assert extension["model"] == "kimodo-soma-rp"
    assert extension["fps"] == 30.0
    assert extension["samples"][0]["num_frames"] == 30
    assert set(extension["samples"][0]["foot_contacts"]) == {
        "LeftFoot",
        "LeftToeBase",
        "RightFoot",
        "RightToeBase",
    }

    decoded = [_decode_accessor(document, index) for index in range(len(document["accessors"]))]
    assert sum(values.size for values in decoded) == 3720
    assert all(np.isfinite(values).all() for values in decoded)


def test_error_fixtures_use_standard_mmcp_envelopes():
    errors = _load("errors.json")
    assert {case["name"] for case in errors} == {
        "schema_validation",
        "version_unsupported",
        "unknown_model",
    }
    for case in errors:
        assert case["expected_status"] >= 400
        assert case["content_type"].startswith("application/json")
        error = case["response"]["error"]
        assert error["code"] == case["name"]
        assert isinstance(error["message"], str) and error["message"]
        assert isinstance(error["details"], dict)


def test_fixtures_contain_no_credentials_or_personal_absolute_paths():
    forbidden = (
        re.compile(r"[A-Za-z]:[\\/]"),
        re.compile(r"/(?:home|Users)/"),
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"(?:token|authorization|password)[\"']?\s*[:=]", re.IGNORECASE),
    )
    for fixture in FIXTURE_DIR.iterdir():
        if fixture.is_file():
            assert fixture.stat().st_size < 250_000, fixture.name
            text = fixture.read_text(encoding="utf-8")
            assert not any(pattern.search(text) for pattern in forbidden), fixture.name
