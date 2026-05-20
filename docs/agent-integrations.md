# DAOS Agent Integrations

## Purpose

DAOS is agent-agnostic at the baseline level.

The mandatory baseline defines:
- the memory/doctrine files
- the lookup order
- the reset-handoff artifact
- the maintenance expectations

It does **not** require one specific runtime or one specific plugin system.

This page is the optional install layer for real agent runtimes.

Use it when you want DAOS to move from:
- portable doctrine only

to:
- runtime-enforced behavior on a specific agent stack

## Boundary

Keep this distinction hard:

- **mandatory baseline** = portable DAOS doctrine and file surfaces
- **agent integration** = runtime-specific install, hooks, file writes, reload steps, and verification

That keeps DAOS portable while still supporting opinionated real installs.

## What belongs here

Good fit for this page:
- runtime-specific plugins or hooks
- exact file paths for that runtime
- installation steps
- restart/reload behavior
- runtime verification steps
- known caveats

Do not move the baseline doctrine itself here.

## Current integrations

- Adapter preflight contract - portable, read-only guidance below
- Deterministic compaction fallback - portable continuity floor below
- Hermes - available below
- Codex - brief adapter guidance available below
- Claude Code - brief adapter guidance available below
- OpenClaw / Quinn - brief adapter guidance available below
- Other runtimes can be added later as separate sections when proven

---

## Adapter preflight contract

### What this adds

DAOS can support real runtime integrations without turning the public repo into one private assistant app. The portable adapter contract is a read-only preflight layer that runs before broad memory fallback or irreversible tool choice.

It covers two durable continuity failures:

1. **Reply-anchor recovery**: after reset, compression, idle expiry, or process restart, an explicit reply/thread/message anchor should beat generic hot memory for that turn.
2. **Action-policy enforcement**: durable preferences that affect risky action classes should become a concrete preflight before a tool path is chosen.

The helper module is:

- `scripts.daos_core.context_preflight.recover_reply_anchor_context(...)`
- `scripts.daos_core.context_preflight.evaluate_action_preflight_policy(...)`

It is intentionally local and stdlib-only. It does not fetch messages, open browsers, access credentials, call the network, or mutate DAOS files. Runtime adapters collect their own evidence first, then pass that evidence into the preflight helper.

### Reply-anchor recovery shape

Adapters that receive a messaging event should preserve a compact anchor shape when the platform provides one:

```text
context_anchor:
  platform
  channel_id / thread_id
  message_id
  quoted_text or quoted_summary when available
session_boundary:
  none / compression / reset / idle-expiry / process-restart
```

Expected behavior:

- local thread context still wins when it is sufficient
- an explicit reply anchor wins over generic hot/shared memory for that turn
- if the anchor resolves to a different lane, report a concise resume receipt instead of guessing
- if the anchor is missing or inaccessible after a boundary, ask for the missing context once
- do not expose transcript paths, local cache paths, or private storage details in receipts

### Action-policy preflight shape

Adapters that perform sensitive or public actions should convert durable preferences into an executable policy before tool selection:

```text
task_class: login-sensitive / public-posting / browser-login / other runtime-defined class
preference: human-readable durable preference
default_action: runtime-supported safe/default path
exception_rule: when another path is allowed
receipt: one short sentence when the policy changes or blocks tool selection
```

Expected behavior:

- no one user's browser/profile preference is a universal DAOS default
- the runtime supplies policy data from its own durable profile or configuration
- sensitive mutations cannot silently violate the durable default
- read-only exceptions and explicit overrides are recorded as such
- receipts stay user-facing and compact, not memory dumps

### Verification checklist

A good adapter integration should prove:

- reply-anchor recovery after simulated session rollover
- anchor-lane conflict handling where the reply anchor wins for the current turn
- low-confidence receipts when an anchor is present but cannot be resolved
- durable action-policy enforcement after a simulated reset/compression boundary
- no local/private path leakage in user-facing receipts

---

## Deterministic compaction fallback

### What this adds

Any runtime that compresses, summarizes, prunes, or rolls session context needs a deterministic continuity floor. LLM-generated summaries can improve resume quality, but they cannot be the only mechanism preserving the window that is about to be dropped.

The runtime invariant is:

> before any context window is discarded, preserve a bounded and redacted deterministic handoff from that exact window.

If the normal summary succeeds, use it. If summary generation fails, the fallback must not depend on a second LLM call. It should be generated from already-available session data and inserted where the runtime would otherwise insert a generic missing-summary marker.

### Minimum fallback contents

A useful fallback should preserve enough information to let the next turn recover the lane without replaying the whole transcript:

