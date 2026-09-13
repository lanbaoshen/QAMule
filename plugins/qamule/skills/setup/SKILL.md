---
name: setup
description: Setup basic environment for QAMule testing
disable-model-invocation: true
---

# Setup

Set up a base QAMule test project in the user's workspace.

## 1. Initialize Project

```bash
uv init --name <project-name> --no-package --bare
touch qamule.lock
```

This creates the base UV project scaffold.

### 2. Add Dependencies

```bash
uv add "pytest" "qamule-pytest" "uiautomator2>=3.7.0"
```

### 3. Installation Dependencies

```bash
uv sync
```

After these steps, the workspace has a minimal QAMule-ready Python project with the core runtime dependencies installed.

### 4. Suggest Next Steps

After setting up the project, suggest useful next actions to the user, such as:

- Use the `knowledge-base` skill to import the basic knowledge base for testing.
- Ask the `QA` agent to explore or test the application.
- Install optional QAMule plugins that match the user's testing needs. Briefly explain why each suggested plugin is relevant, and do not install it unless the user asks:
	- `qamule-dispcap`: record Android display videos during pytest runs.
	- `qamule-jira`: work with Jira issues and Xray test cases or test executions.
	- `qamule-scholar`: record human Android interactions with microphone transcription on macOS.

Install a selected plugin from the QAMule marketplace with:

```bash
copilot plugin install <plugin-name>@qamule
```

After installation, follow the selected plugin's skill for any runtime dependency or environment setup.
