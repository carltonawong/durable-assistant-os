# DAOS Memory Model

<!-- DAOS baseline note: Current public framework baseline is v0.1.6; this file remains part of the current release surface even if its original feature landed in an earlier patch. -->

## Goal

Use memory to make the assistant more useful over time without turning the system into a cluttered archive of everything it has ever seen.

DAOS does not treat memory as a prestige feature.
It treats memory as core infrastructure inside an agent-agnostic operating harness: the shared continuity layer that lets durable collaboration survive across sessions, tools, and even agent swaps.

## Core stance

A durable assistant needs memory, but only the kinds of memory that improve real assistance.

The default failure modes are:
- too little memory, which forces the user to repeat themselves
- too much memory, which creates noise, stale assumptions, and maintenance overhead
- the wrong kind of memory, which makes the assistant sound informed while being operationally wrong

DAOS tries to avoid all three.

## Memory model at a glance

For public packaging, the simplest useful summary is:
- **shared durable memory** holds the important long-lived facts and decisions
- **private agent memory** is optional and stays tiny
- **current working context** tracks what matters right now
- **source-of-truth reality** is what the assistant verifies before acting

That is enough to explain the model without dragging readers through internal implementation detail.

## What memory is for

Memory should help the assistant:
- remember durable user preferences and standing context
- keep track of the minimum current state needed for ongoing work
- preserve important decisions so they do not need to be rediscovered
- reduce repeated explanation and setup friction
- stay oriented across sessions without pretending old notes are always true

## What memory is not for

Memory is not an excuse to keep everything.

It should not become:
- a full transcript warehouse presented as if it were judgment
- a substitute for checking live files, systems, or runtime state
- an ever-growing collection of duplicated notes
- a place to store every temporary plan, status update, or half-formed idea forever

If information is easy to re-derive, not durable, or no longer useful, it usually should not stay in the core memory surface.

## The minimum-viable-memory approach

DAOS favors a small number of memory layers with clear jobs.

A practical model usually needs at least these distinctions:

### 1. Durable user knowledge
This is the long-lived layer.

Examples:
- stable preferences
- recurring responsibilities
- communication style preferences
- durable project context that stays relevant over time
- behavioral rules that the assistant should not repeatedly relearn

This layer should change slowly.

### Durable wiki page governance
When durable memory lives in markdown wiki/docs pages, the pages themselves need lightweight governance.

At minimum, durable pages should carry a small canonical header:
- `Type`
- `Status`
- `Summary`
- `Last Updated`

For drift-prone operational pages, add:
- `Location`
- `Source of Truth`
- `Last Verified`

Keep one distinction explicit:
- `Status` = lifecycle of the page itself
- `State` = condition of the thing the page describes

That is different from DAOS pack-schema objects like `LaneSnapshot.status`, which still refers to lane operating state rather than page lifecycle.

For the fuller doctrine, see `docs/wiki-governance.md`.

### Private agent memory
Some assistants also carry a small private memory layer of their own.

This should usually stay limited to tiny evergreen support facts, for example:
- stable user preferences
- recurring corrections
- stable environment quirks
- small conventions that help the assistant avoid repeated mistakes

It is useful, but it should not become the home for shared doctrine, canonical project definitions, or current shared lane state.
Those belong in shared memory, not mainly inside one agent.

It should also stay separate from agent continuity:
- private agent memory = what this agent tends to remember about the user or environment
- agent continuity = what this agent was last working on and what it should verify before resuming

That boundary matters because private memory should not become a hidden work log, and continuity should not become a second preference/profile store.

In a personal stack, this same layer may appear under different agent-specific names or mechanisms:
- Hermes memory
- Claude Code local memory or instruction layer
- Codex memory or profile layer
- OpenClaw / Quinn local memory

The product name does not matter. The role does:
private agent memory is a small support layer for tiny evergreen facts, not the main home for shared doctrine.

For the public framework, describe this generically rather than tying it to one stack:
an optional per-agent support layer for small durable facts, with implementation varying by runtime.

### 2. Current working context
This is the active-now layer.

Examples:
- current priorities
- the small set of active projects
- what is stuck, next, or under discussion
- short-lived operational facts that matter right now

This layer should be compressed and rewritten as reality changes.

### 3. Source-of-truth reality
This is not memory in the usual sense.
It is the set of live artifacts the assistant should verify against before acting.

Examples:
- repo files
- runtime state
- configs
- tickets
- inboxes
- calendars
- logs

This distinction matters because a note can be useful and still be wrong.
A durable assistant should know when to verify instead of trusting a cached summary.

## Separation of concerns

A good memory model separates at least three things:
- durable facts
- active context
- live operational truth