- recent user asks from the dropped window
- recent tool/action state, including job/process IDs, command outcomes, and external side effects when available
- file/path mentions that anchor the work
- last dropped turns or compact deterministic extracts from them

Keep the fallback bounded and redacted. Do not dump full transcripts, secrets, credentials, private browser/session paths, or large tool outputs.

### Failure receipt

When the fallback is used, user-facing/runtime warnings should say continuity is degraded and a deterministic fallback handoff was inserted. Avoid saying only that a placeholder was inserted or that the window is unrecoverable when bounded recovery data exists.

### Verification checklist

A good adapter integration should prove:

- simulated summary-generation failure inserts the deterministic fallback
- the fallback includes recent user asks, recent tool/action state, file/path mentions, and last dropped turns
- no second LLM call is required on the failure path
- fallback output is bounded and redacted
- warning text says continuity is degraded, not silently healthy

---

## Hermes integration

### What this adds

The Hermes integration makes the public DAOS reset-handoff artifact live in the current stack.

Specifically, the local Hermes plugin can:
- maintain lane-scoped internal handoff state across turns
- inject resume/orientation context on the first turn of a new session
- mirror the current handoff into the shared markdown artifact:
  - `wiki/cache/reset-handoff.md`

This is optional runtime hardening.
It is not required for a portable DAOS install.

### Current local reference implementation

Current live local plugin path:
- `~/.hermes/plugins/daos-session-handoff/`

Current files:
- `~/.hermes/plugins/daos-session-handoff/plugin.yaml`
- `~/.hermes/plugins/daos-session-handoff/__init__.py`

