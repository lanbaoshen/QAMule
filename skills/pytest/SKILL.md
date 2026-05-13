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

## Plugins

- Fixture implementations are fixed contracts; do not read existing fixture source files.
- Use fixtures strictly as documented in this skill.

### Device Mode

- Fixture implementations are fixed contracts; do not read existing fixture source files.
- Use fixtures strictly as documented in this skill.

- Default mode (single device): use fixture `d`, no `--device` argument
- Named device mode: pass `--device NAME:SERIAL` and use matching fixture name in test function
- Multi-device mode: repeat `--device NAME:SERIAL` and reference each name as a fixture

Example:

```bash
# Single device (default)
uv run pytest tests -v
# Named device
uv run pytest tests -v --device phone:emulator-5554 --device tablet:127.0.0.1:9887
```

### Pause on Failure

With `--pause-on-failure` enabled:
- Test execution pauses before teardown on failure
- Device state is preserved for inspection
- Resume by pressing Enter (or wait for timeout auto-resume)

Example:

```bash
uv run pytest tests -v --pause-on-failure
```
