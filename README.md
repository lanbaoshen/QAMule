<p align="center">
    <img src="logo.svg" alt="QAMule" width="200">
</p>

<p align="center">
    <strong>AI-powered GitHub Copilot extension that explores, understands, and tests Android apps autonomously.</strong>
</p>

<p align="center">
    English | <a href="README_ZH.md">中文</a>
</p>

---

> **Explore once, solidify into a script, only intervene when it breaks.**

QAMule is a [GitHub Copilot Extension Plugin](https://code.visualstudio.com/docs/copilot/chat/chat-extensions) that turns AI into an autonomous Android QA engineer. It explores your app on a real device, converts explorations into pytest test scripts, maintains them when the app changes, and collects VLM training trajectories — all without writing test code by hand.

## Philosophy

Traditional UI test automation is fragile: selectors break, flows change, and maintenance costs pile up. QAMule takes a different approach:

1. **Explore** — AI operates the real device once to discover UI elements and user flows.
2. **Solidify** — The exploration is distilled into a deterministic pytest script that runs without AI.
3. **Remember** — A knowledge base (`kb/`) persists discovered screens, selectors, and flows so nothing is ever re-explored.
4. **Repair** — When a test breaks, AI re-inspects the device at the failure scene, patches the script, and updates `kb/`.

This keeps test execution fast and cheap while limiting AI involvement to exploration and repair — where it actually adds value.

## Agents

QAMule provides a multi-agent system where each agent has a specialized role. You only interact with **Coordinator** — it orchestrates the rest.

| Agent | Role | Invoked by |
|---|---|---|
| **Coordinator** | Orchestrator. Checks if a test exists, runs it, routes work to specialists. | You (directly) |
| **Explorer** | Explores new app features on a live device, writes validated pytest scripts, persists knowledge to `kb/`. | Coordinator |
| **First Responder** | Diagnoses failures on a frozen device (pause-on-failure), validates fixes live, then resumes the session. | Coordinator |
| **Maintainer** | Fixes previously passing tests that now fail — applies minimal patches and updates `kb/` when app UI changes. | Coordinator |
| **Distiller** | Operates the device using only screenshots and coordinates to collect VLM training trajectories. | You (directly) |

## Skills

Skills provide domain-specific knowledge that agents and prompts can reference.

| Skill | Description |
|---|---|
| **init** | Scaffolds a complete test automation project (`tests/`, `kb/`, `actions/`, `helpers/`, `conftest.py`, `pyproject.toml`) and installs dependencies. |
| **pytest** | Conventions for writing and running tests — device fixtures, `--pause-on-failure`, project structure. |
| **uiautomator2** | Reference for all `u2cli` commands — device control, element interaction, hierarchy inspection, screenshots. |
| **viewer** | Launches a local web server to browse distilled VLM trajectories with screenshot overlays and action visualization. |

## Key Features

- **Autonomous test generation** — describe a feature, get a working pytest script.
- **Pause-on-Failure (AI-in-the-Loop)** — when a test fails, the session freezes before teardown so an AI agent can inspect the live device, fix the script, and resume.
- **Knowledge base** — `kb/` acts as persistent AI memory for selectors, flows, and screen layouts.
- **VLM trajectory distillation** — the Distiller agent records phone-operating trajectories (screenshot + coordinate only) for training vision-language models.
- **Trajectory viewer** — a zero-dependency local web viewer for reviewing collected trajectories.

## Pause-on-Failure: AI-in-the-Loop

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

When a test fails, the device stays in the exact failure state. The AI agent inspects, fixes, and resumes — no manual intervention needed.

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

```bash
copilot plugin install lanbaoshen/QAMule
```

Enable the plugin in VS Code:

1. Open **Settings** (`Cmd + ,`) → search `chat.extensionPlugins.enabled` → set to `true`.
2. Reload VS Code.

## Quick Start

**1. Initialize a project:**

```
/qamule:init my-app com.example.myapp
```

**2. Test a feature (Agent mode → Coordinator):**

```
Test the login flow for com.example.myapp
```

**3. View collected trajectories:**

```
/qamule:viewer ./dataset
```

This launches a local web server with a timeline UI for browsing distilled trajectories — screenshots, action overlays, and step-by-step playback.



**4. Collect VLM trajectories (Agent mode → Distiller):**

```
Open Bluetooth in Settings on com.android.settings
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
├── dataset/                 # Distilled VLM trajectories
├── pytest_plugins/          # Custom pytest plugins
└── pyproject.toml           # Project config & dependencies
```

## License

[MIT](LICENSE)