Shared DAOS cache path examples:
- WSL: `/mnt/c/Users/<user>/<assistant-home>/wiki/cache/`
- Windows: `C:\Users\<user>\<assistant-home>\wiki\cache\`

Replace these with the actual DAOS wiki/cache path in your environment.

### Expected Hermes behavior

A good Hermes integration should:
1. write/refresh internal lane-scoped handoff state during normal work
2. mirror the current exact handoff into `wiki/cache/reset-handoff.md`
3. inject reset-orientation context on the first turn after a new session/reset
4. follow DAOS lookup order instead of treating plugin state as higher truth
5. avoid turning reset handoff into a long running log

### Install shape

At minimum, the Hermes-side install needs:
- an enabled plugin with `pre_llm_call`
- a write path during normal turns or finalize hooks
- access to the shared DAOS cache directory
- a first-turn resume injection path

A practical local metadata shape is:
- plugin name: `daos-session-handoff`
- hooks:
  - `pre_llm_call`
  - `post_llm_call`
  - `on_session_finalize`

### Verification checklist

Use checks like these after install:

```bash
python -m py_compile ~/.hermes/plugins/daos-session-handoff/__init__.py
hermes plugins list | grep daos-session-handoff
```

Then verify behavior, not just plugin presence:
- confirm the plugin is enabled
- confirm the reported version matches the expected local install
- confirm `wiki/cache/reset-handoff.md` is actually written
- confirm the file is overwritten rather than appended
- confirm first-turn post-reset behavior reads resume context before broader continuity fallback

### Behavioral verification targets

A Hermes integration is only good enough when it can prove:
- the local thread still wins when it is sufficient
- `reset-handoff.md` is used after reset/long idle before broader agent continuity
- the wake-up path preserves the exact next move, not just the broad lane
- verified runtime/files still outrank remembered handoff state for live facts

### Caveats

- Runtime topology may differ by environment.
- Gateway/service management may be foreground, user-service, container, or adapter-specific.
- Verify restart assumptions instead of blindly reusing service-oriented instructions.
- The public DAOS artifact may exist before all agents read/write it consistently; runtime proof matters more than doctrine alone.

### Recommendation

For Hermes, install the mandatory DAOS baseline first.

Only then add the Hermes integration layer.

That order keeps the memory system understandable even if the runtime hook layer changes later.

---

## Codex integration

### What this adds

The Codex integration makes DAOS visible to new Codex chats and coding sessions without requiring the user to paste the memory contract every time.

This is usually an instruction-injection and workspace-doc integration rather than a plugin integration.

### Expected Codex behavior

A good Codex integration should:
1. read the current user message and local thread first
2. load the DAOS memory front door only when shared context is needed
3. read `wiki/cache/reset-handoff.md` after reset, long idle, or model-switch recovery when local thread context is insufficient
4. write durable observations to `wiki/raw/` when non-capture would create future ambiguity
5. verify live operational facts against repo files, runtime state, logs, and configs

### Install shape

Typical Codex install surfaces:
- user-level `~/.codex/config.toml` with a short `developer_instructions` reminder
- workspace-level `AGENTS.md` near the working root
- project-level `AGENTS.md` when a specific repo needs tighter local rules

Keep the global instruction short.
It should point Codex to the DAOS wiki and operating model, not inline the whole doctrine.

### Verification checklist

After install, verify:
- new chats launched from the intended working directory see the correct `AGENTS.md`
- Codex knows the DAOS wiki path
- Codex distinguishes `wiki/raw/` from `wiki/sources/`
- Codex uses the raw-to-ingest pipeline for durable capture
- Codex still treats verified files/runtime/logs/configs as higher authority for live facts

### Caveats

- Codex startup behavior depends on working directory and project-doc discovery.
- User-level config can orient Codex globally, but repo-local `AGENTS.md` remains important for project-specific behavior.
- Avoid making Codex load the whole wiki at session start; DAOS should be a lookup contract, not a context dump.

---

## Claude Code integration

### What this adds

The Claude Code integration makes the DAOS memory contract available to code-editing agents that already rely heavily on project-local instructions.

This is normally an `AGENTS.md` / project-instructions integration, optionally backed by local hooks or commands if that runtime supports them.

### Expected Claude Code behavior

A good Claude Code integration should:
1. read project-local instructions before editing
2. use DAOS lookup order for memory and handoff recovery
3. preserve durable discoveries through `wiki/raw/` or relevant wiki pages
4. update `wiki/index.md` and append `wiki/log.md` when ingesting durable pages
5. keep code truth separate from memory truth by verifying against current files before acting

### Install shape

Typical Claude Code install surfaces:
- workspace or repo `AGENTS.md`
- optional runtime-specific settings file, if supported by the local Claude Code installation
- DAOS starter-pack files under the assistant/workspace root

The project-local instruction should include the smallest stable reminder:
- current thread first
- hot cache / reset handoff / agent continuity in DAOS order
- raw notes for durable capture
- live files outrank memory for current behavior

### Verification checklist

After install, verify:
- Claude Code reads the intended `AGENTS.md`
- Claude Code can locate the DAOS wiki root
- durable decisions create raw notes or page updates instead of chat-only residue
- ingest updates `index.md` and `log.md`
- stale wiki claims are checked against live files before code changes

### Caveats

- Claude Code environments vary, so this section should stay adapter-shaped rather than assuming one universal config path.
- If the runtime has no startup hook, the `AGENTS.md` contract is the practical minimum.

---

## OpenClaw / Quinn integration

### What this adds

The OpenClaw / Quinn integration connects DAOS to an always-on assistant runtime that may span Discord, local workspace tasks, scheduled jobs, and project memory.

This layer is where DAOS should become operationally enforced rather than only documented.

### Expected OpenClaw / Quinn behavior

A good OpenClaw / Quinn integration should:
1. load DAOS orientation at session or lane startup
2. keep `wiki/cache/hot-cache.md` as the shared volatile front door
3. write or refresh `wiki/cache/reset-handoff.md` before reset, sleep, or long idle when possible
4. create dated raw notes for meaningful decisions, corrections, handoffs, and operational changes
5. run maintenance loops for raw ingest, hot-cache spec checks, continuity freshness, source hygiene, and reset verification
6. verify live operational claims against current runtime state, repo files, logs, and config

### Install shape

Typical OpenClaw / Quinn install surfaces:
- workspace `AGENTS.md` or equivalent startup instruction file
- runtime/plugin hook for session start or first-turn orientation
- scheduled maintenance jobs for DAOS upkeep
- write access to the shared DAOS wiki root
- optional dashboard or status surface for memory-health visibility

The install should distinguish:
- file presence
- runtime enablement
- behavior proven after real reset or long idle

### Verification checklist

After install, verify:
- startup or first-turn behavior reads the DAOS front door before acting when local context is insufficient
- `reset-handoff.md` is written and overwritten as a current artifact, not appended as a log
- raw notes are created for durable changes
- ingest/maintenance jobs actually run on schedule
- hot-cache log remains compact fallback history rather than a full snapshot archive
- live runtime checks outrank remembered state for operational facts

### Caveats

- OpenClaw / Quinn deployments may have multiple lanes and channels; local thread context still outranks shared memory for exact handoff.
- Multi-lane churn is normal. Use hot-cache log for recent front-door rescope history before falling back to deeper agent continuity.
- Treat "installed", "enabled", and "proven after reset" as separate verification states.

---

## Future integrations

Good future sections would follow the same pattern:
- runtime purpose
- exact install path
- hook or extension points
- where `reset-handoff.md` is written/read
- verification checklist
- caveats

Possible future sections:
- other agent runtimes with stable hook surfaces

## Bottom line

DAOS should stay portable by default and runtime-opinionated only by explicit choice.

That is why agent integrations belong in an optional install layer rather than the mandatory baseline itself.
