#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage:
    bash skills/dataset/scripts/validate.sh [DATASET_DIR|SESSION_DIR|TRAJECTORY_JSON]

Example:
  bash skills/dataset/scripts/validate.sh dataset/
    bash skills/dataset/scripts/validate.sh dataset/open_wifi_20260514_101530/
    bash skills/dataset/scripts/validate.sh dataset/open_wifi_20260514_101530/trajectory.json
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

INPUT_PATH="${1:-dataset}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[FATAL] python3 is required to run this validator." >&2
  exit 127
fi

if [[ ! -e "$INPUT_PATH" ]]; then
    echo "[FATAL] Input path not found: $INPUT_PATH" >&2
  exit 2
fi

python3 - "$INPUT_PATH" <<'PY'
import json
import re
import sys
from pathlib import Path

SESSION_DIR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*_\d{8}_\d{6}$")
STEP_PNG_RE = re.compile(r"^step_(\d{3})\.png$")

ACTION_REQUIRED_PARAMS = {
    "app_start": {"app"},
    "click": {"x", "y"},
    "long_click": {"x", "y"},
    "swipe": {"x1", "y1", "x2", "y2"},
    "type": {"text"},
    "press": {"key"},
    "wait": {"duration"},
    "finish": {"reason"},
    "impossible": {"reason"},
}

TERMINAL_ACTIONS = {"finish", "impossible"}
NUMERIC_KEYS = {
    "click": {"x", "y"},
    "long_click": {"x", "y"},
    "swipe": {"x1", "y1", "x2", "y2"},
    "wait": {"duration"},
}

input_path = Path(sys.argv[1]).resolve()

if input_path.is_file():
    if input_path.name != "trajectory.json":
        print(
            f"[FATAL] When input is a file, it must be named 'trajectory.json': {input_path}",
            file=sys.stderr,
        )
        sys.exit(2)
    mode = "single_trajectory"
    dataset_root = input_path.parent
    trajectory_files = [input_path]
    session_dirs = [input_path.parent]
elif input_path.is_dir():
    if (input_path / "trajectory.json").is_file():
        mode = "single_session"
        dataset_root = input_path.parent
        trajectory_files = [input_path / "trajectory.json"]
        session_dirs = [input_path]
    else:
        mode = "dataset"
        dataset_root = input_path
        trajectory_files = sorted(p for p in dataset_root.rglob("trajectory.json") if p.is_file())
        session_dirs = sorted(
            p for p in dataset_root.rglob("*") if p.is_dir() and SESSION_DIR_RE.match(p.name)
        )
else:
    print(f"[FATAL] Unsupported input path: {input_path}", file=sys.stderr)
    sys.exit(2)

errors = []
warnings = []


def rel(path: Path) -> str:
    try:
        return path.relative_to(dataset_root).as_posix()
    except ValueError:
        return path.as_posix()


def add_error(location: str, message: str) -> None:
    errors.append(f"[ERROR] {location}: {message}")


def add_warning(location: str, message: str) -> None:
    warnings.append(f"[WARN]  {location}: {message}")


