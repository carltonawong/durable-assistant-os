# DAOS Core Setup

This is the first installable `harness/` artifact for Durable Assistant OS.

Its job is to give a new user a minimum viable DAOS setup in one sitting, then deepen later through use and calibration.

## What this setup is for

Use this setup to install the smallest useful DAOS default:
- assistant charter
- minimum viable operating profile
- lane map starter
- memory / trust defaults
- reminder / planning defaults
- calibration-after-use rule

This is the default starting path, not the full system.

## Core setup principles

- ask only what is needed to start
- prefer early usefulness over exhaustive intake
- use progressive setup, not giant biography capture
- keep the flow one question at a time
- lock defaults clearly enough that later calibration can refine them
- treat simplicity as a durability feature

## Recommended operator framing

Before running setup, tell the user:

- this is a short first-pass install, not a full life-modeling session
- we are aiming for a useful default in one sitting
- deeper tailoring can happen later through calibration
- when something is unclear but low-stakes, pick a sensible default and move on

## Setup outputs

By the end of core setup, you should be able to fill:
- `templates/operating-profile-template.md`
- a first lane map
- a first reminder / planning posture
- a first memory / trust posture

If useful, save the resulting instance profile separately and keep the framework files generic.

Useful companion artifacts:
- `templates/assistant-charter-template.md`
- `templates/operating-profile-template.md`
- `examples/assistant-charter-example.md`
- `examples/first-pass-setup-output-example.md`

## The core setup flow

Run these blocks in order.

### 1. Assistant charter

Goal: define the assistant's operating posture before collecting too much context.

Ask for:
- primary outcome
- primary failure mode
- uncertainty behavior
- proactive behavior
- safety / approval boundary
- desired feel

Recommended prompt pattern:
1. What should this assistant help with most?
2. What would make it feel unhelpful or unsafe fastest?
3. When uncertain, should it ask first or act on likely intent?
4. How proactive should it be by default?
5. What actions always need approval?
6. What should the assistant feel like in daily use?

Minimum completion bar:
- one clear outcome
- one clear failure mode
- one clear ask-vs-act default
- one clear approval boundary

### 2. Minimum viable operating profile

Goal: capture the smallest amount of user reality needed to make the assistant useful.

Ask only for:
- the user's biggest current support need
- the top few live domains or lanes
- the main source of friction
- the support style that would help most

Avoid:
- giant life history
- exhaustive project inventory
- broad questionnaires before usefulness is visible

Recommended prompt pattern:
1. What support would help most right now?
2. What are the top few active lanes in your life or work?
3. What most often slips or gets dropped?
4. What kind of support tends to help versus annoy?

### 3. Lane map starter

Goal: create a simple working map of the user's live lanes.

Recommended starter lanes:
- Personal
- Business / operations
- Build / projects
- Trading / research
- Other as needed

For each active lane, capture only:
- status: `active` / `stalled` / `hiatus` / `archive` / `pending`
- foreground: yes / no
- pressure: low / medium / high
- short note

Important distinctions:
- `hiatus` = intentionally paused
- `stalled` = unintentionally stuck
- `pending` = waiting on an external dependency
- `archive` = filed away unless later relevant

Do not over-model the lane map during core setup.
A usable rough map is better than an elegant taxonomy the user will not maintain.

### 4. Memory defaults

Goal: install the default memory posture early so future behavior stays grounded.

Lock these defaults:
- memory front door: local thread first, then hot cache, then agent continuity
- durable memory home: wiki first, with docs/repo files for publishable framework outputs
- verified reality rule: files, runtime, and live state outrank remembered context for operational facts
- durable capture rule: if a second review shows something should not live mainly in hot cache or chat, create or update durable memory in the same pass

Recommended explanation to the user:
- thread = exact current handoff
- hot cache = shared front door for what matters now
- continuity = per-agent resumable note
- wiki / docs = durable shared truth
- runtime / files = final source of truth for live state

### 5. Trust defaults

Goal: make behavior predictable enough to trust.

Lock these defaults:
- ask when ambiguity would change the action taken
- act when intent is clear and stakes are low or reversible
- require explicit approval for critical, sticky, costly, or socially consequential actions
- surface uncertainty instead of bluffing certainty
- prefer verification over memory for live facts

Recommended prompt pattern:
1. What kinds of mistakes are acceptable if reversible?
2. What kinds of actions should always pause for approval?
3. When the assistant is uncertain, what behavior earns trust?

### 6. Reminder / planning defaults

Goal: define how the assistant should help with action management without overbuilding.

Recommended starter defaults:
- one durable master list / checklist as source of truth
- one clean review layer or dashboard if useful
- gentle same-day follow-up for unresolved overdue items
- default focus set of 3 active priorities
- importance > urgency
- keep high-impact items visible even when they are not urgent

Recommended prompt pattern:
1. Where should the master task list live?
2. Do you want a separate review layer or dashboard?
3. Should overdue items reappear the same day if unresolved?
4. How many active priorities feels manageable by default?
5. Should importance outrank urgency when they conflict?

### 7. Calibration-after-use rule

Goal: keep setup lightweight by explicitly moving depth to later.

At the end of setup, lock this rule:
- start with the minimum useful default
- watch where friction, noise, or misses appear in real use
- calibrate later instead of trying to solve every edge case now

Recommended calibration questions:
- what feels too heavy?
- what still gets missed?
- which lane loses foreground incorrectly?
- which reminders help versus annoy?
- what should be strengthened, softened, added, or removed?

## Suggested output structure

After setup, fill the operating profile in this order:
1. Assistant charter
2. Top-level lane map
3. Per-lane snapshot
4. Reminder / planning defaults
5. Memory / trust defaults
6. Calibration-later notes

Use `templates/operating-profile-template.md` as the default blank structure.

If you want a worked target shape before running setup, read:
- `examples/assistant-charter-example.md`
- `examples/first-pass-setup-output-example.md`

## Install-quality checklist

The core setup is good enough when:
- the assistant has a clear charter
- the user has a usable lane map
- memory and trust defaults are explicit
- reminder / planning defaults are explicit
- the setup can be completed without a giant biography
- later calibration has a clear place to go

## What not to do

- do not ask broad multi-part intake questions when one targeted question will do
- do not force taxonomy debates during first install
- do not make the user model their whole life before value appears
- do not leave memory / trust defaults implicit
- do not treat core setup as final; it is a first operating baseline

## Notes

- `docs/` explains the system publicly
- `harness/` installs the operating defaults
- `templates/` holds reusable blank structures
- `examples/` holds clearly labeled sample instances
- this file should stay more installable than `docs/`, more opinionated than `templates/`, and less bespoke than `examples/`
