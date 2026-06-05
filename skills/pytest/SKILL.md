---
name: pytest
description: "Define pytest script standards for Android uiautomator2 tests, including file/function structure, run commands, device fixture selection, and pause-on-failure usage. Use when creating or executing pytest tests without business-specific content. Trigger keywords: pytest standard, test template, run pytest, --device, pause-on-failure."
user-invocable: false
---

# Pytest Standard

Pytest conventions for Android automation.

## Script Template

- File: `tests/test_<module>.py`
- Function: `test_<behavior>`
- Import `uiautomator2 as u2` and use fixtures
- Assert each major step

Example:

```python
"""Test scenario: <short description>."""
import uiautomator2 as u2


def test_<behavior>(d: u2.Device, agent_checkpoint):
    """<what this test verifies>."""
    # Step 1
    # <u2 operation>
    assert <condition>

    # Step 2
    # <u2 operation>
    assert <condition>
```

## Fixtures and Devices

- Fixture implementations are fixed contracts; do not read existing fixture source files.
- Use fixtures strictly as documented in this skill.
- Default mode (single device): use fixture `d`, no `--device` argument
- Named device mode: pass `--device NAME:SERIAL` and use matching fixture name in test function
- Multi-device mode: repeat `--device NAME:SERIAL` and reference each name as a fixture

Example:

```bash
# Single device (default)
uv run pytest tests -sv
# Named device
uv run pytest tests -sv --device phone:emulator-5554 --device tablet:127.0.0.1:9887
```

## Pause and Checkpoints

If the user does not explicitly request `--pause-on-failure`, do not add it.

With `--pause-on-failure`:
- pytest pauses before teardown on failure
- device state stays available for inspection
- resume by signaling the pytest process

Example:

```bash
uv run pytest tests -sv --pause-on-failure
```

```bash
# To resume after failure pause, run in a new process or terminal:
kill -SIGUSR1 <pytest-pid>
```

Tests can also request an explicit reasoning checkpoint through `agent_checkpoint`, use `agent_checkpoint` only when the test still needs one bounded semantic or visual go/no-go decision that cannot be encoded reliably with the checks above:

```python
import pytest


def test_checkout_summary(agent_checkpoint):
    result = agent_checkpoint(
        "Decide whether the screen already shows the final checkout summary.",
    )
    if result.result is None:
        pytest.skip(f"checkpoint unavailable: {result.outcome} - {result.reason}")
    assert result.result is True
```

Do not use `agent_checkpoint` for checks that can be expressed as selectors, text assertions, state polling, or ordinary failure inspection.

## Run Rules

1. Start every pytest run through `uv` and write output to a log file:

```bash
log="/tmp/qamule-$(date +%Y%m%d-%H%M%S)-$$.log"
touch "$log" && printf "Pytest log initialized: $log\n"

uv run pytest [command/options] >"$log" 2>&1
ec=$?
printf '\nQAMule pytest exit code=%s' "$ec" >>"$log"
```

2. Run the pytest command in `async` mode.

3. In a different terminal, run the monitor command in `sync` mode with no `timeout`:

```bash
bash <path-to-this-skill>/scripts/monitor.sh "$log"
```

4. When `monitor.sh` reports a pause, handle it based on stdout:
    - `checkpoint`: do the requested external task, then resume with a result, for example `bash <path-to-this-skill>/scripts/resume.sh "$log" --result true --reason "verified by external agent"`
    - `failure`: inspect the failure state, then resume without a result, for example `bash <path-to-this-skill>/scripts/resume.sh "$log"`
    - `Test finished.`: the run completed normally; inspect the log and do not resume anything

5. Repeat `monitor` and `resume` until `monitor` reports normal completion as `Test finished.`.

6. Use the commands defined in this skill as-is. Do not write a more complex wrapper.

7. Do not use a subagent for this flow; always run it in the current agent.
