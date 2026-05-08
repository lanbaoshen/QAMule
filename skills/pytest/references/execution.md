# Execution

## Basic

```bash
.venv/bin/pytest tests/test_xxx.py -v --pause-on-failure
```

## Device Selection

Default connects to the only attached device. For multiple devices use `--device`:

```bash
# Single named device
.venv/bin/pytest --device phone:emulator-5554 --pause-on-failure

# Multiple devices
.venv/bin/pytest --device phone:emulator-5554 --device tablet:192.168.1.100 --pause-on-failure
```

Tests reference the device by fixture name matching the `NAME` part:

```python
def test_example(phone: u2.Device):
    phone(text="OK").click()
```

If no `--device` is specified, a fixture named `d` is auto-registered connecting to the default device.

## Pause on Failure

```bash
.venv/bin/pytest tests/test_xxx.py -v --pause-on-failure
```

When a test fails:
1. Teardown is **not** run — device stays in the exact failure state
2. Terminal prints the failure details and waits for Enter
3. You (or the agent) can inspect the device, take screenshots, dump hierarchy
4. Press Enter to continue (auto-resumes after 600s)

Use this when debugging failures interactively or when the QA agent needs to diagnose what went wrong.
