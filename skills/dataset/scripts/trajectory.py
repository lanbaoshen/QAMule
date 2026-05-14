#!/usr/bin/env python3
"""Incremental trajectory writer for dataset sessions.

Usage examples:
  python skills/dataset/scripts/trajectory.py init dataset/open_wifi_20260514_101530 \
    --instruction "Open Wi-Fi in Settings" \
    --app com.android.settings \
    --device-model "Pixel 8" \
    --resolution 1080 2400 \
    --android 14

  python skills/dataset/scripts/trajectory.py append dataset/open_wifi_20260514_101530 \
    --screenshot step_001.png \
    --current-app com.android.settings/.Settings \
    --thought "I can see the Settings home screen and the Network section." \
    --action '{"type":"click","x":540,"y":620}'
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import NoReturn


STEP_PNG_RE = re.compile(r"^step_(\d{3})\.png$")
TASK_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
TERMINAL_ACTIONS = {"finish", "impossible"}


def fail(message: str) -> NoReturn:
    print(f"[FATAL] {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("expected true/false")


def load_trajectory(session_dir: Path) -> tuple[Path, dict]:
    trajectory_path = session_dir / "trajectory.json"
    if not trajectory_path.is_file():
        fail(f"trajectory.json not found in session directory: {session_dir}")

    try:
        data = json.loads(trajectory_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {trajectory_path}: line {exc.lineno}, column {exc.colno}: {exc.msg}")
    except OSError as exc:
        fail(f"cannot read {trajectory_path}: {exc}")

    if not isinstance(data, dict):
        fail("trajectory.json must contain a top-level object")

    steps = data.get("steps")
    if not isinstance(steps, list):
        fail("trajectory.json field 'steps' must be an array")

    return trajectory_path, data


def write_trajectory(trajectory_path: Path, data: dict) -> None:
    data["total_steps"] = len(data.get("steps", []))
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    trajectory_path.write_text(payload, encoding="utf-8")


def expected_screenshot_name(step_number: int) -> str:
    return f"step_{step_number:03d}.png"


def parse_action(raw_action: str) -> dict:
    try:
        action = json.loads(raw_action)
    except json.JSONDecodeError as exc:
        fail(f"invalid action JSON: line {exc.lineno}, column {exc.colno}: {exc.msg}")

    if not isinstance(action, dict):
        fail("action must decode to a JSON object")

    action_type = action.get("type")
    if not isinstance(action_type, str) or not action_type.strip():
        fail("action.type must be a non-empty string")

    return action


def resolve_session_dir(args: argparse.Namespace) -> Path:
    if args.session_dir and args.task_slug:
        fail("pass either SESSION_DIR or --task-slug, not both")

    if args.session_dir:
        return Path(args.session_dir)

    if not args.task_slug:
        fail("init requires either SESSION_DIR or --task-slug")

    if not TASK_SLUG_RE.match(args.task_slug):
        fail("task slug must match pattern '[A-Za-z0-9][A-Za-z0-9_-]*'")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path(args.dataset_root) / f"{args.task_slug}_{timestamp}"


def cmd_init(args: argparse.Namespace) -> int:
    session_dir = resolve_session_dir(args)
    session_dir.mkdir(parents=True, exist_ok=True)

    trajectory_path = session_dir / "trajectory.json"
    if trajectory_path.exists() and not args.force:
        fail(f"trajectory.json already exists: {trajectory_path}. Use --force to overwrite it.")

    data = {
        "task_id": session_dir.name,
        "instruction": args.instruction,
        "app": args.app,
        "device": {
            "model": args.device_model,
            "resolution": [args.resolution[0], args.resolution[1]],
            "android": args.android,
        },
        "steps": [],
        "success": False,
        "total_steps": 0,
    }

    write_trajectory(trajectory_path, data)
    print(session_dir)
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    session_dir = Path(args.session_dir)
    trajectory_path, data = load_trajectory(session_dir)
    steps = data["steps"]

    if steps:
        last_action = steps[-1].get("action", {})
        if isinstance(last_action, dict) and last_action.get("type") in TERMINAL_ACTIONS:
            fail("cannot append after a terminal action; start a new session or edit the JSON manually")

    action = parse_action(args.action)
    step_number = len(steps) + 1
    expected_name = expected_screenshot_name(step_number)
    screenshot_name = args.screenshot

    if not STEP_PNG_RE.match(screenshot_name):
        fail("screenshot must match pattern 'step_{NNN}.png'")
    if screenshot_name != expected_name:
        fail(f"screenshot for step {step_number} must be named {expected_name}")
    if not (session_dir / screenshot_name).is_file():
        fail(f"screenshot not found in session directory: {screenshot_name}")

    step = {
        "step": step_number,
        "screenshot": screenshot_name,
        "current_app": args.current_app,
        "thought": args.thought,
        "action": action,
        "success": args.step_success,
    }
    steps.append(step)

    action_type = action.get("type")
    if action_type == "finish":
        data["success"] = True
    elif action_type == "impossible":
        data["success"] = False

    write_trajectory(trajectory_path, data)
    print(trajectory_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize and append dataset trajectory.json incrementally.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a new trajectory.json for a session")
    init_parser.add_argument(
        "session_dir",
        nargs="?",
        help="session directory, e.g. dataset/open_wifi_20260514_101530",
    )
    init_parser.add_argument(
        "--task-slug",
        help="create dataset/{task_slug}_YYYYMMDD_HHMMSS automatically",
    )
    init_parser.add_argument(
        "--dataset-root",
        default="dataset",
        help="dataset root used together with --task-slug (default: dataset)",
    )
    init_parser.add_argument("--instruction", required=True, help="human task instruction")
    init_parser.add_argument("--app", required=True, help="target app package")
    init_parser.add_argument("--device-model", required=True, help="device model")
    init_parser.add_argument(
        "--resolution",
        required=True,
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="device resolution as width height",
    )
    init_parser.add_argument("--android", required=True, help="android version")
    init_parser.add_argument("--force", action="store_true", help="overwrite an existing trajectory.json")
    init_parser.set_defaults(func=cmd_init)

    append_parser = subparsers.add_parser("append", help="append one recorded step to trajectory.json")
    append_parser.add_argument("session_dir", help="session directory that already contains trajectory.json")
    append_parser.add_argument("--screenshot", required=True, help="step screenshot file name, e.g. step_001.png")
    append_parser.add_argument("--current-app", required=True, help="current package/activity string")
    append_parser.add_argument("--thought", required=True, help="observation and reasoning for this step")
    append_parser.add_argument("--action", required=True, help="JSON object describing the action")
    append_parser.add_argument(
        "--step-success",
        default=True,
        type=parse_bool,
        help="whether this recorded step executed successfully (default: true)",
    )
    append_parser.set_defaults(func=cmd_append)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
