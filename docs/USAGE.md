# Usage

Running the `kimodo-godot-server` MMCP server after [installation](INSTALL.md).

[← Documentation index](README.md)

## Start the server

For the verified Windows checkout, use root `start.bat`. It sets
`TEXT_ENCODER_DEVICE=cpu` and local text encoding, leaving motion inference on
the automatically selected device (CUDA on the reference machine). Wait for
the ready message before connecting the Godot dock to `http://127.0.0.1:8000`.

```bash
# Defaults: port 8000, default Kimodo model, cuda:0 if available else cpu.
kimodo-godot-server

# Pick a model and bind explicitly:
kimodo-godot-server --model soma30 --port 8000 --device cuda:0

# Or run as a module:
python -m motionmcp_kimodo --model soma30
```

Leave the terminal open while Godot connects. Use one server process; multiple
GPU model workers are not validated. Remote deployment is outside Stage 1 support.

## CLI flags

| Flag | Default | Description |
|---|---|---|
| `--host` | `127.0.0.1` | Bind address; remote binding is explicit |
| `--port` | `8000` | Listen port |
| `--model` | env / Kimodo default | Kimodo model id (e.g. `soma30`) |
| `--device` | `cuda:0` or `cpu` | PyTorch device |
| `--text-encoder-mode` | `local` (or env) | Kimodo text encoder: `local`, `dummy`, `api`, `auto` |
| `--quantize` | — | `4bit` or `8bit` when using the local LLM encoder (see below) |

## Environment variables

| Variable | Effect |
|---|---|
| `KIMODO_MODEL` | Default model id when `--model` isn’t passed |
| `TEXT_ENCODER_MODE` | Same as `--text-encoder-mode` when the flag is omitted |
| `TEXT_ENCODER_DEVICE` | Kimodo text-encoder device; reference launcher sets `cpu` |
| `KIMODO_QUANTIZE` | With local LLM encoder: `4bit` or `8bit` (BitsAndBytes). Set by `--quantize` or manually. Ignored with `dummy`. |

### Text encoder and `--quantize`

The server defaults to **`local`** (loads Kimodo’s LLM2Vec text encoder). Use `--text-encoder-mode dummy` for constraint-only runs without an LLM (lower VRAM, no text semantics).

Optional upstream 4-bit text-encoder mode (not the validated CPU-encoder baseline):

```bash
kimodo-godot-server --quantize 4bit
```

`--text-encoder-mode` overrides `TEXT_ENCODER_MODE` when passed. If you omit the flag, an existing env var is used; otherwise the server uses `local`.

`--quantize` does **not** affect motion/diffusion weights — only the text encoder when Kimodo loads `LLM2VecEncoder`.

## Clients and wire format

Clients pull the model’s canonical skeleton from `GET /capabilities` and send it verbatim in `POST /generate`. The wire format is documented in the [MMCP docs](https://animatica.ai/mmcp).

For `kimodo-soma-rp`, the canonical wire skeleton is the 77-joint SOMA
presentation rig and generated glTF contains rotations in that exact order.
Kimodo still evaluates constraints on its internal SOMA-30 control rig.
Therefore, constraint joint names are currently limited to the 30 names shared
by both rigs; presentation-only finger segments, `HeadEnd`, and toe-end joints
cannot yet be targeted directly. The capability response advertises six contact
channels in generated order: left foot/toe/toe-end, then right
foot/toe/toe-end.

This fork's validated client is [Kimodo Motion Studio for Godot](https://github.com/Vega-KH/godot-kimodo).
Backend constraint support does not mean the Stage 1 dock exposes advanced pose/path
authoring; that is Stage 2 work. Proscenium is a separate upstream Blender client.
