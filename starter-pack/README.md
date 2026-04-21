# DAOS Starter Pack

This folder is the fastest copyable scaffold in the repo.

If you want to try DAOS on a real assistant or real user context, copy this folder into your own workspace and fill the files in order.

## Quick translation of DAOS terms

- **assistant charter** — what this assistant is for and how it should behave
- **operating profile** — your working context, priorities, and support preferences
- **lane snapshot** — the current state of one workstream
- **cadence review** — a recurring cleanup and calibration pass

## What is already installed here

This starter pack already includes both parts of the baseline:

### 1. Fillable operator files
- `assistant-charter.md`
- `operating-profile.md`
- `lane-snapshot.md` *(optional)*
- `cadence-review.md` *(later upkeep)*

### 2. Locked mandatory baseline files
- `AGENTS.md`
- `wiki/WIKI.md`
- `wiki/cache/MEMORY-OPERATING-MODEL.md`
- `wiki/cache/HOT-CACHE-SPEC.md`
- `wiki/cache/hot-cache.md`
- `wiki/cache/hot-cache-log.md`
- `wiki/cache/reset-handoff.md`
- `wiki/cache/agent-continuity.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/raw/README.md`
- `wiki/sources/README.md`

The operator mainly fills the first group.
The second group is the installed DAOS spine and should stay structurally intact unless a later framework update explicitly migrates it.

## Suggested order

1. `assistant-charter.md`
2. `operating-profile.md`
3. `lane-snapshot.md` *(only if one lane needs extra structure)*
4. `cadence-review.md` *(for later upkeep, not first install)*

## What each file answers

- `assistant-charter.md` answers: what should this assistant do, how should it act when uncertain, and what requires approval?
- `operating-profile.md` answers: what reality is this assistant operating inside, what lanes matter, and where should memory/trust defaults live?
- `lane-snapshot.md` answers: what is happening inside one high-friction lane right now?
- `cadence-review.md` answers: after real use starts, what should be kept, tuned, or simplified?

## What this folder is

This is a ready-to-copy instance scaffold.
It is the default first-user starting point in the repo.
It is not the canonical doctrine source.

Those locked files are intentionally written as exact starter payloads so installs get the same baseline memory/doctrine behavior instead of relying on free regeneration.

`wiki/cache/reset-handoff.md` is the named public reset/wake-up artifact inside that baseline. Use it as the exact next-session handoff after reset or long idle. Keep it overwritten rather than appended.

## How the starter pack maps to the model

- `assistant-charter.md` — what this assistant is for and how it should behave
- `operating-profile.md` — durable working context, priorities, and support preferences
- `lane-snapshot.md` — optional current state for one workstream
- `cadence-review.md` — later cleanup and calibration surface

Practical memory mapping inside the pack:
- `operating-profile.md` is where you lock the default memory and trust posture
- `lane-snapshot.md` is optional extra context for one lane, not the main memory home
- your durable wiki/docs space is still the long-lived memory home outside this starter folder

Use the files here when you want to operate.
Use `templates/` when you want reusable source templates or want to extend the framework itself.
Use `examples/` when you want to see filled shapes.
Use `examples/starter-pack-example/` when you want to see this exact folder structure already filled.

## Minimum good outcome

A first pass is good enough when:
- the locked baseline files are present and left structurally intact
- `assistant-charter.md` is filled
- `operating-profile.md` is filled enough to orient lanes, trust, and reminder defaults
- `lane-snapshot.md` is either unused or filled for the highest-friction lane
- `cadence-review.md` is saved for later reviews

## Keep it light

Do not try to perfect everything before first use.
The point of this pack is to get to a usable baseline quickly.

If you are unsure what to write, use these starter defaults:
- memory front door = current thread/session first, then short active summary, then reset handoff on reset/long idle, then any broader continuity note
- durable memory home = markdown wiki or docs space first
- verified reality rule = live files and systems outrank remembered notes
- approval rule = ask before risky, costly, sticky, or social actions

After the initial fill, use `harness/first-week.md` as the default next guide.
