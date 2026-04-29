# Dataset Directory

Training data collected by the Distiller agent.

## Structure

```
dataset/
├── {task_slug}_{YYYYMMDD}_{HHMMSS}/  # e.g. open_bluetooth_20260429_143022
│   ├── trajectory.json              # Task metadata + steps
│   ├── step_001.png
│   ├── step_002.png
│   ├── ...
│   └── step_NNN_final.png           # End state screenshot
└── README.md
```

## Review Workflow

Each trajectory has `"success": null` by default. After review, set it to `true` (usable) or `false` (discard).

```bash
# Quick review: list all unreviewed trajectories
grep -rl '"success": null' dataset/*/trajectory.json

# View a trajectory
python -m json.tool dataset/{session_id}/trajectory.json
```
