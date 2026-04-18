# DAOS First Week Guide

This is the next `harness/` artifact after `harness/core-setup.md`.

Its job is simple:
help a new DAOS install survive its first week of real use without immediately becoming cluttered, overbuilt, or ignored.

## Why this file exists

A lot of systems fail after setup, not during setup.

They fail because:
- too much gets added too quickly
- reminders become noise
- the lane map drifts away from reality
- calibration never actually happens
- the assistant becomes impressive on paper but unhelpful in use

This guide is for the short period right after the first install, when the goal is to stabilize the operating baseline.

## First-week rule

The goal of the first week is **not** to perfect the system.
The goal is to learn whether the first setup is actually useful in daily use.

That means:
- operate the system lightly
- notice friction
- capture small corrections
- avoid architecture sprawl

## What to do in the first week

### Day 1: Use the baseline as-is

After finishing core setup:
- use the assistant with the locked first-pass defaults
- do not immediately add many new layers
- let the lane map, trust defaults, and reminder posture get tested by real work

Main question:
- does this already feel net-helpful?

### Day 2-3: Watch for friction, not perfection

During early use, pay attention to:
- what gets missed
- what feels noisy
- which lane keeps losing the foreground incorrectly
- whether ask-vs-act behavior feels right
- whether reminder behavior helps or annoys

Capture only short notes.
Do not redesign the whole system every time you notice one annoyance.

### Day 4-5: Make one small correction at a time

If something is clearly off, make only the smallest useful correction.

Examples:
- tighten the approval boundary
- reduce reminder frequency
- add one lane snapshot for one high-friction lane
- simplify a lane label
- strengthen waiting-on visibility

Avoid:
- rewriting the whole operating profile
- inventing a complex ontology
- adding many new memory layers
- overreacting to one bad day

### Day 6-7: Run the first cadence review

By the end of the first week, run a lightweight review using:
- `templates/cadence-review-template.md`
- or `starter-pack/cadence-review.md`

Main questions:
- what already works?
- what feels too heavy?
- what still gets missed?
- which lane needs more support?
- what should be added, removed, or softened?

## Good first-week outcomes

A good first week usually ends with:
- one working assistant charter still holding up
- one operating profile that still feels mostly real
- maybe one added lane snapshot for one difficult lane
- one or two reminder/trust corrections
- one cadence review that clarifies the next adjustment

That is enough.

## Bad first-week outcomes

The system is drifting if the first week turns into:
- endless framework editing
- too many new files and layers
- reminder noise without better follow-through
- a lane map that no longer matches reality
- no actual review after a week of use

## Recommended operator stance

During the first week, prefer this mindset:
- test the baseline before expanding it
- fix what hurts most first
- keep changes small and reversible
- preserve trust by reducing noise, not by adding ceremony

## Suggested companion artifacts

Use alongside:
- `harness/core-setup.md`
- `docs/quickstart.md`
- `starter-pack/`
- `templates/cadence-review-template.md`
- `examples/cadence-review-example.md`

## Bottom line

A good DAOS install should become more accurate through use.
The first week is where that starts.

Do not overbuild.
Do not abandon it after setup.
Use it lightly, review it once, and improve the smallest thing that matters.
