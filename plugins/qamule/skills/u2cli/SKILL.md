---
name: u2cli
description: Control Android devices.
user-invocable: false
---

# u2cli

`uiautomator2` is a python package that allows you to control Android devices.
It also provides `u2cli` tool to interact with Android devices. Additionally, `u2cli` output contains equivalent Python code, which can be used in your own scripts.

## Usage

- Run `uv run u2cli <command> [args]`; Examples omit `uv run u2cli`.
- If multiple devices are connected at the same time, add `-s <serial>` for a specific device.

## Commands

### Device

- `dump-hierarchy`: Dump the UI hierarchy; Append `| grep <keyword>` to find needed information quickly.
- `screenshot <path>.jpg` use `jpg` to reduce file size and token usage, `app-current`, `device-info`, `window-size`.
- `shell <command> [--timeout <seconds>]`, e.g. `shell "pm list packages"`.

### Apps

- `app-start <package> [--activity <activity>] [--wait] [--stop]`.
- `app-list`, `app-stop <package>`, `app-clear <package>`.
- `app-install <apk>`, `app-uninstall <package>`.

### Input

- `press <key>`, `send-keys <text> [--no-clear]`, `clear-text`.
- `click <x> <y> | <selector>` and `long-click <x> <y> | <selector> [--duration <seconds>] [--timeout <seconds>]`.
- `double-click <x> <y> [--duration <seconds>]` supports coordinates only.
- `swipe <from-x> <from-y> <to-x> <to-y> [--duration <seconds>] [--steps <number>] [--scale <number>]`.
- `drag <start-x> <start-y> <end-x> <end-y> [--duration <seconds>]`.

**For coordinate actions, prefer normalized ratios from `0` to `1`, e.g. `click 0.5 0.5`.**

### Selectors

- `exists <selector> [--timeout <seconds>]`; `wait <selector> [--timeout <seconds>] [--gone]`.
- `scroll <selector> [--direction vert|horiz] [--action forward|backward|toEnd|toBeginning] [--max-swipes <number>] [--to-text <text>]`.
- Text: `--text`, `--text-contains`, `--text-matches`, `--text-starts-with`.
- Other: `--description`, `--description-contains`, `--resource-id`, `--class-name`, `--package`, `--instance`, `--index`.
- State: `--selected`, `--focused`, `--enabled`, `--scrollable`, `--clickable`, `--checked`, `--checkable`.
- Child: `--child KEY=VALUE [KEY=VALUE ...]` or `--child-text`, `--child-resource-id`, `--child-class-name`, `--child-clickable`, `--child-index`.

### System UI

- `open-notification`, `open-quick-settings`, `open-url <url>`.
