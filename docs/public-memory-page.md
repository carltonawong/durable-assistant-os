# DAOS Public Memory Model

## Opening block

Long-running assistants can lose the right foreground when multiple lanes stay live at once. That usually happens because short-term memory layers can conflict across threads, sessions, and tools. To keep that manageable, DAOS organizes memory into two families: **short-term / active memory** and **durable memory**.

In practice, read short-term memory in this order: **local thread first, then hot cache, then agent continuity, then deeper fallback reconstruction**. When short-term memory layers disagree, the local thread usually wins. **Trust the local thread first.**

## The two memory families

DAOS keeps memory simple at the top level by splitting it into two families: **short-term / active memory** and **durable memory**. Short-term / active memory helps an assistant hold the right foreground while work is still live. Durable memory holds the knowledge that should survive session boundaries, tool changes, and longer stretches of time.

This split matters because not every memory failure is the same. Some problems come from losing the current thread; others come from losing the durable truth the system is supposed to build on. Short-term / active memory exists to keep work oriented in the moment. Durable memory exists to keep the system cumulative, portable, and trustworthy over time.

At a practical level, the short-term side includes layers like the local thread, hot cache, and agent continuity. The durable side includes the wiki, canonical docs, reusable skills and methods, and optional per-agent support memory when it stores only small evergreen facts.

## Layers inside short-term / active memory

In DAOS, short-term / active memory is the small stack that helps an assistant stay on the right live foreground. It is not one thing, and the layers do not do the same job. The point of separating them is to keep exact thread continuity, shared front-door context, and per-agent resume state from collapsing into one blurry memory bucket.

**Local thread context** comes first. This means the current message, any replied-to or quoted message, and the most recent turns in the current thread or session. This is the highest-signal layer for reconstructing the exact handoff point. Shared memory can recover the lane, but the local thread usually recovers the last sentence.

**Hot cache** comes next. In public framing, its job is best understood as a shared front door for what matters right now, with “tip of the tongue” describing the feel rather than replacing the function. It helps multiple agents or runtimes orient quickly to the current foreground, major corrections, and active risks. But it should not be treated as exact per-thread continuity, and it can become contested when multiple lanes are genuinely hot at once.

**Agent continuity** follows after hot cache. This should stay literal in public framing: it is a per-agent resumable note about what that agent was last doing and what it should verify before resuming. Its job is not to replace the thread and not to become a second profile store. It exists because shared front-door context is sometimes not enough to tell one specific agent how to pick its lane back up cleanly.

Taken together, these layers give DAOS a practical short-term read order: local thread first, then hot cache, then agent continuity, then deeper fallback reconstruction. They are complementary, not interchangeable. The local thread anchors exact continuity, hot cache shares the current foreground, and agent continuity preserves one agent’s resumable state when the other two layers are not enough.

## Layers inside durable memory

If short-term / active memory keeps an assistant oriented now, durable memory is what makes the system cumulative over time. In DAOS, this is where stable knowledge, decisions, canonical framing, and reusable structure are supposed to live. The goal is not to store everything forever. The goal is to preserve what future agents or future sessions should not have to re-derive.

**The wiki** is the main durable shared memory layer. This is where shared truth across agents belongs: project definitions, architecture, canonical framing, synthesized findings, and durable decisions. For the DAOS memory model itself, the wiki is the primary canonical home rather than hot cache, chat residue, or one agent’s private memory.

**Canonical docs and repo docs** are the public-facing durable layer. They take the stable doctrine already shaped in the wiki and express it in a form that can be shipped, read, and reused outside the original chat lane. In other words, durable memory is not complete until the ideas that matter publicly have been compiled into documentation someone else could actually use.

**Skills and reusable methods** are also part of durable memory, but with a narrower role. Their job is to operationalize how to do something repeatedly. They should usually reflect canonical wiki truth rather than quietly becoming a second doctrine store. If a durable conceptual framing emerges in a skill first, it should be reconciled back into the wiki and any relevant repo docs.

**Private agent memory** belongs at the bottom of the durable stack as an optional support layer. It is often useful in practice, but it should stay narrow: small evergreen facts such as preferences, recurring corrections, or stable environment quirks. It is not the place for canonical doctrine, shared current-lane state, or hidden work-log continuity.

Taken together, durable memory in DAOS is the layer family that keeps the system portable, trustworthy, and resistant to drift. The wiki holds shared truth, docs make that truth publishable, skills preserve reusable operating methods, and private agent memory provides a small amount of stack-specific support without replacing the more canonical layers above it.

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
