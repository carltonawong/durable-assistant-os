# Memory Parity Auditor

The memory parity auditor checks whether a DAOS pack is actually aligned with the memory model, not just whether a few files exist.

Run it from the repo root:

```bash
python scripts/daos_memory_parity.py /path/to/daos-pack
```

For the bundled starter pack:

```bash
python scripts/daos_memory_parity.py starter-pack
```

## What it checks today

The first version is intentionally small and read-only. It checks:

- required baseline memory files exist
- `wiki/log.md` keeps chronological append order, with newest activity at the bottom
- `wiki/cache/hot-cache-log.md` keeps reverse-chronological front-door transition order, with newest entries at the top
- `wiki/cache/hot-cache.md` has the five required front-door sections
- `AGENTS.md` / `wiki/WIKI.md` carry local-thread-first plus hot-cache orientation language
- `wiki/raw/README.md` and `wiki/sources/README.md` exist and describe the raw/source boundary
- `wiki/cache/agent-continuity.md` has a visible freshness marker when it contains fallback continuity material

## Relationship to `daos_validate.py`

`daos_validate.py` asks: is this pack minimally filled and structurally operable?

`daos_memory_parity.py` asks: do the installed memory surfaces follow DAOS semantics?

Use validation first. Use parity when you want a stronger check of the memory layer.

## Script safety

`daos_memory_parity.py` is a read-only local audit.

It:
- reads files inside the DAOS pack path you provide
- does not modify files
- does not send network requests
- does not intentionally read credential files or credential locations
- uses only Python standard library

If you do not want to run scripts from this repo yet, use this document as a manual checklist instead.

## Output

The output is designed to match DAOS maintenance/audit language:

```text
Status: healthy / watch / drift
Findings:
- ...
Repairs made:
- none
Recommended next move:
- ...
```

Status meanings:

- `healthy` — no material parity issues detected
- `watch` — warning-level drift or ambiguity; inspect and apply the smallest safe correction if real
- `drift` — missing or broken baseline parity; repair before treating the pack as aligned

## What it does not check yet

This first slice does not:

- inspect a live assistant runtime
- verify cron scheduler state
- repair files automatically
- judge whether an assistant actually loaded these files on session start
- merge or rewrite durable wiki content

Those are future layers. The goal here is to catch the highest-value install/parity mistakes first, especially the log-order distinction that real OPC/Jarvis testing surfaced:

- `wiki/log.md` is the append-only chronological ledger
- `wiki/cache/hot-cache-log.md` is reverse-chronological front-door transition history

## Why this exists

DAOS installs can look correct while still being semantically wrong. A pack can have files named `hot-cache.md`, `agent-continuity.md`, and `wiki/log.md` but still misuse them.

The parity auditor makes those mistakes visible earlier, before they become trusted memory drift.
