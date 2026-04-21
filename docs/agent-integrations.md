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

- Hermes — available below
- Other runtimes can be added later as separate sections when proven

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

Current shared DAOS cache path used by the integration:
- WSL: `/mnt/c/Users/openq/.openclaw/wiki/cache/`
- Windows: `C:\Users\openq\.openclaw\wiki\cache\`

Treat those as the current local reference paths, not universal literals. Replace them with the actual DAOS wiki/cache path in your own environment.

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

- Hermes runtime topology may differ between environments.
- In the current local environment, the gateway is running in manual WSL foreground mode rather than as a managed service.
- Restart assumptions should therefore be verified instead of blindly reusing service-oriented instructions.
- The public DAOS artifact may exist before all agents read/write it consistently; runtime proof matters more than doctrine alone.

### Recommendation

For Hermes, install the mandatory DAOS baseline first.

Only then add the Hermes integration layer.

That order keeps the memory system understandable even if the runtime hook layer changes later.

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
- Claude Code
- Codex
- OpenClaw / Quinn
- other agent runtimes with stable hook surfaces

## Bottom line

DAOS should stay portable by default and runtime-opinionated only by explicit choice.

That is why agent integrations belong in an optional install layer rather than the mandatory baseline itself.
