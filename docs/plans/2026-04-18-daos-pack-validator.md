# DAOS Pack Validator Implementation Plan

> **For Hermes:** implement this plan with standard-library Python and verify it with `unittest` plus a real CLI run.

**Goal:** Add the next runnable DAOS product step after bootstrap: a validator that checks whether a generated/folder-based DAOS pack is minimally filled enough to operate.

**Architecture:** Use a single standard-library CLI in `scripts/daos_validate.py`. Keep the validation conservative and transparent: require key files, require specific labels to have non-empty values, and report all failures in plain text with a non-zero exit code. Add tests in `tests/test_daos_validate.py` that exercise blank-pack failure, filled-example success, and missing-file failure.

**Tech Stack:** Python 3 stdlib (`argparse`, `pathlib`, `subprocess`, `tempfile`, `unittest`)

---

### Task 1: Add the validator CLI

**Files:**
- Create: `scripts/daos_validate.py`

**Behavior:**
- Accept a path to a DAOS pack directory
- Check for required files: `assistant-charter.md`, `operating-profile.md`
- Check that core labeled fields are not left blank
- Print a success summary on pass
- Print all detected issues and exit non-zero on failure

### Task 2: Add tests

**Files:**
- Create: `tests/test_daos_validate.py`

**Coverage:**
- blank starter-pack fails validation
- filled starter-pack example passes validation
- missing required file fails validation

### Task 3: Wire docs

**Files:**
- Modify: `README.md`
- Modify: `docs/quickstart.md`
- Modify: `docs/adoption-path.md`

**Documentation points:**
- how to run the validator
- that blank scaffolds are expected to fail until filled
- that validation is a lightweight readiness check, not a guarantee of quality

### Task 4: Verify end-to-end

**Commands:**
- `python scripts/daos_validate.py examples/starter-pack-example`
- `python scripts/daos_bootstrap.py /tmp/...`
- `python scripts/daos_validate.py /tmp/...` (expected fail on blank pack)
- `python -m unittest discover -s tests -v`

**Commit message:**
- `feat: add DAOS pack validator`
