#!/usr/bin/env python3
"""
Test suite for yamlfmt functionality across different platforms.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import sysconfig
import tempfile
import unittest
from pathlib import Path


class TestYamlfmtOutput(unittest.TestCase):
    """Test yamlfmt output across different platforms."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_yaml_content = """
# Test YAML file
name: test
version: 1.0.0
dependencies:
  - package1
  - package2
config:
    setting1: value1
    setting2:    value2
list:
- item1
-  item2
-   item3
"""

    def test_platform_detection(self):
        """Test that we can detect the current platform."""
        current_platform = platform.system()
        self.assertIn(current_platform, ["Linux", "Darwin", "Windows"])

    def test_yamlfmt_version(self):
        """Test that yamlfmt can output version information."""
        # Test version output with different possible flags
        result = subprocess.run(
            [sys.executable, "-m", "yamlfmt", "-version"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, f"yamlfmt version command failed: {result.stderr}")

    def test_yamlfmt_format_basic(self):
        """Test basic YAML formatting functionality."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(self.test_yaml_content)
            temp_file = Path(f.name)

        try:
            # Try to format the file
            result = subprocess.run(
                [sys.executable, "-m", "yamlfmt", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            self.assertEqual(result.returncode, 0, f"yamlfmt formatting failed: {result.stderr}")

            self.assertEqual(
                temp_file.read_text(),
                "# Test YAML file\n"
                "name: test\n"
                "version: 1.0.0\n"
                "dependencies:\n"
                "  - package1\n"
                "  - package2\n"
                "config:\n"
                "  setting1: value1\n"
                "  setting2: value2\n"
                "list:\n"
                "  - item1\n"
                "  - item2\n"
                "  - item3\n",
            )

        finally:
            # Clean up temporary file
            if temp_file.exists():
                temp_file.unlink()

    def test_help_output(self):
        """Test that yamlfmt can show help information."""
        result = subprocess.run(
            [sys.executable, "-m", "yamlfmt", "-h"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, f"yamlfmt help command failed: {result.stderr}")

    def test_module_import(self):
        """Test the installed wheel, without falling back to the source tree."""
        import yamlfmt

        self.assertEqual(yamlfmt.BIN_NAME, "yamlfmt")
        self.assertIsNotNone(yamlfmt.__version__)
        src_dir = Path(__file__).resolve().parents[1] / "src"
        self.assertFalse(Path(yamlfmt.__file__).resolve().is_relative_to(src_dir))

    def test_console_script(self):
        """Test the wheel's installed console entry point as well as python -m."""
        result = subprocess.run(["yamlfmt", "-version"], capture_output=True, text=True, timeout=30, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip())

    def test_runtime_identity(self):
        """Fail CI if interpreter selection silently falls back to another runtime."""
        expected = os.environ.get("EXPECTED_PYTHON_VERSION")
        if expected is None:
            self.skipTest("Set EXPECTED_PYTHON_VERSION to check the selected interpreter")
        self.assertEqual(platform.python_implementation(), "CPython")
        self.assertEqual(f"{sys.version_info.major}.{sys.version_info.minor}", expected.removesuffix("t"))
        free_threaded = expected.endswith("t")
        self.assertEqual(bool(sysconfig.get_config_var("Py_GIL_DISABLED")), free_threaded)
        if free_threaded:
            self.assertFalse(sys._is_gil_enabled(), "The free-threaded test must run with the GIL disabled")

    def test_system_info(self):
        """Display system information for debugging."""
        info = {
            "Platform": platform.system(),
            "Platform Release": platform.release(),
            "Platform Version": platform.version(),
            "Architecture": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": sys.version,
            "Python Executable": sys.executable,
            "Py_GIL_DISABLED": sysconfig.get_config_var("Py_GIL_DISABLED"),
            "GIL Enabled": sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True,
        }

        print("\n" + "=" * 50)
        print("SYSTEM INFORMATION")
        print("=" * 50)
        for key, value in info.items():
            print(f"{key:20}: {value}")
        print("=" * 50)


if __name__ == "__main__":
    unittest.main()
