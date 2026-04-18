# Setup Conversation Example

> Example instance material for DAOS.
> This file demonstrates what a lightweight first setup conversation can look like in practice.
> It is not canonical framework doctrine.

## Why this example exists

DAOS setup is supposed to feel like a short, useful wizard.
Not a giant intake interview.

This example shows the *interaction shape* of a good first-pass install.
It is intentionally compressed.

## Example transcript

**Assistant:** This is a short first-pass install, not a full life-modeling session. Goal is to get you a useful default in one sitting, then calibrate later.

**Assistant:** 1. What should this assistant help with most?

**User:** Help me stay oriented across work and personal priorities without dropping important things.

**Assistant:** Locked — primary outcome: keep you oriented and less likely to drop important work.

**Assistant:** 2. What would make it feel unhelpful fastest?

**User:** Being noisy, making confident wrong assumptions, or forcing me to repeat myself.

**Assistant:** Locked — primary failure mode: noise, bad assumptions, repeated re-steering.

**Assistant:** 3. When uncertain, should it ask first or act on likely intent?

**User:** Ask if the ambiguity would change what it does. Otherwise act.

**Assistant:** Locked — ask when ambiguity changes action; otherwise act on likely intent.

**Assistant:** 4. What actions always need approval?

**User:** Anything destructive, public, costly, or socially consequential.

**Assistant:** Locked — approval required for destructive, public, costly, or socially consequential actions.

**Assistant:** 5. What are the top few active lanes right now?

**User:** Operations, client work, build/projects, and personal.

**Assistant:** Locked — active lanes: operations, client work, build/projects, personal.

**Assistant:** 6. Which lane is most foreground right now?

**User:** Operations and client work.

**Assistant:** Locked — current foreground: operations and client work.

**Assistant:** 7. What most often slips or gets dropped?

**User:** Waiting-on follow-ups and deeper project work when inbox stuff takes over.

**Assistant:** Locked — main drift risk: follow-ups and deep-work displacement.

**Assistant:** 8. What kind of support helps most versus annoys?

**User:** Helpful: clear priorities, follow-up visibility, and concise reminders. Annoying: broad nagging and overlong explanations.

**Assistant:** Locked — support posture: concise priority/follow-up help; avoid broad nagging and overexplaining.

**Assistant:** 9. Where should the master list live, and should importance outrank urgency?

**User:** One durable task list. And yes, importance should outrank urgency.

**Assistant:** Locked — one durable master list; importance > urgency.

**Assistant:** 10. Final default: we start light, use the system, then calibrate later instead of solving every edge case now.

**User:** Yes.

**Assistant:** Locked — calibration happens after use, not before.

## What this conversation produced

From a short exchange like this, DAOS can already produce:
- `assistant-charter.md`
- `operating-profile.md`
- a top-level lane map
- trust defaults
- reminder/planning defaults
- a clear calibration-later rule

## Why this is a good example

This setup works because it:
- stays one question at a time
- locks high-leverage defaults early
- avoids giant biography capture
- gets to a usable operating baseline quickly
- leaves room for later refinement

## What not to copy literally

Do not copy the exact answers.
Copy the interaction pattern:
- short question
- clear answer
- explicit lock
- move forward

That is the setup feel DAOS is trying to promote.
