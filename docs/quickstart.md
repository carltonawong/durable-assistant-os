# DAOS Quickstart

Use this when you want a first usable DAOS pack without reading the whole repo.

The default path does not require scripts.

## 15-minute path

1. Copy `starter-pack/` into your own workspace.
2. Open the copied folder.
3. Fill `assistant-charter.md`.
4. Fill `operating-profile.md`.
5. Leave `lane-snapshot.md` blank unless one workstream already needs extra structure.
6. Save `cadence-review.md` for later upkeep.
7. Use `harness/first-week.md` after the first setup.

## What each first-run file does

- `assistant-charter.md` defines what the assistant is for, how it behaves under uncertainty, and what requires approval.
- `operating-profile.md` defines the working context, lanes, memory defaults, and trust posture.
- `lane-snapshot.md` is optional extra structure for one high-friction lane.
- `cadence-review.md` is for later cleanup and calibration, not first install.

## Minimum good first pass

A first pass is good enough when:
- the assistant's main job is clear
- the main failure mode is clear
- approval boundaries are explicit
- active lanes are named
- memory has a durable home
- live files/runtime are treated as higher authority than remembered notes

Do not try to model your entire life or organization before first use.

## Optional read-only checks

If you are comfortable running local Python scripts, use read-only checks after filling the pack:

```bash
python scripts/daos_validate.py /path/to/my-daos-pack
python scripts/daos_memory_parity.py /path/to/my-daos-pack
```

If you do not want to run scripts, use this page, `starter-pack/README.md`, and `docs/memory-parity-auditor.md` as manual checklists.

## Optional generated setup

Manual copying is the default. If you prefer generated setup:

```bash
python scripts/daos_bootstrap.py /path/to/my-daos-pack
```

For an interactive first pass:

```bash
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
