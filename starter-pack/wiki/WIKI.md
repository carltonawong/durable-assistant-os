# WIKI.md

This wiki is the durable shared memory layer for the DAOS install.

It is not the front-door cache and not a transcript dump.

## Purpose

Use the wiki to hold:
- durable knowledge
- architecture and operating rules
- important decisions
- corrections that future agents should not have to rediscover

Do not use it as a transcript dump.
Do not treat it as higher authority than verified runtime/files for live facts.

## Read order reminder

For exact handoff/resume:
1. local thread / reply target / recent turns
2. `wiki/cache/hot-cache.md`
3. if incongruent, `wiki/cache/hot-cache-log.md`
4. if resuming after reset or long idle, `wiki/cache/reset-handoff.md`
5. if still unsure, `wiki/cache/agent-continuity.md`
6. deeper wiki reconstruction
7. verified runtime/files when live state matters

## Write rule

If not capturing something would likely create ambiguity, repeated investigation, or false assumptions later, create a dated raw note under `wiki/raw/`.

## Durable capture rule

Promote to durable memory when the finding changes any of:
- how current work should be interpreted
- what evidence is safe to trust
- the next correct move
- what a future agent would otherwise need to re-derive

## Main surfaces

- `wiki/cache/` = active-memory/front-door surfaces
- `wiki/raw/` = staged raw capture
- `wiki/sources/` = durable source notes
- `wiki/index.md` = durable page/source map
- `wiki/log.md` = durable change log

## Baseline doctrine

The canonical doctrine files in `wiki/cache/` are installed payloads, not free-regenerated suggestions.

Treat them as the memory-system spine unless explicitly migrated by a later framework update.

Do not casually rewrite those baseline doctrine files during ordinary use; update live cache surfaces or write durable notes instead.
