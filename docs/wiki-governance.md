# DAOS Wiki Governance

<!-- DAOS baseline note: Current public framework baseline is v0.2.4; this file remains part of the current release surface even if its original feature landed in an earlier patch. -->

## Why this page exists

DAOS often uses a markdown wiki/docs surface as the durable shared memory layer.

That only works well if the durable pages stay legible, comparable, and trustworthy over time.
This page defines the minimum governance that keeps that from drifting into a pile of half-structured notes.

## The minimum durable-page header

For durable wiki pages, use a small canonical header.

At minimum:
- `Type`
- `Status`
- `Summary`
- `Last Updated`

This is enough to tell a future human or agent what the page is, whether it is current, what it is about, and how fresh the writing is.

## Status vs State

Do not overload one field with two different jobs.

- `Status` = lifecycle of the page itself
- `State` = condition of the thing the page describes

Example:
- a page can have `Status: active` because it is still the canonical page
- while the underlying project can have `State: hiatus` because the work is intentionally paused

That split keeps durable docs clearer and avoids one metadata field turning into prose.

## Source of truth and verification

For drift-prone operational pages, also add:
- `Location`
- `Source of Truth`
- `Last Verified`

Use them narrowly:
- `Location` = where the thing mainly lives
- `Source of Truth` = what should be trusted when docs and reality diverge
- `Last Verified` = when the important claims were checked against real files, runtime, config, logs, or live behavior

`Last Updated` and `Last Verified` are not the same thing.

- `Last Updated` = when the page text changed materially
- `Last Verified` = when the important claims were checked against reality

## Preserve historical freshness

When migrating an older page onto a newer metadata standard without materially changing its substance:
- preserve the older `Last Updated` timestamp
- do not flatten history to the migration time

If exact historical authorship is unclear, use a conservative provenance label instead of inventing one.

## Controlled vocabularies

Keep metadata vocabularies controlled within an install.

- `Type` should come from a closed list
- `Status` should come from a closed list
- if the install uses page directories, derive `Type` from path whenever practical

Do not casually invent synonyms when an existing value already fits.

## Important DAOS nuance

This doctrine does **not** rename the existing `LaneSnapshot.status` field in the DAOS pack schema.

That field is the operating status of a lane inside the structured pack model.
It is not the lifecycle status of a wiki page.

## Bottom line

DAOS durable memory should stay structured enough that:
- current pages look current
- legacy pages read as legacy
- operating condition is not confused with document lifecycle
- historical freshness is not lost during cleanup work
- drift-prone claims say what reality should win
