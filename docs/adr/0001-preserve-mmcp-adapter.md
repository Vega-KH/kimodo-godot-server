# ADR 0001: Preserve the MMCP adapter while adding Studio services

- Status: Accepted
- Date: 2026-09-04

## Context

The project starts from Animatica's `motionmcp-kimodo`, which already maps
MMCP prompts and constraints to Kimodo and encodes motion results. Godot needs
additional lifecycle, installation, job, provenance, and quality services.
Replacing the standard protocol would discard useful compatibility and make
upstream contribution harder.

## Decision

Retain the existing `motionmcp_kimodo` adapter and standard MMCP endpoints.
Build separately versioned `/studio/v1` services around that adapter. Keep the
legacy Python namespace and CLI alias until a deliberate migration removes
them. Default network binding is loopback-only.

The upstream SOMA-30 response slicing is explicitly transitional. The Studio
service boundary will expose and validate SOMA-77 output while translating
supported constraints to the model's internal skeleton.

## Consequences

- Existing MMCP clients remain a useful compatibility oracle.
- Studio-specific changes can evolve without silently changing MMCP behavior.
- Some temporary naming duplication is accepted during the refactor.
- Contract fixtures are required before changing the model output skeleton.
