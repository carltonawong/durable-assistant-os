# DAOS Interactive Wizard Implementation Plan

> **For Hermes:** implement this with standard-library Python, document it, and verify it through a non-interactive piped-input test plus `unittest`.

**Goal:** Add the first interactive generated install step for DAOS: a wizard that asks a compact first-pass question set and writes a filled starter pack into a target directory.

**Architecture:** Use a single CLI in `scripts/daos_wizard.py`. Keep the question set intentionally small and aligned with the DAOS setup philosophy: charter basics, lane list, foreground lanes, master-list posture, and desired feel. Use stable DAOS defaults for memory/trust rules rather than trying to ask everything. Generate a filled pack by writing `assistant-charter.md` and `operating-profile.md`, while leaving `lane-snapshot.md` and `cadence-review.md` as later-use artifacts.

**Tech Stack:** Python 3 stdlib (`argparse`, `pathlib`, `shutil`, `textwrap`, `subprocess`, `tempfile`, `unittest`)

---

### Task 1: Add the wizard CLI

**Files:**
- Create: `scripts/daos_wizard.py`

**Behavior:**
- positional output directory
- prompt for a compact question set
- generate a filled starter pack into the target directory
- fail safely on non-empty targets unless `--force`
- print a short completion summary plus suggested next steps

### Task 2: Add tests

**Files:**
- Create: `tests/test_daos_wizard.py`

**Coverage:**
- piped answers generate a filled pack successfully
- generated pack passes `scripts/daos_validate.py`
- non-empty target fails without `--force`

### Task 3: Document the wizard

**Files:**
- Modify: `README.md`
- Modify: `docs/quickstart.md`
- Modify: `docs/adoption-path.md`

**Documentation points:**
- wizard is the first interactive generated install step
- wizard is intentionally minimal, not a full life-modeling intake
- generated pack should still be reviewed and refined in the first week

### Task 4: Verify end-to-end

**Commands:**
- `python scripts/daos_wizard.py --help`
- run the wizard with piped answers into a temp folder
- `python scripts/daos_validate.py <generated-folder>`
- `python -m unittest discover -s tests -v`

**Commit message:**
- `feat: add DAOS interactive setup wizard`
