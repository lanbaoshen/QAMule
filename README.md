<p align="center">
	<img src="./logo.jpg" width="120" alt="QAMule Logo">
</p>

<h1 align="center">QAMule</h1>

<p align="center">
	Agent-native Android QA solution where the agent is the primary executor.
</p>

<p align="center">
	Explore live apps, preserve failure state, distill stable flows into pytest, and accumulate reusable product knowledge.
</p>

<p align="center">
	<a href="README_ZH.md">中文</a> •
	<a href="#your-first-ai-qa">Your First AI QA</a> •
	<a href="#quick-start">Quick Start</a> •
	<a href="#extensibility">Extensibility</a> •
	<a href="#how-it-works">How It Works</a> •
	<a href="https://github.com/lanbaoshen/QAMule-Practice">Practice Reference</a> •
	<a href="LICENSE">MIT License</a>
</p>

> **Maintenance notice:** This repository has been archived. QAMule is now maintained at [qamule/qamule](https://github.com/qamule/qamule).

---

## Meet QAMule

QAMule is an **agent-first** Android QA framework built for teams that want AI to **execute tests on real devices**, not just generate scripts.

Instead of starting from automation code, QAMule starts from live exploration and validation. Stable behavior can then be distilled into pytest assets, while the knowledge gained along the way is kept in the KB for future runs.

**Paradigm shift:**

| | Traditional Test Automation | QAMule |
|---|---|---|
| **Primary executor** | Scripts | AI agent |
| **Role of AI** | Generate or maintain scripts | Execute the test directly |
| **Scripts** | Required upfront | Optional, used for faster replay |
| **Failure handling** | Snapshot only, environment is lost | Failure state is preserved so the agent can diagnose and try to recover |
| **New scenarios** | Write scripts first, then validate | Explore and test directly |
| **Knowledge retention** | Scattered across scripts and human memory | Continuously written into the KB for reuse |

## Why QAMule

1. **It shortens the path from idea to test.** New pages, unstable flows, and changing UI do not need to wait for script coverage first. The agent can inspect, act, and validate directly on the live device.

2. **It separates testing from data collection cleanly.** QA focuses on validation, regression, and issue reproduction. Distiller focuses on real interaction trajectories for VLM training. Both build on the same KB without mixing responsibilities.

3. **It turns each run into reusable context.** Pages, selectors, flows, dependency apps, and quirks are written back into `kb/`, so later runs start from accumulated experience instead of from scratch.

4. **It keeps scripts valuable without making them the bottleneck.** Stable scenarios can be distilled into pytest for low-cost regression, while the agent stays responsible for handling change.

5. **It preserves the moment that matters most.** Pause-on-failure keeps the failed scene alive so the agent can inspect it before teardown and sometimes recover in place.

6. **It lets the agent step in only where judgment is needed.** Tests can hand one bounded checkpoint to the agent and continue with a simple yes-or-no result.

## Your First AI QA

QAMule behaves a lot like a new QA teammate, except this one lives directly in the device and the pipeline.

- It explores the app on its own and learns pages, paths, and abnormal states.
- It writes what it learns into the KB, gradually building reusable testing knowledge.
- It completes validation itself, and turns stable repetitive work into pytest scripts when automation is worth it.
- In pause mode, it feels like a QA engineer watching the pipeline live and inspecting failures on the spot.
- On the Distiller side, it also acts like a tireless data-labeling intern, continuously collecting real-device trajectories.

## Quick Start

In a few commands, you can explore a page, test a feature, collect a real-device trajectory, and keep the resulting knowledge for reuse.

### Prerequisites

- An Android device connected over USB, or an emulator
- UV for managing the Python environment and dependencies
- ADB, the Android Debug Bridge

### Installation

1. Install QAMule into your project as an agent plugin:

```bash
# GitHub Copilot
copilot plugin marketplace add lanbaoshen/agent-plugins
copilot plugin install QAMule@lanbaoshen

# Claude Code
/plugin marketplace add lanbaoshen/agent-plugins
/plugin install QAMule@lanbaoshen

# VS Code
# command + shift + p -> "Chat: Install plugin from Source" -> "lanbaoshen/agent-plugins"
```

2. Initialize the project structure:

```text
/qamule:init
```

This initializes a base UV project for QAMule and installs the core dependencies.

### Usage

**Explore a page:**
```text
@qa explore the Settings app home page, identify the main sections, and summarize actionable elements
```

**Test a feature:**
```text
@qa validate that the Bluetooth toggle in Settings can be enabled and disabled correctly, and report any unexpected system behavior
```

**Collect one training trajectory:**
```text
@distiller collect one real-device trajectory for opening the Bluetooth settings page in com.android.settings
```

**View the dataset in a page:**
```text
@distiller open the current dataset in a viewer page
```

**Update the knowledge base:**
```text
/qamule:kb Record that this app cannot be launched reliably through adb and must be entered through the in-app UI flow
```

**Query the knowledge base:**
```text
/qamule:kb What is the known navigation path for checking the Android system version on this device?
```

### Pause on failure

When enabled, pytest pauses before teardown after a failure so the agent can inspect the live scene and optionally try recovery.

This is for cases where logs and screenshots are not enough and the exact failed state still matters.

For agent-driven pytest runs, follow the live pause workflow:

1. Start pytest through `uv`:
	```bash
	uv run pytest [command/options]
	```
2. Read `run_id` from the pytest header (for example, `pytest-live-pause: run_id={run_id}`), then watch the run in another terminal:
	```bash
	uv run pytest-live-pause watch --run-id={run_id}
	```
3. When `watch` stops, inspect `kind` and `pause_id`:
	- `checkpoint`: complete the requested external task, then resume with a boolean result.
	- `failure`: follow the `live-pause-failure-triage` workflow to inspect the paused scene, use KB to classify whether the blocker belongs to preconditions, environment, test, product, or an external dependency, then resume with structured failure context.
	- `run is no longer active`: the run has completed; do not resume anything.
4. Repeat `watch` and `resume` until the run finishes.

The division of responsibility is simple:

- `pytest` defines the runtime protocol, such as how to `watch` and when to `resume`.
- `live-pause-failure-triage` defines how to investigate a `kind=failure` pause and decide the next action.
- `kb/` stores reusable project facts such as permission prompts, login prerequisites, ROM quirks, dependency screens, and recovery paths.

So failure pause is not just about dismissing blockers mechanically. First decide whether the current state is relevant to the test goal, then use KB to judge whether it matches known behavior, and only write back new findings when the observation is stable and reusable.

### Live checkpoints

QAMule also supports explicit reasoning checkpoints during a healthy test run. The test can pause at one decision point, ask for a bounded judgment, and then continue.

Use `live_pause.checkpoint` when a local assertion alone is not reliable enough, such as judging a transient screen, a visual summary, or an exploratory branch outcome.

The contract stays simple: the agent returns a boolean result plus an optional reason, and the test decides how to proceed.

Do not use it for conditions that can be verified by selectors, text assertions, state polling, or ordinary failure inspection.

<img src="pytest-run-modes-bilingual.excalidraw.svg" alt="QAMule pytest run modes">

## Extensibility

The project scaffold created by `/qamule:init` is meant to be a starting point, not a closed system. Teams can extend it with additional skills that match their own delivery workflow.

For example, if your agent environment provides a Jira-oriented skill, you can wire it into the initialized project and use Jira as the test case platform for QAMule. In that setup, Jira can become the source for case planning, execution scope, and result tracking, while QAMule remains responsible for live device execution, KB accumulation, and pytest distillation.

This makes QAMule flexible enough to fit teams that already rely on external systems for test management instead of forcing all case management to live inside the framework itself.

QAMule can also serve as the validation stage inside an AI Coding workflow. After an agent or coding assistant finishes a product change, QAMule can take over the verification step and test the changed functionality directly on an emulator or a real device. This makes it possible to connect code generation and device-level validation into one delivery loop instead of stopping at code output alone.

This also makes QAMule easier to embed into an AI-driven delivery workflow, where it serves as the device-level validation stage after code changes rather than existing only as a standalone testing framework.

## How It Works

QAMule is not built around one overloaded agent. It uses distinct roles for testing, data capture, and knowledge accumulation so each run can produce both immediate results and reusable assets.

### QA Agent

QA is the execution layer for product validation. It works in a simple loop:

```text
Observe -> Plan -> Execute -> Verify -> Learn -> Record
	 ^                                               |
	 +-----------------------------------------------+
```

1. **Observe**: capture a screenshot and read the current screen
2. **Plan**: decide the next step from the goal and the KB
3. **Execute**: issue one device command
4. **Verify**: confirm whether the action produced the expected effect
5. **Learn**: write new findings into the KB
6. **Record**: generate pytest scripts for suitable scenarios to support later regression

The point is straightforward: the test starts from the live product, and scripts appear later only when the behavior is stable enough to be worth reusing.

<img src="./qa-agent-workflow-bilingual.excalidraw.svg" alt="QA agent workflow">

### Distiller Agent

Distiller is the data layer. It is focused on **capturing replayable real-device trajectories for vision models**.

It records screenshots, actions, reasoning, foreground app, and results into `dataset/`. It does not generate pytest scripts. Its job is to preserve real interaction behavior, including missteps, corrections, waiting, and recovery, so teams can build training data from what actually happened on the device.

<img src="./distiller-agent-workflow-bilingual.excalidraw.svg" alt="Distiller workflow">

### Knowledge Base

`kb/` is the shared memory layer for both agents. It stores page information, selectors, flows, dependency apps, and known quirks.

- **QA Agent** uses it to reduce repeated exploration and improve testing efficiency.
- **Distiller Agent** uses it to understand the target app and context faster.

This is what makes QAMule compound over time: one run validates the present task, and the same run leaves behind context for the next one.

### Agents

| Agent | Purpose | Output |
|-------|------|------|
| **QA** | Exploratory testing, regression testing, issue reproduction | KB entries + pytest scripts |
| **Distiller** | Training data collection | Coordinate-based trajectory data |

### Skills

| Skill | Responsibility |
|-------|------|
| **uiautomator2** | Internal device operation skill, using `u2cli` for tapping, swiping, input, screenshots, and app management |
| **kb** | Read and write persistent app knowledge: pages, flows, selectors, and abnormal behavior |
| **pytest** | Internal pytest runtime skill for run modes, device binding, pause-on-failure, and live checkpoint workflow |
| **live-pause-failure-triage** | Internal failure triage skill used only for live pause `failure` stops, combining paused-scene inspection with KB-backed classification and structured resume reasons |
| **pytest-authoring** | Internal pytest authoring skill for testcase boundaries, markers, fixture scope, parametrization |
| **dataset** | Manage VLM training trajectories: naming, schema, and visual browsing |
| **init** | One-time project scaffolding |

## Design Principles

1. **The agent is the executor.** AI is not writing tests for another system first. It operates the product and performs the test itself.

2. **Scripts are a leverage layer, not the gate.** Pytest exists to reuse validated behavior, not to decide what is testable.

3. **Testing and data collection are separated by design.** QA produces testing assets, while Distiller produces trajectory data.

4. **The knowledge base is the collaboration layer.** QA and Distiller share page understanding, flow knowledge, and exception experience through the KB.

5. **Live state matters more than postmortem artifacts.** Preserve the state first, let the agent analyze in place, and try recovery when possible.

## Who It Is For

QAMule is a strong fit for teams that need Android QA to move at product speed without throwing away the value of structured regression.

- Android teams shipping fast-moving UI where script maintenance keeps falling behind
- Teams that want AI to participate in execution and validation, not only in code generation
- Teams that want exploratory runs to accumulate into reusable knowledge instead of disappearing after one session
- Teams that care about both regression assets and real-device trajectory data for future model work

## Dependencies

- [uiautomator2](https://github.com/openatx/uiautomator2) — Android automation library
- [uiautomator2-cli](https://github.com/lanbaoshen/uiautomator2-cli) — CLI wrapper designed for agent usage
- [pytest](https://pytest.org/) — structured testing framework
- [pytest-live-pause](https://github.com/lanbaoshen/pytest-live-pause) — pytest plugin for pause-on-failure and live checkpoint workflow
- [pytest-u2device](https://github.com/lanbaoshen/pytest-u2device) — pytest plugin for device binding and uiautomator2 interaction

## License

[MIT](LICENSE) © 2026 Lanbao Shen
