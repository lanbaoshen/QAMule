---
name: qamule-pytest
description: Use when running or writing QAMule pytest tests with device fixtures, artifacts, checkpoints, pauses, or reports.
user-invocable: false
---

# QAMule Pytest

## Devices

Use `d` when no named device is configured:

```python
def test_smoke(d):
    assert d.serial is not None
```

For named fixtures, pass `--device NAME:SERIAL` for each device:

```bash
uv run pytest tests --device phone:emulator-5554 --device tablet:emulator-5556
```

```python
def test_on_phone(phone, tablet):
    assert phone.serial == "emulator-5554"
    assert tablet.serial == "emulator-5556"
```

## Artifacts

Use artifact fixtures rather than constructing paths:

```python
def test_login(phone, testcase_device_artifacts_dir):
    phone.app_start("com.example.app")
    phone.screenshot().save(
        testcase_device_artifacts_dir("phone") / "login.jpg"
    )
```

- `artifacts_dir`: run root
- `testcase_artifacts_dir`: current test
- `testcase_device_artifacts_dir(name)`: current test and device

They create directories on demand at `pytest-artifacts/<session-id>/<sequence>-<testcase>/<device-name>/`.

## Pause Protocol

Use `--pause-on-failure` only to inspect and capture failures in the current test run. (Only used when user specifies it)

```bash
uv run pytest tests --pause-on-failure
```

Use `checkpoint` only when an external decision is needed; prefer selectors, assertions, and polling for deterministic checks.

```python
def test_login(checkpoint):
    checkpoint(
        "confirm the login screen",
        images=["screens/login.jpg"],
    )
```

When checkpoints do not need an external or AI decision, such as during debugging or a deterministic test run, mock every checkpoint result for the run:

```bash
uv run pytest tests --checkpoint-mock-result true|false
```

Mock mode still records each checkpoint and its result, but resumes immediately. Do not start the `watch`/`resume` loop for a mocked run.

Use terminal `mode: async` for every pytest run and record the session ID. Immediately after starting the pytest process, run `watch` synchronously from another terminal without `timeout`; it waits for a `pause_id` or `finish`:

```bash
uv run qamule watch <session-id>
```

When `watch` returns a `pause_id`, inspect the pause state and `resume` it. Then run `watch` again. Repeat until `watch` returns `finish`.

After a `--pause-on-failure` test failure, load `problem-triage` and diagnose the root cause from the pause state, artifacts, logs, failed test, and relevant implementation. Record the classification and evidence, then resume only when the remaining cases can continue unchanged. Do not resume simply to move past the failure; if blocked, state the suspected cause and blocker in the message.

Resume synchronously without `--result`:

```bash
uv run qamule resume <session-id> <pause-id> --message "diagnosed <cause class>"
```

For a checkpoint, do the task and resume synchronously with a result:

```bash
uv run qamule resume <session-id> <pause-id> --result true --message "login screen approved"
```

Use `--result true`, `false`; failure pauses need no result. Attach `--image` evidence when useful.

## Reports

Runs write events and live state under `pytest-sessions/<session-id>/`. Serve a live or completed report:

```bash
uv run qamule report serve <session-id>
```

Show a specific test node detail:

```bash
uv run qamule report show <session_id> <nodeid>
```
