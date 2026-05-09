---
name: dataset
description: 'Manage the VLM training dataset (dataset/). Use when creating trajectory sessions, saving screenshots and trajectory JSON, or reading/validating existing trajectories.'
---

# Dataset Management

Persistent dataset at `dataset/`. Stores VLM training trajectories organized by scenario type. Create the structure if it doesn't exist.

## Structure

```
dataset/
  {normal|edge_cases}/
    {session_dir}/
      step_001.png … step_NNN_final.png
      trajectory.json
```

## trajectory.json

All fields required unless noted.

```json
{
  "task_id": "{session_dir}",
  "instruction": "Human-readable task description",
  "app": "com.example.app",
  "device": { "model": "…", "resolution": [1080, 2400], "android": "14" },
  "steps": [
    {
      "step": 1,
      "screenshot": "step_001.png",
      "screen": { "package": "…", "activity": "…" },
      "thought": "What I see and my reasoning",
      "action": { "type": "click", "x": 512, "y": 750 },
      "success": true
    }
  ],
  "success": null,
  "total_steps": 3
}
```

- `screen` is optional; all other step fields are required.
- Per-step `success`: `true` if the action command executed without error, `false` only if the command itself failed. Wrong coordinate choices or unintended UI outcomes are still `true` — the command ran successfully.
- Top-level `success` is always `null` — human reviewers set it later.

## Action Schema

| type | params | notes |
|------|--------|-------|
| `app_start` | `app` | Launch app |
| `click` | `x, y` | Raw pixel coords |
| `long_click` | `x, y` | Raw pixel coords |
| `swipe` | `x1, y1, x2, y2` | Raw pixel coords |
| `type` | `text` | Into focused field |
| `press` | `key` | Hardware/soft key |
| `scroll` | `direction` | up/down/left/right |
| `wait` | `duration` | Sleep N seconds (e.g. waiting for page load) |
| `finish` | `reason` | Terminal |
| `impossible` | `reason` | Terminal |

## Procedures

### Create session

1. `mkdir -p dataset/{normal|edge_cases}/{task_slug}_{YYYYMMDD}_{HHMMSS}`

### Save steps

- Screenshot → `step_{NNN}.png` (zero-padded 3 digits).
- Final step → rename to `step_{NNN}_final.png`.

### Save trajectory

Write `trajectory.json` after all steps. Post-processing checklist:

1. **Raw pixel coordinates** — store the exact pixel values used during execution. Do NOT normalize. The `device.resolution` field enables training-time normalization.
2. **Valid JSON** — use a JSON encoder, don't manually escape.
3. **Descriptive thoughts** — each `thought` becomes CoT training signal.

> **Training-time normalization**: `norm = round(px / dimension * 1000)` where `dimension` is width (for x) or height (for y) from `device.resolution [width, height]`. Apply this during data loading, not during trajectory generation.

### Read / validate

```bash
ls dataset/{scenario_type}/                                  # list sessions
cat dataset/{scenario_type}/{session_dir}/trajectory.json    # read one
```

Skip sessions with missing fields or unparseable JSON.

### Preview

```bash
.venv/bin/python skills/dataset/scripts/viewer.py [--port 9000] dataset/
```

## Naming Conventions

| Element | Rule | Example |
|---------|------|---------|
| Session dir (= `task_id`) | `{task_slug}_{YYYYMMDD}_{HHMMSS}`, snake_case, <40 chars, ASCII | `open_bluetooth_20260509_143022` |
| Screenshots | `step_{NNN}.png`; final: `step_{NNN}_final.png` | `step_001.png` |
| Scenario dirs | `normal/` or `edge_cases/` | — |

One `trajectory.json` per session. Do NOT modify after saving — append new sessions instead.
