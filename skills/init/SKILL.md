---
name: init
description: "Initialize project structure for QAMule testing. Use when setting up a new project, first-time setup, or when user says: init, initialize, setup project, create test structure."
argument-hint: "<project-name>"
---

# Project Init

Initialize the standard QAMule test project structure in the user's workspace.

## Procedure

### 1. Init Project Structure

```bash
uv init --name <project-name> --no-package --bare
```

### 2. Add QAMule Dependency

```bash
uv add pytest pytest-live-pause pytest-u2device uiautomator2-cli uiautomator2
```

### 3. Init kb, test directories

- Use `kb skill` to create the `kb/` directory with the initial knowledge base structure for the app under test.
- Create the `tests/` directory for generated test files.

### 4. Verify

After creating files, confirm:
- All files are in place
- Install dependencies: `uv sync`
