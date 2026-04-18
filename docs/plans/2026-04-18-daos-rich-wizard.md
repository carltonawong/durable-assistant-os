# DAOS Rich Wizard Plan

## Goal

Make the DAOS wizard more useful without turning it into a heavy intake system.

## Added in this pass

- per-lane optional customization instead of one fixed lane default path
- review-summary checkpoint before files are written
- schema-backed output via the shared pack model

## Explicit non-goals

- no full-screen TUI
- no multi-page app flow
- no exhaustive life-model intake
- no pack editing mode yet

## Design stance

The wizard should stay first-pass and compact.
It can branch a little when lane-specific detail is clearly useful.
But it should still be faster than manually building the same pack from scratch.