When these collapse into one pile, the assistant becomes harder to trust.

For example:
- a durable preference should not be treated like a live process check
- a current focus note should not be treated like a permanent biography fact
- an old project summary should not override the current repo state

The more clearly these are separated, the easier it is to stay helpful without becoming brittle.

## Compression rules

Compression is part of the memory model, not a cleanup chore.

Good memory systems routinely:
- replace stale summaries instead of stacking them forever
- keep front-door context short and operational
- push durable detail into the right long-lived location
- remove or rewrite notes that no longer help
- avoid repeating the same truth across multiple layers unless there is a clear reason

The test is simple:
if a memory layer keeps growing but does not make the assistant more useful, it is drifting.

## Retrieval rules

The assistant should not load everything all the time.

A better pattern is:
- start with the immediate conversation context
- load the minimum front-door context needed to recover the lane
- when resuming after reset or long idle, use a compact exact handoff before broader continuity
- when resuming active work, preserve enough continuity to recover the next concrete move, not just the broad lane
- retrieve deeper memory only when it is actually relevant
- verify against live sources when correctness depends on current reality

This keeps the system faster, cleaner, and less likely to confuse stale notes for truth.

## Volatility in multi-lane systems

A durable memory model also needs to explain why active memory is not enough.

In practice, shared front-door memory is volatile because multiple lanes may all be real at once.
As the foreground shifts between them, the active-memory surface may be rewritten, compressed, or re-scoped.
That can happen with one agent or many.
Multiple agents may intensify the churn, but lane competition is the deeper source of the problem.

No single agent should treat that front-door surface as "theirs."
It is shared orientation context, not private scratch memory, and overwrite/re-scope is normal rather than suspicious by default.

When the front door feels mismatched, the recovery order matters:
- inspect the local thread first
- then read the current front door
- then check recent front-door history before falling back to deeper per-agent continuity

This is why DAOS separates:
- durable facts
- current active context
- live operational truth

If a finding, clarification, or decision should survive foreground churn, it should not rely only on a volatile active-memory surface.
It should be captured in a more stable durable layer.

## What this means in practice

In public terms:
- start with the cheapest, highest-signal context
- only go deeper when the shallow layer is not enough
- do not treat remembered notes as automatically current
- when current reality matters, check the live source

This is how memory stays helpful without pretending to be omniscient.

## Useful memory health

Memory health should be judged by usefulness and trustworthiness, not just by whether files exist.

Useful checks include:
- whether the reset handoff can recover the exact next move after reset or long idle when needed
- whether active continuity can recover the next concrete move when needed
- whether durable claims still match live repo/runtime reality where freshness matters
- whether front-door memory is staying compact instead of becoming a second wiki

If the artifacts are present but the assistant still resumes the wrong lane, trusts stale claims, or forces repeated re-derivation, the memory system is not healthy enough yet.

## Memory write rules

A useful write policy is conservative but proactive.

Write to memory when the information will likely reduce future user repetition, ambiguity, or repeated mistakes.

Good candidates:
- user corrections
- durable preferences
- stable environment facts
- important project conventions
- decisions that are likely to matter again

Usually avoid writing:
- transient status chatter
- things that will be obsolete in hours
- raw dumps that nobody will reread
- duplicate summaries of already-stable source documents

## Trust and memory

Memory helps trust only when it is legible.

The assistant should be able to distinguish:
- what it remembers
- what it just observed
- what it inferred
- what it still needs to verify

A user should not have to guess whether a statement came from durable knowledge, current context, or a live check.

That is also why durable claims should be checked against live reality on a recurring basis when the stack depends on freshness.
The goal is not constant re-verification of everything; it is a lean mismatch audit for the claims that would meaningfully damage trust if they silently drifted.

## Public-framework guidance

For the public DAOS framework, the memory model should stay simple enough that someone can adapt it without inheriting internal sprawl.

That means the public version should emphasize:
- why memory exists
- the minimum categories that matter
- how to separate durable context from live truth
- how and when to compress
- how to avoid stale-memory drift

It should avoid presenting a giant taxonomy unless the taxonomy creates clear practical value.

## Public-framework translation rule

When adapting the memory model for public docs or install-facing material:
- explain the roles of the layers more than the internal mechanics
- prefer plain language over ontology-heavy naming
- keep the model small enough that another stack could adopt it
- preserve the locked boundaries instead of inventing alternate categories for presentation

The point of packaging is to make the doctrine easier to understand, not to quietly rewrite it.

## Working standard

A DAOS memory decision should pass this test:

Does this memory make the assistant more useful, more trustworthy, or less repetitive for a real human without creating unnecessary maintenance burden?

If not, it probably does not belong in the core model.
