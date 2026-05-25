# For agents

DAOS is a portable context-continuity / operating-truth layer. Use it to recover the right operating context after resets, long gaps, model switches, or stale memory.

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

`check` verifies the local pack shape. `doctor` is the read-only proof ladder for installed vs proven runtime behavior; `doctor --json` emits the same receipt for adapters.

## Operating rule

Memory can orient, but current reality wins when freshness matters. Recheck release versions, branch/tag state, publish status, runtime health, and test results against live authority before acting.
