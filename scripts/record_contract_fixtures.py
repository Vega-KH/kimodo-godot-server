"""Record the pre-SOMA-77 MMCP contract from a live loopback server."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

import httpx
import uvicorn

from motionmcp_kimodo import KimodoBackbone

FIXTURE_DIR = Path("tests/contract/fixtures/pre_soma77_mmcp_1_0")
PORT = 8766
SOURCE_COMMITS = {
    "motionmcp_sdk": "a298338bb3684a506ec313dce6d5cb12a6dc5167",
    "kimodo": "3362b92c37faa100fb697972f0fc5485dd94dd4f",
}
MODEL = {
    "repository": "nvidia/Kimodo-SOMA-RP-v1.1",
    "revision": "6c9233af1180b8151e3c4703477104af5dce9dd5",
}


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _request(capabilities: dict[str, Any]) -> dict[str, Any]:
    model = capabilities["models"][0]
    return {
        "protocol_version": capabilities["protocol_version"],
        "model": model["id"],
        "skeleton": model["canonical_skeleton"],
        "segments": [
            {
                "type": "text",
                "prompt": "A person walks forward naturally, then turns to the right.",
                "duration_frames": 30,
            }
        ],
        "constraints": [],
        "timing": {"fps": model["fps"]},
        "options": {
            "diffusion_steps": 5,
            "num_samples": 1,
            "seed": 1234,
            "post_processing": False,
            "transition_frames": 5,
        },
    }


def _error_case(
    client: httpx.Client,
    name: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    response = client.post("/generate", json=payload)
    if response.status_code < 400:
        raise AssertionError(f"{name} unexpectedly returned {response.status_code}")
    return {
        "name": name,
        "request": payload,
        "expected_status": response.status_code,
        "content_type": response.headers["content-type"],
        "response": response.json(),
    }


def main() -> None:
    if os.environ.get("TEXT_ENCODER_MODE") != "local":
        raise RuntimeError("TEXT_ENCODER_MODE must be local")
    if os.environ.get("TEXT_ENCODER_DEVICE") != "cpu":
        raise RuntimeError("TEXT_ENCODER_DEVICE must be cpu")
    if os.environ.get("KIMODO_QUANTIZE"):
        raise RuntimeError("KIMODO_QUANTIZE must be unset for this recording")

    backend = KimodoBackbone(device="cuda:0", text_encoder_mode="local")
    from motionmcp import build_app

    server = uvicorn.Server(
        uvicorn.Config(
            build_app(backend, title="MMCP contract fixture recorder"),
            host="127.0.0.1",
            port=PORT,
            log_level="warning",
        )
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 120
    while not server.started and thread.is_alive() and time.monotonic() < deadline:
        time.sleep(0.1)
    if not server.started:
        raise TimeoutError("MMCP server did not start within 120 seconds")

    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{PORT}", timeout=300) as client:
            capabilities_response = client.get("/capabilities")
            capabilities_response.raise_for_status()
            capabilities = capabilities_response.json()
            request = _request(capabilities)

            generation_response = client.post("/generate", json=request)
            generation_response.raise_for_status()
            generation = generation_response.json()

            missing_skeleton = {
                "protocol_version": request["protocol_version"],
                "model": request["model"],
            }
            future_version = {**request, "protocol_version": "99.0"}
            unknown_model = {**request, "model": "not-a-real-model"}
            errors = [
                _error_case(client, "schema_validation", missing_skeleton),
                _error_case(client, "version_unsupported", future_version),
                _error_case(client, "unknown_model", unknown_model),
            ]
    finally:
        server.should_exit = True
        thread.join(timeout=30)
        if thread.is_alive():
            raise TimeoutError("MMCP server did not stop within 30 seconds")

    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "capabilities": FIXTURE_DIR / "capabilities.json",
        "generate_request": FIXTURE_DIR / "generate_request.json",
        "generate_response": FIXTURE_DIR / "generate_response.gltf",
        "errors": FIXTURE_DIR / "errors.json",
    }
    _write_json(files["capabilities"], capabilities)
    _write_json(files["generate_request"], request)
    _write_json(files["generate_response"], generation)
    _write_json(files["errors"], errors)

    backend_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    metadata = {
        "fixture_schema_version": 1,
        "recorded_on": "2026-09-06",
        "recording_method": "live_loopback",
        "historical_boundary": "pre_soma77_mmcp_1_0",
        "source_commits": {"backend": backend_commit, **SOURCE_COMMITS},
        "model": MODEL,
        "protocol": {
            "version": capabilities["protocol_version"],
            "response_format": "gltf_2.0_json",
        },
        "http": {
            "capabilities": {
                "status": capabilities_response.status_code,
                "content_type": capabilities_response.headers["content-type"],
            },
            "generate": {
                "status": generation_response.status_code,
                "content_type": generation_response.headers["content-type"],
            },
        },
        "runtime": {
            "model_device": "cuda:0",
            "text_encoder_mode": "local",
            "text_encoder_device": "cpu",
            "quantization": None,
        },
        "generation": {
            "seed": request["options"]["seed"],
            "frames": request["segments"][0]["duration_frames"],
            "diffusion_steps": request["options"]["diffusion_steps"],
        },
        "files": {
            name: {"path": path.name, "sha256": _sha256(path)}
            for name, path in files.items()
        },
    }
    _write_json(FIXTURE_DIR / "metadata.json", metadata)
    print(f"Recorded {len(files) + 1} fixtures in {FIXTURE_DIR}")


if __name__ == "__main__":
    main()