def is_non_empty_string(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def summarize_indices(values, max_items=10) -> str:
    values = sorted(values)
    if len(values) <= max_items:
        return ", ".join(str(v) for v in values)
    shown = ", ".join(str(v) for v in values[:max_items])
    return f"{shown}, ... (+{len(values) - max_items} more)"


def validate_action(action, location: str):
    if not isinstance(action, dict):
        add_error(location, "field 'action' must be an object")
        return None

    action_type = action.get("type")
    if not is_non_empty_string(action_type):
        add_error(location, "field 'action.type' must be a non-empty string")
        return None

    if action_type not in ACTION_REQUIRED_PARAMS:
        valid = ", ".join(sorted(ACTION_REQUIRED_PARAMS))
        add_error(location, f"unknown action type '{action_type}', expected one of: {valid}")
        return action_type

    for key in sorted(ACTION_REQUIRED_PARAMS[action_type]):
        if key not in action:
            add_error(location, f"action '{action_type}' is missing required param '{key}'")

    for key in sorted(NUMERIC_KEYS.get(action_type, set())):
        if key in action and not isinstance(action[key], (int, float)):
            add_error(location, f"action '{action_type}.{key}' must be a number")

    if action_type == "type" and "text" in action and not isinstance(action["text"], str):
        add_error(location, "action 'type.text' must be a string")
    if action_type == "press" and "key" in action and not isinstance(action["key"], str):
        add_error(location, "action 'press.key' must be a string")
    if action_type == "app_start":
        if "app" in action and not isinstance(action["app"], str):
            add_error(location, "action 'app_start.app' must be a string")
        if "activity" in action and not isinstance(action["activity"], str):
            add_error(location, "action 'app_start.activity' must be a string when provided")
    if action_type in TERMINAL_ACTIONS and "reason" in action and not isinstance(action["reason"], str):
        add_error(location, f"action '{action_type}.reason' must be a string")

    return action_type


if not trajectory_files:
    add_error(rel(input_path), "no trajectory.json found under input scope")

for session_dir in session_dirs:
    if not (session_dir / "trajectory.json").is_file():
        add_error(rel(session_dir), "session directory matches naming rule but trajectory.json is missing")

for traj_file in trajectory_files:
    session_dir = traj_file.parent
    traj_loc = rel(traj_file)
    session_name = session_dir.name

    if not SESSION_DIR_RE.match(session_name):
        add_warning(
            traj_loc,
            "parent directory does not match '{task_slug}_YYYYMMDD_HHMMSS' naming convention",
        )

    try:
        raw = traj_file.read_text(encoding="utf-8")
        data = json.loads(raw)
    except UnicodeDecodeError:
        add_error(traj_loc, "file is not valid UTF-8")
        continue
    except json.JSONDecodeError as exc:
        add_error(traj_loc, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        continue
    except OSError as exc:
        add_error(traj_loc, f"cannot read file: {exc}")
        continue

    if not isinstance(data, dict):
        add_error(traj_loc, "top-level JSON must be an object")
        continue

    task_id = data.get("task_id")
    instruction = data.get("instruction")
    app = data.get("app")
    device = data.get("device")
    steps = data.get("steps")
    success = data.get("success")
    total_steps = data.get("total_steps")

    if not is_non_empty_string(task_id):
        add_error(traj_loc, "field 'task_id' must be a non-empty string")
    elif task_id != session_name:
        add_warning(traj_loc, f"task_id '{task_id}' does not match session directory '{session_name}'")

    if not is_non_empty_string(instruction):
        add_error(traj_loc, "field 'instruction' must be a non-empty string")

    if not is_non_empty_string(app):
        add_error(traj_loc, "field 'app' must be a non-empty string")

    if not isinstance(device, dict):
        add_error(traj_loc, "field 'device' must be an object")
    else:
        if not is_non_empty_string(device.get("model")):
            add_error(traj_loc, "field 'device.model' must be a non-empty string")

        resolution = device.get("resolution")
        if not (
            isinstance(resolution, list)
            and len(resolution) == 2
            and all(isinstance(v, int) and v > 0 for v in resolution)
        ):
            add_error(traj_loc, "field 'device.resolution' must be [width, height] with positive integers")

        if not is_non_empty_string(device.get("android")):
            add_error(traj_loc, "field 'device.android' must be a non-empty string")

    if not isinstance(steps, list):
        add_error(traj_loc, "field 'steps' must be an array")
        steps = []

    if not isinstance(success, bool):
        add_error(traj_loc, "field 'success' must be true/false")

    if not isinstance(total_steps, int) or total_steps < 0:
        add_error(traj_loc, "field 'total_steps' must be a non-negative integer")
    elif total_steps != len(steps):
        add_error(traj_loc, f"total_steps={total_steps} does not match steps length={len(steps)}")

    referenced_screenshots = set()
    terminal_action_positions = []

    for index, step in enumerate(steps, start=1):
        step_loc = f"{traj_loc} steps[{index - 1}]"

        if not isinstance(step, dict):
            add_error(step_loc, "step item must be an object")
            continue

        step_no = step.get("step")
        if not isinstance(step_no, int):
            add_error(step_loc, "field 'step' must be an integer")
        elif step_no != index:
            add_error(step_loc, f"step number should be {index}, got {step_no}")

        screenshot = step.get("screenshot")
        if not is_non_empty_string(screenshot):
            add_error(step_loc, "field 'screenshot' must be a non-empty string")
        else:
            matched = STEP_PNG_RE.match(screenshot)
            if not matched:
                add_error(step_loc, "screenshot must match pattern 'step_{NNN}.png'")
            else:
                shot_index = int(matched.group(1))
                if shot_index != index:
                    add_warning(step_loc, f"screenshot index is {shot_index:03d}, expected {index:03d}")
            referenced_screenshots.add(screenshot)

            screenshot_path = session_dir / screenshot
            if not screenshot_path.is_file():
                add_error(step_loc, f"referenced screenshot not found: {screenshot}")

        if not is_non_empty_string(step.get("thought")):
            add_error(step_loc, "field 'thought' must be a non-empty string")

        action_type = validate_action(step.get("action"), step_loc)
        if action_type in TERMINAL_ACTIONS:
            terminal_action_positions.append(index)

        step_success = step.get("success")
        if not isinstance(step_success, bool):
            add_error(step_loc, "field 'success' must be true/false")

    if terminal_action_positions:
        last_terminal = terminal_action_positions[-1]
        if last_terminal != len(steps):
            add_warning(
                traj_loc,
                f"terminal action appears at step {last_terminal}, but it is not the final step",
            )

    png_files = sorted(
        p.name for p in session_dir.iterdir() if p.is_file() and p.suffix.lower() == ".png"
    )
    valid_step_pngs = []
    invalid_png_names = []

    for name in png_files:
        match = STEP_PNG_RE.match(name)
        if match:
            valid_step_pngs.append((name, int(match.group(1))))
        else:
            invalid_png_names.append(name)

    if invalid_png_names:
        add_error(
            traj_loc,
            "PNG file name must match 'step_{NNN}.png': " + ", ".join(invalid_png_names),
        )

    if valid_step_pngs:
        indices = {idx for _, idx in valid_step_pngs}
        max_idx = max(indices)
        missing = [i for i in range(1, max_idx + 1) if i not in indices]
        if missing:
            add_error(
                traj_loc,
                "missing screenshot indices in session folder: " + summarize_indices(missing),
            )

    valid_png_names = {name for name, _ in valid_step_pngs}
    unreferenced = sorted(valid_png_names - referenced_screenshots)
    if unreferenced:
        add_warning(
            traj_loc,
            "unreferenced step screenshots: " + ", ".join(unreferenced),
        )


for line in errors:
    print(line)
for line in warnings:
    print(line)

print(
    f"\nMode: {mode}. Scanned {len(trajectory_files)} trajectory file(s) and {len(session_dirs)} session-like directories."
)
print(f"Found {len(errors)} error(s), {len(warnings)} warning(s).")

sys.exit(1 if errors else 0)
PY
