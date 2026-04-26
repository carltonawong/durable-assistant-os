# DAOS Starter Pack

This folder is the default copyable DAOS install.

Copy it into your own workspace, then fill the user-owned files. You can use it manually; scripts are optional.

## What “wiki” means here

In DAOS, the **wiki** is a plain markdown knowledge base that lives in `wiki/`.

It is not Wikipedia, not a hosted app, and not a special database. It is just a structured folder of notes that the human can read and the assistant can maintain.

The wiki is where durable knowledge should live:
- decisions that should survive chat history
- stable project/context notes
- source notes and raw observations that need later synthesis
- compact logs of meaningful memory-system changes

The included `wiki/` folder can be your durable memory home. If you already use another markdown wiki or docs vault, treat this folder as the DAOS shape to copy/adapt.

## The two kinds of files

### 1. Files you fill

Start here:
1. `assistant-charter.md` — what the assistant is for, how it should behave, and what requires approval
2. `operating-profile.md` — your working context, lanes, memory defaults, and trust posture

Use later:
3. `lane-snapshot.md` — optional current-state note for one high-friction lane
4. `cadence-review.md` — recurring cleanup and calibration review after real use starts

### 2. Files DAOS installs

These are the locked baseline spine:
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

You do not need to write these from scratch. They are installed so the assistant has a consistent memory/read-order baseline.

## Minimum first pass

A first pass is good enough when:
- `assistant-charter.md` has one clear outcome, failure mode, uncertainty rule, and approval boundary
- `operating-profile.md` names the main lanes and memory/trust defaults
- `lane-snapshot.md` is either unused or filled for one high-friction lane
- `cadence-review.md` is saved for later, not overfilled during setup

Do not model everything before first use. Get a usable baseline, use it, then calibrate.

## Starter defaults

If you are unsure what to write, use these defaults and refine later:
- memory front door = current thread/session first, then hot cache, then reset handoff on reset/long idle, then agent continuity only if still needed
- durable memory home = the included `wiki/` markdown folder unless you already have another durable docs/wiki space
- verified reality rule = live files, systems, and runtime state outrank remembered notes when freshness matters
- approval rule = ask before risky, costly, destructive, public, or socially consequential actions

## Maintenance in plain English

DAOS works best when temporary context has a path into durable memory.

Basic loop:
1. Use `wiki/cache/hot-cache.md` for what matters now.
2. Use `wiki/cache/reset-handoff.md` for the exact next move after reset or long idle.
3. Put durable observations that should survive into `wiki/raw/` or durable wiki pages.
4. Use `cadence-review.md` after real use starts to decide what to keep, change, or remove.
5. Compress or prune stale temporary notes after durable facts have been captured.

After the initial fill, use `harness/first-week.md` as the default next guide.

## Examples

Use `examples/starter-pack-example/` to see the user-owned files filled without duplicating this locked baseline spine.
