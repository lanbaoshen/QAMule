---
name: init
description: "Initialize a base UV project for QAMule testing and install the core dependencies. Use when setting up a new project, first-time setup, or when user says: init, initialize, setup project."
argument-hint: "<project-name>"
disable-model-invocation: true
---

# Project Init

Initialize a base QAMule test project in the user's workspace.

## Procedure

### 1. Init Project

```bash
uv init --name <project-name> --no-package --bare
```

This creates the base UV project scaffold.

### 2. Add Dependency

```bash
uv add pytest pytest-u2device pytest-live-pause uiautomator2-cli uiautomator2
```

### 3. Install Dependencies

```bash
uv sync
```

After these steps, the workspace has a minimal QAMule-ready Python project with the core runtime dependencies installed.

### 4. Next Steps Suggestion

After initializing the project, you can suggest the next steps to the user, such as:
- Use `kb skill` to import the basic knowledge base for testing.
- Ask `qa` agent to explore or test the application.
- Ask `distiller` agent to generate VLM training data for the application.
