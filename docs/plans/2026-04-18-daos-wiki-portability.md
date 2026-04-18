# DAOS Wiki-First Portability Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Define a portability layer that preserves DAOS durable memory across tools, agents, and machines without collapsing DAOS back into pack-folder sync.

**Architecture:** Treat portability as a bounded export/import of durable memory and pack metadata, not as a generic backup of every live file. Reuse the existing `daos-pack.json` and `.daos/` substrate as the machine-readable control layer, but make the wiki the canonical durable payload.

**Tech Stack:** Python CLI scripts in `scripts/`, markdown + JSON artifacts, existing DAOS schema/update substrate, unittest.

---

## What this plan is and is not

This is **not** a plan for broad pack-folder cloning, hidden sync daemons, or silent round-trip rewriting of user-owned files.

This **is** a plan for a narrow DAOS portability surface with three explicit payload classes:
1. **Durable canonical memory** — wiki pages / durable markdown that should survive platform changes
2. **Pack identity + compatibility metadata** — `daos-pack.json`, `.daos/manifest.json`, migration info
3. **Optional active-memory sidecars** — hot cache / continuity snapshots only when the user explicitly wants a handoff bundle

The portability layer should preserve DAOS's existing trust stance:
- durable truth is wiki-first
- active memory is lower-authority and more disposable
- imports must be inspectable
- user-owned live files are not silently rewritten

## Why this matters

Current DAOS already supports:
- schema-backed generation
- validation/lint
- safe update planning/apply
- a stable machine-readable manifest

That is enough to support a **disciplined portability layer**.

What is missing is a DAOS-native way to answer:
- what exactly should move when a user changes tools or machines?
- what part is durable truth versus temporary orientation?
- how can DAOS import a prior memory bundle without pretending it can safely merge everything?

## Recommended product stance

Portability should mean:
- **export durable memory cleanly**
- **re-hydrate a new DAOS install from that durable memory**
- optionally carry a thin active-memory handoff
- avoid exporting stack-specific noise by default

Public promise:
- your durable assistant memory can move
- your DAOS pack identity and compatibility metadata can move
- short-term context can be included deliberately, not accidentally
- imports are reviewable and trust-preserving

## Suggested payload model

A DAOS portability bundle should be a directory or archive with a small manifest, for example:

```text
portability-bundle/
  portability-manifest.json
  pack/
    daos-pack.json
    .daos/manifest.json
    .daos/migrations/
  durable/
    wiki/
      index.md
      pages/
      sources/
      log.md
  active/
    hot-cache.md
    agent-continuity.md
```

### Payload classes

#### 1. Required durable payload
Always include:
- durable wiki material explicitly marked canonical for the install
- `daos-pack.json`
- `.daos/manifest.json` if present

#### 2. Optional provenance payload
May include:
- `.daos/migrations/`
- selected review notes
- install metadata useful for inspection

#### 3. Optional active-memory payload
Off by default unless explicitly requested:
- hot cache
- agent continuity
- similar resumability surfaces

Rationale:
- active-memory files are helpful for handoff
- but they are not the durable heart of the system
- bundling them by default risks portability confusion and stale-state imports

## Import posture

Imports should be staged and inspectable.

Recommended modes:

### 1. `inspect`
Read a bundle and report:
- payload classes present
- durable pages count
- whether active-memory files are included
- pack identity / framework version / schema version
- obvious conflicts or missing anchors

No writes.

### 2. `plan`
Show what DAOS would do:
- restore pack metadata anchors
- copy durable wiki payload into a target durable-memory root
- optionally place active-memory files into a staging area
- generate review notes for ambiguous collisions

No writes.

### 3. `apply`
Only perform safe, bounded actions:
- write/update DAOS-managed metadata anchors
- copy durable wiki files into an explicit target root when path ownership is clear
- stage active-memory files separately unless the user explicitly opted into restoring them live
- emit an import report

## Conflict posture

### Durable wiki conflicts
Default rule:
- never silently overwrite an existing durable page with a different non-empty page
- instead write a review report or a staged collision directory

### Active-memory conflicts
Default rule:
- never auto-promote imported hot cache / continuity into live front-door state unless the user explicitly requests it
- stage them for review first

### Pack metadata conflicts
Default rule:
- if `pack_id` differs, treat as cross-install import and report clearly
- if `pack_id` matches, treat as same-pack portability/handoff and allow narrower metadata restoration

## Minimum viable implementation order

### Task 1: Write the doctrine/spec page

**Objective:** Lock the portability framing before writing code.

**Files:**
- Create: `docs/portability.md`
- Reference: `docs/public-memory-page.md`
- Reference: `docs/pack-schema.md`
- Reference: `docs/plans/2026-04-18-daos-pack-update-model.md`

