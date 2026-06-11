---
name: pytest
description: "Define how pytest tests should be executed in QAMule, including run commands, device fixture selection, pause-on-failure, and live checkpoint workflow. Use when running or debugging pytest tests without business-specific content. Trigger keywords: run pytest, debug pytest, --device, pause-on-failure, live pause, checkpoint."
user-invocable: false
---

# Pytest Runtime

Pytest runtime conventions for Android automation.

## Collect Tests

You can collect tests with `uv run pytest --collect-only` to see the test structure and markers without executing them

## Multiple Device Control

You can control device via default fixture `d` or define named fixtures for multiple devices:

- Default mode (single device): use fixture `d`, no `--device` argument
- Named device mode: pass `--device NAME:SERIAL` and use matching fixture name in test function
- Multi-device mode: repeat `--device NAME:SERIAL` and reference each name as a fixture

```bash
uv run pytest tests -sv --device phone:emulator-5554 --device tablet:127.0.0.1:9887
```

## Live Pause

Pytest support `--pause-on-failure` to pause the test process on failure for inspection and debugging, if the user explicitly request, add it.

Tests can also request an explicit reasoning checkpoint through `live_pause.checkpoint`, use it only when the test still needs
one bounded semantic or visual go/no-go decision that cannot be encoded reliably with the checks above:

```python
import pytest

def test_checkout_summary(live_pause):
    result = live_pause.checkpoint(task="Task")
    if result.result is None:
        pytest.skip(f"checkpoint unavailable: {result.outcome} - {result.reason}")
    assert result.result is True
```

Do not use it for checks that can be expressed as selectors, text assertions, state polling, or ordinary failure inspection.

If you want to ignore the existing checkpoint in the test, only check the assertion or selector, you can use `uv run pytest --pause-checkpoint-mock true|false` to control whether the checkpoint will be mocked to always return result `true` or `false` without actually executing the checkpoint task.

## Workflow

1. Start every pytest run through `uv` in `async` mode:

```bash
uv run pytest [command/options]
```

2. After pytest starts, it will print the live pause run id on the header like `pytest-live-pause: run_id={run_id}`, you should use `pytest-live-pause watch` command to monitor the run state in a different terminal in `sync` mode with no `timeout`:

```bash
uv run pytest-live-pause watch --run-id={run_id}
```

3. The `pytest-live-pause watch` command will stop if below happens:
    - pytest process exits (normal completion or crash)
    - test pauses on an explicit checkpoint request
    - test failure happens

You can get the `pause_id` and `kind` of pause by inspecting the stdout of `pytest-live-pause watch`:
    - `checkpoint`: do the requested external `task`, then resume with a result, for example `uv run pytest-live-pause resume {pause_id} --result true --reason "verified by external agent"`
    - `failure`: inspect the failure state, then resume without a result, for example `uv run pytest-live-pause resume {pause_id} --failure-reason "investigated failure"`
    - `run is no longer active:` the run completed normally; inspect the log and do not resume anything

4. Repeat `pytest-live-pause watch` and `pytest-live-pause resume` until test run completes.
