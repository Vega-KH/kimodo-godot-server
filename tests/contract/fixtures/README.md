# MMCP contract fixtures

Record sanitized upstream requests and responses here before changing adapter
behavior. Fixtures must not contain model tokens, absolute user paths, or
licensed model weights.

Each fixture set should identify:

- upstream server commit;
- MMCP SDK version or commit;
- Kimodo version or commit;
- request and response schema versions;
- whether the response was recorded or synthesized;
- the expected skeleton identity and joint count.

## Recorded sets

`pre_soma77_mmcp_1_0/` is a live loopback recording of the pinned Goal 1
runtime immediately before the service boundary changes from SOMA-30 to
SOMA-77. Its `metadata.json` pins every source revision and hashes every
payload. The generation response is self-contained glTF JSON with an embedded
binary buffer; it contains animation data, not model weights.

`soma77_mmcp_1_0/` is the corresponding live loopback recording after Goal 3.
It proves the intentionally changed 77-joint canonical/output boundary and six
expanded foot-contact channels. The pre-change set remains immutable.

## Compatibility intent

Preserve these behaviors across the upcoming boundary change:

- `GET /capabilities` and `POST /generate` route shapes;
- MMCP 1.0 version, coordinate system, units, and quaternion ordering;
- canonical-skeleton request validation;
- standard error envelopes;
- self-contained glTF 2.0 JSON and `MMCP_motion` metadata.

The following recorded fields are historical and are intentionally scheduled
to change in Goal 3:

- the advertised canonical skeleton has 30 joints;
- the glTF skin, nodes, and animation channels have 30 joints;
- only four foot-contact channels survive the inherited SOMA-77-to-SOMA-30
  response slice.

Do not rewrite this fixture set when Goal 3 lands. Record a new fixture set so
tests can distinguish deliberate protocol evolution from accidental drift.

## Recording the current boundary

From an authenticated environment with the pinned model already cached:

```powershell
$env:TEXT_ENCODER_MODE = "local"
$env:TEXT_ENCODER_DEVICE = "cpu"
Remove-Item Env:KIMODO_QUANTIZE -ErrorAction SilentlyContinue
python scripts/record_contract_fixtures.py
```

The recorder writes only the current `soma77_mmcp_1_0/` set. Review the diff
and run the contract tests offline before accepting it. Never point the script
at `pre_soma77_mmcp_1_0/`; that directory is historical evidence and immutable.
