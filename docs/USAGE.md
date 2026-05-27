# Usage

Running the `motionmcp-kimodo` MMCP server after [installation](INSTALL.md).

[← Documentation index](README.md)

## Start the server

```bash
# Defaults: port 8000, default Kimodo model, cuda:0 if available else cpu.
motionmcp-kimodo

# Pick a model and bind explicitly:
motionmcp-kimodo --model soma30 --port 8000 --device cuda:0

# Or run as a module:
python -m motionmcp_kimodo --model soma30
```

Leave the terminal open while clients (e.g. Proscenium) connect. Default URL for local Blender: `http://localhost:8000`.

## CLI flags

| Flag | Default | Description |
|---|---|---|
| `--host` | `0.0.0.0` | Bind address |
| `--port` | `8000` | Listen port |
| `--model` | env / Kimodo default | Kimodo model id (e.g. `soma30`) |
| `--device` | `cuda:0` or `cpu` | PyTorch device |
| `--text-encoder-mode` | `dummy` (or env) | Kimodo text encoder: `dummy`, `local`, `api`, `auto` |
| `--quantize` | — | `4bit` or `8bit` for Kimodo’s local text encoder only (see below) |

## Environment variables

| Variable | Effect |
|---|---|
| `KIMODO_MODEL` | Default model id when `--model` isn’t passed |
| `TEXT_ENCODER_MODE` | Same as `--text-encoder-mode` when the flag is omitted |
| `KIMODO_QUANTIZE` | With local LLM encoder: `4bit` or `8bit` (BitsAndBytes). Set by `--quantize` or manually. Ignored with `dummy`. |

### Text encoder and `--quantize`

The server defaults to `--text-encoder-mode dummy` (no LLM loaded). `--quantize` only applies with `local`.

Local LLM with 4-bit quantization:

```bash
motionmcp-kimodo --text-encoder-mode local --quantize 4bit
```

`--text-encoder-mode` overrides `TEXT_ENCODER_MODE` when passed. If you omit the flag, an existing env var is used; otherwise Kimodo runs in `dummy` mode.

`--quantize` does **not** affect motion/diffusion weights — only the text encoder when Kimodo loads `LLM2VecEncoder`.

## Clients and wire format

Clients pull the model’s canonical skeleton from `GET /capabilities` and send it verbatim in `POST /generate`. The wire format is documented in the [MMCP docs](https://animatica.ai/mmcp).

The officially supported client is **[Proscenium for Blender](https://github.com/animatica-ai/proscenium-blender)** — see [Installation](INSTALL.md) for setup.
