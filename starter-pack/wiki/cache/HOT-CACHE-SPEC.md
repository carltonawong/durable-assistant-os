# HOT-CACHE-SPEC.md

## Purpose

The hot cache is the shared front door for what matters now.

It should feel tip-of-tongue, but it is not durable truth and not an exact handoff transcript.

No single agent owns it.
It is shared volatile front-door context and may be overwritten as the active lane shifts.

## Core rule

Use local thread context first.

If the thread is not enough:
1. read `hot-cache.md`
2. if the front door feels incongruent, read `hot-cache-log.md`
3. if resuming after reset or long idle, read `reset-handoff.md`
4. if still unsure of your own prior lane, read `agent-continuity.md`
5. verify important assumptions against wiki/files/runtime before acting

## Allowed sections

The hot cache may contain only:
1. Current Focus
2. Current Corrections
3. Current State
4. Open Problems
5. System Priorities

## Size limits

Keep `hot-cache.md`:
- under 500 words
- exactly 5 sections
- max 3 bullets per section
- 1-2 lines per bullet

## Hot-cache log rule

`hot-cache-log.md` exists for fallback audit/reconstruction and lane-rescope disambiguation.

It is not primary working memory.

Keep it:
- reverse-chronological
- compact
- meaningful
- pruned by recurring hygiene

## Agent continuity rule

`agent-continuity.md` is fallback per-agent resume context.

Use it only after hot cache and, when needed, hot-cache log are not enough.

## Reset handoff rule

`reset-handoff.md` is the named DAOS reset/wake-up artifact.

Use it for exact post-reset resume when the local thread is not enough.

Keep it overwritten, compact, and single-handoff rather than append-only.

## Editing rules

- replace stale bullets instead of stacking duplicates
- prefer front-door context over status-report detail
- keep the log meaningful rather than exhaustive
- prune obvious log bloat during recurring hygiene
- do not treat the hot cache as private scratch memory for one agent
