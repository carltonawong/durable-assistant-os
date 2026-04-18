# DAOS Bootstrap Generator Implementation Plan

> **For Hermes:** implement this plan directly in the repo with standard-library Python and verification via `unittest`.

**Goal:** Add the first runnable/generated install step for DAOS: a script that creates a starter workspace by copying either the blank `starter-pack/` scaffold or the filled `examples/starter-pack-example/` scaffold into a user-chosen target directory.

**Architecture:** Use a single standard-library Python CLI in `scripts/daos_bootstrap.py`. Keep behavior conservative: fail on non-empty targets unless `--force` is passed, and make the source mode explicit through a `--filled-example` flag. Add standard-library tests in `tests/test_daos_bootstrap.py` so the repo gains executable verification without adding external dependencies.

**Tech Stack:** Python 3 stdlib (`argparse`, `pathlib`, `shutil`, `tempfile`, `unittest`)

---

### Task 1: Create the implementation plan artifact

**Objective:** Record the bootstrap-generator design before implementation.

**Files:**
- Create: `docs/plans/2026-04-18-daos-bootstrap-generator.md`

**Verification:**
- Confirm the file exists and names the script path, test path, and verification command.

### Task 2: Implement the bootstrap CLI

**Objective:** Create a runnable script that copies DAOS starter scaffolds into a target folder.

**Files:**
- Create: `scripts/daos_bootstrap.py`

**Requirements:**
- Positional argument: output directory
- Default mode copies `starter-pack/`
- `--filled-example` copies `examples/starter-pack-example/`
- `--force` allows replacing an existing non-empty destination
- Print a compact success summary naming source and destination
- Exit non-zero with a clear message on invalid/unsafe usage

**Verification command:**
- `python scripts/daos_bootstrap.py --help`

### Task 3: Add tests using stdlib only

**Objective:** Verify the bootstrap script without external test dependencies.

**Files:**
- Create: `tests/test_daos_bootstrap.py`

**Coverage:**
- blank starter-pack copy succeeds
- filled-example copy succeeds
- non-empty destination fails without `--force`
- `--force` replaces an existing destination cleanly

**Verification command:**
- `python -m unittest discover -s tests -v`

### Task 4: Document the bootstrap flow

**Objective:** Wire the new runnable path into the repo front door.

**Files:**
- Modify: `README.md`
- Modify: `docs/quickstart.md`
- Modify: `docs/adoption-path.md`

**Documentation points:**
- how to run the script
- when to use blank starter-pack vs filled example
- that this is the first generated install step, not a full productized setup wizard

### Task 5: Verify and commit

**Objective:** Run the script/tests, review repo state, then commit the coherent slice.

**Commands:**
- `python scripts/daos_bootstrap.py --help`
- `python -m unittest discover -s tests -v`
- `git status --short --branch`

**Commit message:**
- `feat: add DAOS bootstrap generator`
