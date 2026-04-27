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
- Use `hot-cache-log.md` as near-term transition recovery when the front door was recently overwritten, not as primary working memory or durable history.
- Use `reset-handoff.md` for exact post-reset/wake-up recovery, not as a running log.
- Use `agent-continuity.md` only after hot cache and hot-cache log are not enough.

## Reset / wake-up rule

This install should preserve `wiki/cache/reset-handoff.md` as the named reset/wake-up artifact before reset when possible.

After reset or long idle wake-up:
- recover the current thread first
- load `wiki/cache/reset-handoff.md`
- follow the DAOS lookup order above before acting

## Manual maintenance protocol

Automation is optional. If no maintenance automation exists, use this manual loop:

- After meaningful work-context changes, update `wiki/cache/hot-cache.md`.
- When the hot cache is overwritten or meaningfully re-scoped, add a short entry to `wiki/cache/hot-cache-log.md`.
- Before reset or long idle, refresh `wiki/cache/reset-handoff.md` with the exact next move and first thing to verify.
- When a fact should survive temporary context, write it to `wiki/raw/` or the appropriate durable wiki page.
- During cadence review, compress stale hot-cache/continuity notes after durable facts have been captured.
- When current facts matter, verify files/runtime/state before trusting memory.

## Automated maintenance protocol

Automation is optional. Add it only after the manual loop is understandable.

Good automation supports the manual loop; it should not become hidden memory truth.

### What to automate first

Start with read-only checks:
1. hot-cache shape check: verify `hot-cache.md` stays compact and has the required sections
2. raw-note ingest reminder: report unprocessed notes in `wiki/raw/`
3. reset-handoff freshness check: warn if reset/idle recovery notes are stale or missing when the workflow depends on them
4. hot-cache-log hygiene: flag oversized logs, repeated no-op entries, and detail-heavy entries that should be promoted before pruning
5. memory drift check: compare durable claims against live files/runtime when freshness matters

### How to set it up

Use whatever scheduler your environment already trusts: cron, GitHub Actions, an assistant heartbeat, a local reminder, or a calendar task.

For each automated check, document three things in the operator's durable notes:
- schedule: when it runs
- command or prompt: exactly what it does
- delivery: where the report goes

Keep the first version report-only. It should say what needs attention, not silently rewrite the system.

### Recommended automation shape

Pick one scheduler and record the same fields for every check:
- scheduler
- frequency
- exact command or prompt
- output destination
- owner or maintainer

Minimum useful cadence:
- daily or weekly: report raw-note backlog and oversized hot-cache logs
- before reset or long idle: refresh `reset-handoff.md`
- weekly: review stale continuity, memory drift, and durable claims that may need live verification

Example cron-style setup:
- daily 09:00: report raw notes and oversized cache/log files
- weekly Friday: review memory drift and stale continuity
- before planned reset: refresh `wiki/cache/reset-handoff.md`

Example assistant-heartbeat setup:
- after meaningful work: ask whether `hot-cache.md` needs a compact update
- weekly: prompt for cadence review and raw-note ingest
- after long idle: check `reset-handoff.md` before resuming

### Safe automation rules

- prefer read-only checks first
- make every write or prune recoverable
- report what changed or needs attention
- do not silently delete detail-heavy recovery logs unless durable facts have been captured elsewhere
- keep schedules and delivery channels explicit for the operator
- document any cron/job/agent hook outside this file so a new maintainer can find it

If automated checks are missing, the install can still work; it just depends on manual cadence reviews until automation is added.
