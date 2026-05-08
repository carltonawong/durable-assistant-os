<p align="center">
  <img src="./docs/assets/daos-wordmark-banner.svg" alt="Durable Assistant OS" width="100%">
</p>

<p align="center">
  <strong>Stop being your AI assistant’s context bank.</strong><br>
  <span>A local continuity harness for AI agents.</span>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/use-daos"><img src="https://img.shields.io/badge/npm-use--daos-CB3837?style=flat-square&logo=npm&logoColor=white" alt="npm package: use-daos"></a>
  <a href="./CHANGELOG.md"><img src="https://img.shields.io/badge/Changelog-CHANGELOG.md-111827?style=flat-square" alt="Changelog"></a>
  <a href="./docs/releases/"><img src="https://img.shields.io/badge/Releases-docs%2Freleases-2563EB?style=flat-square" alt="Release notes"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-green?style=flat-square" alt="License: Apache-2.0"></a>
</p>

<p align="center">
  <code>npx use-daos init → setup → check → on → reset-test → You're complete!</code>
</p>

<p align="center">
  <strong>AI assistants are amazing until you realize you’re becoming their memory system.</strong><br>
  DAOS exists for everyone who has rebuilt context for the same assistant three times in one week — making AI work feel less like starting over, and more like continuing a real conversation.
</p>

Durable Assistant OS (DAOS) is a local continuity layer for AI assistants that need to stay useful after resets, long gaps, model switches, and messy memory.

It gives a human and an assistant a small shared system for:
- knowing what the assistant is for
- separating current context from durable memory
- preserving trust boundaries
- recovering after resets or long gaps
- checking live reality before acting on stale notes

DAOS is not a hosted app and not a full assistant runtime. It is the operating structure you can put beside a runtime.

## Try it first

If you only try one thing, run:

```bash
npx use-daos init
npx use-daos setup
npx use-daos check
npx use-daos on
npx use-daos reset-test
```

That creates a local DAOS home, installs the mandatory wiki/cache baseline, scans nearby agent instruction files, guides setup, checks the pack, shows what DAOS is on, and verifies reset recovery. Run `setup` interactively; for non-interactive smoke tests, use `npx use-daos setup --accept-defaults`.

When the first-run sequence passes, DAOS ends with:

```text
You're complete!
```

The status view starts with:

```text
DAOS Status

Setup
...

DAOS On
- Hot Cache: ...
- Hot Cache Log: ...
- Reset Handoff: ...
- Agent Continuity: ...
```

This is the core product loop:

1. `use-daos init` installs a shared continuity baseline.
2. DAOS scans existing instruction carriers like `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and Copilot instructions.
3. DAOS asks before editing existing instruction files.
4. `use-daos` shows the current setup and continuity status.
5. Your assistant uses the DAOS files to recover orientation without treating memory as live truth.

## What you should have after one sitting

You should have:
- a local DAOS pack with the locked baseline files installed
- a visible `DAOS Status` report
- a `DAOS On` section showing current active-memory surfaces
- explicit continuity files for hot cache, hot-cache log, reset handoff, and agent continuity
- a staged bridge report if DAOS found existing agent instructions
- no silent import of arbitrary old memory content

Do not model everything up front. Start small, use it, then tighten what real use proves is weak.

## DAOS home can be an existing assistant home

The default new-user home is `~/.daos`, but the folder name is not the product. DAOS home is the folder with the DAOS pack/wiki: `assistant-charter.md`, `operating-profile.md`, and `wiki/cache/`.

If you already have an existing assistant home with those surfaces, use it directly instead of creating a duplicate home:

```bash
DAOS_HOME=/path/to/existing-assistant-home use-daos

use-daos on /path/to/existing-assistant-home
```

The important part is that agents can find and read the shared `wiki/cache/` surfaces. The home can be `~/.daos` or another explicit assistant-home path.

## Existing agent instructions

DAOS is designed to coexist with agent-specific memory and instruction systems.

During `use-daos init`, it can scan for instruction carriers such as:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
HERMES.md
OPENCLAW.md
QUINN.md
.cursorrules
.cursor/rules/*
.github/copilot-instructions.md
.hermes/instructions.md
.openclaw/AGENTS.md
```

If DAOS finds them, it stages a review report. In interactive mode, it asks before prepending the DAOS coexistence rule. If approved, it backs up the original first.

