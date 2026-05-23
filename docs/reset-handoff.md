# DAOS Reset Handoff

`wiki/cache/reset-handoff.md` is the narrow reset/wake-up continuity artifact. It preserves the exact next move and first verification after reset, idle, or handoff without becoming a log, transcript, or source of truth.

Use it when local thread context may be unavailable or insufficient and the next move would blur.

## Read order

On wake-up/resume: local thread first; hot cache second; hot-cache log only for genuine recent rescope recovery; reset handoff after reset/idle/handoff; agent continuity only for broader fallback; then durable wiki/source notes and verified runtime/files.

## Canonical file shape

One `Current Handoff` section with: `Last updated`, `Updated by`, `Lane`, `Status`, `Why this handoff exists`, `Exact next move`, `First verification`, and `If stale or contradicted`.

## Field meanings

- `Last updated` / `Updated by` — freshness and provenance.
- `Lane` — the lane or workstream this handoff belongs to.
- `Status` — `empty` = none needed; `fresh` = current enough to review; `stale` = historical clue only; `blocked` = expect a blocker.
- `Why this handoff exists` — why reset-gap recovery is needed.
- `Exact next move` — one concrete step, not a broad summary.
- `First verification` — first reality check before continuing.
- `If stale or contradicted` — what source wins or where to look next.

## Lifecycle, trust, and quality

Keep stored state, effective trust, and quality separate. `fresh` means reviewable, not automatically safe to adopt.

Semantic durability is a separate quality bar. A lifecycle-valid handoff is weak if it only says "review session history" or "continue current task" while nearby work objects share vocabulary.

A semantically durable handoff carries: work-object identity; active source of truth; last verified state; current ask/decision; nearby confusion set; required re-anchor checks; and freshness/confidence (`fresh`, `stale-risk`, `partial`, `generated fallback`, `blocked`, etc.).

Weak handoffs should trigger re-anchor behavior: verify the source of truth or ask instead of confidently adopting a plausible neighboring context.

## Writing rules

- overwrite instead of append
- keep one active handoff, not a diary
- prefer one narrow next move over a broad summary
- point to durable notes/files instead of duplicating them
- clear or rewrite when the exact handoff changes materially
- label thin context as generated/partial and include known gaps

## Runtime expectations

A runtime integration should write the file when exact-resume ambiguity appears, read it on first turn after reset/idle before broader fallback, keep live truth higher authority, normalize lifecycle before reporting, and warn on weak/generated fresh handoffs.

## Adjacent surfaces

Local thread wins when present; hot cache is the shared front door; reset handoff is the exact wake-up move; agent continuity is broader fallback; wiki/docs are durable truth; live reality outranks all memory for current facts.
