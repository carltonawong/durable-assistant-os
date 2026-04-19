# DAOS Graphics Placement Notes

Purpose: keep the README/front door clean while the visual lane is developed separately.

## Recommendation

Use graphics selectively.
Do not turn every concept into a diagram.
Prioritize only the places where a visual clearly reduces first-run confusion.

## Highest-priority graphic placements

### 1. `README.md` — first-run path graphic
**Why:** This is the front door.
A simple visual can make the repo feel immediately operable.

**Best graphic:**
- one short onboarding flow
- `starter-pack/` → fill 2 files → validate → first week

### 2. `docs/public-memory-page.md` — memory-layer graphic
**Why:** The memory model is central and easy to blur in text.

**Best graphic:**
- local thread
- hot front door
- durable wiki/docs memory
- live reality

### 3. `docs/quickstart.md` — first-sitting flow graphic
**Why:** Helps outsiders understand what to do in order without reading every section.

**Best graphic:**
- `starter-pack/README.md`
- `assistant-charter.md`
- `operating-profile.md`
- optional `lane-snapshot.md`
- later `cadence-review.md`

### 4. `starter-pack/README.md` — file-role map
**Why:** This is where users need to understand what each file is for.

**Best graphic:**
- assistant charter = behavior defaults
- operating profile = active reality + memory/trust defaults
- lane snapshot = optional lane detail
- cadence review = later cleanup/calibration

## Secondary-priority graphic placements

### 5. `docs/lane-model.md` — lane map explainer
**Best graphic:**
- a simple lane map with status / foreground / pressure

### 6. `docs/thesis.md` — degradation / repair-loop graphic
**Best graphic:**
- setup success → drift/clutter → external repair loop

### 7. `README.md` or `docs/adoption-path.md` — repo map / adoption stages
**Best graphic:**
- docs explain
- starter-pack operates
- harness guides use
- scripts generate/validate/update/port

## Suggested sequence

1. README first-run path graphic
2. public-memory-page graphic
3. starter-pack file-role map
4. quickstart flow graphic
5. anything else only if confusion remains

## Anti-bloat rule

Do not add graphics just because a section is important.
Add them where they reduce onboarding friction, clarify file roles, or prevent concept blur.
