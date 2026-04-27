---
name: pytest
description: >
  AutoQA-Android pytest conventions and device fixture plugin. Use this skill when writing,
  running, or debugging tests in this project — especially when declaring device fixtures,
  using --device CLI options, structuring conftest.py files, or understanding how test files
  are organized under tests/.
---

# AutoQA-Android pytest Conventions

## Setup (required first time)

Run pytest from the project's virtual environment:

```bash
# python -m venv .venv
pip install pytest
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
# uv venv
uv pip install pytest
```

All `pytest` commands below assume the virtual environment is active or use the full path `.venv/bin/pytest`.

---

## Project structure

```
conftest.py (root)         ← does NOT exist; plugin is loaded via tests/conftest.py
pytest_plugins/
  __init__.py
  device.py                ← --device CLI option + dynamic device fixture registration
  pause_on_failure.py      ← --pause-on-failure flag; blocks before teardown on failure
actions/
  {feature}.py             ← reusable main-app steps (plain functions, no teardown)
helpers/
  system.py                ← system/auxiliary app operations (e.g. enable_bluetooth)
tests/
  conftest.py              ← pytest_plugins = ["pytest_plugins.device", "pytest_plugins.pause_on_failure"] + app fixtures
  test_{module}.py
```

`pythonpath = ["."]` in `pyproject.toml` ensures the project root is on `sys.path` so
`pytest_plugins.device` is importable from `tests/conftest.py` without installing the package.

---

## Device fixture plugin (`pytest_plugins/device.py`)

### How it works

The plugin registers session-scoped `u2.Device` fixtures dynamically at configure time.
Fixture names come from the `--device` CLI option. Tests simply declare the fixture by name.

### Default device (no --device flag)

When no `--device` is given, a fixture named `d` is registered using `u2.connect()` (auto-detect):

```bash
.venv/bin/pytest tests/
```

```python
import uiautomator2 as u2

def test_home(d: u2.Device):
    print(d.device_info)
```

### Named devices (single)

```bash
.venv/bin/pytest --device phone:emulator-5554 tests/
```

```python
def test_home(phone: u2.Device):
    assert phone.device_info
```

### Multiple devices

Repeat `--device` for each device. Each gets its own named fixture:

```bash
.venv/bin/pytest --device phone:emulator-5554 --device rack:10.114.77.100:5555 tests/
```

```python
def test_cross_device(phone: u2.Device, rack: u2.Device):
    phone.app_start("com.example.app")
    rack.app_start("com.example.app")
```

### Serial format

| Device type        | Serial example              |
|--------------------|-----------------------------|
| USB device         | `d74e53a3`                  |
| Emulator           | `emulator-5554`             |
| Network (adb over TCP) | `10.114.77.100:5555`    |

Check connected serials with:
```bash
adb devices
```

### Validation

If `--device` is provided but the format is wrong (missing `:`, blank name, or blank serial),
pytest exits immediately with a `UsageError` before any test runs.

---

## Pause-on-failure plugin (`pytest_plugins/pause_on_failure.py`)

### Purpose

When running with an agent, use `--pause-on-failure`.  On each test-body failure the
session **blocks before teardown**, keeping the device in the exact failure state so the
agent can inspect the screen, dump hierarchy, or interact with the device to diagnose the
problem.  After the agent sends Enter to resume, teardown runs and pytest continues to
the next test — all tests are executed.

### Usage

```bash
.venv/bin/pytest --pause-on-failure tests/
```

The plugin prints a `PAUSED` banner with the failure details, then waits for a newline
on `/dev/tty`.  The agent sends Enter via `send_to_terminal` to resume, after which
teardown proceeds and the next test starts.

A safety timeout of **600 seconds** auto-resumes the session if no input arrives, so
the process never hangs forever.

---

## conftest.py patterns

### App-level fixture (with teardown)

Place in `tests/conftest.py`:

```python
import pytest
import uiautomator2 as u2

@pytest.fixture
def logged_in(phone: u2.Device):
    # setup
    phone.app_start("com.example.app")
    phone(text="Login").click()
    yield
    # teardown
    phone.app_stop("com.example.app")
```

### autouse fixture (every test in the file/folder)

```python
@pytest.fixture(autouse=True)
def launch_app(phone: u2.Device):
    phone.app_start("com.example.app")
    yield
    phone.app_stop("com.example.app")
```

### conftest.py vs actions.py decision rule

| Situation | Where |
|-----------|-------|
| Needs teardown (logout, state cleanup) | `conftest.py` fixture |
| Reusable steps, no teardown | `actions/{feature}.py` plain function |
| Every test in a file needs this state | `conftest.py` fixture with `autouse=True` |

---

## Reference

- [Running tests](references/running-tests.md)
- [Test structure conventions](references/test-structure.md)
