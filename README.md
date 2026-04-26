# Durable Assistant OS

**Current documented baseline:** `v0.1.6`  
**Release notes:** `CHANGELOG.md` and `docs/releases/`

Durable Assistant OS (DAOS) is a copyable operating pack for assistants that need to stay useful after the first impressive session.

It gives a human and an assistant a small shared system for:
- knowing what the assistant is for
- separating current context from durable memory
- preserving trust boundaries
- recovering after resets or long gaps
- checking live reality before acting on stale notes

DAOS is not a hosted app and not a full assistant runtime. It is the operating structure you can put beside a runtime.

![Fragile assistant versus DAOS memory surfaces](docs/assets/daos-fragile-vs-memory-surfaces.png)

## Source pattern

DAOS assumes the **LLM Wiki** pattern: a plain markdown knowledge base that an assistant can read, maintain, and improve over time. Read Karpathy's short note first if this idea is new:

- **Karpathy's LLM Wiki pattern**  
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

Optional companion:
- **Obsidian** — helpful if you want a dedicated vault-style UI for browsing and editing that wiki  
  https://obsidian.md/download

DAOS adds operating discipline around that pattern: a compact front door, reset handoff, durable pages, raw/source notes, and a rule that live reality still outranks remembered notes.

## Who this is for

DAOS is for people who already feel the pain of assistant context drift, memory clutter, repeated re-steering, or unclear trust boundaries.

It is probably not the right first stop if you only want a plug-and-play consumer assistant with no markdown, no operating discipline, and no local files to maintain.

## Why this exists

Assistants usually do not fail at the first impressive answer. They fail later, when context gets noisy, memory stops matching reality, and the user starts maintaining the assistant more than using it.

DAOS exists to keep that operating loop small, legible, and repairable.

## Start here

If you only try one thing, copy `starter-pack/`.

1. Copy `starter-pack/` into your own workspace.
2. Fill `assistant-charter.md`.
3. Fill `operating-profile.md`.
4. Use `harness/first-week.md` during the first week of real use.

You can use DAOS without running scripts. Optional read-only checks are available later.

## The core model

DAOS keeps five things separate:

1. **Local thread** — what is being asked right now.
2. **Hot front door** — the shortest current orientation note.
3. **Reset handoff** — the exact next move after reset or long idle.
4. **Durable memory** — stable knowledge, decisions, and synthesized context.
5. **Live reality** — repo files, configs, runtime state, inboxes, calendars, and other sources that must be checked when freshness matters.

The important rule:

> Memory can orient the assistant, but current reality wins when action depends on what is true now.

## What is in the repo

- `starter-pack/` — the default copyable DAOS pack.
- `docs/quickstart.md` — the shortest first-run procedure.
- `docs/public-memory-page.md` — the plain-language memory model.
- `docs/memory.md` — deeper memory doctrine.
- `harness/first-week.md` — how to calibrate after real use starts.
- `examples/starter-pack-example/` — filled user-owned files for a realistic pack.
- `examples/creative-studio-operating-profile-example.md` — a compact alternate-persona example.
- `scripts/` — optional local helpers; read `docs/script-safety.md` before using them.
- `tests/` — regression tests for the pack, scripts, and safety posture.

## What is already proven

DAOS is not just a set of ideas. The current repo includes:
- a copyable starter pack with a locked baseline memory spine
- optional generated setup and wizard setup
- read-only validation and memory-parity checks
- tests covering generation, validation, wizard flow, portability, update safety, and script trust posture
- release notes and changelog entries showing how the operating model has been hardened over time

The detailed development trail lives in `CHANGELOG.md`, `docs/releases/`, and git history rather than public planning files.

## Optional scripts

Scripts are not required for first value. If you are cautious, start manually with `starter-pack/`.

Read-only checks:

```bash
python scripts/daos_validate.py /path/to/my-daos-pack
python scripts/daos_memory_parity.py /path/to/my-daos-pack
```

Setup helpers and advanced maintenance tools are documented in `docs/script-safety.md`.

## What good looks like after one sitting

You should have:
- a clear assistant charter
- a usable operating profile
- explicit approval boundaries
- a durable memory home
- a simple active-context front door
- a first-week calibration path

Do not model everything up front. Start small, use it, then tighten what real use proves is weak.

## Public-framework hygiene

DAOS should stay tight:
- fewer public artifacts with clearer jobs
- no roadmap or planning graveyard in the front door
- no template soup
- no assumption that a reader has our private runtime setup

Every public file should help a stranger understand, install, verify, or operate the system.
