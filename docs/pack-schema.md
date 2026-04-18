# DAOS Pack Schema

## Why this page exists

DAOS now has a canonical pack model behind the generator, validator, and wizard.

The human operating surface is still markdown.
But generated packs now also include a machine-readable manifest:
- `daos-pack.json`

That manifest gives DAOS a stable substrate for:
- schema-backed generation
- validation
- richer wizard work later
- future import/export or app layers if they become warranted

## Current canonical objects

### `DaosPack`
Top-level generated pack object.

Fields:
- `schema_version`
- `pack_kind`
- `generator`
- `assistant_charter`
- `operating_profile`

### `AssistantCharter`
Locks the main behavioral defaults early.

Current field groups:
- primary outcome
- main help mode
- primary failure mode
- uncertainty defaults
- proactive defaults
- safety / approval defaults
- desired feel

### `OperatingProfile`
Carries the first-pass operating baseline.

Current field groups:
- charter summary fields
- top-level lane map
- per-lane snapshots
- reminder / planning defaults
- memory / trust defaults
- calibration-later fields

### `LaneSnapshot`
Current canonical lane object.

Fields:
- `name`
- `status`
- `foreground`
- `pressure`
- `short_note`

## Current file model

A generated pack currently centers on:
- `assistant-charter.md`
- `operating-profile.md`
- `daos-pack.json`

And usually includes these supporting files:
- `README.md`
- `lane-snapshot.md`
- `cadence-review.md`

## Compatibility note

DAOS still accepts older packs that do not yet have `daos-pack.json`.
Validation warns about that instead of hard-failing.

That keeps the current repo examples usable while moving generated packs onto a canonical schema path.

## Design stance

This is intentionally a small schema.
It is not trying to model everything.
It is trying to give DAOS one stable internal shape so the next product layers can build on something real.
