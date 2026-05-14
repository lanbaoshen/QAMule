<p align="center">
  <img src="logo.svg" width="120" alt="QAMule Logo">
</p>

<h1 align="center">QAMule</h1>

<p align="center">
  AI-native Android testing framework — the agent <em>is</em> the tester.
</p>

<p align="center">
  <a href="README_ZH.md">中文</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="https://github.com/lanbaoshen/QAMule-Practice">Practice Reference</a> •
  <a href="LICENSE">MIT License</a>
</p>

---

## What Is QAMule?

QAMule is an **agent-first** QA framework for Android. Unlike traditional automation where scripts are the core and AI assists, here the **AI agent directly operates the device to complete testing**. Test scripts are merely an optional acceleration layer — generated after successful tests to skip agent reasoning on repeated scenarios.

**The paradigm shift:**

| | Traditional AI Testing | QAMule |
|---|---|---|
| **Core executor** | Scripts | AI Agent |
| **AI's role** | Generates/maintains scripts | Performs testing directly |
| **Scripts** | Required | Optional (caching for speed) |
| **Failure handling** | Breaks, needs human fix | Agent self-diagnoses and recovers |
| **New scenarios** | Must write new scripts first | Agent explores and tests immediately |

## Quick Start

### Prerequisites

- Android device connected via USB (or emulator)
- UV (Manage Python environments and packages)
- ADB (Android Debug Bridge)

### Installation

1. Clone or add QAMule as an agent plugin in your project:

```
# Github Copilot
copilot plugin marketplace add lanbaoshen/agent-plugins
copilot plugin install QAMule@lanbaoshen

# Claude Code
/plugin marketplace add lanbaoshen/agent-plugins
/plugin install QAMule@lanbaoshen

# VSCode
# command + shift + p -> "Chat: Install plugin from Source" -> "lanbaoshen/agent-plugins"
```

2. Ask the agent to initialize:

```
/qamule:init
```

This copies config files, creates directories (`kb/`, `tests/`, `dataset/`), and installs dependencies.

### Usage

**Test something:**
```
@QAMule QA test the login flow
```

**Explore an app:**
```
@QAMule QA explore the settings page
```

**Collect VLM training data:**
```
@QAMule Distiller open Bluetooth in Settings on com.android.settings
```

**Update knowledge base:**
```
/qamule:kb This app can only be launched via UI
```

**Check test coverage:**
```
/qamule:testcase what features are covered so far?
```

## How It Works

### QA Agent — Test by Doing

The QA Agent executes a human-like testing loop:

```
Observe → Plan → Act → Verify → Learn → Record
   ↑                                         |
   └─────────────────────────────────────────┘
```

1. **Observe** — Takes a screenshot, reads the screen
2. **Plan** — Matches visible elements to the test goal, consults the knowledge base
3. **Act** — Executes one device command (tap, swipe, type, etc.)
4. **Verify** — Confirms the action's effect via screenshot
5. **Learn** — Persists any new findings (selectors, screens, quirks) to KB
6. **Record** — On success, optionally generates a pytest script for future acceleration

Scripts are a **byproduct of successful testing**, not a prerequisite.

### Distiller Agent — Train the Next Generation

The Distiller operates devices using **only pixel coordinates** (no selectors) and records every interaction as VLM training trajectories. It preserves authentic behavior including misclicks and recovery — real training signal for visual reasoning models.

### Knowledge Base — Memory That Grows

Every screen, element, flow, and quirk the agent discovers is persisted in `kb/`. The agent never re-explores what it already knows. Knowledge accumulates over time, making the agent faster with each session.

### Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **QA** | Exploratory & regression testing | KB entries + pytest scripts |
| **Distiller** | Training data collection | Coordinate-based trajectories |

### Skills

| Skill | Responsibility |
|-------|---------------|
| **uiautomator2** | Device operations via `u2cli` — tap, swipe, type, screenshot, app management |
| **kb** | Read/write persistent app knowledge — screens, flows, selectors, quirks |
| **pytest** | Define pytest script conventions, fixtures, run modes, and pause-on-failure usage |
| **testcase** | Search existing tests before redundant manual testing |
| **dataset** | Manage VLM training trajectories — naming, schema, viewer |
| **init** | One-time project scaffolding |

## Design Principles

1. **Agent is the tester.** The AI doesn't write tests for something else to run — it *performs* the testing itself, directly operating the device.

2. **Scripts are acceleration, not necessity.** A generated pytest script is a cache: it replays a proven scenario without agent reasoning. No script? The agent just tests it live.

3. **Knowledge compounds.** Every session makes the next one faster. The KB grows, the agent's context improves, redundant exploration disappears.

4. **Training data is a natural byproduct.** The Distiller turns device interactions into VLM training trajectories — one interaction, two outputs (test result + training data).

5. **Self-healing on failure.** When a test fails, the device state is frozen (pause-on-failure) and the agent inspects, diagnoses, and recovers — no human intervention needed.

## Roadmap

- [ ] **Test reports** — Structured post-test reports summarizing results, screenshots, and coverage.
- [ ] **iOS support** — Swap `uiautomator2` skill for an XCUITest-based skill; agent and KB layers remain unchanged.
- [ ] **HarmonyOS support** — Add a HarmonyOS automation skill to extend coverage to Huawei devices.

## Dependencies

- [uiautomator2](https://github.com/openatx/uiautomator2) — Android automation library
- [uiautomator2-cli](https://github.com/lanbaoshen/uiautomator2-cli) — CLI wrapper for agent use
- [pytest](https://pytest.org/) — Test framework for generated scripts

## License

[MIT](LICENSE) © 2026 Lanbao Shen
