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

1. `docs/public-memory-page.md` — public explanation of the DAOS memory model
2. `harness/core-setup.md` — minimum viable install path
3. `templates/operating-profile-template.md` — reusable fill-in structure
4. `examples/user-operating-profile-example.md` — worked example of what a filled profile can look like

## Current file set

- `docs/public-memory-page.md` — integration-ready public draft for the DAOS memory model
- `harness/core-setup.md` — first installable harness file for minimum viable DAOS setup
- `templates/operating-profile-template.md` — first reusable template for filling a minimum viable DAOS operating profile
- `examples/user-operating-profile-example.md` — first example file showing a filled operating profile without becoming framework canon

## Folder roles

- `docs/` — public-facing conceptual and explanatory documentation
- `harness/` — installable assistant setup material, onboarding flow, and operating surfaces
- `templates/` — reusable schemas, profile templates, checklists, and cadence templates
- `examples/` — clearly labeled example-instance material, including generic or instance-derived examples where useful

## Current status

This repository is being seeded from locked DAOS doctrine already captured in the shared wiki.

Current first-pass packaging status:
- `docs/` has its first public file
- `harness/` has its first install file
- `templates/` has its first reusable template
- `examples/` has its first generic worked example

So the repo now has one concrete file in each top-level layer.

## Near-term direction

The current focus is not adding more random files. It is tightening the front door, refining the first-pass files, and only then deciding the next highest-leverage repo deliverables.

## Commit checkpoints

Use commits at coherent checkpoints, not after every tiny edit.

Commit when all three are true:
- one repo-facing slice is coherent
- the public/private boundary for that slice is stable
- the change can be described with one clean commit message

Current recommended checkpoint:
- first-pass file set across `docs/`, `harness/`, `templates/`, and `examples/`
- generic/public-safe example naming
- README front-door refinement

Recommended commit message:
- `establish first-pass DAOS repo structure and generic starter files`
