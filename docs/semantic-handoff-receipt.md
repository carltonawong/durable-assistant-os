# Semantic handoff receipt

Portable evidence for `use-daos doctor --json` after compaction, reset, idle expiry, or handoff. It is not a task manager, supervisor, or cloud sync layer.

```json
{
  "semantic_handoff": {
    "work_object_identity": "lane:exact-work-object",
    "active_source_of_truth": "issue, file, ticket, or live system",
    "last_verified_state": "last fact checked against live authority",
    "current_user_ask": "active ask at handoff time",
    "nearby_confusion_set": ["similar wrong object", "plausible neighbor"],
    "required_reanchor_checks": ["first live fact to re-check"],
    "status": "verified"
  }
}
```

Statuses: `verified` = captured from current/live context; `generated_fallback` = bounded fallback, re-anchor before irreversible action; `stale_risk` = verify source of truth first.

Bad: "continue current task." Good: exact identity, truth source, last verified fact, active ask, confusing neighbors, and first recheck.
