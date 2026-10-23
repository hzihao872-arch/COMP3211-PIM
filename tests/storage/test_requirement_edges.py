"""FR-45: systematic snapshot schema rejection and live-state preservation."""

import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from controller.cli import CommandController
from model.manager import PIMManager


class SnapshotRequirementTests(unittest.TestCase):
    def test_missing_extra_keys_and_invalid_fields_are_rejected_atomically(self):
        """Mutate each root/record key and every data field in a valid four-type file."""
        rows = [
            {"id": 1, "type": "note", "text": "memo"},
            {"id": 2, "type": "task", "description": "work", "deadline": "2026-01-01 00:00"},
            {"id": 3, "type": "event", "description": "meet", "start_time": "2026-01-01 00:00", "alarm_time": "2026-01-02 00:00"},
            {"id": 4, "type": "contact", "name": "Li", "address": "Road", "mobile_number": "+001"},
        ]
        root = {"format": "COMP3211-PIM", "version": 1, "next_id": 5, "records": rows}
        mutations = []
        for key in root:
            sample = copy.deepcopy(root)
            del sample[key]
            mutations.append((f"missing root {key}", sample))
        sample = copy.deepcopy(root)
        sample["extra"] = True
        mutations.append(("extra root key", sample))
        for key, bad_values in {
            "format": [None, "unknown"], "version": [None, True, 2],
            "next_id": [None, True, 0, 4, "5"], "records": [None, {}, "records"],
        }.items():
            for bad in bad_values:
                sample = copy.deepcopy(root)
                sample[key] = bad
                mutations.append((f"invalid root {key}: {bad!r}", sample))
        for index, row in enumerate(rows):
            for key in row:
                sample = copy.deepcopy(root)
                del sample["records"][index][key]
                mutations.append((f"missing {row['type']} {key}", sample))
            sample = copy.deepcopy(root)
            sample["records"][index]["extra"] = "unexpected"
            mutations.append((f"extra {row['type']} key", sample))
            for key in row:
                if key == "id":
                    bad_values = [None, True, 0, "1", 99]
                elif key == "type":
                    bad_values = [None, "unknown", row["type"].upper()]
                elif key in {"deadline", "start_time", "alarm_time"}:
                    bad_values = [None, "2026-02-30 00:00", "2026-01-01T00:00", "2026-01-01 00:00+08:00"]
                else:
                    bad_values = [None, 3, "   ", "two\nlines", "bad\ud800"]
                for bad in bad_values:
                    sample = copy.deepcopy(root)
                    sample["records"][index][key] = bad
                    mutations.append((f"invalid {row['type']} {key}: {bad!r}", sample))
        for label, changed_rows in (("non-object row", [None]), ("duplicate IDs", [rows[0], rows[0]]),
                                    ("descending IDs", list(reversed(rows)))):
            sample = copy.deepcopy(root)
            sample["records"] = changed_rows
            mutations.append((label, sample))
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            manager = PIMManager()
            manager.create_note("retain this collection")
            controller = CommandController(manager, cwd)
            before = manager.list_all(), manager.next_id
            for label, snapshot in mutations:
                with self.subTest(case=label):
                    (cwd / "candidate.pim").write_text(json.dumps(snapshot), encoding="utf-8")
                    output = io.StringIO()
                    # Explicitly authorize replacement so this still exercises file validation.
                    controller.run(io.StringIO('load "candidate.pim" force=true\nshow 1\n'), output)
                    self.assertEqual(output.getvalue().count("Error: FORMAT:"), 1)
                    self.assertIn("text: retain this collection", output.getvalue())
                    self.assertIs(controller._manager, manager)
                    self.assertEqual((manager.list_all(), manager.next_id), before)