DAOS does **not** import arbitrary memory files like `MEMORY.md` by default. Existing private memory can keep orienting its own agent, while DAOS becomes the shared continuity layer across tools.

## Why this exists

Assistants usually do not fail at the first impressive answer. They fail later, when context gets noisy, short-term state is mistaken for durable truth, and the user starts maintaining the assistant more than using it.

DAOS exists to keep that operating loop small, legible, and repairable.

The important rule:

> Memory can orient the assistant, but current reality wins when action depends on what is true now.

## The core model

DAOS is not about making agents remember more. It is about making the right context available to the right agent at the right moment.

It keeps six things separate:

1. **Local thread** — what is being asked right now.
2. **Hot front door** — the shortest current orientation note.
3. **Recent front-door history** — compact recovery when Current Focus context was just pruned, displaced, or re-scoped.
4. **Reset handoff** — the exact next move after reset or long idle.
5. **Durable memory** — stable knowledge, decisions, and synthesized context.
6. **Live reality** — repo files, configs, runtime state, inboxes, calendars, and other sources that must be checked when freshness matters.

DAOS treats short-term context as controlled volatility, not durable truth:

- rewrite volatile front-door context as Current Focus changes
- log recent front-door churn only when it helps another agent recover from a prune, displacement, or re-scope
- promote decisions, corrections, and findings that would create ambiguity if lost
- verify live facts against files, runtime state, inboxes, calendars, or other source systems
- treat current-state claims like release versions, publish status, branch/tag state, runtime health, and test results as freshness-sensitive
- ignore transient chatter, obsolete details, and facts easy to re-derive
- resolve conflict by source authority: live reality > durable docs > active cache > continuity > private/session memory

## Manual path

You can still use DAOS without npm or scripts.

1. Copy `starter-pack/` into your workspace.
2. Fill `assistant-charter.md`.
3. Fill `operating-profile.md`.
4. Use the `wiki/cache/` files as the assistant's shared continuity layer.

The CLI is the easier first path, but the pack remains plain markdown by design.

## What is in the repo

- `bin/use-daos.js` — thin npm wrapper for the DAOS CLI.
- `scripts/daos.py` — Python reference CLI used by the wrapper.
- `starter-pack/` — the default DAOS baseline installed by `use-daos init`.
- `docs/quickstart.md` — short first-run procedure.
- `docs/memory.md` — deeper memory doctrine.
- `docs/agent-integrations.md` — notes for wiring DAOS beside assistants.
- `docs/portability.md` — durable wiki portability model.
- `docs/reset-current-state-receipt.md` — small proof shape for reset recovery without stale-memory trust.
- `harness/mandatory-baseline.md` — locked baseline install contract.
- `examples/starter-pack-example/` — filled user-owned files for a realistic pack.
- `tests/` — regression tests for scripts, package behavior, and safety posture.

The GitHub source tree also carries tests and selected verification material. Heavier internal eval artifacts stay out of the npm runtime package so `use-daos` installs as focused local tooling, not a benchmark archive.

## What is already proven

The current v0.2 line includes:
- `use-daos init` and no-args `use-daos` as the first-user CLI surface
- `use-daos setup`, `use-daos check`, `use-daos on`, and `use-daos reset-test` as the explicit first-run proof loop
- mandatory baseline install from the starter pack
- safe instruction-carrier scanning
- approval-gated instruction edits with backups
- `DAOS Status` / `DAOS On` active-context summaries
- wrapper tests for Node/npm delegation, Python discovery, exit-code forwarding, and interactive prompts
- packed-tarball smoke testing from a fresh npm consumer project
- regression tests covering generation, validation, wizard flow, portability, update safety, memory parity, and script trust posture

## Requirements

- Node.js 18+
- Python 3 available as one of:
  - `python3`
  - `python`
  - `py -3`
  - or `DAOS_PYTHON=/path/to/python`

If Python is missing, the wrapper prints a direct setup message instead of failing silently.

## Safety posture

DAOS is local-first and markdown-first.

The first-user path should not:
- send network requests from the Python core
- import arbitrary old memory content by default
- silently edit existing instruction files
- overwrite user-owned operating files without explicit action
- treat remembered notes as live truth

## Documentation principle

DAOS docs should stay practical: every public file should help a reader understand, install, verify, or operate the system.
