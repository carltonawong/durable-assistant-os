# Durable Assistant OS

Durable Assistant OS (DAOS) is a framework for building assistants that stay useful over time instead of degrading into clutter, drift, and unreliable memory.

## What DAOS is

DAOS is aimed at a simple problem: most assistants feel impressive once, then slowly get worse. Memory gets noisy, the wrong context takes the foreground, setup becomes heavy, and trust drops.

DAOS is the attempt to package a more durable model:
- clear memory boundaries
- lightweight but explicit behavior defaults
- progressive setup instead of giant intake
- reusable repo files that can be explained, installed, templated, and demonstrated

## Try DAOS in the shortest possible path

1. Read `docs/quickstart.md`
2. Copy `starter-pack/` into your own workspace **or** run `python scripts/daos_bootstrap.py /path/to/my-daos-pack`
3. Fill the copied/generated pack
4. Run `python scripts/daos_validate.py /path/to/my-daos-pack`
5. Use `harness/first-week.md` once the baseline is live

Default path rule:
- operate from `starter-pack/` or a generated pack
- use `templates/` only when you are extending or reusing framework blanks

If you want the interactive path instead:
- run `python scripts/daos_wizard.py /path/to/my-daos-pack`

## What the repo gives you today

### Core doctrine
- `docs/thesis.md` — why DAOS exists
- `docs/quickstart.md` — fastest path to first value
- `docs/adoption-path.md` — how to mature a baseline after first use
- `docs/public-memory-page.md` and `docs/memory.md` — memory model
- `docs/trust.md`, `docs/setup.md`, `docs/lane-model.md` — behavior/setup/lane doctrine

### Working surfaces
- `starter-pack/` — default copyable operating instance
- `templates/` — reusable source blanks
- `examples/` — worked examples of filled artifacts and flows, including less Carlton-shaped profiles such as a creative-studio example
- `harness/core-setup.md` and `harness/first-week.md` — install + stabilization guidance

### Tooling
- `scripts/daos_bootstrap.py` — generate a blank or filled pack
- `scripts/daos_wizard.py` — interactive generated setup
- `scripts/daos_validate.py` — operability + lint/calibration checks
- `scripts/daos_update.py` — safe in-place pack inspection/apply
- `scripts/daos_portability.py` — wiki-first export/inspect/plan/apply for durable memory portability

## Read deeper only if you need it

Use this lighter reading path instead of a giant catalog:
1. `docs/quickstart.md`
2. `docs/adoption-path.md`
3. `docs/thesis.md`
4. `docs/public-memory-page.md`
5. `docs/pack-schema.md` or `docs/portability.md` only if you need those specific mechanics

## One-line repo map

- `docs/` explain
- `harness/` guide real use
- `starter-pack/` is the default operating surface
- `templates/` are source blanks
- `examples/` demonstrate filled outcomes
- `scripts/` generate, validate, update, and port

## Current status

DAOS is currently strongest as:
- a methodology for durable assistant operation
- a tooling kit for generating, validating, updating, and porting that structure

It is **not** yet a full runtime integration layer by itself.

## Near-term direction

Current focus:
- tighten the front door
- reduce doc sprawl
- make examples easier for outsiders to map onto their own work
- avoid expanding the control surface unless real usage proves the need

## Public-framework hygiene

Baseline hygiene present:
- Apache-2.0 license
- contribution guidance
- security reporting guidance
- basic ownership/ignore files

## Commit checkpoints

Use commits at coherent checkpoints, not after every tiny edit.

Commit when all three are true:
- one repo-facing slice is coherent
- the public/private boundary for that slice is stable
- the change can be described with one clean commit message
