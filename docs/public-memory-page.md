# DAOS Public Memory Model

## Opening block

Long-running assistants can lose the right foreground when multiple lanes stay live at once. That usually happens because short-term memory layers can conflict across threads, sessions, and tools. To keep that manageable, DAOS organizes memory into two families: **short-term / active memory** and **durable memory**.

In practice, read short-term memory in this order: **local thread first, then hot cache, then agent continuity, then deeper fallback reconstruction**. When short-term memory layers disagree, the local thread usually wins. **Trust the local thread first.**

## The two memory families

DAOS keeps memory simple at the top level by splitting it into two families: **short-term / active memory** and **durable memory**. Short-term / active memory helps an assistant hold the right foreground while work is still live. Durable memory holds the knowledge that should survive session boundaries, tool changes, and longer stretches of time.

This split matters because not every memory failure is the same. Some problems come from losing the current thread; others come from losing the durable truth the system is supposed to build on. Short-term / active memory exists to keep work oriented in the moment. Durable memory exists to keep the system cumulative, portable, and trustworthy over time.

At a practical level, the short-term side includes layers like the local thread, hot cache, and agent continuity. The durable side includes the wiki, canonical docs, reusable skills and methods, and optional per-agent support memory when it stores only small evergreen facts.

## Layers inside short-term / active memory

_Draft pending. Locked doctrine already established in the DAOS wiki; this repo draft preserves the accepted opening and two-family framing first._

## Layers inside durable memory

_Draft pending._

## Conflict resolution

Current locked doctrine for this page:
- local thread first
- the Thread Priority Rule governs short-term / active memory conflicts only
- durable truth is not silently overridden by live thread context
- hot cache is a front door, not a replacement for durable truth

## When to use which layers

_Draft pending._

## Maintenance / update posture

_Draft pending._

## Status

This page is the first repo-integrated DAOS public memory draft. It preserves the currently locked public doctrine and is ready for the remaining sections to be filled in from the existing DAOS source trail.
