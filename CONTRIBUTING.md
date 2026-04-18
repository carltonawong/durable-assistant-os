# Contributing to Durable Assistant OS

Thanks for contributing to DAOS.

## Current contribution posture

This repository is still in an early framework-shaping phase.

Contributions are most useful when they:
- improve clarity at the front door
- tighten installability
- reduce ambiguity between docs, harness, templates, and examples
- preserve the separation between framework doctrine and instance-specific material

## Before opening a change

Please check whether the proposed change belongs in:
- `docs/` — public explanation and doctrine
- `harness/` — installable setup flow and operating defaults
- `templates/` — reusable blank structures
- `examples/` — clearly labeled demonstration material

Do not let example-instance content quietly become framework canon.

## Contribution guidelines

- prefer small, coherent changes over mixed batches
- keep public-facing wording simple and low-bloat
- preserve existing memory/trust boundaries unless the change is explicit and deliberate
- when refining doctrine, make sure the public page, deeper reference docs, and install flow do not drift apart
- avoid adding files that do not clearly improve explanation, installability, reuse, or demonstration

## Good contribution shapes

Examples of good contributions:
- clarifying README/front-door navigation
- improving the setup flow in `harness/core-setup.md`
- adding or tightening reusable templates
- making doc-role boundaries easier for outsiders to understand
- improving consistency between doctrine and public packaging

## Commit guidance

Use coherent checkpoints.
A change is usually ready to commit when:
- one repo-facing slice is coherent
- the public/private boundary is stable
- the change can be described with one clean commit message

## Review standard

The main question is not just "is this true?"
It is also:
- does this make DAOS easier to understand?
- does this make DAOS easier to install?
- does this preserve the framework/example boundary?
- does this reduce future confusion rather than add it?
