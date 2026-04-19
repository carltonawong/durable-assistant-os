# Durable Assistant OS

Durable Assistant OS (DAOS) is a framework for building assistants that stay useful over time instead of degrading into clutter, drift, and unreliable memory.

## Why DAOS was created

Most assistants do not fail at setup.
They fail after they start being used.

At first, they seem useful. Then memory gets noisy, context drifts, trust drops, and the system becomes harder to operate. Over time, the user can end up spending more energy fixing the assistant than benefiting from it.

Worse, those fixes often happen outside the assistant’s own runtime. One tool runs the system. Another tool repairs it. Continuity depends on manual rescue instead of a durable operating model.

DAOS was created to solve that problem.

It is built to help assistants:
- resist drift, clutter, and stale memory
- stay useful under repeated real-world use
- remain portable across tools, sessions, and agent swaps
- get easier to operate as they mature, not harder

The goal is not maximum complexity.
The goal is an assistant that stays usable, trustworthy, and repairable over time.

## What DAOS is

DAOS gives you a structured assistant operating pack plus docs and scripts for keeping memory, trust, and upkeep from degrading over time.

DAOS is currently strongest as:
- a methodology for durable assistant operation
- a tooling kit for generating, validating, updating, and porting that structure

It is **not** yet a full runtime integration layer by itself.

Think of DAOS as a way to structure memory and operating behavior, plus scripts/templates to help you instantiate that structure.

## If you're new, do this first

Most users should start here instead of reading the whole repo:

1. Copy `starter-pack/` into your own workspace.
2. Fill `assistant-charter.md` and `operating-profile.md` first.
3. Run `python scripts/daos_validate.py /path/to/my-daos-pack`.
4. Use `harness/first-week.md` once the baseline is live.

If you want the fuller first-run walkthrough, go next to `docs/quickstart.md`.

## Who this is for

DAOS is most useful if you are:
- setting up one assistant for yourself
- configuring an assistant for another person or team
- building a repeatable assistant operating pack

If that sounds like you, use the quick-start block above first, then `docs/quickstart.md` if you want the fuller walkthrough.

## The simple mental model

DAOS tries to keep assistant memory from collapsing into one blurry pile.

It separates:
- **the local thread** — what is being asked right now
- **a hot front door** — the shortest shared summary of what matters now
- **durable wiki/docs memory** — what should survive and be shared
- **live reality** — the files, systems, and runtime state that must be checked before acting

![DAOS memory model](docs/assets/daos-memory-model.svg)

If you want the fuller explanation, read `docs/public-memory-page.md` first and `docs/memory.md` only after that.

## Recommended companions

DAOS is easier to operate the intended way if you use these alongside it:

- **Obsidian** for browsing and editing the durable markdown memory surface  
  https://obsidian.md/download
- **Karpathy's LLM Wiki pattern** for the persistent-wiki mental model behind DAOS memory  
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Short version:
- Obsidian is the easiest way to inspect the wiki as a living graph of markdown pages.
- Karpathy's LLM Wiki pattern explains why DAOS prefers a maintained wiki over re-deriving knowledge from raw files every time.

## Try DAOS in the shortest possible path

You do not need all three options below.
Most people should use the default path and ignore the alternates.

**Recommended default:** copy `starter-pack/` first.
It is the simplest path and the best place to understand DAOS before using bootstrap or the wizard.

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

## What you should have after the first setup

After one sitting, you should have:
- a clear definition of what your assistant is for
- explicit trust and approval boundaries
- a durable place for key working context
- a simple structure for keeping active work from drifting

If you want the interactive path instead:
- run `python scripts/daos_wizard.py /path/to/my-daos-pack`

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
