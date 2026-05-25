
# DAOS baseline note: current public framework baseline is v0.2.7; this module remains part of the current release surface.
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_HOT_CACHE_SECTIONS = (
    "Current Focus",
    "Current Corrections",
    "Current State",
    "Open Problems",
    "System Priorities",
)
BASELINE_MEMORY_FILES = (
    "AGENTS.md",
    "wiki/WIKI.md",
    "wiki/cache/HOT-CACHE-SPEC.md",
    "wiki/cache/MEMORY-OPERATING-MODEL.md",
    "wiki/cache/hot-cache.md",
    "wiki/cache/hot-cache-log.md",
    "wiki/cache/agent-continuity.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/raw/README.md",
    "wiki/sources/README.md",
)
DATED_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\b")
SECTION_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


@dataclass
class ParityFinding:
    severity: str
    message: str


@dataclass
class ParityResult:
    findings: list[ParityFinding] = field(default_factory=list)
    repairs_made: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        severities = {finding.severity for finding in self.findings}
        if "error" in severities:
            return "drift"
        if "warning" in severities:
            return "watch"
        return "healthy"

    def error(self, message: str) -> None:
        self.findings.append(ParityFinding("error", message))

    def warning(self, message: str) -> None:
        self.findings.append(ParityFinding("warning", message))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def dated_headings(path: Path) -> list[str]:
    dates: list[str] = []
    for line in read_text(path).splitlines():
        match = DATED_HEADING_RE.match(line)
        if match:
            dates.append(match.group(1))
    return dates


def markdown_sections(path: Path) -> list[str]:
    sections: list[str] = []
    for line in read_text(path).splitlines():
        match = SECTION_HEADING_RE.match(line)
        if match:
            sections.append(match.group(1).strip())
    return sections


def check_required_files(root: Path, result: ParityResult) -> None:
    missing = [name for name in BASELINE_MEMORY_FILES if not (root / name).is_file()]
    if missing:
        result.error("missing baseline memory files: " + ", ".join(missing))


def check_wiki_log_order(root: Path, result: ParityResult) -> None:
    path = root / "wiki" / "log.md"
    if not path.is_file():
        return
    dates = dated_headings(path)
    if len(dates) >= 2 and dates != sorted(dates, reverse=True):
        result.warning("wiki/log.md dated entries are not newest-first; newest activity should be at the top")


def check_hot_cache_log_order(root: Path, result: ParityResult) -> None:
    path = root / "wiki" / "cache" / "hot-cache-log.md"
    if not path.is_file():
        return
    dates = dated_headings(path)
    if len(dates) >= 2 and dates != sorted(dates, reverse=True):
        result.warning("wiki/cache/hot-cache-log.md dated entries are not reverse-chronological; newest front-door transitions should be at the top")


def check_hot_cache_shape(root: Path, result: ParityResult) -> None:
    path = root / "wiki" / "cache" / "hot-cache.md"
    if not path.is_file():
        return
    sections = markdown_sections(path)
    expected = list(REQUIRED_HOT_CACHE_SECTIONS)
    if sections != expected:
        result.warning(
            "wiki/cache/hot-cache.md section shape drifted; expected exactly: "
            + ", ".join(expected)
        )


def check_read_order_semantics(root: Path, result: ParityResult) -> None:
    candidates = [root / "AGENTS.md", root / "wiki" / "WIKI.md"]
    combined = "\n".join(read_text(path).lower() for path in candidates if path.is_file())
    if not combined:
        return
    if "thread" not in combined or "hot-cache" not in combined:
        result.warning("read-order semantics may be thin; expected local thread plus hot-cache orientation language")


def check_raw_source_boundaries(root: Path, result: ParityResult) -> None:
    raw_readme = root / "wiki" / "raw" / "README.md"
    source_readme = root / "wiki" / "sources" / "README.md"
    combined = "\n".join(read_text(path).lower() for path in (raw_readme, source_readme) if path.is_file())
    if not combined:
        return
    if "raw" not in combined or "source" not in combined:
        result.warning("raw/source boundary docs may be too thin; expected explicit raw and source classification language")


def check_agent_continuity_freshness(root: Path, result: ParityResult) -> None:
    path = root / "wiki" / "cache" / "agent-continuity.md"
    if not path.is_file():
        return
    text = read_text(path).lower()
    if "agent" in text and "last updated" not in text and "updated" not in text:
        result.warning("wiki/cache/agent-continuity.md has fallback material but no visible freshness marker")


def audit_memory_parity(pack_dir: str | Path) -> ParityResult:
    root = Path(pack_dir).expanduser().resolve()
    result = ParityResult()
    if not root.exists():
        result.error(f"pack directory does not exist: {root}")
        return result
    if not root.is_dir():
        result.error(f"pack path is not a directory: {root}")
        return result

    check_required_files(root, result)
    check_wiki_log_order(root, result)
    check_hot_cache_log_order(root, result)
    check_hot_cache_shape(root, result)
    check_read_order_semantics(root, result)
    check_raw_source_boundaries(root, result)
    check_agent_continuity_freshness(root, result)
    return result
