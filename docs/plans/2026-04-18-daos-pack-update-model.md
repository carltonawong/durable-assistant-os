# DAOS Pack Update Model Plan

## Goal

Define how DAOS should update long-lived user packs without overwriting the user's real operating setup as the framework evolves.

## Core stance

- DAOS packs are expected to diverge over time.
- The updater should treat that divergence as normal, not as damage.
- DAOS should update schema, managed metadata, and clearly framework-owned surfaces first.
- DAOS should avoid rewriting user-authored working files unless the change is narrowly defined and provably safe.
- Silent auto-sync is the wrong default for DAOS.

## Why this matters

DAOS is not a static starter kit.
It is meant to become a durable operating baseline for real users.

That means two truths have to coexist:
- the framework should keep improving
- each user's live pack should become more customized over time

An update model that assumes downstream packs stay close to repo templates will eventually break trust.

## Ownership model

Every file in a DAOS pack should eventually fall into one of four classes:

### 1. User-owned

These are the live operating files that should be treated as the user's.

Examples:
- `assistant-charter.md`
- `operating-profile.md`
- lane-specific notes
- review history
- any file carrying real user decisions or real operating context

Default rule:
- never overwrite automatically

### 2. Framework-owned

These are files the framework can refresh more freely because they are reference or support material rather than the user's live operating surface.

Examples:
- generated reference readmes
- optional framework reference docs copied into a pack
- helper files whose value is mostly upstream alignment

Default rule:
- safe to replace when tracked and unchanged locally

### 3. Mixed or migration-sensitive

These are files that start from framework structure but may accumulate user edits.

Examples:
- starter scaffolds that remain partly templated
- files where new required fields may be added later

Default rule:
- only apply additive, schema-aware changes
- otherwise generate a migration note instead of rewriting

### 4. Managed metadata

These are DAOS control files used for versioning, update planning, backups, and safe migration behavior.

Examples:
- `daos-pack.json`
- later `.daos/manifest.json`
- later `.daos/files.json`
- later `.daos/backups/`

Default rule:
- updater-owned

## Current substrate already in place

DAOS now has the minimum internal substrate needed to support an update model later:
- canonical pack schema
- `schema_version`
- schema-backed generation
- shared render/validate core
- machine-readable `daos-pack.json`

That is enough to begin designing a safe upgrade path.
It is not yet enough to perform user-safe upgrades.

## Version model

DAOS should keep two separate version concepts:

### Schema version

This answers:
- what pack shape does this installer/validator/updater expect?

Current example:
- `schema_version = 1`

### Framework version

This answers:
- what DAOS release generated or last upgraded this pack?

Examples:
- `0.1.0-alpha1`
- `0.1.0`
- `0.1.1`

Reason for the split:
- many framework changes should not require a schema bump
- schema changes should be explicit when pack compatibility changes

## Metadata model

The current `daos-pack.json` should stay the public machine-readable anchor.

Current top-level metadata includes:
- `schema_version`
- `framework_version`
- `pack_id`
- `pack_kind`
- `generator`

Later it should likely add lifecycle metadata such as:
- `created_at`
- `last_upgraded_at`

Later, DAOS should add a hidden control surface such as:

```text
.daos/
  manifest.json
  files.json
  backups/
  migrations/
```

Suggested roles:
- `manifest.json` = update state and version info
- `files.json` = ownership, source mapping, and hashes
- `backups/` = pre-migration snapshots
- `migrations/` = applied migration records

## File tracking model

For safe updates, DAOS should eventually track per-file metadata such as:
- path
- ownership class
- source template or generator
- installed hash
- current hash
- last updater version

This makes it possible to distinguish:
- unchanged framework-managed files
- user-edited files
- files that need manual review

Without that layer, the updater has no reliable way to know whether replacing a file is safe.

## Update behavior

The updater should be designed around three modes:

### 1. Check

