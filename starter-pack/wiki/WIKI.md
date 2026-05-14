# WIKI.md

<!-- DAOS baseline note: Current public framework baseline is v0.2.5; this file remains part of the current release surface even if its original feature landed in an earlier patch. -->

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

During active project work, capture a project checkpoint before future assumptions drift when a step changes infrastructure, data ownership, provider/tool/account choice, auth, deployment/runtime mode, live-vs-dry-run posture, risk, money, customer impact, or operator setup.

A project checkpoint should record what changed, why it matters, the source of truth or verification target, what not to assume next time, and the next blocker or step.

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

## Durable page discipline

For durable wiki pages, prefer a small canonical header.

At minimum:
- `Type`
- `Status`
- `Summary`
- `Last Updated`

If the page describes something with a meaningful operating condition, track that separately as `State`.

For drift-prone operational pages, also add:
- `Location`
- `Source of Truth`
- `Last Verified`

Keep these distinctions clear:
- `Status` = lifecycle of the page itself
- `State` = condition of the thing the page describes

If you migrate an older page onto a newer metadata standard without materially changing its substance, preserve the older `Last Updated` timestamp instead of flattening freshness history to the migration time.

Keep metadata vocabularies controlled inside the install.
Do not casually invent new synonyms for lifecycle/status fields when an existing value already fits.

## Baseline doctrine

The canonical doctrine files in `wiki/cache/` are installed payloads, not free-regenerated suggestions.

Treat them as the memory-system spine unless explicitly migrated by a later framework update.

Do not casually rewrite those baseline doctrine files during ordinary use; update live cache surfaces or write durable notes instead.
