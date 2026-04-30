# Dataset Directory

Training data collected by the Distiller agent.

## Structure

```
dataset/
├── normal/                                        # Happy-path, standard user journeys
│   ├── {task_slug}_{YYYYMMDD}_{HHMMSS}/          # e.g. open_bluetooth_20260429_143022
│   │   ├── trajectory.json                       # Task metadata + steps
│   │   ├── step_001.png
│   │   ├── step_002.png
│   │   ├── ...
│   │   └── step_NNN_final.png                    # End state screenshot
│   └── ...
├── edge_cases/                                    # Error recovery, permission denied, unusual states, boundary conditions
│   ├── {task_slug}_{YYYYMMDD}_{HHMMSS}/
│   │   ├── trajectory.json
│   │   └── step_*.png
│   └── ...
└── README.md
```

## Review Workflow

Each trajectory has `"success": null` by default. After review, set it to `true` (usable) or `false` (discard).

```bash
# Quick review: list all unreviewed trajectories
grep -rl '"success": null' dataset/normal/*/trajectory.json dataset/edge_cases/*/trajectory.json

# View a trajectory
python -m json.tool dataset/{normal|edge_cases}/{task_slug}_{YYYYMMDD}_{HHMMSS}/trajectory.json

# Count trajectories by type
echo "normal:     $(ls dataset/normal/ 2>/dev/null | wc -l | tr -d ' ')"
echo "edge_cases: $(ls dataset/edge_cases/ 2>/dev/null | wc -l | tr -d ' ')"
```
