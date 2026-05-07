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
| Apps | `app-start`, `app-stop`, `app-list`, `app-list-running`, `app-info`, `app-clear`, `app-install`, `app-uninstall`, `app-wait` | `.venv/bin/u2cli app-start com.android.settings` |
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

## Key command details

For full details, see [commands reference](./references/commands.md). Highlights:

- **`click`** / **`long-click`**: accepts `--timeout` for waiting before click; `long-click` has `--duration`
- **`click-coord X Y`**: pixel coords or **0.0–1.0** relative; **`double-click X Y`** has `--duration` (delay between taps)
- **`send-keys TEXT`**: types into focused field, clears first; use `--no-clear` to append
- **`set-text TEXT`**: sets text on a specific element (uses selectors)
- **`swipe FX FY TX TY`**: coords can be **0-1** relative or pixels; `--duration` or `--steps`
- **`swipe-ext {left|right|up|down}`**: `--scale` controls distance (fraction of screen). **Direction = finger movement**, which is opposite to content movement: `up` scrolls content DOWN (see more below); `down` scrolls content UP (go back to top); `left` scrolls content RIGHT (next page/tab); `right` scrolls content LEFT (previous page/tab). To scroll down a list and reveal more items, use `swipe-ext up`. To go to the next page, use `swipe-ext left`.
- **`swipe-element`**: swipe on a specific element; `--direction` required, `--steps`
- **`wait`**: `--timeout`, `--gone` (wait for disappearance)
- **`app-start PACKAGE`**: `--activity`, `--wait`, `--stop`
- **`app-wait PACKAGE`**: `--timeout`, `--front` (wait for foreground)
- **`dump-hierarchy`**: Get current UI tree;
- **`press KEY`**: named keys: `home`, `back`, `menu`, `enter`, `delete`, `recent`, `volume_up`, `volume_down`, `power`, `camera`, `search`, `space`; or integer keycode

## Scripting tip

Every `u2cli` command prints equivalent Python code — copy it into a script for multi-step automation.
