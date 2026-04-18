# DAOS Lane Model

## Why this page exists

DAOS needs a simple way to represent a user's live domains without turning the system into a giant ontology.

The lane model is that answer.
It is the lightweight map that tells the assistant where attention belongs, what is active, what is stuck, and what should stay in the background.

## What a lane is

A lane is a top-level area of life or work that is real enough to deserve its own continuity.

Examples:
- Personal
- Business / operations
- Build / projects
- Trading / research

A lane is not meant to be a perfect taxonomy.
It is meant to be a useful working division.

If a lane helps the assistant stay oriented, it is doing its job.
If it mostly adds modeling overhead, it is probably too granular.

## Why DAOS uses lanes

Without a lane model, assistants tend to fail in two ways:
- everything collapses into one blurry stream
- or the system over-classifies reality until maintenance becomes the work

DAOS wants the middle path:
- enough separation to preserve orientation
- not so much structure that the user has to maintain an artificial ontology

The lane map is there to keep the right foreground visible, not to impress anyone with complexity.

## Starter lane map

A good default starter map is:
- Personal
- Business / operations
- Build / projects
- Trading / research
- Other, if needed

This is a starting point, not a universal rule.
Some users will need fewer lanes.
Some will need different ones.
The standard is usefulness, not symmetry.

## Per-lane snapshot

For each active lane, DAOS tries to capture only a small amount of state:
- status
- foreground
- pressure
- short note

That is enough to keep a lightweight operating picture without creating a second project-management system by accident.

## Status values

DAOS uses a small working set of lane or project-state labels:
- `active`
- `stalled`
- `hiatus`
- `archive`
- `pending`

### active
The lane is live and should be considered part of the normal operating foreground.

### stalled
The lane matters, but motion has unintentionally broken down.
This is not a final state. It is usually a diagnostic state.

### hiatus
The lane is intentionally paused.
It should not be treated like a problem unless the pause intention changes.

### archive
The lane is filed away and should stay out of the active foreground unless it becomes relevant again.

### pending
The lane is waiting on an outside dependency.
The assistant should track the dependency instead of repeatedly trying to force motion from the inside.

## Why stalled and hiatus must stay separate

This distinction matters.

- `hiatus` means: we meant to pause
- `stalled` means: we did not mean to lose motion

If the assistant confuses these, it either nags people about intentional pauses or quietly ignores work that actually needs help.

## Foreground

Foreground is a simple yes / no question:
- is this lane currently in the live foreground?

This is not the same as importance in the abstract.
A lane can matter a lot over time and still not be today's foreground.

Foreground exists so the assistant can avoid treating every meaningful lane as equally live at once.
That is one of the main ways DAOS reduces context blur.

## Pressure

Pressure is a simple low / medium / high rating.

Its job is not to be a precise metric.
Its job is to signal where the user is likely to feel cost, urgency, or fragility.

A lane can be:
- high pressure and active
- high pressure and stalled
- low pressure and still worth tracking

Pressure helps the assistant decide where support may matter most without pretending to calculate the user's life mechanically.

## The short note

Each lane also gets a short note.

This should stay compact.
Its purpose is to answer a simple question:
- what is the most important current thing to know about this lane?

It is not meant to become a hidden work log.
Longer durable context belongs elsewhere.

## Anti-bloat rule

Do not over-model the lane map.

A usable rough map is better than an elegant taxonomy the user will not maintain.

Good lane modeling:
- helps orientation
- reduces wrong-foreground mistakes
- makes support more targeted

Bad lane modeling:
- creates many near-duplicate categories
- turns everyday support into classification work
- asks the user to maintain more structure than value justifies

## How this connects to setup

The lane model is part of first install because it is one of the fastest ways to make the assistant concretely useful.

That is why it appears inside:
- `harness/core-setup.md`
- `templates/operating-profile-template.md`
- example instance material

The setup goal is not to perfect the lane map.
It is to establish a usable first map that can later be refined.

Useful companion artifacts:
- `templates/lane-snapshot-template.md`
- `examples/lane-snapshot-example.md`

## How this connects to calibration

The lane model should improve through use.

Good later calibration questions include:
- which lane most often loses the foreground incorrectly?
- which lane needs more support?
- which lane is actually stalled versus intentionally quiet?
- does anything need to be split, merged, renamed, paused, or archived?

This keeps the lane model adaptive instead of frozen.

If you want a concrete example of lane-level upkeep after first install, see:
- `templates/cadence-review-template.md`
- `examples/cadence-review-example.md`

## Bottom line

The DAOS lane model is simple on purpose.

It gives the assistant a lightweight map of reality:
- what areas exist
- which ones are live
- which ones are stuck
- which ones are under pressure
- which ones should stay in the background

That is enough structure to improve continuity and targeting without turning the framework into a bureaucracy of categories.
