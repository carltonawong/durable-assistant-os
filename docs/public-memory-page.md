# DAOS Public Memory Model

## Opening block

Long-running assistants can lose the right foreground when multiple lanes stay live at once. That usually happens because short-term memory layers can conflict across threads, sessions, and tools. To keep that manageable, DAOS organizes memory into two families: **short-term / active memory** and **durable memory**.

In practice, read short-term memory in this order: **local thread first, then hot cache, then agent continuity, then deeper fallback reconstruction**. When short-term memory layers disagree, the local thread usually wins. **Trust the local thread first.**

## The two memory families

DAOS keeps memory simple at the top level by splitting it into two families: **short-term / active memory** and **durable memory**. Short-term / active memory helps an assistant hold the right foreground while work is live. Durable memory holds the knowledge that should survive session boundaries, tool changes, and longer stretches of time.

This split matters because not every memory failure is the same. Some problems come from losing the current thread; others come from losing the durable truth the system is supposed to build on. Short-term / active memory keeps work oriented in the moment. Durable memory keeps the system cumulative, portable, and trustworthy over time.

In practice, the short-term side includes the local thread, hot cache, and agent continuity. The durable side includes the wiki, canonical docs, reusable skills and methods, and optional per-agent support memory when it stores only small evergreen facts.

## Layers inside short-term / active memory

In DAOS, short-term / active memory is the small stack that keeps an assistant on the right live foreground. The layers do different jobs. Separating them keeps exact thread continuity, shared front-door context, and per-agent resume state from collapsing into one blurry memory bucket.

**Local thread context** comes first. This means the current message, any replied-to or quoted message, and the most recent turns in the current thread or session. It is the highest-signal layer for reconstructing the exact handoff point. Shared memory can recover the lane, but the local thread usually recovers the last sentence.

**Hot cache** comes next. In public framing, its job is best understood as a shared front door for what matters right now, with “tip of the tongue” describing the feel rather than replacing the function. It helps multiple agents or runtimes orient quickly to the current foreground, major corrections, and active risks. But it should not be treated as exact per-thread continuity, and it can become contested when multiple lanes are genuinely hot at once.

**Agent continuity** follows after hot cache. This should stay literal in public framing: it is a per-agent resumable note about what that agent was last doing and what it should verify before resuming. Its job is not to replace the thread or become a second profile store. It exists because shared front-door context is sometimes not enough to tell one specific agent how to pick its lane back up cleanly.

Taken together, these layers give DAOS a practical short-term read order: local thread first, then hot cache, then agent continuity, then deeper fallback reconstruction. They are complementary, not interchangeable. The local thread anchors exact continuity, hot cache shares the current foreground, and agent continuity preserves one agent’s resumable state when the other two layers are not enough.

## Layers inside durable memory

If short-term / active memory keeps an assistant oriented now, durable memory is what makes the system cumulative over time. In DAOS, this is where stable knowledge, decisions, canonical framing, and reusable structure are meant to live. The goal is not to store everything forever. It is to preserve what future agents or future sessions should not have to re-derive.

**The wiki** is the main durable shared memory layer. This is where shared truth across agents belongs: project definitions, architecture, canonical framing, synthesized findings, and durable decisions. For the DAOS memory model itself, the wiki is the primary canonical home rather than hot cache, chat residue, or one agent’s private memory.

**Canonical docs and repo docs** are the public-facing durable layer. They take stable doctrine already shaped in the wiki and express it in a form that can be shipped, read, and reused outside the original chat lane. In other words, durable memory is not complete until the ideas that matter publicly have been compiled into documentation someone else could actually use.

**Skills and reusable methods** are also part of durable memory, but with a narrower role. Their job is to operationalize how to do something repeatedly. They should usually reflect canonical wiki truth rather than quietly becoming a second doctrine store. If a durable conceptual framing emerges in a skill first, it should be reconciled back into the wiki and any relevant repo docs.

**Private agent memory** belongs at the bottom of the durable stack as an optional support layer. It is often useful in practice, but it should stay narrow: small evergreen facts such as preferences, recurring corrections, or stable environment quirks. It is not the place for canonical doctrine, shared current-lane state, or hidden work-log continuity.

Taken together, durable memory in DAOS is the layer family that keeps the system portable, trustworthy, and resistant to drift. The wiki holds shared truth, docs make that truth publishable, skills preserve reusable operating methods, and private agent memory provides a small amount of stack-specific support without replacing the more canonical layers above it.

## Conflict resolution

Conflict resolution in DAOS starts with a simple rule: when short-term / active memory surfaces disagree, trust the local thread first. This is the Thread Priority Rule. It exists because the current message, reply target, and recent turns are usually the highest-signal source for what the assistant is actually being asked to do right now. Hot cache, agent continuity, and other recent lane residue can help orient the assistant, but they are fallback layers, not the default winner.

