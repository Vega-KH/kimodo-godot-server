"""Goal 1 integration smoke test for the CPU-resident LLM2Vec encoder."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

import httpx
import numpy as np
import psutil
import torch
import uvicorn
from motionmcp import GenerateRequest, Options, TextSegment, Timing, build_app
from motionmcp.gltf import build_gltf
from motionmcp.protocol import PROTOCOL_VERSION

from motionmcp_kimodo import KimodoBackbone

PROMPT = "A person walks forward naturally, then turns to the right."
FRAMES = 30
SEED = 1234
STEPS = 5
PORT = 8765


class MemorySampler:
    def __init__(self) -> None:
        self.process = psutil.Process()
        self.peak_process_rss = 0
        self.peak_system_used = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._sample, daemon=True)

    def _sample(self) -> None:
        while not self._stop.wait(0.1):
            self.peak_process_rss = max(
                self.peak_process_rss, self.process.memory_info().rss
            )
            self.peak_system_used = max(
                self.peak_system_used, psutil.virtual_memory().used
            )

    def start(self) -> None:
        self._sample_once()
        self._thread.start()

    def _sample_once(self) -> None:
        self.peak_process_rss = max(
            self.peak_process_rss, self.process.memory_info().rss
        )
        self.peak_system_used = max(self.peak_system_used, psutil.virtual_memory().used)

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()
        self._sample_once()


def _validate_gltf(document: dict[str, Any]) -> dict[str, Any]:
    assert document["asset"]["version"] == "2.0"
    assert document["extensionsUsed"] == ["MMCP_motion"]
    extension = document["extensions"]["MMCP_motion"]
    assert extension["fps"] == 30.0
    assert extension["samples"][0]["num_frames"] == FRAMES
    assert len(document["animations"]) == 1

    uri = document["buffers"][0]["uri"]
    prefix = "data:application/octet-stream;base64,"
    assert uri.startswith(prefix)
    buffer = base64.b64decode(uri[len(prefix) :], validate=True)
    assert len(buffer) == document["buffers"][0]["byteLength"]

    widths = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}
    decoded_values = 0
    for accessor in document["accessors"]:
        assert accessor["componentType"] == 5126
        view = document["bufferViews"][accessor["bufferView"]]
        offset = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
        count = accessor["count"] * widths[accessor["type"]]
        values = np.frombuffer(buffer, dtype="<f4", count=count, offset=offset)
        assert values.size == count
        assert np.isfinite(values).all()
        decoded_values += values.size

    return {
        "nodes": len(document["nodes"]),
        "animations": len(document["animations"]),
        "accessors": len(document["accessors"]),
        "decoded_finite_float_values": decoded_values,
        "embedded_buffer_bytes": len(buffer),
        "fps": extension["fps"],
        "frames": extension["samples"][0]["num_frames"],
    }


def _document_hash(document: dict[str, Any]) -> str:
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    if os.environ.get("TEXT_ENCODER_MODE") != "local":
        raise RuntimeError("TEXT_ENCODER_MODE must be set to local")
    if os.environ.get("TEXT_ENCODER_DEVICE") != "cpu":
        raise RuntimeError("TEXT_ENCODER_DEVICE must be set to cpu")
    if os.environ.get("KIMODO_QUANTIZE"):
        raise RuntimeError("KIMODO_QUANTIZE must be unset for this full-encoder test")

    sampler = MemorySampler()
    sampler.start()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    evidence: dict[str, Any] = {
        "prompt": PROMPT,
        "frames": FRAMES,
        "seed": SEED,
        "diffusion_steps": STEPS,
        "text_encoder_mode": os.environ["TEXT_ENCODER_MODE"],
        "text_encoder_device_requested": os.environ["TEXT_ENCODER_DEVICE"],
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "torch_version": torch.__version__,
        "cuda_build": torch.version.cuda,
    }

    try:
        backbone = KimodoBackbone(device="cuda:0", text_encoder_mode="local")
        started = time.perf_counter()
        backbone.setup()
        evidence["cold_setup_seconds"] = time.perf_counter() - started

        text_encoder = backbone.model.text_encoder
        evidence["text_encoder_class"] = type(text_encoder).__name__
        evidence["text_encoder_device_observed"] = str(text_encoder.get_device())
        if text_encoder.get_device().type != "cpu":
            raise AssertionError(f"text encoder unexpectedly on {text_encoder.get_device()}")

        spec = backbone.capabilities()
        request = GenerateRequest(
            protocol_version=PROTOCOL_VERSION,
            model=spec.id,
            skeleton=spec.canonical_skeleton,
            segments=[
                TextSegment(type="text", prompt=PROMPT, duration_frames=FRAMES)
            ],
            constraints=[],
            timing=Timing(fps=spec.fps),
            options=Options(
                diffusion_steps=STEPS,
                num_samples=1,
                seed=SEED,
                post_processing=False,
            ),
        )

        started = time.perf_counter()
        result = asyncio.run(backbone.generate(request.model_copy(deep=True)))
        evidence["direct_generation_seconds"] = time.perf_counter() - started
        assert np.isfinite(result.rotations).all()
        assert np.isfinite(result.root_translations).all()
        direct_gltf = build_gltf(
            skeleton=request.skeleton.model_dump(mode="json"),
            joint_names=[joint.name for joint in request.skeleton.joints],
            rotations_quat=result.rotations,
            root_translations=result.root_translations,
            fps=spec.fps,
            model_id=spec.id,
            foot_contacts=result.foot_contacts or None,
        )
        evidence["direct_gltf"] = _validate_gltf(direct_gltf)
        evidence["direct_gltf_sha256"] = _document_hash(direct_gltf)

        # Reuse the loaded backbone in the real FastAPI/uvicorn stack. The lifespan
        # setup hook becomes a no-op so the 8B encoder is not loaded a second time.
        backbone.setup = lambda: None  # type: ignore[method-assign]
        app = build_app(backbone, title="Goal 1 full-encoder smoke")
        server = uvicorn.Server(
            uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="warning")
        )
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()
        deadline = time.monotonic() + 30
        while not server.started and time.monotonic() < deadline:
            time.sleep(0.05)
        if not server.started:
            raise TimeoutError("uvicorn did not start within 30 seconds")

        try:
            with httpx.Client(base_url=f"http://127.0.0.1:{PORT}", timeout=300) as client:
                capabilities = client.get("/capabilities")
                capabilities.raise_for_status()
                evidence["capabilities_status"] = capabilities.status_code
                evidence["capabilities_models"] = [
                    item["id"] for item in capabilities.json()["models"]
                ]

                started = time.perf_counter()
                response = client.post(
                    "/generate", json=request.model_dump(mode="json", exclude_none=True)
                )
                evidence["live_generation_seconds"] = time.perf_counter() - started
                response.raise_for_status()
                evidence["live_status"] = response.status_code
                evidence["live_content_type"] = response.headers["content-type"]
                live_gltf = response.json()
                evidence["live_gltf"] = _validate_gltf(live_gltf)
                evidence["live_gltf_sha256"] = _document_hash(live_gltf)
                evidence["direct_live_exact_match"] = (
                    evidence["direct_gltf_sha256"] == evidence["live_gltf_sha256"]
                )
        finally:
            server.should_exit = True
            server_thread.join(timeout=30)
            if server_thread.is_alive():
                raise TimeoutError("uvicorn did not stop within 30 seconds")

        evidence["text_encoder_device_after_generations"] = str(
            text_encoder.get_device()
        )
    finally:
        sampler.stop()
        evidence["peak_process_rss_bytes"] = sampler.peak_process_rss
        evidence["peak_system_used_bytes"] = sampler.peak_system_used
        evidence["total_system_memory_bytes"] = psutil.virtual_memory().total
        evidence["peak_cuda_allocated_bytes"] = (
            torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0
        )
        evidence["peak_cuda_reserved_bytes"] = (
            torch.cuda.max_memory_reserved() if torch.cuda.is_available() else 0
        )

        artifact = Path("artifacts/goal1/full_encoder_evidence.json")
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(evidence, indent=2), flush=True)


if __name__ == "__main__":
    main()
