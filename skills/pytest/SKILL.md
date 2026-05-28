---
name: pytest
description: "Define pytest script standards for Android uiautomator2 tests, including file/function structure, run commands, device fixture selection, and pause-on-failure usage. Use when creating or executing pytest tests without business-specific content. Trigger keywords: pytest standard, test template, run pytest, --device, pause-on-failure."
user-invocable: false
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

If user not specify weather to use `--pause-on-failure` or not, default to not using it

With `--pause-on-failure` enabled:
- Test execution pauses before teardown on failure
- Device state is preserved for inspection
- Resume by sending a signal to the pytest process, the command will be printed in the pytest output when paused

Example:

```bash
uv run pytest tests -v --pause-on-failure
```

```bash
# To resume after failure pause, run in a new process or terminal:
kill -SIGUSR1 <pytest-pid>
```

## Rules

- Every pytest run command should be executed via `uv` and redirect output to this log file for later review:

```bash
log="/tmp/qamule-$(date +%Y%m%d-%H%M%S)-$$.log"
touch "$log" && printf "Pytest log initialized: $log\n"

uv run pytest [command/options] >"$log" 2>&1
ec=$?
printf '\nQAMule pytest exit code=%s' "$ec" >>"$log"
```

- If `--pause-on-failure` is not used, you must use `sync` mode to run this process and review the log file after completion

- If `--pause-on-failure` is used, you must use `async` mode to run this process and run the following command **in `sync` mode** to monitor the log file for the pause or exit message **in a different terminal**:

```bash
bash <path-to-this-skill>/scripts/monitor.sh "$log"
```

- Don't write complex command, just use the command defined in skill
- Don't use `subagent` to run this process, always **run in the current agent**.
