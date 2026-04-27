"""pytest plugin — device fixture registration."""

from __future__ import annotations

import pytest
import uiautomator2 as u2


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the --device CLI option.

    Args:
        parser: The pytest argument parser.
    """
    parser.addoption(
        "--device",
        action="append",
        default=[],
        metavar="NAME:SERIAL",
        help=(
            "Register a named device fixture. "
            "Format: NAME:SERIAL, e.g. --device phone:emulator-5554. "
            "Repeat for multiple devices."
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    """Dynamically register session-scoped device fixtures from --device options.

    Each --device NAME:SERIAL argument creates a fixture named NAME that
    yields a connected u2.Device for the given serial. Tests declare the
    fixture by parameter name, e.g.::

        def test_demo(phone: u2.Device):
            print(phone.device_info)

    Args:
        config: The pytest configuration object.

    Raises:
        pytest.UsageError: If a --device value is not in NAME:SERIAL format.
    """
    specs = config.getoption("--device", default=[])
    if not specs:
        _register_device_fixture(config, "d", None)
        return
    for spec in specs:
        name, sep, serial = spec.partition(":")
        if not sep or not name.strip() or not serial.strip():
            raise pytest.UsageError(
                f"Invalid --device value {spec!r}. "
                "Expected NAME:SERIAL, e.g. --device phone:emulator-5554"
            )
        _register_device_fixture(config, name.strip(), serial.strip())


def _register_device_fixture(config: pytest.Config, name: str, serial: str | None) -> None:
    """Create and register a session-scoped u2.Device fixture via a plugin object.

    The fixture is registered as an inline plugin so pytest discovers it
    during collection without requiring ``globals()`` injection.

    Args:
        config: The pytest configuration object used to register the plugin.
        name: Fixture name used as a test function parameter.
        serial: Android device serial as reported by ``adb devices``, or
            ``None`` to connect to the default device via ``u2.connect()``.
    """

    @pytest.fixture(scope="session", name=name)
    def _device_fixture() -> u2.Device:
        return u2.connect(serial) if serial else u2.connect()

    class _DevicePlugin:
        pass

    setattr(_DevicePlugin, name, staticmethod(_device_fixture))
    config.pluginmanager.register(_DevicePlugin(), name=f"autoqa_device_{name}")
