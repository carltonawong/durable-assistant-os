# DAOS Mandatory Baseline

This file defines the minimum hardened DAOS install.

Use it when deciding what a quick install must write exactly, what the operator fills later, and what stays live/mutable after install.

## Purpose

A DAOS install should not depend on the model regenerating core memory doctrine correctly from prose every time.

The mandatory baseline exists to make the most important memory and continuity surfaces:
- exact
- reproducible
- hard to drift
- easy to audit

## The three artifact classes

### 1. Locked baseline files
These should be written literally by the installer as canonical payloads.

They define doctrine, lookup order, and memory-surface roles.

### 2. Fillable templates
These are structured files the installer/operator fills for the specific instance.

They should keep their structure stable, but their contents are expected to vary.

### 3. Live mutable surfaces
These are the files the running system updates during normal use.

They start from a canonical installed shape, but should not stay static.

## Mandatory baseline decision rule

A file belongs in the locked baseline when any of these are true:
- its wording defines the system's memory or trust behavior
- semantic drift would materially weaken reliability
- future installs should match near-exactly across environments
- the file is part of the minimum safety/continuity spine

A file belongs in fillable templates when:
- the structure should stay stable
- but the content is inherently user/org/instance-specific

A file belongs in live mutable surfaces when:
- its value comes from being rewritten as reality changes
- and freezing it would make the system less truthful

## Locked baseline files

The mandatory baseline should install these exact files:

### Local bootstrap
- `AGENTS.md`

### Durable wiki doctrine
- `wiki/WIKI.md`
- `wiki/cache/MEMORY-OPERATING-MODEL.md`
- `wiki/cache/HOT-CACHE-SPEC.md`

### Active-memory surface starters
- `wiki/cache/hot-cache.md`
- `wiki/cache/hot-cache-log.md`
- `wiki/cache/reset-handoff.md`
- `wiki/cache/agent-continuity.md`

### Durable wiki structure starters
- `wiki/index.md`
- `wiki/log.md`
- `wiki/raw/README.md`
- `wiki/sources/README.md`

## Fillable templates

These should ship in the starter pack but remain operator-filled:
- `assistant-charter.md`
- `operating-profile.md`
- `lane-snapshot.md`
- `cadence-review.md`

## Live mutable surfaces

These are mandatory runtime surfaces, but not fixed-content files:
- `wiki/cache/hot-cache.md`
- `wiki/cache/hot-cache-log.md`
- `wiki/cache/reset-handoff.md`
- `wiki/cache/agent-continuity.md`
- `wiki/raw/`
- `wiki/sources/`

`wiki/cache/reset-handoff.md` is the named public DAOS reset/wake-up continuity artifact.

Agent- or runtime-specific sidecars may still exist, but this file is the public baseline surface.

## Mandatory behavior baseline

A hardened DAOS install must also provide these behaviors:
- local thread/context first
- DAOS memory lookup order after local thread
- verified reality outranks remembered state for live facts
- durable capture when non-capture would create ambiguity later
- project checkpoint capture before active work changes future assumptions invisibly
- reset/wake-up continuity mechanism
- maintenance automation for ingest, compression, audits, and hygiene

## Project checkpoint baseline

During active project work, do not wait for final completion before preserving the operational decision layer.

Capture a durable checkpoint in the same pass when a step changes future assumptions about:
- infrastructure or hosting
- data ownership, database ownership, or routing
- provider/tool/account choice
- auth, secrets, keys, or protected surfaces
- deployment/runtime mode
- live-vs-dry-run behavior
- risk, money, or customer-impacting behavior
- operator-facing setup assumptions

A useful checkpoint records:
- what changed
- why it matters
- the source of truth or verification target
- what not to assume next time
- the next blocker or concrete step

Hot cache, current chat, and short logs may point to the checkpoint, but they should not be its only durable home.

## Mandatory maintenance baseline

At minimum, the installed system should have recurring automation for:
- raw ingest / durable promotion
- hot-cache freshness/spec audit
- agent-continuity freshness audit
- source hygiene
- hot-cache-log pruning as part of hygiene
- runtime re-verification of important claims
- reset/wake-up continuity verification

## Install stance

The DAOS installer should prefer:
- literal writes for locked baseline files
- structured fills for operator-owned templates
- explicit runtime ownership for mutable surfaces

Do not let core doctrine depend on free regeneration when exact installed payloads are possible.
