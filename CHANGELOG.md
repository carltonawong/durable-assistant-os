# Changelog

All notable framework-facing changes to Durable Assistant OS (DAOS) should be recorded here.

## Versioning policy

DAOS uses pre-1.0 semantic versioning:
- `v0.1.0` = first coherent public baseline
- `v0.1.x` = small hardening, clarification, or safe behavioral refinement
- `v0.2.0+` = meaningful capability or structure change

Use this changelog for framework/toolkit changes that adopters should know about.
Do not add entries for every typo fix or private WIP note.

## Unreleased

### Changed
- Refreshed starter-pack cache templates and older-touched public surface files with baseline-provenance notes so GitHub per-file last-touched labels are not mistaken for the current framework version.

## v0.1.6 - 2026-04-25

### Changed
- Compressed the README and quickstart into a clearer stranger-facing front door with fewer cross-references.
- Restored the fragile-assistant vs DAOS memory-surfaces visual near the top of the README so the core contrast is visible before deeper docs.
- Made Karpathy's LLM Wiki pattern visible from the front door and starter pack so adopters understand the markdown-wiki structure before customizing it.
- Reduced examples to a smaller set of copyable examples, with the filled starter-pack example now overlaying user-owned files onto the locked `starter-pack/` spine instead of duplicating it.
- Updated `scripts/daos_bootstrap.py` so `--filled-example` preserves the locked baseline spine while applying the filled example files.
- Generated and updater-created manifests now advertise the current framework baseline, `v0.1.6`.

### Hardened
- Removed public `docs/plans/` workbench artifacts from the release surface; shipped behavior remains represented by docs, scripts, tests, changelog, release notes, tags, and git history.
- Clarified starter-pack maintenance as manual-first with optional visible automation, including what a plain markdown `wiki/` means for new users.
- Eliminated duplicated locked baseline files from `examples/starter-pack-example/`, reducing maintenance drift risk.

### Notes
- Scope this as a public-surface hardening patch, not a new runtime or architecture release.
- Internal roadmap/planning docs remain private by default unless intentionally promoted into a shipped, proof-backed repo slice.

## v0.1.5 - 2026-04-24

### Added
- `scripts/daos_memory_parity.py`, a stdlib-only read-only audit for checking whether a DAOS pack's memory surfaces match DAOS parity rules.
- `scripts/daos_core/parity.py` plus tests for semantic memory-surface checks, including log-order differences between `wiki/log.md` and `wiki/cache/hot-cache-log.md`.
- `docs/memory-parity-auditor.md` documenting the new parity auditor, output shape, safety posture, and relationship to normal validation.
- `docs/script-safety.md` documenting DAOS as starter-pack-first, scripts as optional helpers, and the current no-network/no-intentional-credential-location-read/no-shell/no-telemetry posture.

### Changed
- README and quickstart now foreground read-only checks and manual checklist alternatives before any optional helper scripts.
- `daos_validate.py` and `daos_memory_parity.py` help text now explicitly states that the checks are read-only and modify no files.
- Generated and updater-created manifests now advertise the current framework baseline, `v0.1.5`.

### Hardened
- `daos_update.py` and `daos_portability.py` remain available, but are demoted out of README/quickstart first-run command lists and documented as advanced write-capable tools.
- Regression coverage now prevents network/subprocess imports in DAOS scripts and prevents advanced write-capable scripts from creeping back into front-door docs.

### Notes
- Scope this as a patch release: starter-pack trust, script-safety clarity, and read-only memory parity verification.
- No new memory layer, runtime integration, cron behavior, auto-repair mode, or broad architecture expansion is introduced.

## v0.1.4 - 2026-04-24

### Added
- `docs/agent-integrations.md` now includes brief adapter guidance for Codex, Claude Code, and OpenClaw / Quinn so future installs have a concrete shape for startup orientation, durable capture, reset handoff, and live-fact verification.

### Fixed
- Portability review artifacts now use stable POSIX-style durable-wiki decision keys so review-driven apply works consistently on Windows and Unix-like systems.
- Portability export now preflights requested active-memory sidecar files before creating the output bundle, avoiding traceback-driven partial bundles.
- Generated and updater-created DAOS manifests now advertise the current framework baseline, `v0.1.4`, instead of the stale `0.1.0-alpha3` value.

### Hardened
- `daos_update.py` now reports additive migrations to user-owned files honestly instead of saying every protected file was left untouched.
- Update migration records now explicitly list user-owned files that received safe additive migrations.

## v0.1.3b - 2026-04-22

### Changed
- `docs/memory.md` and `docs/public-memory-page.md` now say more explicitly that the shared front door is volatile orientation context rather than private memory owned by one agent.
- `starter-pack/wiki/cache/HOT-CACHE-SPEC.md` and `starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md` now teach that overwrite/re-scope is normal on the shared front door and that recent front-door history should be checked before deeper per-agent continuity when the live front door feels mismatched.
- The filled starter-pack example now mirrors the same front-door volatility rule so adopters see the doctrine both in the locked baseline and in a concrete example.

