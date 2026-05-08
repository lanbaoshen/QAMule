---
name: pytest
description: "Generate pytest test scripts from successful device operations. Use when the QA agent completes a purposeful test scenario (not exploration) and the user wants a reusable, repeatable test or execute tests. Trigger keywords: generate test, record test, save as test, create test script, execute tests, pytest."
---

# Pytest Recorder

Generate reusable pytest test files from successful QA operations on Android devices.

## Procedure

### 1. Collect u2 Python Code During Execution

Every `u2cli` command prints equivalent Python code in its output. As you execute each step:
- Note the Python code snippet from the output
- Note what assertion confirms success (element appeared, text changed, etc.)

### 2. Determine Test Identity

From the task, derive:
- **Test name**: `test_{action}_{target}`
- **File name**: `tests/test_{feature}.py` — group by feature, not by individual flow
- **Scenario description**: One-line docstring

If the target file already exists, append the new test function to it instead of creating a new file.

### 3. Assemble the Test File

Write the test to `tests/` using this structure:

```python
"""Test scenario: {one-line description}."""
import uiautomator2 as u2


def test_{name}(d: u2.Device):
    """{Scenario description}."""
    # Step 1: {what this does}
    {u2 python code}
    assert {assertion}

    # Step 2: {what this does}
    {u2 python code}
    assert {assertion}

    # ...
```

The `d` fixture is provided by `pytest_plugins/device.py` (session-scoped, auto-registered).
Do NOT redefine it in test files. For multi-device tests, use `--device name:serial` and
reference the named fixture (e.g., `def test_foo(phone: u2.Device)`).

## Rules

1. **Only record successful paths** — every line must have been executed and verified on device
2. **Exact selectors** — use what actually worked, do not guess
3. **No sleep** — use `wait()` / `wait_gone()`
4. **Realistic timeouts** — use what actually worked
5. After generating, tell the user how to run — see [execution](./references/execution.md) for `--device` and `--pause-on-failure` usage
