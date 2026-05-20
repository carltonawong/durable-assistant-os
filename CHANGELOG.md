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
- Added a portable, read-only adapter preflight helper for reply-anchor context recovery and durable action-policy enforcement, with regression tests for session rollover, anchor conflicts, sensitive-action blocking, and read-only exceptions.
- Extended `use-daos doctor` with continuity ownership, handoff lifecycle, and surface-inventory proof sections.

### Changed
- Documented the adapter preflight contract in `docs/agent-integrations.md` without hardcoding any one private runtime or user preference as a universal DAOS default.
- Documented a Deterministic compaction fallback integration invariant so runtimes preserve a bounded and redacted pre-drop handoff when LLM summary generation fails.
- Updated the memory parity auditor and docs to treat `wiki/log.md` as newest-first, matching the current DAOS maintenance convention.

## v0.2.5 - 2026-05-14

### Added
- Added a read-only GitHub Actions enforcement workflow that runs the full Python suite, npm wrapper/package gates, packed-install smoke, release/front-door consistency gate, and npm pack dry-run on pull requests and pushes to `main`.
- Added regression tests that keep the workflow read-only and prevent accidental publish/release/write-permission behavior.
- Added `docs/maintenance.md`, a manual-first upkeep loop with optional automation guardrails so public DAOS users can run the same class of drift checks without Carlton's private crons or runtime.
- Added `docs/releases/v0.2.5.md` as the release note for the enforcement hardening patch.

### Changed
- Bumped package metadata and generated framework manifests to `0.2.5` / `v0.2.5`.

## v0.2.4 - 2026-05-13

### Added
- Added `use-daos doctor --runtime hermes --detect-runtime`, a conservative read-only Hermes detector that returns the same runtime-evidence shape as JSON fixtures without claiming one-shot proof.
- Added `collect_runtime_evidence(pack_dir, runtime=None, detect=False)` as the adapter-facing runtime evidence collection seam.
- Added `docs/releases/v0.2.4.md` as the release note for the doctor-adapter patch.

### Changed
- Bumped package metadata and generated framework manifests to `0.2.4` / `v0.2.4`.

## v0.2.3 - 2026-05-10

### Added
- Added `use-daos doctor`, a read-only proof-ladder receipt that distinguishes installed, bridged, activated, and proven DAOS states, with optional runtime fixture evidence for source precedence and reset/wake one-shot proof.

### Changed
- Added npm/GitHub metadata keywords, repository, homepage, and issue links so public package surfaces point back to the repo clearly.
- Fixed the instruction bridge review path so scan reports live at `import-stage/instruction-scan.md` inside the DAOS home instead of under a nested `.daos/import-stage/` directory.
- Clarified that `use-daos setup` expects an interactive terminal and that non-interactive smoke tests should use `use-daos setup --accept-defaults`.
- Softened README proof-material wording so public docs point to tests and selected verification material without implying the npm package includes internal eval artifacts.
- Clarified the public DAOS framing from memory-first language toward context continuity: DAOS helps agents keep the right context visible across resets, gaps, tool changes, and live verification.
- Reframed `docs/public-memory-page.md` as the public context model while preserving the existing packaged file path.
- Updated `docs/memory.md`, `docs/quickstart.md`, and `starter-pack/README.md` to make memory one mechanism inside the broader continuity model.
- Bumped package metadata to `0.2.3` and generated framework manifests to `v0.2.3`.

### Hardened
- Made the source-authority rule more visible in public docs: live reality outranks durable docs, active cache, continuity notes, and private/session memory when freshness matters.
- Added a compact freshness-sensitive claim rule so current release/version, publish, branch/tag, runtime health, scan, and test-result claims require live authority instead of cached memory alone.
- Added a small reset-current-state receipt proof shape so reset recovery preserves objective, last verified result, approval boundary, stale risk, and the first live fact to recheck without importing the heavier eval corpus.
- Added `use-daos boot-check` / `use-daos doctor`, a read-only runtime hierarchy check that distinguishes installed structure from startup root, prompt/context precedence, shared-session topology, reset/handoff wiring, and cache freshness.

## v0.2.2 - 2026-05-05

### Changed
- Compressed the installed `starter-pack/AGENTS.md` startup surface so agents read the short operating contract by default instead of the full maintenance and automation doctrine.
- Moved detailed maintenance/automation guidance into `starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md` as conditional reference material.
- Added the explicit baseline rule that default-read memory surfaces should stay small and detailed doctrine should live behind targeted references.
- Clarified hot-cache doctrine around compact `Current Focus` entries, fallback-only hot-cache-log reads, and pruning stale temporary context after durable state exists while preserving the existing `Current Focus` section contract.

