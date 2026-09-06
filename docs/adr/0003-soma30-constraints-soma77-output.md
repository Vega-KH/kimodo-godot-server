# ADR 0003: Keep SOMA-30 constraints behind a SOMA-77 MMCP boundary

- Status: Accepted
- Date: 2026-09-06

## Context

Kimodo-SOMA-RP-v1.1 operates on a 30-joint control skeleton but expands its
public result to a 77-joint presentation skeleton. The inherited MMCP adapter
advertised SOMA-30 and sliced the generated 77-joint rotations back to 30.
That discarded head-end, finger-chain, and toe-end motion before Godot could
decode or retarget it. It also exposed four internal foot-contact names even
though the expanded model result has six channels.

MMCP 1.0 exposes one canonical skeleton in model capabilities. A request must
send that canonical skeleton, while constraint translation is an adapter
implementation detail.

## Decision

Advertise the exact ordered SOMA-77 output skeleton as the MMCP canonical
skeleton and return all 77 generated rotations. Include explicit output joint
names and map the six expanded contact channels as:

1. `LeftFoot`
2. `LeftToeBase`
3. `LeftToeEnd`
4. `RightFoot`
5. `RightToeBase`
6. `RightToeEnd`

Continue translating constraints against `model.skeleton`, the internal
SOMA-30 rig. Constraint names must therefore belong to the 30-joint shared
subset. Validate skeleton names/hierarchy during setup and validate generated
joint count, dimensions, finite rotations/root translations, and contact
channel count before glTF encoding.

## Consequences

- The protocol version remains MMCP 1.0, but clients that cached the old
  30-joint canonical must refresh capabilities before generating.
- Godot and other clients receive Kimodo's complete presentation motion.
- Existing constraints targeting shared joints retain their meaning and are
  compiled into native SOMA-30 Kimodo constraint objects.
- Presentation-only joints cannot be constrained directly until a defined
  77-to-30 constraint projection is designed; requests naming them receive a
  structured `unknown_joint` error.
- Historical and current contract fixtures remain separate so the intentional
  boundary change cannot hide unrelated protocol drift.
