# Test Configuration for yamlfmt

This directory contains tests for the yamlfmt cross-platform functionality.

## Test Files

- `test_yamlfmt.py`: Main test suite that validates yamlfmt functionality across different platforms

## Running Tests

### Local Testing

Build and install a wheel first (Go and Git are required for the build), then run
the standard-library test suite. For example, on Linux or macOS:

```bash
uv venv --python 3.15t
uv build --python 3.15t
source .venv/bin/activate
uv pip install --no-deps --force-reinstall dist/*.whl
EXPECTED_PYTHON_VERSION=3.15t python tests/test_yamlfmt.py -v
```

Use another version such as `3.11` or `3.15` in both the interpreter selection and
`EXPECTED_PYTHON_VERSION` to test it instead. On Windows, activate with
`.venv\Scripts\activate.ps1` and set `$env:EXPECTED_PYTHON_VERSION` before running
the test script. The tests intentionally import the installed wheel, not `src/`.

### CI Testing

The tests are automatically run in GitHub Actions across multiple platforms:

- Linux (Ubuntu)
- macOS
- Windows

Each platform builds and installs the package with Python 3.11, 3.12, 3.13, 3.14,
3.15, and free-threaded 3.15 (`3.15t`). Prereleases are allowed for 3.15 until the
final release. `EXPECTED_PYTHON_VERSION` verifies the actual interpreter version
and free-threaded build flag, and the `3.15t` lane asserts that the GIL is disabled.
All matrix entries are required; none use `continue-on-error`.

## Test Coverage

The test suite covers:

1. **Platform Detection**: Verifies the current platform can be detected
2. **Version Output**: Tests that yamlfmt can output version information
3. **Basic Formatting**: Checks the formatted YAML against the expected output
4. **Console Script**: Executes the installed `yamlfmt` entry point
5. **Help Output**: Tests that yamlfmt can show help information
6. **Module Import**: Verifies imports come from the installed wheel rather than `src/`
7. **Runtime Identity**: Checks the requested Python version and free-threaded/GIL state
8. **System Information**: Displays system information for debugging

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention (`test_*`)
2. Include appropriate error handling for cross-platform compatibility
3. Add descriptive docstrings
4. Use appropriate assertions for validation
