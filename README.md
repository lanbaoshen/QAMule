<p align="center">
	<img src="./logo.svg" width="120" alt="QAMule Logo">
</p>

<h1 align="center">QAMule</h1>

<p align="center">
	An agent-native Android testing framework — the agent itself is the tester.
</p>

<p align="center">
	<a href="README_ZH.md">中文</a> •
	<a href="#quick-start">Quick Start</a> •
	<a href="#how-it-works">How It Works</a> •
	<a href="https://github.com/lanbaoshen/QAMule-Practice">Practice Reference</a> •
	<a href="LICENSE">MIT License</a>
</p>

---

## What Is This?

QAMule is an **agent-first** Android QA framework. It does not use AI to help you generate scripts first. Instead, it lets an **AI agent operate the device directly to complete testing**. Scripts still matter, but they are no longer the prerequisite for testing. They become an acceleration cache built after a behavior has already been validated.

The key shift is not "using AI to assist automation." The key shift is moving the test entry point from scripts to agents, then turning long-term reuse into KB entries, pytest assets, and datasets.

**Paradigm shift:**

| | Traditional Test Automation | QAMule |
|---|---|---|
| **Primary executor** | Scripts | AI agent |
| **Role of AI** | Generate or maintain scripts | Execute the test directly |
| **Scripts** | Required upfront | Optional, used for faster replay |
| **Failure handling** | Snapshot only, environment is lost | Failure state is preserved so the agent can diagnose and try to recover |
| **New scenarios** | Write scripts first, then validate | Explore and test directly |
| **Knowledge retention** | Scattered across scripts and human memory | Continuously written into the KB for reuse |

## Core Highlights

1. **The agent tests directly.** When QAMule sees a new page, flow, or feature, its first response is not to patch scripts. It lets the agent inspect, try, and validate first. That makes it a natural fit for Android teams with fast-changing requirements, lagging regression coverage, and high exploration cost.

2. **QA and Distiller have distinct roles.** The QA agent handles exploration, validation, regression, issue reproduction, and eventually pytest script distillation for mature scenarios. The Distiller agent captures real visual interaction trajectories and turns them into VLM training data. Their outputs differ, but they share the same KB.

3. **The KB makes experience reusable.** Pages, elements, flows, dependency apps, and abnormal behaviors are continuously written into `kb/`. One exploration run does not only solve the current task. It also leaves context behind for future QA and Distiller runs.

4. **Scripts are a cache of successful experience.** Pytest is not the entry point to testing. It is the artifact of stable, validated scenarios. The agent handles change; scripts provide cheap regression.

5. **Failure state is preserved.** QAMule freezes the failing scene with pause-on-failure, so the agent can keep observing, analyzing, and sometimes recovering before teardown runs, instead of relying only on postmortem logs.

## Quick Start

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

This copies config files, creates the project skeleton, and installs the base dependencies.

### Usage

**Explore a page:**
```text
@QAMule QA explore the Settings page
```

**Test a feature:**
```text
@QAMule QA test whether the Bluetooth toggle in Settings works correctly
```

**Collect one training trajectory:**
```text
@QAMule Distiller open Bluetooth in com.android.settings
```

**Update the knowledge base:**
```text
/qamule:kb This app can only be launched through the UI
```

**Query the knowledge base:**
```text
/qamule:kb How do I check the system version?
```

**Review existing coverage:**
```text
/qamule:testcase Which features are covered right now?
```

## How It Works

### QA Agent — test by doing, then distill

The QA agent follows a human-like testing loop:

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

Scripts are the **distilled result** of a successful test, not a prerequisite before the test starts.

<img src="./qa-agent-workflow-bilingual.excalidraw.svg">

### Distiller Agent — collect real trajectories for vision models

Distiller does one thing only: **capture high-quality, replayable trajectories from real device interaction**.

It uses screenshots and the current app state as its main observation input, executes actions with absolute coordinates, and logs screenshots, actions, reasoning, foreground app, and results step by step into `dataset/`. It does not generate pytest scripts. Its focus is preserving real interaction behavior, including missteps, corrections, waiting, and recovery. It also reuses page and flow knowledge from the KB to reduce blind trial and error.

<img src="./distiller-agent-workflow-bilingual.excalidraw.svg">

### Knowledge Base — shared memory for both agents

`kb/` is QAMule's long-term memory layer. It stores page information, element selectors, business flows, dependency apps, and known quirks.

- **QA Agent** uses it to reduce repeated exploration and improve testing efficiency.
- **Distiller Agent** uses it to understand the target app and context faster.

One of QAMule's core design choices is not asking a single agent to produce everything. Different agents collaborate around the same shared knowledge and accumulate it over time, while producing different kinds of testing and data assets.

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
| **pytest** | Internal pytest conventions for script structure, fixture contracts, run modes, and pause-on-failure usage |
| **testcase** | Look up existing cases before manual testing to avoid duplicate effort |
| **dataset** | Manage VLM training trajectories: naming, schema, and visual browsing |
| **init** | One-time project scaffolding |

## Design Principles

1. **The agent is the tester.** AI is not writing tests for another system. It executes the test itself.

2. **Scripts are an acceleration layer, not the prerequisite.** Pytest exists to reuse validated behavior, not to limit testing to what already has scripts.

3. **QA and Distiller are separated, not blended.** One produces testing assets, the other produces data assets.

4. **The knowledge base is the collaboration layer.** QA and Distiller share page understanding, flow knowledge, and exception experience through the KB, reducing repeated exploration.

5. **Failure state matters more than logs.** Preserve the state first, let the agent analyze in place, and try recovery when possible.

## Who This Fits

- Android teams with fast iteration and high script maintenance cost
- Teams that want AI to participate in test execution, not just code generation
- Teams that want to turn the testing process into long-term knowledge assets
- Teams that care about both engineering test coverage and vision-operation model data accumulation

## Dependencies

- [uiautomator2](https://github.com/openatx/uiautomator2) — Android automation library
- [uiautomator2-cli](https://github.com/lanbaoshen/uiautomator2-cli) — CLI wrapper designed for agent usage
- [pytest](https://pytest.org/) — structured testing framework

## License

[MIT](LICENSE) © 2026 Lanbao Shen
