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
    def test_user_priority_is_preserved_and_defaults_empty(self):
        existing = [make_row("a", user_priority="high", status="ignored")]
        merged = mts.merge_rows(existing, [make_row("a"), make_row("b")])
        by_id = {r["id"]: r for r in merged}
        self.assertEqual(by_id["a"]["user_priority"], "high")
        self.assertEqual(by_id["a"]["status"], "ignored")
        self.assertEqual(by_id["b"]["user_priority"], "")

    def test_old_13_column_file_round_trips_with_new_columns(self):
        old_table = "| " + " | ".join(mts.ROW_FIELDS[:12] + ["status"]) + " |\n|" + "---|" * 13 + "\n" \
            + "| a | C | T | due | 2026-10-12 | structured |  | assignment |  |  | 2h | high | done |"
        rows = mts.parse_table(old_table)
        merged = mts.merge_rows(rows, [make_row("a", category="task", points="10")])
        table = mts.format_table(merged)
        back = mts.parse_table(table)
        self.assertEqual(back[0]["status"], "done")
        self.assertEqual(back[0]["category"], "task")
        self.assertEqual(back[0]["user_priority"], "")

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

    def test_cells_containing_pipes_round_trip(self):
        # format_table escapes | as \| ; parse_table must not split on it
        row = make_row("p2", title="P2 | Part A", raw_excerpt='"due Thu | no late"', status="done")
        parsed = mts.parse_table(mts.format_table([row]))
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["title"], "P2 | Part A")
        self.assertEqual(parsed[0]["raw_excerpt"], '"due Thu | no late"')
        self.assertEqual(parsed[0]["status"], "done")

    def test_status_survives_regeneration_for_rows_with_pipes(self):
        # a consumer ticked the row; the next run re-extracts it — status must not reset to pending
        existing_md = mts.format_table([make_row("p2", title="P2 | Part A", status="done")])
        existing = mts.parse_table(existing_md)
        merged = mts.merge_rows(existing, [make_row("p2", title="P2 | Part A (updated)")])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["status"], "done")

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
