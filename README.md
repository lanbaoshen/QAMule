<p align="center">
    <img src="logo.svg" alt="logo.svg" width="200">
</p>

AI-powered GitHub Copilot extension that explores, understands, and tests Android apps autonomously.

> Explore once, solidify into a script, only intervene when it breaks.

QAMule lets AI explore your Android app on a real device, convert the exploration into pytest test scripts, and maintain them automatically — so you don't write UI test code by hand.

## Prerequisites

| Dependency | Version | Install |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| [Python](https://www.python.org/) | >= 3.10 | via `uv` or system package manager |
| [adb](https://developer.android.com/tools/adb) | latest | `brew install android-platform-tools` (macOS) |
| [VS Code](https://code.visualstudio.com/) | latest | — |
| [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) | latest | VS Code Extensions Marketplace |

Make sure `adb devices` shows your device before running tests.

## Installation

Install the plugin via Copilot CLI:

```bash
copilot plugin install lanbaoshen/QAMule
```

### Enable the Plugin in VS Code

1. Open VS Code **Settings** (`Cmd + ,`).
2. Search for `chat.extensionPlugins.enabled`.
3. Set it to **`true`**.
4. Reload VS Code.

## Quick Start

### 1. Initialize a test project

Open **Copilot Chat** and run:

```
/qamule:init
```

Or:

```
/qamule:init <project-name> <android-package-name>
```

For example:

```
/qamule:init my-app com.example.myapp
```

This scaffolds the full project structure — `tests/`, `kb/`, `actions/`, `helpers/`, `conftest.py`, `pyproject.toml` — and runs `uv sync` to install dependencies.

### 2. Use the Coordinator agent

In VS Code Copilot Chat, switch to **Agent** mode, select **Coordinator**, and describe what you want to test. Coordinator is the only agent you need to invoke directly — it automatically delegates to the specialist agents as needed.

| Agent | Invoked by | Description |
|---|---|---|
| **Coordinator** | You | Main entry point. Checks if a test already exists, runs it, and routes work to the right specialist agent automatically. |
| **Explorer** | Coordinator | Explores an app feature step-by-step on a live device, writes a validated pytest script, and persists discovered screens/flows to `kb/`. |
| **First Responder** | Coordinator | Inspects the live failure scene when pytest is paused, classifies the root cause, validates a fix on the frozen device, then resumes the session. |
| **Maintainer** | Coordinator | Diagnoses the root cause of a previously passing test that is now failing, applies the minimal fix, and updates `kb/` if the app UI changed. |

Example prompt:

```
# In Agent mode → select "Coordinator"
Test the login flow for com.example.myapp
```

## How It Works

1. **Explore** — AI controls the real device via uiautomator2, inspecting the UI hierarchy at each step.
2. **Solidify** — The exploration is converted into a pytest script that runs without AI.
3. **Remember** — `kb/` stores discovered screens, flows, and selectors so nothing is re-explored.
4. **Repair** — When a test breaks, the fixer agent re-inspects the device, patches the script, and updates `kb/`.

### Pause-on-Failure: AI-in-the-Loop

QAMule includes a built-in pytest plugin (`--pause-on-failure`) that enables a unique **AI-in-the-loop** testing workflow:

```
pytest runs test suite
        │
    ┌───▼───┐
    │ PASS?  │── Yes ──▶ next test
    └───┬────┘
        │ No
        ▼
  ╔═══════════════════════════════╗
  ║  SESSION PAUSED               ║
  ║  Device frozen at failure     ║
  ║  Teardown has NOT run yet     ║
  ╚═══════════════╤═══════════════╝
                  ▼
    AI agent inspects device state
    → dump-hierarchy / screenshot
    → diagnose root cause
    → fix script or actions.py
                  │
                  ▼
        Send Enter to resume
        │
    ┌───▼───┐
    │Teardown│──▶ continue session
    └───────┘
```

When a test fails, the session **blocks before teardown**, keeping the device in the exact failure state. The AI agent can then:

1. Inspect the live device (`dump-hierarchy`, `screenshot`) to see what actually happened.
2. Fix the test script, selectors, or actions in-place.
3. Send a newline to resume — teardown runs and the session continues.

A safety timeout (default 600s) prevents the process from hanging if the agent disconnects.

```bash
# Run with pause-on-failure enabled
.venv/bin/python -m pytest tests/ -v --pause-on-failure
```

## Project Structure (after init)

```
├── kb/                      # Knowledge base — AI's memory
│   ├── app/
│   │   ├── _overview.md     # Package name, entry point
│   │   ├── _index.md        # Known screens, flows, actions
│   │   ├── screens/         # Per-screen selectors & notes
│   │   └── flows/           # Step-by-step flow docs
│   └── helpers/
│       └── _index.md        # Helper function registry
├── tests/
│   ├── conftest.py          # Fixtures (device, app launch)
│   ├── README.md            # Test case index
│   └── test_*.py            # Test scripts
├── actions/                 # Reusable app action functions
├── helpers/                 # System-level helpers
├── pytest_plugins/          # Custom pytest plugins
└── pyproject.toml           # Project config & dependencies
```

## License

[MIT](LICENSE)
