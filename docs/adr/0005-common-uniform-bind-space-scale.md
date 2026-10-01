# 0005 — Common positive uniform bind-space scale

Status: accepted, 2026-10-01 (user-approved Goal 19 correction)

## Context

Godette's corrected Blender export has matching raw glTF bind/rest matrices,
but its scaled parent empty is normalized during Godot import. Imported
rest × inverse-bind products consequently retain a common scale of 1.078262.
Rejecting this as a changed reference pose is unnecessarily restrictive.

## Decision

Refine ADR 0004's compatibility comparison without changing its reference-pose
requirement. For each binding, calculate mesh-relative inverse × rest × bind.
Accept only a positive uniform scalar basis, zero positional discrepancy, and
one scalar shared across every binding of every skinned mesh. The existing
position tolerance remains; basis tolerance applies to the scalar-normalized
residual. Reject inconsistent scales, rotation, translation, reflection, shear
and anisotropy. Invalid/non-invertible mesh transforms receive a separate error.

Report the detected scalar in compatibility diagnostics. Do not normalize skin
resources, alter rests, rewrite imported models, or change retarget mathematics.
Selection, baking and production-library preflight use the same validator.
This is not support for arbitrary bind-shape transforms or alternate poses.

## Verification

Synthetic multi-mesh cases cover common scales 0.5, 1.0782628 and 2 with rotated,
translated and scaled scene nodes; exact skin preservation; inconsistent scales;
and common non-scalar negative cases. A scaled synthetic convention also goes
through baking and saved-library playback. Private Godette's corrected export
passes, while its original export and Mannequiny retain actionable rejection.
Private source-model hashes remain unchanged.
