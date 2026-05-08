# Reset current-state receipt

## Purpose

This is a small public-safe proof shape for reset recovery.
It shows how DAOS should help an assistant continue after a reset or long gap without treating remembered context as current truth.

The goal is not to preserve every detail.
The goal is to preserve the next safe move, the approval boundary, and the first thing to verify.

## Before reset

A useful receipt should capture:

- **Objective:** what outcome the assistant was helping with.
- **Current state:** what was last known, with a timestamp or source when available.
- **Last verified result:** the strongest live check already performed.
- **Pending decision:** what needs a human choice or stronger evidence.
- **Approval boundary:** what must not happen without explicit approval.
- **Stale risk:** what might change before the assistant resumes.
- **Next action:** the smallest concrete continuation step.

Example:

```md
Objective: Prepare a small docs/test hardening patch.
Current state: Branch is open with one commit; local tests passed before reset.
Last verified result: release-front-door and package tests passed locally.
Pending decision: wait for CI before merging.
Approval boundary: no tag, release, or npm publish.
Stale risk: main branch or CI status may change while idle.
Next action: fetch main, check PR/CI state, then merge only if green.
```

## After reset

A DAOS-aligned assistant should:

1. Read the immediate user request and local thread first.
2. Use the hot cache or reset handoff to recover the lane.
3. Treat remembered status as orientation, not proof.
4. Recheck freshness-sensitive facts against live authority.
5. Continue only inside the recorded approval boundary.

For the example above, the assistant should not say "CI passed" just because the receipt says local tests passed.
It should run the live PR/check query first.

## What the assistant should refuse to trust blindly

The assistant should recheck these before acting or reporting confidently:

- branch and tag state
- PR and CI status
- release or publish state
- runtime or deployment health
- security/leak scan results
- test results after a rebase or upstream change

Memory can explain where to look.
It cannot certify these current-state claims on its own.

## Success criteria

A reset-current-state receipt works when the resumed assistant can answer:

- What am I trying to complete?
- What is the smallest safe next move?
- What live fact must I verify before acting?
- What must I not do without approval?
- Which remembered facts are now only stale clues?

If the assistant has to excavate chat history, broad session search, and unrelated logs before it can answer those questions, the receipt is too weak.

## Non-goals

This receipt is not:

- a full project plan
- a benchmark archive
- a replacement for tests
- a second hot cache
- permission to perform sticky external actions

Keep it short enough that a future assistant can use it before it becomes another memory pile.
