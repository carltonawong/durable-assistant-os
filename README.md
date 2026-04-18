# Durable Assistant OS

Durable Assistant OS (DAOS) is a framework for building assistants that stay useful over time instead of degrading into clutter, drift, and unreliable memory.

## What DAOS is

DAOS is aimed at a simple problem: most assistants feel impressive once, then slowly get worse. Memory gets noisy, the wrong context takes the foreground, setup becomes heavy, and trust drops.

DAOS is the attempt to package a more durable model:
- clear memory boundaries
- lightweight but explicit behavior defaults
- progressive setup instead of giant intake
- reusable repo files that can be explained, installed, templated, and demonstrated

## Read this repo in this order

1. `docs/thesis.md` — the product thesis and framing for why DAOS exists
2. `docs/public-memory-page.md` — the front-door public explanation of the DAOS memory model
3. `docs/memory.md` — the deeper reference layer for DAOS memory doctrine
4. `harness/core-setup.md` — the minimum viable install path
5. `templates/assistant-charter-template.md` — reusable blank charter for locking assistant behavior defaults early
6. `templates/operating-profile-template.md` — reusable fill-in structure for a first DAOS profile
7. `templates/cadence-review-template.md` — reusable upkeep template for heartbeat, weekly, and monthly review
8. `examples/user-operating-profile-example.md` — worked example of what a filled profile can look like

## Current artifact map

### docs/
- `docs/thesis.md` — the repo's core claim, framing, and design stance
- `docs/public-memory-page.md` — the public-facing memory overview
- `docs/memory.md` — deeper DAOS memory doctrine and architecture notes

### harness/
- `harness/core-setup.md` — first runnable one-sitting setup flow for installing DAOS defaults

### templates/
- `templates/assistant-charter-template.md` — blank assistant-charter structure for locking behavior defaults early
- `templates/operating-profile-template.md` — blank operating-profile structure
- `templates/cadence-review-template.md` — blank cadence/review structure for upkeep and recalibration

### examples/
- `examples/user-operating-profile-example.md` — generic worked example showing what a filled profile can look like without becoming framework canon

## Document roles

A few files are intentionally close together but do different jobs:

- `docs/thesis.md` explains **why** DAOS exists
- `docs/public-memory-page.md` explains the memory model in the cleanest public-facing form
- `docs/memory.md` is the deeper doctrine/reference layer behind that public page
- `harness/core-setup.md` explains **how to install** a minimum viable DAOS setup
- `templates/` provides reusable blank structures
- `examples/` demonstrates what a filled instance can look like

Simple rule:
- `docs/` = explain
- `harness/` = install
- `templates/` = reuse
- `examples/` = demonstrate

## Current status

This repository is being seeded from locked DAOS doctrine already captured in the shared wiki.

Current first-pass packaging status:
- the core thesis exists
- the public memory front door exists
- the deeper memory reference layer exists
- the first installable harness flow exists
- the first reusable assistant charter template exists
- the first reusable profile template exists
- the first cadence/review template exists
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

Baseline hygiene targets:
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
