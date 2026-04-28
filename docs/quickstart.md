# DAOS Quickstart

Use this when you want a first usable DAOS pack without reading the whole repo.

## Fast path

```bash
npx daos init
npx daos
```

`daos init` installs the DAOS baseline into your DAOS home, scans the current working directory for existing agent instruction files, and stages a bridge review when needed.

No-args `daos` shows the compact status view:

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

That is enough for a first pass. You do not need to understand every file before using it.

## If DAOS finds existing agent instructions

DAOS scans instruction carriers such as:

```text
AGENTS.md
CLAUDE.md
GEMINI.md
.cursorrules
.cursor/rules/*
.github/copilot-instructions.md
.hermes/instructions.md
.openclaw/AGENTS.md
```

In interactive mode, DAOS asks before editing those files. If you approve, it prepends the DAOS coexistence rule and backs up the original under `.daos/backups/instructions/`.

If you do not approve, or if the command is non-interactive, DAOS writes a review report instead:

```text
.daos/import-stage/instruction-scan.md
```

DAOS does not import arbitrary old memory files like `MEMORY.md` by default.

## Existing assistant homes

The default new-user home is `~/.daos`, but DAOS can also read an existing assistant home that already contains the DAOS pack/wiki surfaces. The folder name does not matter as much as the structure.

For an existing OpenClaw/Hermes-style home, point DAOS at it explicitly:

```bash
DAOS_HOME=/path/to/existing-assistant-home daos

daos on /path/to/existing-assistant-home
```

Use this when the existing home already has `wiki/cache/hot-cache.md`, `wiki/cache/hot-cache-log.md`, `wiki/cache/reset-handoff.md`, and related DAOS surfaces. This avoids creating a second `~/.daos` home when your current assistant home already acts as the DAOS home.

## What each first-run file does

- `assistant-charter.md` defines what the assistant is for, how it behaves under uncertainty, and what requires approval.
- `operating-profile.md` defines the working context, lanes, memory defaults, and trust posture.
- `wiki/cache/hot-cache.md` is the compact current front door.
- `wiki/cache/hot-cache-log.md` is recent front-door transition history.
- `wiki/cache/reset-handoff.md` is the exact next move after reset or long idle.
- `wiki/cache/agent-continuity.md` is last-resort continuity for agent-specific recovery.
- `lane-snapshot.md` is optional extra structure for one high-friction lane.
- `cadence-review.md` is for later cleanup and calibration, not first install.

## Minimum good first pass

A first pass is good enough when:
- the assistant's main job is clear
- approval boundaries are explicit
- the current focus is visible in `wiki/cache/hot-cache.md`
- reset recovery has an exact next move when real work begins
- any existing instruction files are reviewed or explicitly left alone
- live files/runtime are treated as higher authority than remembered notes

Do not try to model your entire life or organization before first use.

## Manual path

If you do not want npm or scripts:

1. Copy `starter-pack/` into your own workspace.
2. Open the copied folder.
3. Fill `assistant-charter.md`.
4. Fill `operating-profile.md`.
5. Use `wiki/cache/` as the assistant's shared continuity layer.
6. Use `harness/first-week.md` after the first setup.

The CLI is the easier path, but DAOS remains plain markdown by design.

## Optional read-only checks

If you are comfortable running local Python scripts, use read-only checks after filling the pack:

```bash
python scripts/daos_validate.py /path/to/my-daos-pack
python scripts/daos_memory_parity.py /path/to/my-daos-pack
```

If you do not want to run scripts, use this page, `starter-pack/README.md`, and `docs/memory-parity-auditor.md` as manual checklists.

## Advanced generated setup

The v0.2 front door is `npx daos init`. Older local Python helpers remain available for development and manual workflows:

```bash
python scripts/daos_bootstrap.py /path/to/my-daos-pack
python scripts/daos_wizard.py /path/to/my-daos-pack
```

Read `docs/script-safety.md` first if you want to understand the script trust posture.

## Examples

Use examples to understand shape, not to copy blindly:
- `examples/starter-pack-example/` shows filled user-owned files for a realistic pack.
- `examples/creative-studio-operating-profile-example.md` shows a different persona and lane shape.

## Next step

After setup, stop configuring and use the pack for a week.

Then run the first-week calibration path in `harness/first-week.md`.
