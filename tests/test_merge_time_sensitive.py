import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "course-manager" / "scripts"))

import merge_time_sensitive as mts  # noqa: E402


def make_row(row_id, **overrides):
    row = {
        "id": row_id,
        "course": "MATH-4317-A",
        "title": "HW3",
        "event_kind": "due",
        "when": "2026-10-12",
        "confidence": "structured",
        "raw_excerpt": "",
        "source_type": "assignment",
        "source_url": "https://example.instructure.com/courses/1/assignments/2",
        "source_snapshot": "raw/assignments/2/latest.md",
        "estimated_workload": "2h",
        "priority_hint": "high",
        "status": "pending",
    }
    row.update(overrides)
    return row


class TestMergeRows(unittest.TestCase):
    def test_new_id_is_staged_as_pending(self):
        merged = mts.merge_rows(existing_rows=[], new_rows=[make_row("a")])
        self.assertEqual(merged[0]["status"], "pending")

    def test_existing_status_is_preserved_even_when_other_fields_change(self):
        existing = [make_row("a", status="imported", when="2026-10-12")]
        new = [make_row("a", status="pending", when="2026-10-15")]  # teacher moved the date
        merged = mts.merge_rows(existing, new)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["status"], "imported")
        self.assertEqual(merged[0]["when"], "2026-10-15")

    def test_dismissed_status_is_never_reset_to_pending(self):
        existing = [make_row("a", status="dismissed")]
        new = [make_row("a", status="pending")]
        merged = mts.merge_rows(existing, new)
        self.assertEqual(merged[0]["status"], "dismissed")

    def test_row_missing_from_new_candidates_is_preserved_not_deleted(self):
        existing = [make_row("a", status="imported"), make_row("b", status="pending")]
        new = [make_row("a", status="pending")]
        merged = mts.merge_rows(existing, new)
        ids = {row["id"] for row in merged}
        self.assertEqual(ids, {"a", "b"})
        preserved = next(row for row in merged if row["id"] == "b")
        self.assertEqual(preserved["status"], "pending")

    def test_multiple_new_and_existing_rows_merge_independently(self):
        existing = [make_row("a", status="imported"), make_row("b", status="dismissed")]
        new = [make_row("a", when="2026-11-01"), make_row("c")]
        merged = mts.merge_rows(existing, new)
        by_id = {row["id"]: row for row in merged}
        self.assertEqual(by_id["a"]["status"], "imported")
        self.assertEqual(by_id["a"]["when"], "2026-11-01")
        self.assertEqual(by_id["b"]["status"], "dismissed")
        self.assertEqual(by_id["c"]["status"], "pending")


class TestTableParsingAndFormatting(unittest.TestCase):
    def test_parse_table_round_trips_through_format_table(self):
        rows = [make_row("a"), make_row("b", status="imported")]
        table = mts.format_table(rows)
        parsed = mts.parse_table(table)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["id"], "a")
        self.assertEqual(parsed[1]["status"], "imported")

    def test_parse_table_on_missing_table_returns_empty_list(self):
        self.assertEqual(mts.parse_table("# Just a heading\n\nNo table here.\n"), [])

    def test_replace_table_preserves_surrounding_content(self):
        markdown = "# Title\n\n> [!info] usage note\n\n| id | status |\n|---|---|\n| a | pending |\n"
        new_table = "| id | status |\n|---|---|\n| a | imported |"
        result = mts.replace_table(markdown, new_table)
        self.assertIn("# Title", result)
        self.assertIn("> [!info] usage note", result)
        self.assertIn("| a | imported |", result)
        self.assertNotIn("| a | pending |", result)

    def test_replace_table_appends_when_no_table_exists_yet(self):
        markdown = "# Title\n\n> [!info] usage note\n"
        new_table = "| id | status |\n|---|---|\n| a | pending |"
        result = mts.replace_table(markdown, new_table)
        self.assertIn("# Title", result)
        self.assertIn("| a | pending |", result)


if __name__ == "__main__":
    unittest.main()
