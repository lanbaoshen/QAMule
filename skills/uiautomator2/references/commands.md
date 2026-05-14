# u2cli Commands Reference

This reference captures the full command surface of `uv run u2cli` for this repository.

## Global Usage

```bash
uv run u2cli [OPTIONS] COMMAND [ARGS]...
```

Global options:
- `-s, --serial TEXT`: target device serial (or use `ANDROID_SERIAL`)
- `--help`: show help

## Complete Command List

### App Lifecycle

| Command | Description |
| --- | --- |
| `app-start` | Start (launch) an Android app by package name. |
| `app-wait` | Wait until an app is running (or in foreground with `--front`). |
| `app-stop` | Force-stop an app (or all third-party apps with `--all`). |
| `app-list` | List installed packages. |
| `app-list-running` | List currently running packages. |
| `app-info` | Get app version info (`versionName`, `versionCode`). |
| `app-clear` | Clear app data (`pm clear <package>`). |
| `app-install` | Install an APK from a local path or URL. |
| `app-uninstall` | Uninstall an app by package name. |

### UI Element Actions

| Command | Description |
| --- | --- |
| `click` | Click on a UI element matching selector options. |
| `long-click` | Long-click on a UI element. |
| `click-coord` | Click at absolute or relative (`0-1`) coordinates. |
| `long-click-coord` | Long-click at absolute or relative (`0-1`) coordinates. |
| `double-click` | Double-click at coordinates. |
| `swipe` | Swipe from `(FX, FY)` to `(TX, TY)`. |
| `swipe-ext` | High-level directional swipe across the screen. |
| `swipe-element` | Swipe on a matched UI element in a direction. |
| `wait` | Wait for an element to appear (or disappear with `--gone`). |
| `exists` | Check whether a UI element exists. |

### Text Operations

| Command | Description |
| --- | --- |
| `send-keys` | Type text into the currently focused input field. |
| `set-text` | Set text on a matched UI element (clears first). |
| `clear-text` | Clear text from a matched UI element. |
| `get-text` | Get text from a matched UI element. |

### XPath Operations

| Command | Description |
| --- | --- |
| `xpath-click` | Click an element found by XPath. |
| `xpath-exists` | Check whether an XPath element exists. |
| `xpath-get-text` | Get text from an XPath element. |
| `xpath-set-text` | Set text on an XPath element. |

### Device, UI, and System

| Command | Description |
| --- | --- |
| `current-app` | Show the current foreground app (package/activity/pid). |
| `device-info` | Show device information. |
| `ui-info` | Show UiAutomator device info (size, orientation, package). |
| `window-size` | Get screen window size (`width`, `height`). |
| `orientation` | Get or set screen orientation. |
| `element-info` | Get detailed info for a matched UI element. |
| `dump-hierarchy` | Dump current UI hierarchy (simplified tree by default). |
| `screenshot` | Take a screenshot and save to a file. |
| `open-notification` | Pull down notification shade. |
| `open-quick-settings` | Pull down quick settings panel. |
| `open-url` | Open URL in the default browser via intent. |
| `press` | Press hardware/soft key by name or keycode. |
| `shell` | Run a shell command on device. |
| `screen-on` | Turn screen on (wake). |
| `screen-off` | Turn screen off (sleep). |

### Runtime and Daemon

| Command | Description |
| --- | --- |
| `repl` | Run interactive u2cli commands without repeated process startup. |
| `daemon` | Manage the background daemon process. |

`daemon` subcommands:
- `daemon start`: start daemon for current serial
- `daemon status`: show daemon status
- `daemon logs`: show daemon log tail
- `daemon stop`: stop daemon

## Common Selector Options

These options are shared by many element-based commands (such as `click`, `exists`, `wait`, `set-text`, `clear-text`, `get-text`, `element-info`, `scroll`, `swipe-element`):

| Option | Meaning |
| --- | --- |
| `--text` | Exact text match |
| `--text-contains` | Text contains substring |
| `--text-matches` | Text matches regex |
| `--text-starts-with` | Text starts with prefix |
| `--resource-id` | Resource ID (example: `com.pkg:id/btn`) |
| `--class-name` | UI class name |
| `--description` | Content description exact match |
| `--description-contains` | Content description contains substring |
| `--package` | Package name |
| `--index` | Sibling index |
| `--instance` | Global instance index (0-based) |
| `--checkable` | Element is checkable |
| `--checked` | Element is checked |
| `--clickable` | Element is clickable |
| `--scrollable` | Element is scrollable |
| `--enabled` | Element is enabled |
| `--focused` | Element is focused |
| `--selected` | Element is selected |

## Flat List (Alphabetical)

```text
app-clear
app-info
app-install
app-list
app-list-running
app-start
app-stop
app-uninstall
app-wait
clear-text
click
click-coord
current-app
daemon
device-info
double-click
dump-hierarchy
element-info
exists
get-text
long-click
long-click-coord
open-notification
open-quick-settings
open-url
orientation
press
repl
screen-off
screen-on
screenshot
send-keys
set-text
shell
swipe
swipe-element
swipe-ext
ui-info
wait
window-size
xpath-click
xpath-exists
xpath-get-text
xpath-set-text
```
