# DAOS Docker deep simulation

This harness runs the v0.2 product-behavior simulation inside a clean Linux container.
It is meant for release confidence, not as a replacement for a human first-run usability pass.

## What it simulates

- builds the local repo into an npm tarball with `npm pack --json`
- installs that tarball into a fresh consumer project
- runs fresh default `~/.daos` init/status
- runs explicit existing `.openclaw` / assistant-home `status` and `on`
- verifies explicit existing-home mode does not create a default `~/.daos`
- verifies existing instruction files are not silently edited
- verifies `MEMORY.md` content is not imported by default
- writes a handoff and runs `reset-test`

## Run from the repo root

```bash
mkdir -p simulation-output
docker build -f docker/deep-simulation.Dockerfile -t daos-deep-sim:local .
docker run --rm -v "$PWD/simulation-output:/simulation-output" daos-deep-sim:local
```

Expected terminal result:

```text
Transcript: /simulation-output/daos-v02-deep-simulation-audit.md
Checks: 15/15 passed
```

The transcript will be written to:

```text
simulation-output/daos-v02-deep-simulation-audit.md
```

## Windows PowerShell

```powershell
mkdir simulation-output -Force
docker build -f docker/deep-simulation.Dockerfile -t daos-deep-sim:local .
docker run --rm -v "${PWD}/simulation-output:/simulation-output" daos-deep-sim:local
```

## Manual human pass still needed

This proves mechanics and safety invariants in a clean container. It does not prove that a stranger understands the product without help. The human pass is still:

1. give a fresh evaluator only README/quickstart
2. have them install/run DAOS
3. watch whether `DAOS On`, personalization, existing-home mode, and instruction review make sense
4. force a real assistant reset and check whether the assistant resumes correctly from DAOS surfaces
