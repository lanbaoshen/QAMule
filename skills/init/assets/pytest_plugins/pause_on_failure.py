"""pytest plugin — pause test execution for live agent inspection.

Enable with ``--pause-on-failure`` to pause a failing test body before
teardown runs. Tests can also request an explicit agent checkpoint via the
``agent_checkpoint`` fixture when a script needs external reasoning.

Paused sessions emit a machine-readable log line that external monitors can
detect, then block until the configured signal arrives or the safety timeout
expires. The external agent can optionally write a JSON result file before
resuming the pytest process.
"""

from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
import json
import os
import signal
import tempfile
import threading
from typing import Any, Callable
import uuid

import pytest

_PAUSE_TIMEOUT = 600  # seconds
_DEFAULT_RESUME_SIGNAL = "SIGUSR1"
_DEFAULT_RESULT_DIR = os.path.join(tempfile.gettempdir(), "qamule-pauses")
_PAUSE_EVENT_PREFIX = "QAMULE_PAUSE_EVENT "
_PAUSE_RESUME_PREFIX = "QAMULE_PAUSE_RESUME "
_PAUSE_WARNING_PREFIX = "QAMULE_PAUSE_WARNING "


@dataclass(frozen=True)
class PauseResult:
    """Result returned after a pause session finishes."""

    reason: str
    request_id: str
    outcome: str
    result_path: str | None
    resume_signal: str
    payload: dict[str, Any] | None


@dataclass(frozen=True)
class CheckpointResult:
    """Decision returned by an explicit agent checkpoint."""

    request_id: str
    outcome: str
    result_path: str | None
    resume_signal: str
    result: bool | None
    reason: str | None


def _resolve_signal(name: str) -> signal.Signals:
    try:
        sig = getattr(signal, name)
    except AttributeError as exc:
        raise pytest.UsageError(f"Unsupported signal: {name}") from exc
    if not isinstance(sig, signal.Signals):
        raise pytest.UsageError(f"Unsupported signal: {name}")
    return sig


def _emit_event(prefix: str, payload: dict[str, Any]) -> None:
    print(
        f"{prefix}{json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)}",
        flush=True,
    )


