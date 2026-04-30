---
name: viewer
description: "Launch a local web viewer to browse distilled VLM trajectories. Use when: view trajectory, browse dataset, review distillation results, 查看轨迹, 浏览数据集, 回放操作步骤."
argument-hint: "Path to the dataset directory, e.g. ./dataset"
---

# Trajectory Viewer

A zero-dependency local server that renders distilled trajectories into a human-readable timeline with screenshot overlays.

## When to Use

- After distillation is complete and the user wants to review results
- When the user asks to view, browse, or inspect trajectories
- For quality-checking collected training data

## Procedure

1. Identify the dataset directory (defaults to `./dataset` in the project root).
2. Launch the viewer from the project root:

```bash
.venv/bin/python ./skills/viewer/scripts/server.py <DATASET_DIR>
```

   The script is located at [`./scripts/server.py`](./scripts/server.py) within this skill.

3. The browser opens automatically. The user can browse trajectories by scenario group, click into any trajectory to see the step-by-step timeline with screenshots and action overlays.

## Features

- **Real-time directory scanning** — no manifest or pre-generation needed; refresh to see new trajectories
- **Lazy loading** — only fetches images for the selected trajectory
- **Action overlays** — click coordinates shown as pulsing red dots on screenshots; swipe as arrows
- **Dark editorial theme** — optimized for screenshot readability

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 8932 | Port to serve on |
| `--no-open` | false | Don't open browser automatically |

## Example

```bash
# View the dataset in the current project
.venv/bin/python skills/viewer/scripts/server.py ./dataset

# Specify a different port
.venv/bin/python skills/viewer/scripts/server.py /path/to/dataset --port 9000
```
