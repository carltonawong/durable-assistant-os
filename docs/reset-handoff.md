# DAOS Reset Handoff

## Purpose

`wiki/cache/reset-handoff.md` is the named DAOS reset/wake-up continuity artifact.

Its job is narrow:
- preserve the exact next move when a reset or long idle gap would otherwise blur it
- preserve the first thing to verify before continuing
- give the next session a compact wake-up point without pretending to be durable truth

It is not:
- a full work log
- a second hot cache
- a replacement for the local thread
- a replacement for durable wiki/docs memory

## When to use it

Use reset handoff when all three are true:
1. a real reset, long idle gap, or likely session boundary exists
2. the exact next move would be ambiguous without a handoff
3. the information is too current/narrow for durable memory but too important to lose between sessions

If the current thread is still available and sufficient, use that first.

## Read order

On wake-up/resume, DAOS prefers:
1. local thread / reply target / immediate recent turns
2. `wiki/cache/hot-cache.md`
3. `wiki/cache/hot-cache-log.md` only when local context is thin or recent front-door prune/rescope history is genuinely needed
4. `wiki/cache/reset-handoff.md` when the resume follows reset or long idle
5. `wiki/cache/agent-continuity.md` if broader lane recovery is still needed
6. deeper wiki reconstruction and verified runtime/files

## Canonical file shape

```md
# Reset Handoff

Use this as the named DAOS reset/wake-up continuity artifact.

## Current Handoff
**Last updated:** YYYY-MM-DD HH:MM TZ
**Updated by:** Agent / Runtime
**Lane:** [lane]
**Status:** empty | fresh | stale | blocked

- Why this handoff exists:
- Exact next move:
- First verification:
- If stale or contradicted:
```

## Field meanings

- **Last updated** — freshness marker for the current handoff
- **Updated by** — agent/runtime that wrote it
- **Lane** — the lane or focus item this handoff belongs to
- **Status**
  - `empty` = no meaningful handoff currently needed
  - `fresh` = safe to use as the narrow wake-up point
  - `stale` = historical clue only; verify before trusting
  - `blocked` = the next session should expect a blocker rather than clean continuation
- **Why this handoff exists** — short explanation of why a reset-gap handoff is needed
- **Exact next move** — the one concrete next step, not a broad project summary
- **First verification** — the first reality check before continuing
- **If stale or contradicted** — what source should win or where to look next

## Writing rules

- overwrite instead of append
- keep one active handoff, not a diary
- prefer one narrow next move over a broad summary
- point to durable notes or files instead of duplicating their content
- clear or rewrite when the exact handoff changes materially

## Runtime expectations

A runtime integration should, at minimum:
- be able to write the file before or during ordinary work when exact resume ambiguity appears
- read it on the first turn after reset/long idle before broader continuity recovery
- avoid treating it as higher authority than live files/runtime/wiki truth
- avoid letting it silently replace hot-cache scope or durable memory

## Relationship to adjacent surfaces

- **Local thread** = best exact handoff when it still exists
- **Hot cache** = shared front door for what matters now
- **Reset handoff** = exact wake-up move after reset/long idle
- **Agent continuity** = broader resumable state for one agent/lane
- **Wiki/docs memory** = durable shared truth
- **Live reality** = current source of truth for operational facts

## Design stance

Reset handoff is intentionally small.

It exists to harden wake-up quality without creating another heavy memory layer.