def _load_pause_payload(result_path: str) -> dict[str, Any] | None:
    try:
        with open(result_path, encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        return {
            "status": "error",
            "message": f"Invalid pause result JSON: {exc}",
        }

    if isinstance(payload, dict):
        return payload

    return {
        "status": "error",
        "message": "Pause result must be a JSON object.",
    }


def _pause_timeout(config: pytest.Config, override: int | None = None) -> int:
    if override is not None:
        return override
    return int(config.getoption("--pause-timeout", default=_PAUSE_TIMEOUT))


def _pause_result_dir(config: pytest.Config) -> str:
    return str(
        config.getoption(
            "--pause-result-dir",
            default=_DEFAULT_RESULT_DIR,
        )
    )


def _checkpoint_warning(
    pause_result: PauseResult,
    *,
    outcome: str,
    reason: str,
) -> CheckpointResult:
    _emit_event(
        _PAUSE_WARNING_PREFIX,
        {
            "event": "qamule.pause_warning",
            "pause_reason": pause_result.reason,
            "request_id": pause_result.request_id,
            "outcome": outcome,
            "reason": reason,
            "result_path": pause_result.result_path,
        },
    )
    return CheckpointResult(
        request_id=pause_result.request_id,
        outcome=outcome,
        result_path=pause_result.result_path,
        resume_signal=pause_result.resume_signal,
        result=None,
        reason=reason,
    )


def _checkpoint_result_from_pause(pause_result: PauseResult) -> CheckpointResult:
    payload = pause_result.payload
    if payload is None:
        if pause_result.outcome == "signal":
            return _checkpoint_warning(
                pause_result,
                outcome="missing_result",
                reason="Checkpoint resumed without a result payload.",
            )
        return CheckpointResult(
            request_id=pause_result.request_id,
            outcome=pause_result.outcome,
            result_path=pause_result.result_path,
            resume_signal=pause_result.resume_signal,
            result=None,
            reason=None,
        )

    payload_error = payload.get("message") if payload.get("status") == "error" else None
    if isinstance(payload_error, str):
        return _checkpoint_warning(
            pause_result,
            outcome="invalid_result",
            reason=payload_error,
        )

    result = payload.get("result")
    reason = payload.get("reason")
    extra_keys = set(payload) - {"result", "reason"}

    if not isinstance(result, bool):
        return _checkpoint_warning(
            pause_result,
            outcome="invalid_result",
            reason=(
                "Agent checkpoint result must be JSON like "
                "{'result': true|false, 'reason': '...'}."
            ),
        )
    if reason is not None and not isinstance(reason, str):
        return _checkpoint_warning(
            pause_result,
            outcome="invalid_result",
            reason="Agent checkpoint result field 'reason' must be a string.",
        )
    if extra_keys:
        return _checkpoint_warning(
            pause_result,
            outcome="invalid_result",
            reason="Agent checkpoint result JSON only accepts 'result' and 'reason'.",
        )

    return CheckpointResult(
        request_id=pause_result.request_id,
        outcome=pause_result.outcome,
        result_path=pause_result.result_path,
        resume_signal=pause_result.resume_signal,
        result=result,
        reason=reason,
    )


def _pause_session(
    item: pytest.Item,
    *,
    reason: str,
    heading: str,
    details: str | None = None,
    context: dict[str, Any] | None = None,
    expects_result: bool = False,
    timeout: int | None = None,
) -> PauseResult:
    resume = threading.Event()
    resume_signal = _resolve_signal(
        item.config.getoption(
            "--pause-resume-signal",
            default=_DEFAULT_RESUME_SIGNAL,
        )
    )
    timeout_seconds = _pause_timeout(item.config, override=timeout)

    pid = os.getpid()
    request_id = uuid.uuid4().hex
    result_path: str | None = None
    if expects_result:
        result_dir = _pause_result_dir(item.config)
        os.makedirs(result_dir, exist_ok=True)
        result_path = os.path.join(result_dir, f"{request_id}.json")

    pause_event = {
        "event": "qamule.pause",
        "reason": reason,
        "request_id": request_id,
        "nodeid": item.nodeid,
        "pid": pid,
        "signal": resume_signal.name,
        "timeout_sec": timeout_seconds,
        "context": context or {},
    }
    if result_path is not None:
        pause_event["result_path"] = result_path

    def _resume_from_signal(signum: int, frame: object) -> None:
        del signum, frame
        resume.set()

    previous_handler = signal.getsignal(resume_signal)
    signal.signal(resume_signal, _resume_from_signal)

    try:
        print(
            f"\n{'=' * 60}\n"
            f"PAUSED - {heading}\n"
            f"Reason: {reason}\n"
            f"Test: {item.nodeid}\n"
            f"{'=' * 60}\n"
            f">>> Send {resume_signal.name} to continue: `kill -{resume_signal.name} {pid}`\n",
            flush=True,
        )
        if result_path is not None:
            print(f">>> Write JSON result to: {result_path}", flush=True)
        print(f">>> Auto-resumes in {timeout_seconds}s ...", flush=True)
        if details:
            print(f"Details:\n{details}", flush=True)
        _emit_event(_PAUSE_EVENT_PREFIX, pause_event)
        resume.wait(timeout=timeout_seconds)
    finally:
        signal.signal(resume_signal, previous_handler)

    payload = _load_pause_payload(result_path) if result_path is not None else None
    outcome = "signal" if resume.is_set() else "timeout"
    resume_event = {
        "event": "qamule.resume",
        "reason": reason,
        "request_id": request_id,
        "nodeid": item.nodeid,
        "outcome": outcome,
        "signal": resume_signal.name,
        "has_result": payload is not None,
    }
    if result_path is not None:
        resume_event["result_path"] = result_path
    _emit_event(_PAUSE_RESUME_PREFIX, resume_event)
    return PauseResult(
        reason=reason,
        request_id=request_id,
        outcome=outcome,
        result_path=result_path,
        resume_signal=resume_signal.name,
        payload=payload,
    )


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
    parser.addoption(
        "--pause-timeout",
        action="store",
        type=int,
        default=_PAUSE_TIMEOUT,
        help=(
            "Maximum pause duration in seconds before auto-resume "
            f"(default: {_PAUSE_TIMEOUT})."
        ),
    )
    parser.addoption(
        "--pause-result-dir",
        action="store",
        default=_DEFAULT_RESULT_DIR,
        help=(
            "Directory where pause result JSON files are written and read "
            f"(default: {_DEFAULT_RESULT_DIR})."
        ),
    )


@pytest.fixture
def agent_checkpoint(
    request: pytest.FixtureRequest,
) -> Callable[..., CheckpointResult]:
    """Pause a running test and wait for a boolean decision from an agent."""

    def _checkpoint(
        task: str,
        *,
        timeout: int | None = None,
    ) -> CheckpointResult:
        pause_result = _pause_session(
            request.node,
            reason="checkpoint",
            heading="agent checkpoint requested.",
            details=task,
            context={"task": task},
            expects_result=True,
            timeout=timeout,
        )
        return _checkpoint_result_from_pause(pause_result)

    return _checkpoint


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

    result = _pause_session(
        item,
        reason="failure",
        heading="test failed, device state preserved.",
        details=report.longreprtext,
        context={
            "longrepr": report.longreprtext,
            "outcome": report.outcome,
            "when": report.when,
        },
        expects_result=True,
    )
    if result.payload is not None:
        _emit_event(
            "QAMULE_PAUSE_RESULT ",
            {
                "event": "qamule.pause_result",
                "reason": "failure",
                "request_id": result.request_id,
                "nodeid": item.nodeid,
                "payload": result.payload,
            },
        )
