# Durable Assistant OS

Durable Assistant OS (DAOS) is a framework for building assistants that stay useful over time instead of degrading into clutter, drift, and unreliable memory.

## What DAOS is

DAOS is aimed at a simple problem: most assistants feel impressive once, then slowly get worse. Memory gets noisy, the wrong context takes the foreground, setup becomes heavy, and trust drops.

DAOS is the attempt to package a more durable model:
- clear memory boundaries
- lightweight but explicit behavior defaults
- progressive setup instead of giant intake
- reusable repo files that can be explained, installed, templated, and demonstrated

## If you want to try DAOS right now

Take the shortest path first:
1. `docs/quickstart.md`
2. `harness/core-setup.md`
3. `templates/assistant-charter-template.md`
4. `templates/operating-profile-template.md`

If one lane needs more structure, add:
- `templates/lane-snapshot-template.md`

When the initial setup is in place, maintain it with:
- `templates/cadence-review-template.md`

## Read this repo in this order

1. `docs/quickstart.md` — the shortest path to trying DAOS right away
2. `docs/thesis.md` — the product thesis and framing for why DAOS exists
3. `docs/public-memory-page.md` — the front-door public explanation of the DAOS memory model
4. `docs/memory.md` — the deeper reference layer for DAOS memory doctrine
5. `docs/trust.md` — the public trust and behavior model for ask-vs-act, approval, and verification posture
6. `docs/setup.md` — the public setup philosophy for progressive install and early usefulness
7. `docs/lane-model.md` — the public lane model for lightweight domain mapping and foreground control
8. `harness/core-setup.md` — the minimum viable install path
9. `templates/assistant-charter-template.md` — reusable blank charter for locking assistant behavior defaults early
10. `examples/assistant-charter-example.md` — worked example of a filled first-pass charter
11. `templates/operating-profile-template.md` — reusable fill-in structure for a first DAOS profile
12. `examples/first-pass-setup-output-example.md` — worked example of what one finished first sitting can produce
13. `templates/lane-snapshot-template.md` — reusable single-lane operating snapshot for higher-friction lanes
14. `examples/lane-snapshot-example.md` — worked example of a filled lane-specific snapshot
15. `templates/cadence-review-template.md` — reusable upkeep template for heartbeat, weekly, and monthly review
16. `examples/cadence-review-example.md` — worked example of a lightweight review/calibration pass
17. `examples/user-operating-profile-example.md` — worked example of what a filled profile can look like

## Current artifact map

### docs/
- `docs/quickstart.md` — fastest newcomer path to a first useful DAOS install
- `docs/thesis.md` — the repo's core claim, framing, and design stance
- `docs/public-memory-page.md` — the public-facing memory overview
- `docs/memory.md` — deeper DAOS memory doctrine and architecture notes
- `docs/trust.md` — the public trust and behavior model
- `docs/setup.md` — the public setup philosophy
- `docs/lane-model.md` — the public lane model

### harness/
- `harness/core-setup.md` — first runnable one-sitting setup flow for installing DAOS defaults

### templates/
- `templates/assistant-charter-template.md` — blank assistant-charter structure for locking behavior defaults early
- `templates/operating-profile-template.md` — blank operating-profile structure
- `templates/lane-snapshot-template.md` — blank lane-specific operating snapshot for higher-friction lanes
- `templates/cadence-review-template.md` — blank cadence/review structure for upkeep and recalibration

### examples/
- `examples/assistant-charter-example.md` — generic worked example of a filled first-pass charter
- `examples/first-pass-setup-output-example.md` — generic worked example of a minimum viable setup outcome after one sitting
- `examples/lane-snapshot-example.md` — generic worked example of a lane-specific snapshot for one live lane
- `examples/cadence-review-example.md` — generic worked example of a lightweight review/calibration pass
- `examples/user-operating-profile-example.md` — generic worked example showing what a filled profile can look like without becoming framework canon

## Document roles

A few files are intentionally close together but do different jobs:

- `docs/thesis.md` explains **why** DAOS exists
- `docs/quickstart.md` explains **how to try it quickly without reading everything first**
- `docs/public-memory-page.md` explains the memory model in the cleanest public-facing form
- `docs/memory.md` is the deeper doctrine/reference layer behind that public page
- `docs/trust.md` explains the public behavior and trust model
- `docs/setup.md` explains the public setup philosophy and progressive-install stance
- `docs/lane-model.md` explains the public lane model, including statuses, foreground, and pressure
- `harness/core-setup.md` explains **how to install** a minimum viable DAOS setup
- `templates/` provides reusable blank structures
- `examples/` demonstrates what a filled instance can look like, including both smaller setup artifacts and fuller profile outputs

Simple rule:
- `docs/` = explain
- `harness/` = install
- `templates/` = reuse
- `examples/` = demonstrate

## Current status

This repository is being seeded from locked DAOS doctrine already captured in the shared wiki.

Current first-pass packaging status:
- the core thesis exists
- the first quickstart path exists
- the public memory front door exists
- the deeper memory reference layer exists
- the public trust/behavior page exists
- the public setup philosophy page exists
- the public lane-model page exists
- the first installable harness flow exists
- the first reusable assistant charter template exists
- the first reusable assistant charter example exists
- the first reusable profile template exists
- the first first-sitting setup output example exists
- the first reusable lane snapshot template exists
- the first lane snapshot example exists
- the first cadence/review template exists
- the first cadence review example exists
- the first generic worked example exists

So the repo now has a usable first-pass stack across doctrine, installation, templates, and example material.

## Near-term direction

The current focus is not adding random files. It is:
- tightening the repo front door
- refining the first-pass install and template surfaces
- improving public-framework hygiene
- only then deciding the next highest-leverage deliverables

## Public-framework hygiene

This repo is still early, but it should increasingly behave like a framework others can inspect and adopt.

Baseline hygiene now present:
- Apache-2.0 license
- clear README front door
- contribution guidance
- security reporting guidance
- basic repository ownership/ignore files

## Commit checkpoints

Use commits at coherent checkpoints, not after every tiny edit.

Commit when all three are true:
- one repo-facing slice is coherent
- the public/private boundary for that slice is stable
- the change can be described with one clean commit message
