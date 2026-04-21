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

### Added
- Public named reset/wake-up artifact: `wiki/cache/reset-handoff.md` in the locked starter-pack baseline.

### Changed
- DAOS read-order doctrine now places reset handoff ahead of broader agent continuity when resuming after reset or long idle.
- Validation and safe-update tooling now recognize and restore the public reset-handoff baseline artifact.
- Public/docs-facing memory model now describes reset handoff as a first-class DAOS surface rather than an implicit implementation detail.

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
