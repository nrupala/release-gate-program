#!/usr/bin/env python3
"""Tests for scripts/check_docs.py, the document-set validator.

Each test builds a small fixture document tree in a temporary directory,
copies the real validator into it, and runs it as a subprocess — the same
way CI runs it. Run with: ``python3 -m unittest discover -s tests -v``
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = REPO_ROOT / "scripts" / "check_docs.py"


class CheckDocsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="check-docs-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "scripts").mkdir()
        shutil.copy(VALIDATOR, self.tmp / "scripts" / "check_docs.py")

    def write(self, name, text):
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_validator(self):
        return subprocess.run(
            [sys.executable, str(self.tmp / "scripts" / "check_docs.py"),
             str(self.tmp)],
            capture_output=True, text=True, timeout=60,
        )

    def test_valid_set_passes(self):
        self.write("LICENSE", "licence text\n")
        self.write("README.md", "# Doc\n\nSee [LICENSE](LICENSE).\n")
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 problem(s)", result.stdout)

    def test_broken_relative_link_fails(self):
        self.write("README.md", "# Doc\n\nSee [missing](NOPE.md).\n")
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("broken relative link", result.stdout)

    def test_empty_markdown_fails(self):
        self.write("README.md", "# Doc\n")
        self.write("EMPTY.md", "   \n")
        result = self.run_validator()
        self.assertEqual(result.returncode, 1)
        self.assertIn("file is empty", result.stdout)

    def test_external_links_are_not_checked_as_files(self):
        self.write(
            "README.md",
            "# Doc\n\n[site](https://example.com/nonexistent) "
            "[mail](mailto:a@example.com) [anchor](#doc)\n",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
