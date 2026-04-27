# QAMule

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

### 2. Use Agents to write or fix tests

In VS Code Copilot Chat, switch to **Agent** mode and select one of the QAMule agents:

| Agent | Description |
|---|---|
| **Android Test Author** | Explores an app feature on a live device, writes a pytest test, extracts reusable actions, and updates the knowledge base. |
| **Android Test Fixer** | Diagnoses a failing test, re-inspects the device UI, fixes the script, and updates KB if the app changed. |

Example prompts:

```
# In Agent mode → select "Android Test Author"
Test the login flow for com.example.myapp

# In Agent mode → select "Android Test Fixer"
Fix test_login.py — UiObjectNotFoundError on the submit button
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
