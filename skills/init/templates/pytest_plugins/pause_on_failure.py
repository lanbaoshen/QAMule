"""pytest plugin — pause test session on failure so an agent can inspect the device.

Enable with ``--pause-on-failure``.  When a test body fails the session
blocks *before* teardown runs, keeping the device in the exact failure
state.  The agent (or a human) sends a newline to stdin to resume, after
which normal teardown and ``-x`` early-exit proceed as usual.

A safety timeout (default 600 s) ensures the process never hangs forever
if the controlling agent disconnects.
"""

from __future__ import annotations

import sys
import threading

import pytest

_PAUSE_TIMEOUT = 600  # seconds


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the ``--pause-on-failure`` CLI flag.

    Args:
        parser: The pytest argument parser.
    """
    parser.addoption(
        "--pause-on-failure",
        action="store_true",
        default=False,
        help=(
            "Pause the session when a test fails, before teardown runs. "
            "Press Enter (or send a newline) to continue. "
            f"Auto-resumes after {_PAUSE_TIMEOUT}s if no input is received."
        ),
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Intercept test-body failures and block before teardown.

    Args:
        item: The test item that just ran.
        call: Information about the test call phase.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return
    if not item.config.getoption("--pause-on-failure", default=False):
        return

    print(
        f"\n{'=' * 60}\n"
        f"PAUSED — test failed, device state preserved.\n"
        f"Test: {item.nodeid}\n"
        f"Failure:\n{report.longreprtext}\n"
        f"{'=' * 60}\n"
        f">>> Press Enter to continue (auto-resumes in {_PAUSE_TIMEOUT}s) …",
        flush=True,
    )

    resume = threading.Event()

    def _wait_tty() -> None:
        try:
            tty = open("/dev/tty", "r")
            tty.readline()
            tty.close()
        except Exception:
            return
        resume.set()

    reader = threading.Thread(target=_wait_tty, daemon=True)
    reader.start()
    resume.wait(timeout=_PAUSE_TIMEOUT)
