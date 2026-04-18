#!/usr/bin/env python3
"""Interactive DAOS setup wizard that generates a filled starter pack."""

from __future__ import annotations

import argparse
import sys

from daos_bootstrap import bootstrap
from daos_core import DaosPack, wizard_pack, write_pack_core_files


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a compact DAOS setup wizard and generate a filled starter pack."
    )
    parser.add_argument("output_dir", help="Destination directory for the generated DAOS pack")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing non-empty destination directory",
    )
    return parser.parse_args(argv)


def prompt(question: str) -> str:
    try:
        answer = input(f"{question}\n> ").strip()
    except EOFError as exc:
        raise ValueError("Wizard input ended early.") from exc
    if not answer:
        raise ValueError(f"A response is required for: {question}")
    return answer


def prompt_with_default(question: str, default: str) -> str:
    try:
        answer = input(f"{question} [{default}]\n> ").strip()
    except EOFError as exc:
        raise ValueError("Wizard input ended early.") from exc
    return answer or default


def parse_csv_list(raw: str) -> list[str]:
    items = [item.strip() for item in raw.split(",") if item.strip()]
    if not items:
        raise ValueError("Please provide at least one item.")
    return items


def parse_yes_no(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"y", "yes"}:
        return True
    if value in {"n", "no"}:
        return False
    raise ValueError("Please answer yes or no.")


def collect_lane_customizations(lanes: list[str], foreground_lanes: list[str]) -> dict[str, dict[str, str]]:
    customizations: dict[str, dict[str, str]] = {}
    foreground_set = set(foreground_lanes)
    for lane in lanes:
        customize = parse_yes_no(prompt(f"Customize lane '{lane}' details? (yes/no)"))
        if not customize:
            continue
        default_status = "active"
        default_pressure = "high" if lane in foreground_set else "medium"
        status = prompt_with_default(f"Status for '{lane}'?", default_status)
        short_note = prompt(f"Short note for '{lane}'?")
        customizations[lane] = {
            "status": status,
            "pressure": default_pressure,
            "short_note": short_note,
        }
    return customizations


def collect_answers() -> dict[str, object]:
    outcome = prompt("1. What should this assistant help with most?")
    failure_mode = prompt("2. What would make it feel unhelpful fastest?")
    uncertainty_behavior = prompt("3. When uncertain, how should it behave?")
    proactive_behavior = prompt("4. What should trigger interruption or proactive nudges?")
    approval_boundary = prompt("5. What always requires approval?")
    desired_feel = prompt("6. What should the assistant feel like in daily use?")
    lanes = parse_csv_list(prompt("7. What are the top active lanes right now? (comma-separated)"))
    foreground_lanes = parse_csv_list(prompt("8. Which lanes are in the foreground right now? (comma-separated)"))
    slips = prompt("9. What most often slips or gets dropped?")
    master_list_source = prompt("10. Where should the master task list live?")
    importance_over_urgency = parse_yes_no(prompt("11. Should importance outrank urgency? (yes/no)"))
    lane_customizations = collect_lane_customizations(lanes, foreground_lanes)

    return {
        "outcome": outcome,
        "failure_mode": failure_mode,
        "uncertainty_behavior": uncertainty_behavior,
        "proactive_behavior": proactive_behavior,
        "approval_boundary": approval_boundary,
        "desired_feel": desired_feel,
        "lanes": lanes,
        "foreground_lanes": foreground_lanes,
        "slips": slips,
        "master_list_source": master_list_source,
        "importance_over_urgency": importance_over_urgency,
        "lane_customizations": lane_customizations,
    }


def print_review_summary(pack: DaosPack) -> None:
    print("\nReview summary")
    print(f"- Outcome: {pack.assistant_charter.primary_outcome}")
    print(f"- Desired feel: {pack.assistant_charter.desired_feel}")
    print(f"- Lanes: {', '.join(pack.operating_profile.top_level_lanes)}")
    for lane in pack.operating_profile.lane_snapshots:
        print(
            f"  - {lane.name}: status={lane.status}, foreground={lane.foreground}, "
            f"pressure={lane.pressure}, note={lane.short_note}"
        )
    print(f"- Master list source: {pack.operating_profile.master_list_source}")


def confirm_write(pack: DaosPack) -> bool:
    print_review_summary(pack)
    return parse_yes_no(prompt("Write files now? (yes/no)"))


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    print("DAOS interactive setup wizard")
    print("This is a short first-pass install, not a full life-modeling session.")

    try:
        answers = collect_answers()
        pack = wizard_pack(answers, generator="scripts/daos_wizard.py")
        if not confirm_write(pack):
            raise ValueError("Wizard cancelled at review step.")
        destination = bootstrap(args.output_dir, use_filled_example=False, force=args.force)
        write_pack_core_files(destination, pack)
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"\nGenerated DAOS starter pack: {destination}")
    print("Next steps:")
    print("- review assistant-charter.md and operating-profile.md")
    print("- leave cadence-review.md for later")
    print("- run python scripts/daos_validate.py <pack-dir> to check readiness")
    print("- use harness/first-week.md after the first install")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
