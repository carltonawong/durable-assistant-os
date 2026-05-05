# AGENTS.md

This install uses the DAOS mandatory baseline.

## Default read path

Before acting on current operational context, use the cheapest sufficient surface:

1. current message / reply target / recent thread flow
2. `wiki/cache/hot-cache.md`
3. `wiki/cache/hot-cache-log.md` only when local context is thin or recent front-door prune/rescope history is genuinely needed
4. `wiki/cache/reset-handoff.md` only after reset or long idle
5. `wiki/cache/agent-continuity.md` only if the above is not enough
6. durable wiki pages only when shared long-term knowledge is needed
7. live files/runtime/state when current operational truth matters

## Hard rules

- Do not treat remembered notes as automatically current.
- Do not let hot cache or continuity override the immediate thread on their own.
- For live facts, verified reality outranks memory.
- If not recording something would likely create ambiguity, repeated investigation, or false assumptions later, write a dated raw note under `wiki/raw/`.
- During active project work, capture a durable checkpoint when a step changes infrastructure, data ownership, provider/tool/account choice, auth, deployment/runtime mode, live-vs-dry-run posture, risk, money, customer impact, or operator setup assumptions.
- A project checkpoint should say what changed, why it matters, the source of truth or verification target, what not to assume next time, and the next blocker or step.
- Keep `hot-cache.md` compact and front-door only.
- Use `hot-cache-log.md` as near-term transition recovery when the front door was recently overwritten, not as primary working memory or durable history.
- Use `reset-handoff.md` for exact post-reset/wake-up recovery, not as a running log.
- Use `agent-continuity.md` only after local context, hot cache, and any genuinely needed hot-cache log context are not enough; mark/prune entries after roughly 7 days without a concrete next action.
- If the current thread fits an existing `Current Focus` entry in `hot-cache.md`, continue from local context and the durable record; do not rewrite the hot cache just to claim foreground.

## Reset / wake-up rule

This install should preserve `wiki/cache/reset-handoff.md` as the named reset/wake-up artifact before reset when possible.

After reset or long idle wake-up:
- recover the current thread first
- load `wiki/cache/reset-handoff.md`
- follow the DAOS lookup order above before acting

## Maintenance

Normal loop:

- update `wiki/cache/hot-cache.md` after meaningful work-context changes
- add a short `wiki/cache/hot-cache-log.md` entry when the front door is overwritten or re-scoped
- prune stale `Current Focus` entries after roughly 24 hours with no material movement or expected next action, after durable state has been captured
- refresh `wiki/cache/reset-handoff.md` before reset or long idle
- write durable facts to `wiki/raw/` or durable wiki pages
- compress stale temporary notes after durable facts have been captured

Read `wiki/cache/MEMORY-OPERATING-MODEL.md` only when you need the fuller memory, maintenance, or automation reference. Do not make every startup pay for that doctrine.
