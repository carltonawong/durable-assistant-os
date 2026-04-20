# Durable Assistant OS

**Release discipline:** pre-1.0 semver with `CHANGELOG.md` as the source of truth for framework-facing changes.
**Current documented baseline:** `v0.1.1`; use `CHANGELOG.md` and `docs/releases/` for release notes.

Durable Assistant OS (DAOS) is a starter pack + toolkit for building assistants that stay useful over time instead of degrading into drift, clutter, and maintenance burden.

It gives you a structured assistant operating pack plus docs and scripts for keeping memory, trust, and upkeep from falling apart over time.

It is strongest today as:
- a methodology for durable assistant operation
- a tooling kit for generating, validating, updating, and porting that structure

It is **not** yet a full runtime integration layer by itself.

If you only try one thing in this repo, copy `starter-pack/`.

## If you're new, do this first

If you only try one thing here, copy `starter-pack/`.

1. Copy `starter-pack/` into your own workspace.
2. Fill `assistant-charter.md` and `operating-profile.md`.
3. Run `python scripts/daos_validate.py /path/to/my-daos-pack`.
4. Use `harness/first-week.md` once the baseline is live.

If you want the fuller walkthrough after that, read `docs/quickstart.md`.

## What you should have after one sitting

After the first setup, you should have:

- a clear definition of what your assistant is for
- explicit trust and approval boundaries
- a durable place for key working context
- a simple structure for keeping active work from drifting

Want to see what a filled pack looks like? Start with `examples/creative-studio-operating-profile-example.md`.

If this problem sounds familiar, start with `starter-pack/` and ignore the rest until you need it.

## Why DAOS exists

Most assistants do not fail at setup.
They fail once upkeep starts costing more than the help is worth.

Memory gets noisy, context drifts, trust drops, and the user ends up maintaining the assistant more than using it.

DAOS exists to reduce that degradation and make assistants more usable, trustworthy, and repairable over time.

## Who this is for

DAOS is most useful if you are:
- setting up one assistant for yourself
- configuring an assistant for another person or team
- building a repeatable assistant operating pack

## The simple mental model

DAOS tries to stop assistant memory and context from collapsing into one blurry pile.

It separates:
- **the local thread** — what is being asked right now
- **a hot front door** — the shortest shared summary of what matters now
- **durable wiki/docs memory** — what should survive and be shared
- **live reality** — the files, systems, and runtime state that must be checked before acting

![DAOS memory model](docs/assets/daos-memory-model.svg)

If you want the fuller explanation, read `docs/public-memory-page.md` first and `docs/memory.md` only after that.

## Optional companions

Useful, but not required before first value:

- **Obsidian** for browsing and editing the durable markdown memory surface  
  https://obsidian.md/download
- **Karpathy's LLM Wiki pattern** for the persistent-wiki mental model behind DAOS memory  
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Short version:
- Obsidian is the easiest way to inspect the wiki as a living graph of markdown pages.
- Karpathy's LLM Wiki pattern explains why DAOS prefers a maintained wiki over re-deriving knowledge from raw files every time.

## Try DAOS

Most people should use the default path below and ignore the alternates.

**Recommended default:** copy `starter-pack/` first.
It is the simplest way to understand DAOS and get a usable baseline quickly.

### Default path — Copy the ready-made pack
Best if you want the most literal first run.
1. Copy `starter-pack/` into your own workspace.
2. Open `starter-pack/README.md` and fill the files in that order.
3. Run `python scripts/daos_validate.py /path/to/my-daos-pack`.
4. Use `harness/first-week.md` once the baseline is live.

### Alternate path — Generate a new pack
Best if you want a clean generated scaffold.
1. Run `python scripts/daos_bootstrap.py /path/to/my-daos-pack`.
2. Fill the generated files.
3. Run `python scripts/daos_validate.py /path/to/my-daos-pack`.
4. Use `harness/first-week.md` once the baseline is live.

### Alternate path — Use the guided wizard
Best if you want the repo to walk you through setup.
1. Run `python scripts/daos_wizard.py /path/to/my-daos-pack`.
2. Review/fill anything still missing.
3. Run `python scripts/daos_validate.py /path/to/my-daos-pack`.
4. Use `harness/first-week.md` once the baseline is live.

Default path rule:
- operate from `starter-pack/` or a generated pack
- use `templates/` only when you are extending or reusing framework blanks

## What the repo gives you today

### Start here
- `docs/quickstart.md` — fastest path to first value
- `docs/public-memory-page.md` — the memory model in plain English
- `docs/adoption-path.md` — what to do after first install

### Core doctrine
- `docs/thesis.md` — why DAOS exists
- `docs/memory.md` — deeper memory doctrine
- `docs/trust.md` — behavior and trust posture
- `docs/setup.md` — setup philosophy
- `docs/lane-model.md` — lane framing

### Working surfaces
- `starter-pack/` — default copyable operating instance
- `templates/` — reusable source blanks
- `examples/` — worked examples, including non-Carlton-shaped profiles such as a creative studio
- `harness/core-setup.md` and `harness/first-week.md` — install + stabilization guidance

### Tooling
- `scripts/daos_bootstrap.py` — generate a blank or filled pack
- `scripts/daos_wizard.py` — interactive generated setup
- `scripts/daos_validate.py` — operability + lint/calibration checks
- `scripts/daos_update.py` — safe in-place pack inspection/apply
- `scripts/daos_portability.py` — wiki-first export/inspect/plan/apply for durable memory portability

## Suggested reading order

Use this lighter path instead of reading the whole repo front to back:
1. `docs/quickstart.md`
2. `docs/public-memory-page.md`
3. `docs/adoption-path.md`
4. `docs/thesis.md`
5. `docs/memory.md` only if you want the deeper doctrine
6. `docs/pack-schema.md` or `docs/portability.md` only if you need those mechanics

## One-line repo map

- `docs/` explain
- `harness/` guide real use
- `starter-pack/` is the default operating surface
- `templates/` are source blanks
- `examples/` demonstrate filled outcomes
- `scripts/` generate, validate, update, and port

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
