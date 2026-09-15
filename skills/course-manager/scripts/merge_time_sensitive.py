"""Merge helpers for CourseManager's PlanVault time-sensitive staging file.

The one piece of must-be-correct mechanical logic in this skill: a
consuming planning tool (e.g. PlanVault) owns the `status` column on each
row, and regenerating the staging file must never silently reset or drop
what it already set. See references/time-sensitive.md for the full schema
and rule.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROW_FIELDS = [
    "id", "course", "title", "event_kind", "when", "confidence",
    "raw_excerpt", "source_type", "source_url", "source_snapshot",
    "estimated_workload", "priority_hint", "status",
]


def merge_rows(existing_rows: list[dict], new_rows: list[dict]) -> list[dict]:
    """Merge this run's candidate rows into the existing staging-file rows.

    - A row whose `id` already existed keeps its existing `status`,
      regardless of whether other fields (e.g. `when`) changed.
    - A row with a new `id` gets `status: "pending"`.
    - An existing row whose `id` is absent from this run's candidates is
      preserved as-is, never silently dropped (mirrors canvas-manager's
      manifest.py: missing from this run means "not seen again," not
      "delete it").
    """
    existing_by_id = {row["id"]: row for row in existing_rows}
    seen_ids: set[str] = set()
    merged: list[dict] = []

    for new_row in new_rows:
        rid = new_row["id"]
        seen_ids.add(rid)
        merged_row = dict(new_row)
        merged_row["status"] = existing_by_id[rid]["status"] if rid in existing_by_id else "pending"
        merged.append(merged_row)

    for rid, row in existing_by_id.items():
        if rid not in seen_ids:
            merged.append(row)

    return merged


def parse_table(markdown: str) -> list[dict]:
    """Parse the staging file's single Markdown table into row dicts.

    Tolerant of a missing table (returns []) — a first-ever run has no
    existing file to merge against.
    """
    lines = [ln for ln in markdown.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 3:
        return []
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def format_table(rows: list[dict]) -> str:
    """Render row dicts back into the staging file's Markdown table."""
    header = "| " + " | ".join(ROW_FIELDS) + " |"
    separator = "|" + "|".join(["---"] * len(ROW_FIELDS)) + "|"
    body_lines = []
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|") for field in ROW_FIELDS]
        body_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body_lines])


def replace_table(markdown: str, new_table: str) -> str:
    """Replace the first Markdown table found in `markdown` with `new_table`,
    preserving everything else (frontmatter, the `> [!info]` usage note)
    byte-for-byte. If no table exists yet, append it at the end."""
    lines = markdown.splitlines()
    table_start = next((i for i, ln in enumerate(lines) if re.match(r"^\s*\|", ln)), None)
    if table_start is None:
        suffix = "\n" if markdown and not markdown.endswith("\n") else ""
        return markdown + suffix + "\n" + new_table + "\n"
    table_end = table_start
    while table_end < len(lines) and re.match(r"^\s*\|", lines[table_end]):
        table_end += 1
    return "\n".join([*lines[:table_start], new_table, *lines[table_end:]])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge new time-sensitive candidates into the PlanVault "
        "staging file, preserving each existing row's status column."
    )
    parser.add_argument("--staging-file", required=True, type=Path)
    parser.add_argument(
        "--input", required=True, type=Path,
        help="JSON file: list of this run's candidate row objects (no status field needed; new rows are staged as pending).",
    )
    args = parser.parse_args()

    existing_markdown = args.staging_file.read_text(encoding="utf-8") if args.staging_file.exists() else ""
    existing_rows = parse_table(existing_markdown)
    new_rows = json.loads(args.input.read_text(encoding="utf-8"))
    for row in new_rows:
        row.setdefault("status", "pending")

    merged = merge_rows(existing_rows, new_rows)
    new_table = format_table(merged)
    args.staging_file.parent.mkdir(parents=True, exist_ok=True)
    args.staging_file.write_text(replace_table(existing_markdown, new_table), encoding="utf-8")
    print(json.dumps({"total_rows": len(merged), "new_or_updated": len(new_rows)}, indent=2))


if __name__ == "__main__":
    main()
