---
name: uiautomator2
description: >
  Android device automation via u2cli (uiautomator2-cli). Use this skill whenever the user wants to
  click/tap elements, swipe screens, start or stop apps, press hardware keys, type text,
  take screenshots, inspect UI hierarchy, or perform any of the listed actions on an Android device.
  Use when the user's request contains keywords related to: clicking, tapping, swiping, scrolling, pressing
  keys, starting/stopping apps, typing text, taking screenshots, finding elements, opening URLs, or checking
  element existence on an Android device.
  If the user requests an action not covered by the supported commands, respond with:
  "This action is not supported by uiautomator2-cli. Please refer to the supported commands."
---

# uiautomator2 Android Automation

You have access to `.venv/bin/u2cli`, a CLI for controlling Android devices via uiautomator2.

> **Read the full skill file before using any commands. This file has almost 200+ lines**

> **Device unavailable**: If no devices are detected, respond: "No devices detected. Please connect a device and ensure `adb devices` lists it before retrying."

## Setup (required first time)

```bash
# Via UV (recommended)
uv pip install uiautomator2-cli
# or
# pip install uiautomator2-cli
```

## Device targeting

Multiple devices → use `-s` or `ANDROID_SERIAL`:

```bash
.venv/bin/u2cli -s emulator-5554 click --text "OK"
```

Global flags: `--json` for JSON output.

## Procedure

1. **Discover** — run `screenshot` + `dump-hierarchy` to see current screen and element attributes
2. **Act** — pick the right command from the reference below
3. **Verify** — use `exists`, `wait`, or `screenshot` to confirm result

> **IMPORTANT**: Each `u2cli` command must be run separately. Do not combine commands in a single terminal line.

> For full details, see [commands reference](./references/commands.md).

> Every `u2cli` command prints equivalent Python code — copy it into a script for multi-step automation.

> Using `click-coord` when the target element has no selectable attributes. You must determine the element coordinates based on the actual resolution of the image.

### Quick element lookup

Use grep to filter `dump-hierarchy` output and locate element attributes fast:

```bash
.venv/bin/u2cli dump-hierarchy | grep -i "keyword"
```

The hierarchy output shows indented nodes with attributes like `text=`, `resource-id=`, `content-desc=`, `class=`. Grep for visible text or partial resource-id to find the right selector quickly.

## Command quick reference

| Goal | Commands | Example |
|------|----------|---------|
| Inspect UI | `dump-hierarchy`, `screenshot`, `current-app` | `.venv/bin/u2cli dump-hierarchy` |
| Click | `click`, `long-click`, `double-click`, `click-coord`, `xpath-click` | `.venv/bin/u2cli click --text "OK"` |
| Type | `send-keys`, `set-text`, `clear-text` | `.venv/bin/u2cli send-keys "hello"` |
| Swipe/Scroll | `swipe`, `swipe-ext`, `swipe-element`, `scroll` | `.venv/bin/u2cli swipe-ext up` |
| Keys | `press` | `.venv/bin/u2cli press back` |
| Apps | `app-start`, `app-stop`, `app-list`, `app-list-running`, `app-info`, `app-clear`, `app-install`, `app-uninstall`, `app-wait` | `.venv/bin/u2cli app-start com.android.settings --wait --stop` |
| Wait/Check | `wait`, `exists`, `xpath-exists` | `.venv/bin/u2cli wait --text "Done" --timeout 10` |
| Read | `get-text`, `xpath-get-text`, `element-info`, `device-info`, `window-size`, `ui-info` | `.venv/bin/u2cli get-text --resource-id "com.app:id/label"` |
| Screen | `screen-on`, `screen-off`, `orientation`, `screenshot` | `.venv/bin/u2cli screenshot /tmp/s.png` |
| Other | `open-url`, `open-notification`, `open-quick-settings`, `shell` | `.venv/bin/u2cli open-url "https://example.com"` |

## Element selectors

Most commands that target UI elements accept these options (combinable):

| Option | Matches |
|--------|-------------------------------|
| `--text TEXT` | Exact text |
| `--text-contains TEXT` | Substring |
| `--text-matches TEXT` | Regex |
| `--text-starts-with TEXT` | Prefix |
| `--resource-id ID` | Resource ID (e.g. `com.pkg:id/btn`) |
| `--class-name CLASS` | Widget class (e.g. `android.widget.Button`) |
| `--description TEXT` | Content description (exact) |
| `--description-contains TEXT` | Content description substring |
| `--package TEXT` | Package name |
| `--index N` | Sibling index |
| `--instance N` | Nth match (0-based) when multiple elements match |
| `--clickable`, `--scrollable`, `--enabled`, `--focused`, `--checked`, `--selected`, `--checkable` | Boolean state flags |