### Hardened
- Reduced the default token cost of DAOS-enabled agent startup while preserving the reset, hot-cache, raw-note, project-checkpoint, and live-verification rules.

## v0.2.1 - 2026-05-05

### Changed
- Added `docs/releases/v0.2.1.md` as a post-release trust patch note for the v0.2 line.
- Updated `docs/releases/v0.2.0.md` verification details to match the final test and package dry-run results.
- Removed public eval documentation that referenced untracked continuity-debt runner scripts.

### Hardened
- Clarified package verification around the npm tarball contents, including that eval/proof docs, eval examples, the adversarial eval runner, and `daos_continuity_*` experimental scripts are not included in the package.

## v0.2.0 - 2026-04-29

### Added
- Added a unified `scripts/daos.py` front door with `init`, `status`, and no-args status behavior.
- Added `use-daos setup`, a guided first-run activation step for the minimum assistant charter, operating profile, current focus, and reset handoff.
- Added a thin npm wrapper so the intended first-user surface can be `npx use-daos init` and `npx use-daos` while still delegating to the Python reference implementation.
- Added `DAOS Status` output with a `DAOS On` section summarizing active continuity surfaces: Hot Cache, Hot Cache Log, Reset Handoff, and Agent Continuity.
- Added `use-daos on` as a direct command for viewing the current DAOS On surface, including explicit existing-home paths.
- Polished `use-daos on` output so it opens with `DAOS On` rather than the generic status heading, and blank homes now explain that the home is readable but still needs personalization before it is operational.
- Added bridge-aware `use-daos init` behavior that installs the mandatory starter-pack baseline and scans existing agent instruction carriers for coexistence review.
- Added tests for common existing agent ecosystems, including Claude, Gemini, GitHub Copilot, Cursor, Hermes, OpenClaw/Quinn, memory-only, and mixed instruction environments.
- Added npm-wrapper tests covering help delegation, init/status, no-args status via `DAOS_HOME`, Python-missing messaging, exit-code forwarding, and interactive approval prompts.
- Generated and updater-created manifests now advertise the current framework baseline, `v0.2.0`.

### Changed
- Reframed the README front door around the v0.2 product loop: `npx use-daos init` followed by no-args `npx use-daos`.
- Expanded the explicit first-run proof path to `npx use-daos init`, `npx use-daos setup`, `npx use-daos check`, `npx use-daos on`, and `npx use-daos reset-test`, ending with `You're complete!` when reset recovery passes.
- Clarified that DAOS home is the folder with the DAOS pack/wiki surfaces, so existing assistant homes such as `.openclaw` can be used directly instead of duplicating memory into `~/.daos`.
- Shifted immediate-value proof from file presence to visible active-context content under `DAOS On`.
- Kept deeper commands such as `check`, `orient`, `reset-test`, `handoff`, and `memory-audit` available as advanced/operator surfaces rather than the primary public story.
- Added a `package.json.files` allowlist so npm packaging excludes tests, large docs assets, and Python bytecode caches.
- Strengthened memory doctrine around project checkpoints so active work that changes infrastructure, data ownership, provider/tool/account choice, auth, deployment/runtime mode, live-vs-dry-run posture, risk, money, customer impact, or operator setup is captured durably before assumptions drift.
- Refreshed starter-pack cache templates and older-touched public surface files with baseline-provenance notes so GitHub per-file last-touched labels are not mistaken for the current framework version.

### Hardened
- `use-daos init` does not silently edit existing instruction files; interactive mode asks for approval before prepending the DAOS coexistence rule.
- Approved instruction edits create backups under `.daos/backups/instructions/`.
- Non-interactive or declined instruction edits are staged as review artifacts instead of being applied.
- `use-daos setup` refuses to silently answer personalization questions in non-interactive mode unless answers are supplied or defaults are explicitly accepted.
- `use-daos setup` refuses to overwrite existing personalized setup-managed files unless `--force` is explicit, and forced overwrites create setup backups first.
- Arbitrary old memory content such as `MEMORY.md` is not imported by default.
- npm-wrapper interactivity now preserves TTY behavior so Python approval prompts still work through Node/npm.
- npm-wrapper Python discovery now rejects Python runtimes older than Python 3.8 instead of accepting any `python --version` success.
- Packed-tarball smoke testing now verifies install-from-package behavior in a fresh consumer project, not just from the repo root.
- Packed-tarball smoke testing now verifies explicit existing assistant homes can be read without creating a default `~/.daos` home.

### Notes
- Scope this as the first practical DAOS product-surface release, not a hosted runtime or autonomous assistant app.
- Keep the Python-core plus npm-wrapper approach until the CLI contract stabilizes enough to justify a native TypeScript port.

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
