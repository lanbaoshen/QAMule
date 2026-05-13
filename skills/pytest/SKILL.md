---
name: pytest
description: "Define pytest script standards for Android uiautomator2 tests, including file/function structure, run commands, device fixture selection, and pause-on-failure usage. Use when creating or executing pytest tests without business-specific content. Trigger keywords: pytest standard, test template, run pytest, --device, pause-on-failure."
---

# Pytest Standard

Define pytest conventions for Android automation.

## Script Template

- File naming: `tests/test_<module>.py`
- Function naming: `test_<behavior>`
- Use `uiautomator2 as u2` and typed device fixtures
- Add assertions for each major step
- Use `wait()` / `wait_gone()`; avoid `sleep()`

### Template

```python
"""Test scenario: <short description>."""
import uiautomator2 as u2


def test_<behavior>(d: u2.Device):
    """<what this test verifies>."""
    # Step 1
    # <u2 operation>
    assert <condition>

    # Step 2
    # <u2 operation>
    assert <condition>
```

## Device Mode

- Default mode (single device): use fixture `d`, no `--device` argument
- Named device mode: pass `--device NAME:SERIAL` and use matching fixture name in test function
- Multi-device mode: repeat `--device NAME:SERIAL` and reference each name as a fixture

## Run Commands

Basic:

```bash
uv run pytest tests/test_xxx.py -v
```

With failure pause:

```bash
uv run pytest tests/test_xxx.py -v --pause-on-failure
```

Named device:

```bash
uv run pytest --device phone:emulator-5554 --pause-on-failure
```

Multiple devices:

```bash
uv run pytest --device phone:emulator-5554 --device tablet:192.168.1.100 --pause-on-failure
```

## Pause on Failure

With `--pause-on-failure` enabled:
- Test execution pauses before teardown on failure
- Device state is preserved for inspection
- Resume by pressing Enter (or wait for timeout auto-resume)

## Completion Checks

Before finishing, verify:
- Script contains no business-domain assumptions unless user provided them
- Every major step has an assertion
- No `sleep` calls are introduced
- Fixture names and CLI `--device` arguments match
- Returned command is directly executable
