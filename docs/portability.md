# DAOS Portability

## Why this page exists

DAOS portability should move the durable memory layer cleanly without collapsing DAOS back into pack-folder sync.

The core stance is:
- durable truth is wiki-first
- pack metadata should move with it
- active-memory handoff is optional, not default
- imports should be inspectable before writes

## What portability means in DAOS

DAOS portability is not "copy every live file and hope."
It is a bounded transfer of:
1. durable wiki memory
2. pack identity and compatibility metadata
3. optional active-memory sidecars when explicitly requested

## Current bundle layout

A portability export currently produces a directory like:

```text
bundle/
  portability-manifest.json
  pack/
    daos-pack.json
    .daos/manifest.json
    .daos/migrations/
  durable/
    wiki/
      ...durable wiki files...
  active/
    hot-cache.md
    agent-continuity.md
```

## Current commands

### Export

```bash
python scripts/daos_portability.py export \
  --pack-dir /tmp/pack \
  --wiki-root /tmp/wiki \
  --out /tmp/bundle
```

Optional active-memory handoff:

```bash
python scripts/daos_portability.py export \
  --pack-dir /tmp/pack \
  --wiki-root /tmp/wiki \
  --out /tmp/bundle \
  --include-active-memory \
  --hot-cache /tmp/hot-cache.md \
  --agent-continuity /tmp/agent-continuity.md
```

### Inspect

```bash
python scripts/daos_portability.py inspect /tmp/bundle
```

### Plan

```bash
python scripts/daos_portability.py plan /tmp/bundle --target-wiki-root /tmp/new-wiki
```

### Apply

```bash
python scripts/daos_portability.py apply \
  /tmp/bundle \
  --target-wiki-root /tmp/new-wiki \
  --target-pack-dir /tmp/new-pack
```

## Current behavior

### Export includes by default
- durable wiki payload
- `daos-pack.json`
- `.daos/manifest.json` when present
- `.daos/migrations/` when present
- `portability-manifest.json`

### Export excludes by default
- hot cache
- agent continuity
- similar active-memory handoff files

### Inspect reports
- bundle version
- schema/framework version
- pack id
- durable wiki file count
- whether active memory is included
- whether migrations are included

### Plan reports
- where pack metadata would come from
- how many durable wiki files would be copied
- whether active-memory payload would be staged for review

### Apply currently does
- restore `daos-pack.json` into a target pack root
- restore or synthesize `.daos/manifest.json` in the target pack root
- copy non-conflicting durable wiki files into the target wiki root
- emit a collision review note instead of silently overwriting conflicting durable wiki files
- keep active-memory payload staged-only by default

## Current non-goals
- no archive compression yet
- no automatic merge of conflicting durable markdown
- no automatic activation of hot cache or continuity on import
- no hidden sync layer

## Recommendation

Use:
- `daos_update.py` when the same DAOS pack should evolve in place
- `daos_portability.py` when durable wiki memory and pack identity need to move across installs or machines
