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

Lowest-friction real start:
- copy `starter-pack/` into your own workspace and fill that first

First generated install step:
- `python scripts/daos_bootstrap.py /path/to/my-daos-pack`
- add `--filled-example` to generate from the filled starter-pack example instead

First interactive generated install step:
- `python scripts/daos_wizard.py /path/to/my-daos-pack`
- the wizard asks a compact first-pass question set and writes a filled starter pack

First readiness check:
- `python scripts/daos_validate.py /path/to/my-daos-pack`
- blank scaffolds are expected to fail until you fill the required fields

If one lane needs more structure, add:
- `templates/lane-snapshot-template.md`

When the initial setup is in place, maintain it with:
- `templates/cadence-review-template.md`

After first install, use:
- `harness/first-week.md`

## Read this repo in this order

1. `docs/quickstart.md` — the shortest path to trying DAOS right away
2. `docs/adoption-path.md` — the staged path from trying DAOS to deeper structure
3. `docs/thesis.md` — the product thesis and framing for why DAOS exists
4. `docs/public-memory-page.md` — the front-door public explanation of the DAOS memory model
5. `docs/memory.md` — the deeper reference layer for DAOS memory doctrine
6. `docs/trust.md` — the public trust and behavior model for ask-vs-act, approval, and verification posture
7. `docs/setup.md` — the public setup philosophy for progressive install and early usefulness
8. `docs/lane-model.md` — the public lane model for lightweight domain mapping and foreground control
9. `harness/core-setup.md` — the minimum viable install path
10. `harness/first-week.md` — the first-week stabilization guide after initial setup
11. `templates/assistant-charter-template.md` — reusable blank charter for locking assistant behavior defaults early
12. `examples/assistant-charter-example.md` — worked example of a filled first-pass charter
13. `templates/operating-profile-template.md` — reusable fill-in structure for a first DAOS profile
14. `examples/first-pass-setup-output-example.md` — worked example of what one finished first sitting can produce
15. `templates/lane-snapshot-template.md` — reusable single-lane operating snapshot for higher-friction lanes
16. `examples/lane-snapshot-example.md` — worked example of a filled lane-specific snapshot
17. `templates/cadence-review-template.md` — reusable upkeep template for heartbeat, weekly, and monthly review
18. `examples/cadence-review-example.md` — worked example of a lightweight review/calibration pass
19. `examples/setup-conversation-example.md` — worked example of what a first DAOS setup conversation can sound like
20. `examples/user-operating-profile-example.md` — worked example of what a filled profile can look like
21. `examples/starter-pack-example/` — worked folder-level example of a filled DAOS starter pack

## Current artifact map

### docs/
- `docs/quickstart.md` — fastest newcomer path to a first useful DAOS install
- `docs/adoption-path.md` — staged adoption map from first try through deeper structure decisions
- `docs/thesis.md` — the repo's core claim, framing, and design stance
- `docs/public-memory-page.md` — the public-facing memory overview
- `docs/memory.md` — deeper DAOS memory doctrine and architecture notes
- `docs/trust.md` — the public trust and behavior model
- `docs/setup.md` — the public setup philosophy
- `docs/lane-model.md` — the public lane model

### harness/
- `harness/core-setup.md` — first runnable one-sitting setup flow for installing DAOS defaults
- `harness/first-week.md` — post-setup stabilization guide for the first week of real use

### starter-pack/
- `starter-pack/README.md` — copyable scaffold for trying DAOS on a real instance quickly
- `starter-pack/assistant-charter.md` — ready-to-fill working charter
- `starter-pack/operating-profile.md` — ready-to-fill working profile
- `starter-pack/lane-snapshot.md` — optional ready-to-fill lane-specific working note
- `starter-pack/cadence-review.md` — later-use working review sheet

### scripts/
- `scripts/daos_bootstrap.py` — generate a DAOS working folder by copying the blank starter-pack or the filled example into a target path
- `scripts/daos_validate.py` — check whether a DAOS pack is minimally filled enough to operate
- `scripts/daos_wizard.py` — run a compact setup wizard and generate a filled DAOS starter pack

### tests/
- `tests/test_daos_bootstrap.py` — standard-library verification for the bootstrap generator script
- `tests/test_daos_validate.py` — standard-library verification for the DAOS pack validator
- `tests/test_daos_wizard.py` — standard-library verification for the interactive setup wizard

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
- `examples/setup-conversation-example.md` — generic worked example of the setup conversation shape itself
- `examples/user-operating-profile-example.md` — generic worked example showing what a filled profile can look like without becoming framework canon
- `examples/starter-pack-example/` — generic worked folder showing the copyable starter-pack in a filled state

## Document roles

A few files are intentionally close together but do different jobs:

- `docs/thesis.md` explains **why** DAOS exists
- `docs/quickstart.md` explains **how to try it quickly without reading everything first**
- `docs/adoption-path.md` explains **how DAOS should mature after first install and week-one use**
- `docs/public-memory-page.md` explains the memory model in the cleanest public-facing form
- `docs/memory.md` is the deeper doctrine/reference layer behind that public page
- `docs/trust.md` explains the public behavior and trust model
- `docs/setup.md` explains the public setup philosophy and progressive-install stance
- `docs/lane-model.md` explains the public lane model, including statuses, foreground, and pressure
- `harness/core-setup.md` explains **how to install** a minimum viable DAOS setup
- `harness/first-week.md` explains **how to keep the first install from drifting during real use**
- `starter-pack/` provides a copyable real-world working scaffold for first-time adopters
- `scripts/daos_bootstrap.py` provides the first runnable/generated DAOS install step
- `scripts/daos_validate.py` provides the first runnable readiness check for a filled DAOS pack
- `scripts/daos_wizard.py` provides the first interactive generated DAOS setup path
- `templates/` provides reusable blank structures
- `examples/` demonstrates what a filled instance or setup interaction can look like, including both smaller setup artifacts and fuller profile outputs

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
- the first starter-pack scaffold exists
- the first post-setup first-week guide exists
- the first staged adoption-path guide exists
- the first runnable bootstrap generator exists
- the first runnable pack validator exists
- the first interactive setup wizard exists
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
- the first setup conversation example exists
- the first filled starter-pack example exists
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
