---
name: dataset
description: 'Manage VLM trajectory data in dataset/. Use when creating sessions, writing trajectory.json, validating samples, or previewing the dataset.'
---

# Dataset Management

Use this skill to create and validate VLM trajectory sessions in `dataset/`.

## Structure

```
dataset/
  {task_slug}_{YYYYMMDD}_{HHMMSS}/
    step_001.png … step_NNN.png
    trajectory.json
```

### trajectory.json

Template:

```json
{
  "task_id": "{session_dir}",
  "instruction": "Human task instruction here",
  "app": "com.example.app",
  "device": { "model": "…", "resolution": [1080, 2400], "android": "14" },
  "steps": [
    {
      "step": 1,
      "screenshot": "step_001.png",
      "thought": "What I see and my reasoning to decide the next action.",
      "action": { "type": "click", "x": 512, "y": 750 },
      "success": true
    }
  ],
  "success": true,
  "total_steps": 1
}
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

#### Validation Rules

- session dir: `mkdir -p "dataset/{task_slug}_$(date +%Y%m%d_%H%M%S)"`
- Save screenshots as `step_{NNN}.png` (3-digit zero padding).
- `trajectory.json` following the template above.
- Validate with scripts:

```bash
# Validate a single session directory
bash skills/dataset/scripts/validate.sh dataset/{session_dir}/
# Validate full dataset
bash skills/dataset/scripts/validate.sh dataset/
```

### Preview Dataset with Viewer for Human Evaluation

```bash
uv run python skills/dataset/scripts/viewer.py dataset/
```
