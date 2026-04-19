# DAOS Adoption Path

## The simple progression

The thing being adopted here is the operating pack and workflow, not a monolithic runtime.

DAOS is meant to be adopted in stages, not all at once:
1. **try the shape**
2. **install a small baseline**
3. **use it for a week**
4. **stabilize what actually helped**
5. **only add structure if reality earns it**

That progression is the point.
DAOS should feel more like progressive hardening than a giant upfront framework install.

## Stage 1 — Try the shape

Goal:
- understand the operating model without overcommitting

Use:
- `docs/quickstart.md`
- `docs/public-memory-page.md`
- `examples/`
- `starter-pack/`

Rule:
- choose only one install path when you start: copy `starter-pack/`, run bootstrap, or run the wizard

Success looks like:
- you can picture how the baseline would work for you
- the repo feels actionable rather than abstract

Failure mode:
- reading doctrine for too long without trying the operating surface

## Stage 2 — Create your first operating pack

Goal:
- create the smallest useful DAOS setup in one sitting

Use:
- `harness/core-setup.md`
- `starter-pack/` or `python scripts/daos_bootstrap.py /path/to/my-daos-pack`
- `python scripts/daos_validate.py /path/to/my-daos-pack`
- `python scripts/daos_wizard.py /path/to/my-daos-pack` if you want guided setup

Success looks like:
- you have a filled charter
- you have a usable operating profile
- memory and trust defaults are explicit
- setup stayed smaller than your whole life

Failure mode:
- turning setup into an ontology project before the assistant is useful

## Stage 3 — Survive the first week

Goal:
- learn from real use instead of premature redesign

Use:
- `harness/first-week.md`
- `starter-pack/cadence-review.md`
- `templates/cadence-review-template.md`

Success looks like:
- the system is still light enough to use
- the first real corrections come from evidence
- support gets clearer instead of noisier

Failure mode:
- rebuilding the framework every time one annoyance appears

## Stage 4 — Stabilize what works

Goal:
- convert a trial install into a repeatable operating rhythm

Common moves:
- keep one durable task source of truth
- run cadence review often enough to catch drift
- add lane snapshots only where they clearly help
- tighten trust or memory defaults based on repeated evidence

Success looks like:
- the assistant behaves predictably
- the foreground is usually right
- maintenance burden stays lower than the value created

Failure mode:
- the system becomes a maintenance hobby

## Stage 5 — Earn deeper structure

Goal:
- decide whether more structure is truly justified

Only add more when all of these are true:
- the baseline is already useful
- the same friction appears repeatedly
- the new layer would clearly reduce confusion or drift
- the maintenance cost is worth it

Examples of structure that may be earned later:
- richer lane-specific notes
- stronger review surfaces
- more publishable doctrine for shared operating models
- deeper generated or runtime-integrated flows

Failure mode:
- mistaking complexity for maturity

## The default decision rule

Before adding any new layer, ask:
- is the current baseline already helping?
- is this a repeated problem or a one-off irritation?
- will this reduce friction more than it creates maintenance?
- can I make the smallest useful change first?

If the answer is unclear, keep DAOS lighter.

## Suggested reading path by stage

- Stage 1: `docs/quickstart.md`
- Stage 2: `harness/core-setup.md`
- Stage 3: `harness/first-week.md`
- Stage 4: `starter-pack/cadence-review.md`
- Stage 5: `docs/thesis.md`, `docs/memory.md`, `docs/trust.md`, `docs/lane-model.md`

## Bottom line

Do not start with full complexity.
Do not stop at setup.
Use the baseline.
Stabilize it in reality.
Then decide whether deeper structure is actually earned.
