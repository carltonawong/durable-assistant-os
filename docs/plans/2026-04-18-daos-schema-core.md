# DAOS Schema Core Plan

## Goal

Define a canonical DAOS pack model so generation, validation, and future wizard/UI layers target one shared structure instead of re-encoding the pack ad hoc in each script.

## Canonical objects

- `DaosPack`
  - `schema_version`
  - `pack_kind`
  - `generator`
  - `assistant_charter`
  - `operating_profile`
- `AssistantCharter`
  - core outcome
  - failure mode
  - uncertainty defaults
  - proactive defaults
  - approval boundary
  - desired feel
- `OperatingProfile`
  - charter summary fields
  - top-level lanes
  - per-lane snapshots
  - reminder/planning defaults
  - memory/trust defaults
  - calibration fields
- `LaneSnapshot`
  - `name`
  - `status`
  - `foreground`
  - `pressure`
  - `short_note`

## File consequences

Generated packs should now have:
- `assistant-charter.md`
- `operating-profile.md`
- `daos-pack.json`
- supporting starter-pack files (`README.md`, `lane-snapshot.md`, `cadence-review.md`)

## Validation stance

- Markdown remains the human operating surface.
- `daos-pack.json` is the machine-readable anchor.
- Older manifestless packs can still validate, but generated packs should include the manifest.

## Why this shape

- It is enough to support generator, validator, and wizard alignment.
- It keeps lane data explicit.
- It gives future import/export or app layers something stable to target without forcing a full platform rewrite now.
