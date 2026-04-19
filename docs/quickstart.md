# DAOS Quickstart

## Who this is for

This page is for assistant operators/builders who want a first usable DAOS pack without reading the whole repo first.

The operator fills the pack.
The assistant later uses it.

This is not the full doctrine path.
It is the shortest path to a first useful setup.

## Quick translation of DAOS terms

- **assistant charter** — what this assistant is for and how it should behave
- **operating profile** — your working context, priorities, and support preferences
- **lane snapshot** — the current state of one workstream
- **cadence review** — a recurring cleanup and calibration pass

## Recommended companions first

DAOS works best when your durable memory actually lives in readable markdown surfaces.
Before you start, install or review:

- **Obsidian** — best operator-facing way to browse/edit the markdown memory surface  
  https://obsidian.md/download
- **Karpathy's LLM Wiki pattern** — the clearest public explanation of the persistent-wiki model DAOS is leaning toward  
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

You do not need to master both before trying DAOS.
But DAOS will make more sense if you understand that the durable memory target is a maintained markdown wiki, not just chat residue.

## The 15-minute path

## Step 1 — Start with the default path

**Recommended default:** copy `starter-pack/` first.
It is the simplest path and the best place to understand DAOS before using bootstrap or the wizard.

### Default path — Copy `starter-pack/`
Best if you want the most literal first run.
- copy `starter-pack/` into your own workspace
- open `starter-pack/README.md`
- fill the files in that order

### Alternate path — Generate a new pack
Best if you want a clean scaffold.
- run `python scripts/daos_bootstrap.py /path/to/my-daos-pack`
- fill the generated files

### Alternate path — Use the guided wizard
Best if you want interactive setup.
- run `python scripts/daos_wizard.py /path/to/my-daos-pack`
- review/fill anything still missing

## Step 2 — Know what you are creating

A first DAOS install should leave you with:
- a filled assistant charter
- a filled operating profile
- optional lane/continuity notes only where they help
- a durable markdown memory surface the assistant can later use

## What you should have after the first setup

After one sitting, you should have:
- a clear definition of what your assistant is for
- explicit trust and approval boundaries
- a durable place for key working context
- a simple structure for keeping active work from drifting

## Step 3 — Fill the baseline in order

For the default path, use this order:
1. Read `docs/setup.md`
2. Read `docs/public-memory-page.md`
3. Run `harness/core-setup.md`
4. Fill `assistant-charter.md`
5. Fill `operating-profile.md`
6. Fill `lane-snapshot.md` only if one lane needs more structure
7. Save `cadence-review.md` for later upkeep, not first install

## Step 4 — Validate and use it

- run `python scripts/daos_validate.py /path/to/my-daos-pack`
- then use `harness/first-week.md` to keep the system light and calibrated

That is enough to install a first-pass DAOS baseline.

If you want to understand what comes after setup and the first week, read `docs/adoption-path.md`.

## If you need the tooling list

You do not need all of these before first value, but these are the next tools:
- `scripts/daos_bootstrap.py` — generate a blank or filled pack
- `scripts/daos_wizard.py` — interactive setup
- `scripts/daos_validate.py` — readiness + lint/calibration checks
- `scripts/daos_update.py` — safe in-place pack inspection/apply
- `scripts/daos_portability.py` — durable wiki export/inspect/plan/apply when moving installs

## If you want examples before filling anything

Read these worked examples first:
- `examples/assistant-charter-example.md`
- `examples/creative-studio-assistant-charter-example.md`
- `examples/first-pass-setup-output-example.md`
- `examples/lane-snapshot-example.md`
- `examples/cadence-review-example.md`
- `examples/setup-conversation-example.md`
- `examples/user-operating-profile-example.md`
- `examples/creative-studio-operating-profile-example.md`
- `examples/starter-pack-example/`

Use them to understand the target shape.
Do not copy them blindly.

## Minimum outcome of a first DAOS install

A first pass is good enough when you have:
- a clear assistant charter
- a top-level lane map
- per-lane status / foreground / pressure notes
- explicit memory and trust defaults
- a basic reminder / planning posture
- one clear place for later calibration

You do not need a perfect life model.
You need a usable operating baseline.

## Fast decision rule

If you are unsure whether to add more structure, use this rule:
- if the assistant is already useful, stop and operate
- if one lane keeps drifting, add a lane snapshot
- if support starts feeling noisy or stale, run a cadence review
- if setup still feels confusing, simplify before expanding

## Suggested first sitting output

A good first sitting should leave you with:
- one filled assistant charter
- one filled operating profile
- optionally one lane snapshot for the highest-friction lane
- a clear note that cadence review happens later, not during setup

Then the next step is not more setup.
The next step is the first week of real use guided by `harness/first-week.md`.

## What to skip at first

Do not start by:
- trying to model your entire life
- designing a universal taxonomy
- building too many memory layers
- writing long doctrine for your own instance
- creating a maintenance burden before value appears

## If you want the deeper theory later

Once the first setup is useful, then read more of the repo in this order:
1. `docs/thesis.md`
2. `docs/public-memory-page.md`
3. `docs/memory.md`
4. `docs/trust.md`
5. `docs/lane-model.md`

That sequence explains why the quickstart is designed this way.

## Bottom line

DAOS should be tried like an operating baseline, not admired like a concept deck.

Start small.
Lock the high-leverage defaults.
Use it.
Then calibrate.

If you want the lowest-friction real start, copy `starter-pack/` and begin there.
