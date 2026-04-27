---
name: init
description: 'Scaffold a new QAMule test automation project. Use when: /init, initialize project, scaffold project, 初始化项目, 新建测试项目, 搭建项目骨架, create project skeleton, set up Android test project.'
argument-hint: 'Project name and Android app package name, e.g. my-app com.example.myapp'
---

# Initialize QAMule Project

Scaffold a complete Android test automation project (uiautomator2 + pytest) in the current workspace.

## Input

The user should provide two arguments (space-separated after `/init`):

1. **Project name** — used in `pyproject.toml` (e.g. `qamule-myapp`). If omitted, derive from the workspace folder name.
2. **Package name** — Android app package (e.g. `com.example.myapp`). If omitted, **ask the user**.

## Procedure

### 1. Copy template tree

Copy the entire `templates/` directory from this skill into the workspace root:

```bash
cp -rn ./templates/. "$WORKSPACE_ROOT/"
```

> Use `cp -rn` (no-clobber) so existing files are never overwritten.

The templates directory is located at: `[templates/](./templates/)`

### 2. Install dependencies

```bash
cd "$WORKSPACE_ROOT" && uv sync
```