Read the pack and report:
- current schema version
- current framework version
- missing metadata
- whether the pack looks upgradeable

No writes.

### 2. Plan

Show what would happen:
- metadata updates
- safe file refreshes
- additive migrations
- manual review items

Still no writes.

### 3. Apply

Perform only changes that satisfy the DAOS safety rules:
- backup first
- update metadata
- apply safe additive migrations
- never silently overwrite user-owned files
- write a migration report

### Current implemented scope

DAOS now ships a first narrow `apply` path in `scripts/daos_update.py`.

Current apply behavior:
- create or repair `daos-pack.json`
- add `framework_version` and `pack_id` when missing
- preserve existing metadata fields when possible
- write `.daos/manifest.json`
- write a migration record in `.daos/migrations/`
- backup any pre-existing `daos-pack.json` into `.daos/backups/`
- leave `assistant-charter.md` and `operating-profile.md` untouched

Current non-goals:
- no prose merging
- no operating-profile rewrites
- no auto-refresh of user-owned live files

## Migration rules

The updater should prefer a small number of migration classes:

### Safe automatic migrations

Examples:
- add missing metadata fields
- add a new manifest file
- add a new optional support file
- append a new missing required field to a known scaffold shape

### Review-required migrations

Examples:
- framework field meaning changed
- a mixed file was edited by the user
- two plausible migration targets exist
- a new default may conflict with current user intent

In these cases:
- do not rewrite automatically
- emit an upgrade note with exact suggested edits

### Never-silent migrations

Examples:
- destructive rewrites
- dropping or renaming user fields
- changing user-authored decisions in place
- replacing filled operating files wholesale

These should always require explicit human review.

## DAOS-specific migration stance

DAOS should version the pack shape, not try to keep every user's prose synchronized.

That means the primary unit of migration is:
- field structure
- metadata
- validation expectations
- support files

It is not:
- rewriting the user's actual charter language
- normalizing their lane notes back to framework defaults
- forcing downstream packs to match current examples

## Backup posture

Before any applied migration, DAOS should create a dated backup of the files it may touch.

Minimum acceptable behavior:
- snapshot touched files before write
- store backups inside a DAOS-controlled folder
- say exactly what was backed up

If safe merging is unclear, DAOS should leave the user's file untouched and write a sidecar migration note instead.

## Release and support posture

DAOS should not promise "everything always auto-updates cleanly."

A better public promise is:
- packs remain inspectable
- updates are opt-in
- safe updates are automated where possible
- risky changes are surfaced explicitly instead of hidden

Recommended release posture:
- patch releases = validator tweaks, docs, safe metadata updates
- minor releases = additive schema-safe capabilities
- major releases = intentional migration boundaries

## Minimum viable updater

The first serviceable DAOS updater should not try to be magical.

It should do only this:
- read manifest/version info
- detect missing or outdated schema metadata
- classify touched files
- back up before changes
- apply safe additive migrations only
- generate `UPGRADE-REPORT.md`

That is enough to create a trustworthy update story without pretending DAOS can solve arbitrary merge problems.

## Explicit non-goals

- no silent auto-update daemon
- no full bidirectional sync with upstream templates
- no rewriting user-authored prose to match the latest framework language
- no "smart" merge engine that hides ambiguity
- no treating personalized packs as if they should stay repo-identical

## Recommended implementation order

After the current schema/generator/wizard hardening work is stable, the update path should likely proceed in this order:

1. extend manifest/version data
2. add per-file ownership and hash tracking
3. add report-only update planning
4. add safe additive migrations
5. add manual migration-note generation
6. only later consider richer guided upgrade UX

## Working standard

A DAOS update path is good enough when:
- users can personalize their packs heavily without fearing upstream updates
- DAOS can still detect what version/schema the pack is on
- safe additive improvements are possible
- risky changes are surfaced clearly instead of hidden
- trust goes up rather than down after framework evolution