**Implementation notes:**
Document:
- wiki-first portability definition
- payload classes
- inspect/plan/apply modes
- conflict posture
- non-goals

### Task 2: Add portability bundle schema docs

**Objective:** Define the machine-readable manifest for an exported bundle.

**Files:**
- Modify: `docs/pack-schema.md`
- Create: `docs/examples/portability-manifest-example.json` or `examples/portability-manifest-example.json`

**Implementation notes:**
Add a `portability-manifest.json` spec with fields such as:
- `bundle_version`
- `exported_at`
- `pack_id`
- `schema_version`
- `framework_version`
- `durable_payload`
- `active_payload`
- `source_root_kind`

### Task 3: Create failing export tests

**Objective:** Define the smallest trustworthy export behavior.

**Files:**
- Create/Modify: `tests/test_daos_portability.py`
- Reference: `tests/test_daos_update.py`

**First tests:**
- export builds a portability manifest
- export includes `daos-pack.json`
- export includes durable wiki files when a wiki root is provided
- export excludes active-memory files by default
- export can include active-memory files with an explicit flag

### Task 4: Implement `scripts/daos_portability.py export`

**Objective:** Ship a reportable exporter before import exists.

**Files:**
- Create: `scripts/daos_portability.py`

**Implementation notes:**
Support:
- `export --pack-dir ... --wiki-root ... --out ...`
- optional `--include-active-memory`
- explicit paths for active-memory files if included
- generated `portability-manifest.json`

Do not archive/compress yet unless it is trivial. A plain output directory is enough for v1.

### Task 5: Create failing inspect/plan import tests

**Objective:** Define safe read-only import behavior first.

**Files:**
- Modify: `tests/test_daos_portability.py`

**First tests:**
- inspect reports payload counts and pack metadata
- plan reports staged actions without writes
- plan warns on durable collision
- plan stages active-memory restore as review-only by default

### Task 6: Implement `inspect` and `plan`

**Objective:** Make bundle intake trustworthy before any write path exists.

**Files:**
- Modify: `scripts/daos_portability.py`

**Implementation notes:**
Produce plain-text reports mirroring `daos_update.py` style:
- bundle status
- payload summary
- conflicts
- proposed writes/staging actions

### Task 7: Create failing apply tests for safe import

**Objective:** Bound the write path tightly.

**Files:**
- Modify: `tests/test_daos_portability.py`

**First tests:**
- apply restores DAOS-managed metadata anchors when missing
- apply copies durable wiki files into an empty target root
- apply refuses to overwrite conflicting durable files silently
- apply stages active-memory payload separately by default
- apply writes an import report / migration record

### Task 8: Implement `apply`

**Objective:** Ship the narrow safe import path.

**Files:**
- Modify: `scripts/daos_portability.py`

**Implementation notes:**
Write only:
- DAOS-managed metadata anchors
- durable wiki files where no collision exists
- staged imports / review artifacts for ambiguous cases

Do not auto-merge markdown.
Do not auto-activate hot cache.
Do not silently reconcile conflicting canon.

### Task 9: Add README + quickstart coverage

**Objective:** Make the feature legible from the front door.

**Files:**
- Modify: `README.md`
- Modify: `docs/quickstart.md`

**Implementation notes:**
Explain when to use:
- `daos_update.py` = upgrade a pack in place
- `daos_portability.py` = move durable memory / pack identity across installs

### Task 10: Add end-to-end verification command examples

**Objective:** Make manual testing easy.

**Files:**
- Modify: `docs/portability.md`

**Example commands:**
- `python scripts/daos_portability.py export --pack-dir /tmp/pack --wiki-root /tmp/wiki --out /tmp/bundle`
- `python scripts/daos_portability.py inspect /tmp/bundle`
- `python scripts/daos_portability.py plan /tmp/bundle --target-wiki-root /tmp/new-wiki`
- `python scripts/daos_portability.py apply /tmp/bundle --target-wiki-root /tmp/new-wiki`

## Non-goals for v1

- no background sync
- no bidirectional reconciliation engine
- no hidden wiki/database abstraction layer
- no automatic merging of conflicting durable markdown
- no live hot-cache activation on import by default
- no stack-specific adapters yet

## Recommendation on priority

This is worth doing, but **after** the current additive-safe updater lane is committed and stable.

Reason:
- updater work is already in-flight in the working tree and now test-backed
- portability will benefit from a slightly more mature `.daos/` metadata layer
- DAOS can explain portability now, but it should not split focus before the current update posture is landed cleanly

## Success criteria

The portability layer is good enough when:
- DAOS can export durable wiki memory plus pack metadata in a bounded format
- a new install can inspect that bundle without writes
- safe import can restore non-conflicting durable memory and DAOS metadata
- active-memory handoff remains explicit and optional
- the feature strengthens DAOS's anti-lock-in story without weakening trust
