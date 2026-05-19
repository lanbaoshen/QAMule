"""pytest plugin — pause test session on failure so an agent can inspect the device.

Enable with ``--pause-on-failure``.  When a test body fails the session
blocks *before* teardown runs, keeping the device in the exact failure
state.  Resume by sending a signal to the pytest process, after which
normal teardown and ``-x`` early-exit proceed as usual.

A safety timeout (default 600 s) ensures the process never hangs forever
if the controlling agent disconnects.
"""

from __future__ import annotations

from collections.abc import Generator
import os
import signal
import threading
from typing import Any

import pytest

_PAUSE_TIMEOUT = 600  # seconds
_DEFAULT_RESUME_SIGNAL = "SIGUSR1"


def _resolve_signal(name: str) -> signal.Signals:
    try:
        sig = getattr(signal, name)
    except AttributeError as exc:
        raise pytest.UsageError(f"Unsupported signal: {name}") from exc
    if not isinstance(sig, signal.Signals):
        raise pytest.UsageError(f"Unsupported signal: {name}")
    return sig


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
            "Send the configured signal to continue. "
            f"Auto-resumes after {_PAUSE_TIMEOUT}s if no input is received."
        ),
    )
    parser.addoption(
        "--pause-resume-signal",
        action="store",
        default=_DEFAULT_RESUME_SIGNAL,
        help=(
            "Signal used to resume a paused test session "
            f"(default: {_DEFAULT_RESUME_SIGNAL})."
        ),
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo
) -> Generator[None, Any, None]:
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

    resume = threading.Event()
    resume_signal = _resolve_signal(
        item.config.getoption(
            "--pause-resume-signal",
            default=_DEFAULT_RESUME_SIGNAL,
        )
    )
    pid = os.getpid()

    def _resume_from_signal(signum: int, frame: object) -> None:
        del signum, frame
        resume.set()

    previous_handler = signal.getsignal(resume_signal)
    signal.signal(resume_signal, _resume_from_signal)

    try:
        print(
            f"\n{'=' * 60}\n"
            f"PAUSED — test failed, device state preserved.\n"
            f"Test: {item.nodeid}\n"
            f"Failure:\n{report.longreprtext}\n"
            f"{'=' * 60}\n"
            f">>> Send {resume_signal.name} to continue: "
            f"`kill -{resume_signal.name} {pid}`, "
            f"Auto-resumes in {_PAUSE_TIMEOUT}s ...",
            flush=True,
        )
        resume.wait(timeout=_PAUSE_TIMEOUT)
    finally:
        signal.signal(resume_signal, previous_handler)
