# Script Safety

<!-- DAOS baseline note: Current public framework baseline is v0.2.2; this file remains part of the current release surface even if its original feature landed in an earlier patch. -->

DAOS is designed around the copyable `starter-pack/` first.

You can use DAOS without running any script:
1. copy `starter-pack/`
2. fill the markdown files
3. use the pack with your assistant

Scripts are optional helpers. They exist to reduce setup mistakes, but they should not be required before you understand what DAOS is doing.

## Trust posture

Packaged DAOS scripts are local Python scripts using the standard library.

Current safety commitments:
- no network access
- no intentional reads from credential files or credential locations
- no shell command execution from packaged DAOS scripts
- no background services
- no hidden telemetry

If a future packaged script needs network access, credentials, shell execution, credential-location reads, or background behavior, it should be documented explicitly before release.

## Recommended first commands

If you are cautious, start with read-only checks:

```bash
python scripts/daos_validate.py /path/to/my-daos-pack
python scripts/daos_memory_parity.py /path/to/my-daos-pack
```

These read files and print findings. They do not modify your pack.

## Script tiers

### Core, read-only checks

| Script | Purpose | Writes files? | Recommended for first users? |
|---|---|---:|---:|
| `scripts/daos_validate.py` | Check whether a pack is minimally filled and structurally operable | No | Yes |
| `scripts/daos_memory_parity.py` | Check whether memory surfaces follow DAOS semantics | No | Optional |

### Optional setup helpers

| Script | Purpose | Writes files? | Recommended for first users? |
|---|---|---:|---:|
| `scripts/daos_bootstrap.py` | Generate a fresh DAOS pack into a target folder | Yes, target folder only | Optional |
| `scripts/daos_wizard.py` | Ask setup questions and generate a filled pack | Yes, target folder only after confirmation | Optional |

For the lowest-friction start, copy `starter-pack/` manually instead of using these.

### Advanced maintenance / portability

These tools are intentionally not part of the README/quickstart first-run command list.
Use them only after the starter pack is already useful and you have a specific maintenance or migration need.

| Script | Purpose | Writes files? | Recommended for first users? |
|---|---|---:|---:|
| `scripts/daos_update.py check` / `plan` | Inspect an existing pack for safe updates | No | Advanced |
| `scripts/daos_update.py apply` | Apply safe in-place pack updates with backups | Yes | Advanced, review first |
| `scripts/daos_portability.py inspect` / `plan` | Inspect or plan a portability import | No, except optional review output for `plan` | Advanced |
| `scripts/daos_portability.py export` | Copy a pack/wiki into a portability bundle | Yes, output bundle only | Advanced |
| `scripts/daos_portability.py apply` | Apply a portability bundle into target pack/wiki paths | Yes | Advanced, review first |

## Manual alternative

If you do not want to run scripts from this repo, use the docs as checklists:
- `starter-pack/README.md`
- `docs/quickstart.md`
- `docs/memory-parity-auditor.md`
- `harness/first-week.md`

The scripts should make DAOS easier to check, not harder to trust.
