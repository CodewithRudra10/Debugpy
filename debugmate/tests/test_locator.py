import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from debugmate.core.locator import locate_error
from debugmate.core.parser import ParsedError


class LocateErrorTests(unittest.TestCase):
    def test_reads_requested_source_line(self):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "sample.py"
            source_path.write_text("first line\nsecond line\n", encoding="utf-8")
            error = ParsedError("NameError", "failure", str(source_path), 2)

            located = locate_error(error)

        self.assertEqual(located.file, str(source_path))
        self.assertEqual(located.line, 2)
        self.assertEqual(located.source, "second line\n")

    @unittest.skipUnless(os.name == "nt", "Windows root-relative path behavior")
    def test_resolves_root_relative_path_from_current_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "locator.py"
            source_path.write_text("source line\n", encoding="utf-8")
            error = ParsedError("NameError", "failure", "\\locator.py", 1)

            with patch("debugmate.core.locator.Path.cwd", return_value=Path(directory)):
                located = locate_error(error)

        self.assertEqual(located.file, str(source_path))
        self.assertEqual(located.source, "source line\n")

    def test_missing_file_reports_resolved_path(self):
        with tempfile.TemporaryDirectory() as directory:
            error = ParsedError("NameError", "failure", "missing.py", 1)

            with patch("debugmate.core.locator.Path.cwd", return_value=Path(directory)):
                with self.assertRaisesRegex(FileNotFoundError, "missing.py"):
                    locate_error(error)


if __name__ == "__main__":
    unittest.main()
