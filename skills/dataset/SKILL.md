---
name: dataset
description: 'Manage VLM trajectory data in dataset/. Use when creating sessions, writing trajectory.json, validating samples, or previewing the dataset.'
---

# Dataset Management

Use this skill to create and validate VLM trajectory sessions in `dataset/`.

## Structure

```
dataset/
  {session_dir}/
    step_001.png … step_NNN.png
    trajectory.json
```

### Init Session Directory

Initialize once at the start of a session:

```bash
uv run python <path-to-this-skill>/scripts/trajectory.py init \
  --task-slug open_wifi \
  --instruction "Human task instruction here" \
  --app com.example.app \
  --device-model "Pixel 8" \
  --resolution 1080 2400 \
  --android 14
```

It will print the created session directory.

### Screenshot

Save screenshots as `step_{NNN}.png` (3-digit zero padding) in the session directory.

### Append Steps

```bash
uv run python <path-to-this-skill>/scripts/trajectory.py append dataset/{session_dir} \
  --screenshot step_001.png \
  --current-app com.example.app/.MainActivity \
  --thought "I can see the main screen and the login button is visible." \
  --action '{"type":"click","x":512,"y":750}' \
  --step-success true
```

#### Action Types

| type | params | notes |
|------|--------|-------|
| `app_start` | `app, activity(optional)` | Launch app |
| `click` | `x, y` | Raw pixel coords |
| `long_click` | `x, y` | Raw pixel coords |
| `swipe` | `x1, y1, x2, y2` | Raw pixel coords |
| `type` | `text` | Into focused field |
| `press` | `key` | Hardware/soft key |
| `wait` | `duration` | Sleep N seconds (e.g. waiting for page load) |
| `finish` | `reason` | Terminal, task completed |
| `impossible` | `reason` | Terminal, task cannot be completed |

### Validation

Validate with scripts:

```bash
# Validate a single session directory
bash <path-to-this-skill>/scripts/validate.sh dataset/{session_dir}/
# Validate full dataset
bash <path-to-this-skill>/scripts/validate.sh dataset/
```

### Preview Dataset with Viewer for Human Evaluation

```bash
uv run python <path-to-this-skill>/scripts/viewer.py dataset/
```
