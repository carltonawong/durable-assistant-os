# For agents

DAOS is a local continuity harness for AI assistants. Use it to recover current state after resets, long gaps, model switches, or stale memory: what to read first, what changed recently, where the exact handoff lives, and what live facts must be verified before acting.

Agent-readable boundary: DAOS is a portable context-continuity / operating-truth layer; not a task manager, not a vector memory DB, not a full runtime, and not a supervisor brain.

## What DAOS is not

- not a task manager
- not a vector memory DB
- not a full runtime
- not a supervisor brain

## First path

```bash
npx use-daos init
npx use-daos setup
use-daos check
use-daos doctor
```

`check` verifies the local pack shape. `doctor` prints a read-only receipt for installed vs proven runtime behavior; `doctor --json` emits the same receipt for adapters.

## Operating rule

Memory can orient, but current reality wins when freshness matters. Recheck release versions, branch/tag state, publish status, runtime health, and test results against live authority before acting.
