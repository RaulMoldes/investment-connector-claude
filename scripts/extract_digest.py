#!/usr/bin/env python3
"""
extract_digest.py — pull the Telegram/Email digest block out of a weekly report.

The routine writes the full report with a section that starts with "## Email Digest"
and contains a fenced code block. This script extracts that fenced block's contents
and prints them to stdout. If the marker isn't found, it falls back to a best-effort
summary built from the "Ideas This Week" section.

Usage:
    python3 scripts/extract_digest.py history/2026-W17.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


DIGEST_HEADER_PATTERNS = [
    re.compile(r"^##\s+Email\s+Digest", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^##\s+Digest", re.IGNORECASE | re.MULTILINE),
]


def extract_fenced_block_after(text: str, start: int) -> str | None:
    """Find the first fenced ``` block after `start` and return its contents."""
    fence_open = re.search(r"^```[a-zA-Z]*\s*$", text[start:], re.MULTILINE)
    if not fence_open:
        return None
    block_start = start + fence_open.end()
    fence_close = re.search(r"^```\s*$", text[block_start:], re.MULTILINE)
    if not fence_close:
        return None
    return text[block_start : block_start + fence_close.start()].strip()


def fallback_summary(text: str, report_id: str) -> str:
    """If no explicit digest block, build a minimal one from the Ideas section."""
    ideas_match = re.search(
        r"^##\s+Ideas\s+This\s+Week\s*$(.*?)(?=^##\s+)",
        text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    if not ideas_match:
        return (
            f"Weekly Research — {report_id}\n\n"
            "Could not extract a digest from the report. "
            "Check the full report on GitHub."
        )

    ideas_block = ideas_match.group(1)
    # Pull each "### N. ..." heading line
    idea_lines = re.findall(r"^###\s+\d+\.\s+(.+)$", ideas_block, re.MULTILINE)

    lines = [f"Weekly Research — {report_id}", ""]
    if idea_lines:
        lines.append("Ideas:")
        for idea in idea_lines:
            lines.append(f"  • {idea.strip()}")
    else:
        lines.append("No clear ideas flagged this week (see full report).")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: extract_digest.py <path-to-report.md>", file=sys.stderr)
        return 1

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    report_id = path.stem  # e.g. "2026-W17"

    # Try to find the explicit digest section
    for pattern in DIGEST_HEADER_PATTERNS:
        match = pattern.search(text)
        if match:
            digest = extract_fenced_block_after(text, match.end())
            if digest:
                print(digest)
                return 0

    # Fallback
    print(fallback_summary(text, report_id))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
