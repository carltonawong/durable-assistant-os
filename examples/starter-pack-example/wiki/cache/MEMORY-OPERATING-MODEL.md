# MEMORY-OPERATING-MODEL.md

## Purpose

This file defines the DAOS memory operating model for a hardened install.

## Core principle

Use the cheapest sufficient memory layer first.

## Required handoff order

1. current message + reply target / quoted message
2. current session local flow
3. hot cache
4. if front-door context feels incongruent, hot-cache log
5. if resuming after reset or long idle, reset handoff
6. agent continuity
7. wiki and durable reconstruction
8. verified runtime/files when live operational facts matter

## Hard rules

- Shared memory recovers the lane; local context recovers the exact handoff point.
- Do not resume from summaries first when the answer is already in the immediate conversation.
- Hot cache, hot-cache log, and continuity are orientation aids, not automatic truth.
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

### 4. Agent continuity
- `wiki/cache/agent-continuity.md`

Fallback per-agent resume context.

### 5. Reset handoff
- `wiki/cache/reset-handoff.md`

Named exact reset/wake-up handoff for the next session.

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

- update hot cache when shared current operational state changes
- refresh reset handoff when the exact next move changes and a reset/idle resume would otherwise be ambiguous
- update agent continuity when resumable state meaningfully changes
- create a raw note when non-capture would likely create ambiguity later
- ingest regularly into durable wiki surfaces

## Reset continuity rule

A hardened DAOS install should preserve `wiki/cache/reset-handoff.md` before reset when possible.

After reset, the next session should load that artifact plus this lookup order before acting.
