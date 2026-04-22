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

No unreleased framework-facing changes are staged after `v0.1.3` yet.

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
