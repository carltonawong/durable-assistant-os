# DAOS Quickstart

## Who this is for

Use this page if you want the fastest path to trying DAOS without reading the entire repo first.

This is not the full doctrine path.
It is the shortest path to a first useful setup.

## The 15-minute path

If you want to try DAOS right now, do these in order:

Fastest option:
- copy `starter-pack/` into your own workspace and fill the files there
- treat that copied pack as your working instance
- treat `templates/` as reusable source blanks, not the default first-user starting point

Fastest generated option:
- run `python scripts/daos_bootstrap.py /path/to/my-daos-pack`
- add `--filled-example` if you want a filled starter-pack instead of a blank scaffold
- generated packs now include `daos-pack.json` as the machine-readable manifest
- then run `python scripts/daos_validate.py /path/to/my-daos-pack` once you have actually filled the pack
- expect lint/calibration warnings when the pack shape looks operable but still likely fragile

Fastest interactive option:
- run `python scripts/daos_wizard.py /path/to/my-daos-pack`
- the wizard now supports optional lane-by-lane customization and a review summary before it writes files
- then run `python scripts/daos_validate.py /path/to/my-daos-pack`

1. Read `docs/setup.md`
2. Run `harness/core-setup.md`
3. Fill the copied/generated pack first
4. Use `templates/assistant-charter-template.md` only if you need the reusable source blank
5. Use `templates/operating-profile-template.md` only if you need the reusable source blank
6. If one lane needs more structure, fill `templates/lane-snapshot-template.md`
7. When the first setup is done, use `templates/cadence-review-template.md` for upkeep
8. During real use, use `harness/first-week.md` to keep the system light and calibrated

That is enough to install a first-pass DAOS baseline.

If you want to understand what comes after setup and the first week, read `docs/adoption-path.md`.

If you need more than first install, the next tools are:
- `scripts/daos_bootstrap.py` — generate a blank or filled pack
- `scripts/daos_wizard.py` — interactive setup
- `scripts/daos_validate.py` — readiness + lint/calibration checks
- `scripts/daos_update.py` — safe in-place pack inspection/apply
- `scripts/daos_portability.py` — durable wiki export/inspect/plan/apply when moving installs

You do not need all of those before first value.

## If you want examples before filling anything

Read these worked examples first:
- `examples/assistant-charter-example.md`
- `examples/first-pass-setup-output-example.md`
- `examples/lane-snapshot-example.md`
- `examples/cadence-review-example.md`
- `examples/setup-conversation-example.md`
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
