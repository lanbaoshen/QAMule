---
name: init
description: "Initialize project structure for QAMule testing. Use when setting up a new project, first-time setup, or when user says: init, initialize, setup project, create test structure."
---

# Project Init

Initialize the standard QAMule test project structure in the user's workspace.

## Procedure

### 1. Copy Asset Files

Copy the [assets](./assets/) directory into the project root, skipping any files that already exist:

```bash
cp -rn <path-to-this-skill>/assets/* <project-root>/
```

The `-n` flag ensures existing files are never overwritten.

### 2. Init kb, test directories and datasets

- Use `kb skill` to create the `kb/` directory with the initial knowledge base structure for the app under test.
- Use `pytest skill` to create the `tests/` directory for generated test files.
- Use `dataset skill` to create the `dataset/` directory for storing screenshots and training data.

### 3. Verify

After creating files, confirm:
- All files are in place
- Install dependencies: `uv sync`
