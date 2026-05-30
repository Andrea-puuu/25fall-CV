"""Tests for verifying the LICENSE file contents."""

import os
import re

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LICENSE_PATH = os.path.join(REPO_ROOT, "LICENSE")

EXPECTED_COPYRIGHT_HOLDER = "anytimeflammate_"
EXPECTED_YEAR = "2026"


class TestLicenseFile:
    """Verify that a LICENSE file exists with the correct copyright holder and year."""

    def test_license_file_exists(self):
        assert os.path.isfile(LICENSE_PATH), (
            f"LICENSE file not found at {LICENSE_PATH}"
        )

    def test_license_contains_correct_year(self):
        content = _read_license()
        copyright_line = _find_copyright_line(content)
        assert EXPECTED_YEAR in copyright_line, (
            f"Expected year '{EXPECTED_YEAR}' in copyright line, "
            f"got: '{copyright_line}'"
        )

    def test_license_contains_correct_copyright_holder(self):
        content = _read_license()
        copyright_line = _find_copyright_line(content)
        assert EXPECTED_COPYRIGHT_HOLDER in copyright_line, (
            f"Expected copyright holder '{EXPECTED_COPYRIGHT_HOLDER}' in "
            f"copyright line, got: '{copyright_line}'"
        )

    def test_copyright_line_format(self):
        """Verify the copyright line matches 'Copyright (c) <year> <holder>'."""
        content = _read_license()
        copyright_line = _find_copyright_line(content)
        pattern = rf"Copyright \(c\) {re.escape(EXPECTED_YEAR)} {re.escape(EXPECTED_COPYRIGHT_HOLDER)}"
        assert re.search(pattern, copyright_line), (
            f"Copyright line does not match expected format "
            f"'Copyright (c) {EXPECTED_YEAR} {EXPECTED_COPYRIGHT_HOLDER}'. "
            f"Got: '{copyright_line}'"
        )

    def test_license_is_mit(self):
        content = _read_license()
        assert content.startswith("MIT License"), (
            "LICENSE file does not start with 'MIT License'"
        )


def _read_license() -> str:
    with open(LICENSE_PATH, encoding="utf-8") as f:
        return f.read()


def _find_copyright_line(content: str) -> str:
    for line in content.splitlines():
        if "Copyright" in line:
            return line.strip()
    pytest.fail("No line containing 'Copyright' found in LICENSE file")
