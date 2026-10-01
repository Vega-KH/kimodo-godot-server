# 0004 — Matching bind/rest poses and generic partial profiles

Status: accepted, 2026-09-30 (Goal 19 user-approved scope)

## Context

Mannequiny's imported defaults differ materially from its skin bind reference.
This is not established to be malformed glTF. Supporting alternate saved
reference poses would introduce a second interpretation of every animation,
skin, extra branch and accepted-library track. The user agrees that this cost
is not warranted for regular-humanoid support now.

## Decision

- Require one deform skeleton and matching mesh skin bind/skeleton rest poses.
  Compare rest × inverse-bind against the mesh transform relative to the
  skeleton, accounting for intervening scene transforms. Allow numerical export
  rounding (basis-vector error ≤0.001; position error ≤max(0.0001,
  skeleton rest extent ×0.0001)). Check each binding of every skinned mesh.
- Fail safely with the affected mesh/bone, discrepancy, limitation and repair
  guidance. Do not substitute another reference, mutate source assets, or
  prescribe bone remapping for a bind/rest mismatch. Selection, baking and
  production-library preflight share this check.
- Rotation-only libraries cannot safely encode shear/reflection or arbitrary
  anisotropic bone scale. Reject those bone bases explicitly; allow positive
  uniform scale and small exporter rounding. This is separate from ordinary
  scene-node transforms and root-travel scaling.
- Profile schema 2 stores reviewed semantic mappings, intentional optional
  omissions, root/translation policies and explicit paired palm landmarks.
  Required anatomy: pelvis, head, major limb chains, hands/feet and at least
  one torso segment. Optional anatomy includes digits, eyes/jaw, neck,
  shoulders, toes and additional torso segments. Mapped subsets must preserve
  anatomical order and distinct targets.
- A hand and its mapped digits share one non-degenerate anatomical frame;
  insufficient geometry requires a helpful rejection, not invented bones or
  per-thumb roll offsets. Landmark names are profile data, not transfer branches.
- Traverse actual hierarchy rather than assuming parent-first bone numbers.
  Unmapped branches keep local rests, inherit animated ancestors and receive
  no tracks. Omitted intermediate roles do not discard mapped descendant motion.
- Upgrade certified schema-1 profiles in memory only for an exact skeleton
  signature, deriving their existing full-hand landmarks and recertifying.
  Save Profile is the only operation that rewrites the profile resource.

## Consequences

Synthetic convention/anatomy families and independent pose oracles define
generality. Jenny04 and Remy are private compatibility examples, Mannequiny a
rejection example. No private model is redistributed or selected by filename
inside production transfer code. Godette/control rigs remain Goal 20; an
alternate-reference-pose workflow is deferred until a concrete product need
justifies its compatibility cost. Existing session/archive data is preserved.
