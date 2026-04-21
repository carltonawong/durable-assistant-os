# AGENTS.md

This install uses the DAOS mandatory baseline.

Before acting on current operational context:
1. read the current message / reply target / recent thread flow first
2. read `wiki/cache/hot-cache.md`
3. if the front door feels incongruent, read `wiki/cache/hot-cache-log.md`
4. if resuming after reset or long idle, read `wiki/cache/reset-handoff.md`
5. if still unsure what you were last doing, read `wiki/cache/agent-continuity.md`
6. for durable shared knowledge, use the wiki
7. for live operational truth, verify against files/runtime/state

## Hard rules

- Do not treat remembered notes as automatically current.
- Do not let hot cache or continuity override the immediate thread on their own.
- For live facts, verified reality outranks memory.
- If not recording something would likely create ambiguity, repeated investigation, or false assumptions later, write a dated raw note under `wiki/raw/`.
- Keep `hot-cache.md` compact and front-door only.
- Use `hot-cache-log.md` as fallback reconstruction context, not primary working memory.
- Use `reset-handoff.md` for exact post-reset/wake-up recovery, not as a running log.
- Use `agent-continuity.md` only after hot cache and hot-cache log are not enough.

## Reset / wake-up rule

This install should preserve `wiki/cache/reset-handoff.md` as the named reset/wake-up artifact before reset when possible.

After reset or long idle wake-up:
- recover the current thread first
- load `wiki/cache/reset-handoff.md`
- follow the DAOS lookup order above before acting

## Maintenance rule

This install assumes recurring upkeep exists for ingest, compression, audits, hygiene, and reset-continuity verification.

If those loops are missing or stale, the install is not fully hardened.
