# DAOS Pack Schema

## Why this page exists

DAOS now has a canonical pack model behind the generator, validator, and wizard.

The human operating surface is still markdown.
But generated packs now also include a machine-readable manifest:
- `daos-pack.json`

That manifest gives DAOS a stable substrate for:
- schema-backed generation
- validation
- lint / calibration diagnostics
- safe update inspection/planning
- wiki-first portability bundles
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

Important note:
- `LaneSnapshot.status` is the operating condition of the lane inside the structured pack model.
- It is not the same thing as wiki-page `Status`, which DAOS uses for the lifecycle of a durable page/document.

## Current file model

A generated pack currently centers on:
- `assistant-charter.md`
- `operating-profile.md`
- `daos-pack.json`

A hardened starter pack also includes a locked baseline doctrine spine:
- `AGENTS.md`
- `wiki/WIKI.md`
- `wiki/cache/MEMORY-OPERATING-MODEL.md`
- `wiki/cache/HOT-CACHE-SPEC.md`
- `wiki/cache/hot-cache.md`
- `wiki/cache/hot-cache-log.md`
- `wiki/cache/reset-handoff.md`
- `wiki/cache/agent-continuity.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/raw/README.md`
- `wiki/sources/README.md`

The manifest currently includes:
- `schema_version`
- `framework_version` (the current framework release baseline, for example `v0.1.6`)
- `pack_id`
- `pack_kind`
- `generator`
- structured assistant/profile data

And usually includes these supporting files:
- `README.md`
- `lane-snapshot.md`
- `cadence-review.md`

Related doctrine page:
- `docs/reset-handoff.md` explains the public contract for `wiki/cache/reset-handoff.md`.

## Compatibility note

DAOS still accepts older packs that do not yet have `daos-pack.json`.
Validation warns about that instead of hard-failing.

That keeps the current repo examples usable while moving generated packs onto a canonical schema path.

## Validation posture

DAOS validation now does two things:
- **errors** for missing or unfilled structure that makes the pack not minimally operable
- **warnings** for calibration/lint smells that suggest the pack may still be fragile in real use

Current warning examples include:
- duplicate lane names
- lane snapshots that are missing from the top-level lane map
- overloaded foreground sets (more than 3 foreground lanes)
- memory front doors that skip the usual thread/cache/continuity staging

## Design stance

This is intentionally a small schema.
It is not trying to model everything.
It is trying to give DAOS one stable internal shape so the next product layers can build on something real.
