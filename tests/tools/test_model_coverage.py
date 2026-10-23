"""Verify that coverage counts source lines, not interpreter bookkeeping."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import model_coverage


class CoverageMeasurementTests(unittest.TestCase):
    def report_for(self, source):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            model = root / "model"
            model.mkdir()
            path = model / "sample.py"
            path.write_text(source, encoding="utf-8")

            def exercise():
                # Execute the real fixture under trace; leave its function uncalled.
                exec(compile(source, str(path), "exec"), {"__file__": str(path)})
                return unittest.TestResult()

            output = io.StringIO()
            with patch.object(model_coverage, "MODEL", model), \
                    patch.object(model_coverage, "SOURCE", root), \
                    patch.object(model_coverage, "_run_suite", exercise), \
                    patch.object(model_coverage.sys, "path", list(model_coverage.sys.path)), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(model_coverage.main(), 0)
            return output.getvalue()

    def test_docstring_only_module_has_no_executable_source_lines(self):
        report = self.report_for('"""Documentation only."""\n')
        self.assertIn("model/sample.py: 0/0 (n/a)", report)

    def test_unexecuted_real_line_stays_in_denominator_and_is_listed(self):
        report = self.report_for('"""Fixture."""\nvalue = 1\ndef unused():\n    return value\n')
        self.assertIn("model/sample.py: 2/3 (66.67%)", report)
        self.assertIn("Missing source lines: 4", report)


if __name__ == "__main__":
    unittest.main()