This rule is more than a lookup order. It is also a behavioral default. If the immediate thread and the assistant’s own recently active lane memory feel in tension, the assistant should stay with the thread unless there is stronger evidence that directly contradicts that read. In practice, stronger evidence means a higher-authority and more directly relevant source such as explicit user clarification in the thread, verified files or runtime state when the dispute is about live reality, or canonical durable docs when the dispute is about stable doctrine.

Just as important, the Thread Priority Rule is scoped. It governs conflicts inside short-term / active memory surfaces: local thread context, hot cache, agent continuity, and other recent lane residue. It does **not** mean that a live thread silently overrides durable shared truth already compiled into the wiki or other canonical docs. If the conflict is about durable doctrine rather than immediate thread intent, the assistant should surface that mismatch, verify whether the user intends to change the doctrine, and update the durable layer explicitly if needed.

The practical conflict model is simple: local thread first for live short-term disagreements, stronger evidence only when directly relevant, and durable truth changed only on purpose. That keeps DAOS responsive in the moment without letting one active conversation accidentally rewrite the system’s longer-term memory.

## When to use which layers

In practice, DAOS works best when each layer is used for the kind of memory it is actually good at. If every layer is used for everything, the system gets blurry fast. The simplest rule is: use the cheapest layer that can answer the current question without pretending it is more authoritative than it is.

Use **local thread context** when you need the exact handoff point, the latest user steer, or the meaning of the current exchange. Use **hot cache** when you need a quick shared front door for what matters now across agents or runtimes. Use **agent continuity** when the hot cache is not enough and one specific agent needs help resuming its own lane cleanly.

Use **the wiki** when the information should become durable shared truth: architecture, project definitions, stable decisions, synthesized findings, and canonical framing. Use **skills** when the question is procedural and reusable: how to perform a workflow repeatedly, not just what the system currently believes. Use **repo docs** when the material needs to be public-facing, project-facing, or packaging-ready for someone outside the original chat lane.

Use **private agent memory** only for small evergreen support facts that help one agent avoid relearning the same preferences, recurring corrections, or environment quirks. It is useful when present, but it should stay narrow and should not compete with the wiki for canon or with continuity layers for current work state.

A practical DAOS read path therefore looks like this: local thread first for exact continuity, hot cache and agent continuity for active-memory recovery, wiki for durable shared truth, skills for reusable operating method, and repo docs for published expression. If a fact needs to survive and be shared, move it upward into the durable layers. If it only needs to help in the current moment, keep it in the short-term ones.

## Maintenance / update posture

DAOS is not designed as a memory system that stays healthy by accident. Its maintenance posture is deliberate: keep the write path simple, automate ingest where possible, and make hygiene a recurring behavior rather than a once-in-a-while cleanup project. The goal is not just to preserve facts, but to resist drift, sprawl, and stale context over time.

The write path should stay low-friction. When a meaningful discovery, correction, decision, or workflow change appears, capture it in a compact dated raw note or write it directly into the wiki if you are already in maintenance mode. Do not force full curation in the middle of live work. The important thing is that durable material does not get stranded in chat, hot cache, or private scratch memory.

A useful DAOS hardening rule is second-pass escalation: if a review pass makes it obvious that the write-up contains incident chronology, repeated micro-remediations, debugging sequence, or lessons about where information should live, treat that realization itself as evidence that durable capture is needed. In that same pass, compress the hot cache back to front-door context and move the fuller sequence into a raw note or durable page.

From there, ingest can be scheduled or opportunistic. A practical DAOS pattern is: agents capture raw notes quickly, an ingest pass promotes them into durable wiki pages, and index/log surfaces are updated so the new knowledge becomes discoverable. Hot cache and agent continuity should also be refreshed when shared operational state or resumable lane state has meaningfully changed, but they should stay compact and front-door only.

Hygiene should be explicit and recurring. Daily anti-bloat review helps catch accidental cache drift, duplicate notes, or overgrown temporary memory. A deeper weekly consolidation or pruning pass helps merge overlapping sources, compress stale detail, and keep the durable layers readable. This is why DAOS treats maintenance as part of the product behavior, not as a nice-to-have manual discipline.

The overall posture is simple: capture quickly, promote durably, compress regularly, and verify against reality when live state matters. A durable assistant should become clearer and more trustworthy over time, not more cluttered.

## Closing note

DAOS is meant to make durable assistant memory simpler, not heavier. The point of this model is to keep the right foreground live, preserve the right truths over time, and make those truths portable across sessions, tools, and agents without turning memory into a bureaucratic system of its own.
