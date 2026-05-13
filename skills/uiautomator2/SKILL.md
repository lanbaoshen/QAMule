---
name: uiautomator2
description: >
  Android device automation via u2cli (uiautomator2-cli). Use this skill whenever the user wants to
  click/tap elements, swipe screens, start or stop apps, press hardware keys, type text,
  take screenshots, inspect UI hierarchy, or perform any actions on an Android device.
---

# uiautomator2 Device Operations

Use this skill as the execution layer for Android UI.
You have access to `.venv/bin/u2cli`, a CLI for controlling Android devices via the uiautomator2.

## Target Device Selection

If target device is not specified, it defaults to the only connected adb device.
If multiple devices are connected, specify target device with `-s {device_id}` for all commands, example:

```bash
# Default to single connected device
.venv/bin/u2cli device-info

# Target specific device by ID
.venv/bin/u2cli -s emulator-5554 device-info
```

## Core Features

### Inspect UI

- `dump-hierarchy`: Dump current UI hierarchy in XML format for analysis and element selection. The output is compressed by u2cli before returning. You can combine this command with `grep` command to find specific elements, like `.venv/bin/u2cli dump-hierarchy | grep -i "keyword"`.
- `screenshot`: Capture current screen and save to a local file. The output is the file path and size of the screenshot. Example: `.venv/bin/u2cli screenshot /tmp/screenshot.png`.
- `current-app`: Get the current foreground app's package name, activity and pid.

### Click & Swipe & Wait & Exists

- `click`: Click on a specific UI element. Example:

```bash
# Click a element with exact text "Submit"
.venv/bin/u2cli click --text "Submit"

# Click a element match multiple conditions
.venv/bin/u2cli click --class-name "android.widget.Button" --text-contains "Submit" --enabled
```

- `long-click`: Long click on a specific UI element, with the same selector options as `click`.
- `double-click`: Double click on a specific UI element, with the same selector options as `click`.
- `click-coords`: Click on specific screen coordinates. Example:

```bash
# Click by absolute coordinates
.venv/bin/u2cli click-coords 100 200
# Click by relative coordinates (percentage of screen size)
.venv/bin/u2cli click-coords 0.5 0.5
```

- `xpath-click`: Click on a UI element specified by an XPath expression. Example: `.venv/bin/u2cli xpath-click "//android.widget.TextView[@text='Submit']"`.
- `swipe`: Swipe from one point to another. Example:

```bash
# Swipe by absolute coordinates
.venv/bin/u2cli swipe 100 200 300 400
# Swipe by relative coordinates (percentage of screen size)
.venv/bin/u2cli swipe 0.5 0.5 0.8 0.8
```

- `swipe-ext`: Finger swipe with direction (Opposite to the screen orientation) Example:

```bash
# Swipe screen up
.venv/bin/u2cli swipe-ext down
# Swipe screen right
.venv/bin/u2cli swipe-ext left
```

- `scroll`: Do not use `scroll` command, it may cause unexpected behavior or loop. Instead, use `swipe` or `swipe-ext` to perform scroll actions.

- `wait`: Wait for a specific UI element to appear within a timeout. Example: `.venv/bin/u2cli wait --text "Loading..." --timeout 10`.
- `exists`: Check if a specific UI element exists. Example: `.venv/bin/u2cli exists --text "Submit"`.
- `xpath-exists`: Check if a UI element specified by an XPath expression exists. Example: `.venv/bin/u2cli xpath-exists "//android.widget.TextView[@text='Submit']"`.

#### Element selector

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


### Type Text

- `send-keys`: Clear and send text to an input box. Example: `.venv/bin/u2cli send-keys "Hello World"`.
- `clear-text`: Clear text from an input box.

### Press Keys

- `press-key`: Simulate pressing a hardware key, such as "home", "back", "volume-up", etc. Example: `.venv/bin/u2cli press-key home`.

### Apps

- `app-start`: Start an app by its package name or with specific activity, support `--wait` and `--stop` options. Example:

```bash
# Package only
.venv/bin/u2cli app-start com.example.app --wait

# With activity
.venv/bin/u2cli app-start com.example.app --activity .MainActivity --wait --stop
```

- `app-stop`: Stop an app by its package name. Example: `.venv/bin/u2cli app-stop com.example.app`.
- `app-list`: List all installed apps with package names.
- `app-install`: Install an APK file to the device. Example: `.venv/bin/u2cli app-install /path/to/app.apk`.
- `app-uninstall`: Uninstall an app by its package name. Example: `.venv/bin/u2cli app-uninstall com.example.app`.
- `app-clear`: Clear app data by its package name. Example: `.venv/bin/u2cli app-clear com.example.app`.

### Other

- `shell`: Execute a shell command on the device. Example: `.venv/bin/u2cli shell "ls /sdcard"`.
- `open-notification`: Open the notification shade.
- `open-quick-settings`: Open the quick settings panel.
- `open-url`: Open a URL in the default browser. Example: `.venv/bin/u2cli open-url "https://www.example.com"`.

## Full Command Reference

If you need to use other u2cli commands or options not covered above, refer to the official u2cli documentation for the full command [reference](./references/commands.md)
