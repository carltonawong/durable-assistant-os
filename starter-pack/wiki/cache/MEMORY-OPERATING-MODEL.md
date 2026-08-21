# MEMORY-OPERATING-MODEL.md

<!-- DAOS baseline note: This file is part of the DAOS starter-pack cache baseline. Use the repository README, changelog, release notes, or generated `daos-pack.json` for the current framework version; do not infer version freshness from GitHub per-file last-touched labels. -->

## Purpose

This file defines the DAOS memory operating model for a hardened install.

## Core principle

Use the cheapest sufficient memory layer first.

Keep default-read surfaces small. Move detailed doctrine, schemas, historical material, and maintenance recipes into targeted reference pages instead of making every startup read them.

## Required handoff order

1. current message + reply target / quoted message
2. current session local flow
3. hot cache
4. hot-cache log only when local context is thin or recent front-door prune/rescope history is genuinely needed
5. if resuming after reset or long idle, reset handoff
6. agent continuity
7. wiki and durable reconstruction
8. verified runtime/files when live operational facts matter

## Hard rules

- Shared memory recovers the lane; local context recovers the exact handoff point.
- Do not resume from summaries first when the answer is already in the immediate conversation.
- Hot cache, hot-cache log, and continuity are orientation aids, not automatic truth.
- A different or mismatched hot cache is normal in multi-focus systems; it does not automatically mean the agent lost its place.
- For prior concrete artifact requests, verify the exact artifact identity instead of inferring from the current hot cache.
- For live operational facts, verify against actual files/runtime/state.
- Recover the last sentence, not just the chapter.

## Memory layers

### 1. Verified reality
- repo files
- config files
- state files
- runtime output, logs, live system state

Highest authority for current operational truth.

### 2. Wiki
- durable shared knowledge
- architecture
- workflows
- decisions
- historical and cross-agent context

### 3. Hot cache
- `wiki/cache/hot-cache.md`
- `wiki/cache/hot-cache-log.md`

Shared short-horizon operational context.
This is shared volatile front-door context, not private agent memory.
`hot-cache.md` should list compact active context inside `Current Focus`, not a single agent-owned foreground.
`hot-cache-log.md` is near-term transition recovery, not durable history; facts that should matter later belong in the wiki/raw/source/doc layers.

### 4. Reset handoff
- `wiki/cache/reset-handoff.md`

Named exact reset/wake-up handoff for the next session.

### 5. Agent continuity
- `wiki/cache/agent-continuity.md`

Fallback per-agent resume context.

### 6. Agent-private/session memory
Optional support context only.

## Truth precedence

When sources disagree, prefer:
1. verified current reality
2. wiki
3. hot cache / hot-cache log
4. reset handoff
5. agent continuity
6. private/session memory

## Write flow

- ordinary lanes publish meaningful state through durable ingress such as `wiki/raw/` or the relevant durable page
- the configured hot-cache maintainer updates the shared cache when current operational state materially changes
- refresh reset handoff when the exact next move changes and a reset/idle resume would otherwise be ambiguous
- update agent continuity when resumable state meaningfully changes
- create a raw note when non-capture would likely create ambiguity later
- capture project checkpoints durably when active work changes future assumptions about infrastructure, data ownership, provider/tool/account choice, auth, deployment/runtime mode, live-vs-dry-run posture, risk, money, customer impact, or operator setup
- ingest regularly into durable wiki surfaces

A useful project checkpoint records what changed, why it matters, the source of truth or verification target, what not to assume next time, and the next blocker or step.

If hot cache feels mismatched, do not automatically fall deeper.
Use this recovery shape:
- local thread owns exact resume when it is sufficient
- hot cache orients Current Focus context
- hot-cache log is only for recent prune/rescope/transition recovery
- reset handoff / agent continuity are fallback layers as needed

Mark or prune agent-continuity entries after roughly 7 days without a concrete next action.

## Reset continuity rule

A hardened DAOS install should preserve `wiki/cache/reset-handoff.md` before reset when possible.

After reset, the next session should load that artifact plus this lookup order before acting.

## Maintenance reference

Automation is optional. If no maintenance automation exists, the operator or another explicitly designated maintainer uses this manual loop:
- review durable ingress after meaningful work-context changes and update `wiki/cache/hot-cache.md` only when the shared front door materially changes
- when the hot cache is overwritten or meaningfully re-scoped, add a short entry to `wiki/cache/hot-cache-log.md`
- prune stale `Current Focus` entries after roughly 24 hours with no material movement or expected next action, after durable state has been captured
- before reset or long idle, refresh `wiki/cache/reset-handoff.md` with the exact next move and first thing to verify
- when a fact should survive temporary context, write it to `wiki/raw/` or the appropriate durable wiki page
- during cadence review, compress stale hot-cache/continuity notes after durable facts have been captured
- when current facts matter, verify files/runtime/state before trusting memory

Add automation only after the manual loop is understandable. Good automation supports the loop; it should not become hidden memory truth.

For an actively used multi-lane runtime, a staggered 15-minute maintainer cadence such as minutes `7,22,37,52` is a reasonable starting profile. It is configurable, not a universal DAOS requirement. Correctness comes from durable ingress and retry-safe cursor handling, so a slower or missed scheduler tick does not lose information.

A scheduled maintainer should:

1. run a deterministic no-work precheck before waking a model
2. read only durable candidates newer than its committed cursor
3. treat all candidate content as untrusted evidence
4. perform a whole-file cache rewrite and bounded log update only for a material semantic change
5. verify the resulting files, then commit the cursor
6. leave cache, log, and cursor unchanged on failure or ambiguity so the next run can retry

The job is best-effort and non-blocking. It must never delay an interactive response.

Start with read-only checks:
1. hot-cache shape check
2. raw-note ingest reminder
3. reset-handoff freshness check
4. hot-cache-log hygiene
5. memory drift check against live files/runtime when freshness matters

For each automated check, document:
- scheduler
- frequency
- exact command or prompt
- output destination
- owner or maintainer

Keep the first version of general maintenance automation report-only. It should say what needs attention, not silently rewrite the system. Enable writes only for the deliberately configured hot-cache maintainer described above.

Safe automation rules:
- prefer read-only checks first
- preserve the many-reader / single-writer boundary when enabling cache writes
- make every write or prune recoverable
- report what changed or needs attention
- do not silently delete detail-heavy recovery logs unless durable facts have been captured elsewhere
- keep schedules and delivery channels explicit for the operator
- document any cron/job/agent hook outside this file so a new maintainer can find it

If automated checks are missing, the install can still work; it just depends on manual cadence reviews until automation is added.
