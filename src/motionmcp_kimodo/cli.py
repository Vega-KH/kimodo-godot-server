# SPDX-License-Identifier: Apache-2.0
"""``motionmcp-kimodo`` CLI entry point."""

from __future__ import annotations

import argparse
import os

from motionmcp import serve

from .backbone import KimodoBackbone


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="motionmcp-kimodo",
        description="Run an MMCP server backed by the Kimodo motion model. "
                    "Requires the canonical skeleton served at /capabilities.",
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--model",
        default=None,
        help="Kimodo model id (default: env KIMODO_MODEL, then kimodo.DEFAULT_MODEL)",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="torch device (default: cuda:0 if available, else cpu)",
    )
    parser.add_argument(
        "--text-encoder-mode",
        default=None,
        choices=["dummy", "local", "api", "auto"],
        metavar="MODE",
        help="Kimodo text encoder: local (default, LLM2Vec), dummy (no LLM), api, auto. "
             "Overrides TEXT_ENCODER_MODE when set; otherwise env or local.",
    )
    parser.add_argument(
        "--quantize",
        default=None,
        help="BitsAndBytes quant for the Kimodo text encoder when mode is local "
        "(4bit or 8bit). No effect with dummy.",
    )

    args = parser.parse_args()

    if args.quantize:
        os.environ["KIMODO_QUANTIZE"] = args.quantize.lower()

    serve(
        KimodoBackbone(
            model_id=args.model,
            device=args.device,
            text_encoder_mode=args.text_encoder_mode,
        ),
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    main()