### Hardened
- DAOS now says more clearly that a hot-cache/front-door surface is shared volatile context, not a durable personal scratchpad for any one agent.
- DAOS now says more clearly that mismatch recovery should prefer local thread plus recent front-door history before deeper continuity reconstruction.

### Notes
- Scope this as a small doctrine patch on top of `v0.1.3`, not a new schema or runtime-layer release.
- This patch is about shared-memory behavior across agents generally, not just one local OpenClaw implementation.
- README now adds two front-door explainer visuals so the baseline mental model and first-setup outcome are easier to grasp quickly.

## v0.1.3 - 2026-04-22

### Added
- `docs/wiki-governance.md` as the canonical DAOS doctrine page for durable wiki page metadata, page lifecycle vs subject state, and verification/source-of-truth semantics.

### Changed
- README now points to the new wiki-governance doctrine and advances the documented DAOS baseline to `v0.1.3`.
- `docs/memory.md` and `docs/public-memory-page.md` now make explicit that durable wiki/docs memory works best when the pages themselves follow a small canonical metadata standard.
- `docs/pack-schema.md` now clarifies that `LaneSnapshot.status` is lane operating state, not wiki-page lifecycle status.
- `starter-pack/wiki/WIKI.md` and the filled starter-pack example now include the compact durable-page governance rule: small canonical headers, `Status` vs `State`, preserved historical `Last Updated`, and `Source of Truth` / `Last Verified` on drift-prone pages.

### Hardened
- DAOS now says more clearly that durable wiki cleanup should preserve historical freshness instead of rewriting it away during schema-only migrations.
- DAOS now says more clearly that page lifecycle and subject operating condition should not be collapsed into one overloaded metadata field.

### Notes
- Scope this as a patch release: wiki/doctrine hardening, starter-pack baseline clarification, and safe metadata-governance refinement without a schema migration.
- Do not treat this as a lane-schema rename release; `LaneSnapshot.status` remains unchanged.

## v0.1.2 - 2026-04-21

### Added
- Public named reset/wake-up artifact: `wiki/cache/reset-handoff.md` in the locked starter-pack baseline.
- Optional runtime-specific install layer: `docs/agent-integrations.md`, with the first Hermes integration section.

### Changed
- DAOS read-order doctrine now places reset handoff ahead of broader agent continuity when resuming after reset or long idle.
- Validation and safe-update tooling now recognize and restore the public reset-handoff baseline artifact.
- Public/docs-facing memory model now describes reset handoff as a first-class DAOS surface rather than an implicit implementation detail.
- Front-door adoption docs now point baseline users to optional agent integrations only after the portable baseline is working.
- README and starter-pack docs now say more clearly that the locked mandatory baseline files already ship inside `starter-pack/` and should not be hand-authored by operators.
- Standalone example materials and the filled starter-pack example are now aligned with the hardened reset-handoff memory-front-door order.

### Hardened
- `starter-pack/wiki/WIKI.md` and its filled example counterpart now more explicitly distinguish durable wiki doctrine from front-door cache behavior and discourage casual baseline-doctrine rewrites during ordinary use.

### Notes
- Scope this as a patch hardening release: stronger baseline packaging, clearer reset/wake-up continuity doctrine, and a separated optional runtime-install layer.
- Keep the mandatory baseline portable; runtime hooks stay optional and runtime-specific.

## v0.1.0 - 2026-04-20

### Added
- First formal DAOS release baseline.
- `CHANGELOG.md` as the framework-facing release history surface.
- `docs/releases/v0.1.0.md` release notes.

### Changed
- README now names the DAOS release discipline and current baseline explicitly.
- Release notes now have a stable home under `docs/releases/`.

### Notes
- This release captures DAOS in its current public shape: starter pack + toolkit, with strongest maturity today in methodology, memory/trust doctrine, and supporting scripts.
- DAOS remains pre-1.0 and should still be treated as a fast-evolving framework/toolkit rather than a locked runtime platform.

## v0.1.1 - 2026-04-20

### Hardened
- Clarify that exact resume quality matters, not just lane recovery.
- Clarify that durable claims should be checked against live reality when freshness matters.
- Clarify that memory-health evaluation should reflect usefulness and trustworthiness, not mere artifact presence.

### Changed
- Tighten active continuity guidance without adding new memory layers.
- Add lean durable-vs-live mismatch audit guidance.
- Strengthen maintenance wording around drift detection and correction.

### Notes
- Scope this as a hardening patch only.
- Do not expand memory architecture, portability surface, or control-surface complexity in this release.
