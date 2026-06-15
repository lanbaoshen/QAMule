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
uv run pytest tests --device phone:emulator-5554 --device tablet:127.0.0.1:9887
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

Do not use `--pause-checkpoint-mock` for normal test execution. Use it only for local partial validation, such as when authoring scripts or doing an initial smoke check where the checkpoint itself is not the target of verification. In those cases, `uv run pytest --pause-checkpoint-mock true|false` can mock checkpoint results as `true` or `false` without executing the checkpoint task.

## Mandatory Watch Workflow

For every non-collection pytest execution, the `pytest-live-pause watch` step is mandatory. Do not monitor a running pytest process only through the original pytest terminal output. The watch process is the authoritative way to detect completion, checkpoint pauses, and failure pauses.

1. Start every pytest run through `uv` in `async` mode:

```bash
uv run pytest [command/options]
```

2. After pytest starts, it will print the live pause run id on the header like `pytest-live-pause: run_id={run_id}`. Immediately use `pytest-live-pause watch` to monitor the run state in a different terminal in `sync` mode with no `timeout`:

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

4. Repeat `pytest-live-pause watch` and `pytest-live-pause resume` until test run completes. Do not stop after starting pytest unless a watch command has confirmed that the run is no longer active or has completed.
