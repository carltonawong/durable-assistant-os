# DAOS Quickstart

Use this when you want a first usable DAOS pack without reading the whole repo.

## Fast path

```bash
npx use-daos init
npx use-daos setup
npx use-daos check
npx use-daos on
npx use-daos reset-test
npx use-daos doctor
```

`use-daos init` installs the DAOS baseline into your DAOS home, scans the current working directory for existing agent instruction files, and stages a bridge review when needed.

`use-daos setup` is the guided activation step. It explains and fills the minimum assistant charter, operating profile, current focus, and reset handoff. Run it in an interactive terminal; for non-interactive smoke tests, use `use-daos setup --accept-defaults`.

`use-daos check`, `use-daos on`, `use-daos reset-test`, and `use-daos doctor` should all default to the active DAOS home. `doctor` is read-only and separates installed / bridged / activated / proven instead of treating file presence as runtime proof. When the reset-test sequence passes, DAOS ends with:

```text
You're complete!
```

No-args `use-daos` still shows the compact status view:

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

That is enough for a first pass. You do not need to understand every layer before using DAOS as a context-continuity harness.

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
import-stage/instruction-scan.md
```

The path is relative to your DAOS home. If your DAOS home is `~/.daos`, the report is `~/.daos/import-stage/instruction-scan.md`.

DAOS does not import arbitrary old memory files like `MEMORY.md` by default.

## Existing assistant homes

The default new-user home is `~/.daos`, but DAOS can also read an existing assistant home that already contains the DAOS pack/wiki surfaces. The folder name does not matter as much as the structure.

For an existing assistant home, point DAOS at it explicitly:

```bash
DAOS_HOME=/path/to/existing-assistant-home use-daos

use-daos on /path/to/existing-assistant-home
```

Use this when the existing home already has `wiki/cache/hot-cache.md`, `wiki/cache/hot-cache-log.md`, `wiki/cache/reset-handoff.md`, and related DAOS surfaces. This avoids creating a second `~/.daos` home when your current assistant home already acts as the DAOS home.

## Boot/runtime doctor

`use-daos check` tells you whether the pack itself is minimally operable. If you also want to check whether a runtime is likely to start DAOS-first, run:

```bash
use-daos boot-check /path/to/existing-assistant-home
```

That read-only command reports structure plus an explicit warning when runtime boot order is not verified. Adapter-specific exports can pass a JSON fixture:

```bash
use-daos boot-check /path/to/existing-assistant-home --runtime-config runtime.json
```

The fixture can describe `startup_root`, `daos_home`, `prompt_precedence`, `session_topology`, and `reset_handoff` wiring so DAOS can catch cases where files are installed but private memory or split sessions still win at runtime.

`use-daos doctor` accepts the same fixture through `--runtime-file`. It can also collect conservative read-only runtime evidence for supported adapters:

```bash
use-daos doctor /path/to/existing-assistant-home --runtime hermes --detect-runtime
```

The Hermes detector reports `runtime`, `startup_root`, `daos_home`, `prompt_precedence`, `reset_wake`, and `unexpected_writes`. Runtime fixtures may also include `continuity_surfaces`, `handoff_lifecycle`, and `surface_inventory` for ownership/lifecycle proof beyond file presence. The detector can prove detected wiring, but not `one_shot_proven` without an actual reset/session proof.

## What each first-run file does

- `assistant-charter.md` defines what the assistant is for, how it behaves under uncertainty, and what requires approval.
- `operating-profile.md` defines the working context, lanes, context/memory defaults, and trust posture.
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

Do not try to model your entire life or organization before first use. DAOS should make day-one continuity easier, not turn setup into a taxonomy project.

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

The v0.2 front door is `npx use-daos init`. Older local Python helpers remain available for development and manual workflows:

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
