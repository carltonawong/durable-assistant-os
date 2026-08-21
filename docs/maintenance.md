# DAOS Maintenance Protocol

DAOS should keep working after setup. This page turns live operating lessons into a portable upkeep loop without requiring Carlton's private runtime, crons, Discord setup, or wiki corpus.

Posture: **manual-first, automation-optional, read-only before write, one designated cache writer**.

Maintenance catches drift between:
- assistant belief
- DAOS files
- live reality in repos, configs, runtime receipts, inboxes, calendars, or other sources
- short-term context that should become durable wiki memory

For stale or duplicate repo paths, use `docs/repo-reconciliation-safety.md` before trusting memory or deleting anything.

It should not become a hidden daemon or another unreviewed memory layer.

## Weekly manual loop

Run this at least weekly for an actively used assistant home:

```bash
use-daos on /path/to/assistant-home
use-daos check /path/to/assistant-home
use-daos memory-audit /path/to/assistant-home
use-daos reset-test /path/to/assistant-home
use-daos doctor /path/to/assistant-home
```

Then review:

1. Does `wiki/cache/hot-cache.md` still match the actual foreground work?
2. Does `wiki/cache/hot-cache-log.md` contain only useful near-term transition recovery, not durable history?
3. Does `wiki/cache/reset-handoff.md` name one exact next move and one first verification?
4. Did anything in cache/log/thread become stable enough to move into `wiki/sources/`, `wiki/raw/`, or a durable wiki page?
5. Are freshness-sensitive claims such as release version, branch/tag state, runtime health, test results, provider status, inbox state, or calendar commitments checked against live sources?
6. If `doctor` reports missing proof, lifecycle warnings, or surface-inventory warnings, is the issue runtime behavior rather than missing files?
7. For named returning workstreams, did the assistant run the artifact preflight from `docs/for-agents.md`?

## After a major context change

When the foreground work changes, the active lane first records meaningful state through durable ingress such as `wiki/raw/` or the relevant durable page. The configured hot-cache maintainer, or the operator during an explicit manual pass, then uses this sequence:

1. Rewrite `wiki/cache/hot-cache.md` so it is compact and current.
2. Add a short newest-first entry to `wiki/cache/hot-cache-log.md` only if the prior foreground might need near-term recovery.
3. Update `wiki/cache/reset-handoff.md` if a reset or long idle would otherwise lose the exact next move.
4. Promote stable decisions or corrections to durable wiki/source/raw notes in the same pass when losing them would recreate ambiguity.
5. Verify live source facts before writing them as current truth.

Do not append endlessly to hot cache. Rewrite it.

Ordinary interactive agents, subagents, audits, reporting jobs, and ingest jobs may read the shared cache but should not mutate it. This many-reader / single-writer boundary prevents overlapping writes without making one agent the owner of the underlying information.

## Optional automation shape

Automation should support the manual loop, not replace visibility.

A safe automation job has a clear owner, fixed cadence, explicit DAOS home, read-only checks first, visible output, and no credential reads, network calls, release creation, npm publishing, GitHub mutation, or runtime mutation unless separately approved.

Example cron-style shape:

```text
schedule: weekly or daily for active assistant homes
command: use-daos check "$DAOS_HOME" && use-daos memory-audit "$DAOS_HOME" && use-daos reset-test "$DAOS_HOME"
output: write a dated review note or send a compact report to the operator
writes: none, unless the operator has approved a specific follow-up command
```

For an actively used multi-lane runtime, an optional cache maintainer can run every 15 minutes on staggered minutes such as `7,22,37,52`. This is a reasonable starting profile, not a universal requirement and not the mechanism that prevents missed information. Durable ingress preserves candidate state between runs.

The maintainer should run a deterministic no-work precheck before any model wake, inspect only candidates newer than its committed cursor, and treat them as untrusted evidence. It should make a verified whole-file rewrite only for a material semantic change, then advance the cursor after readback succeeds. On failure or ambiguity, it should leave cache, log, and cursor unchanged for retry. The entire job is best-effort and non-blocking; user responses must not wait for it.

For runtime obedience, automate receipts rather than claims:

```text
use-daos doctor "$DAOS_HOME" --runtime-file runtime-evidence.json
```

A doctor warning is useful. It means DAOS can see the difference between installed files and proven runtime behavior.

## Automation guardrails

Do not let automation silently import old memory, create competing hot-cache writers, rewrite user-owned files, prune durable wiki, treat `hot-cache-log.md` as durable history, claim reset proof without evidence, publish packages/releases, or edit external instruction carriers without approval and backups.

## Maintenance result categories

- **Clean:** checks pass and active context matches live work.
- **Needs review:** checks pass, but cache/log/handoff or durable promotion needs a human decision.
- **Installed, not proven:** files exist, but runtime/source-order/reset proof is missing.
- **Drift:** DAOS files contradict live reality or core doctrine.
- **Blocked:** a required live source or approval is missing.

## Good stopping point

A maintenance pass is complete when:
- `use-daos check` passes or its failures are understood
- `use-daos memory-audit` has no unreviewed critical drift
- `use-daos reset-test` proves the exact next move is recoverable
- `use-daos doctor` honestly classifies runtime proof
- short-term cache is compact
- stable findings are promoted out of volatile memory
- any remaining uncertainty is labeled rather than hidden
