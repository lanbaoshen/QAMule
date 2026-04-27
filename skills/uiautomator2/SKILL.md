---
name: uiautomator2
description: >
  Android device automation via u2cli (uiautomator2-cli). Use this skill whenever the user wants to control
  an Android device, automate UI interactions, run Android tests, click/tap elements, swipe screens, start
  or stop apps, press hardware keys, type text, take screenshots, inspect UI hierarchy, or automate any
  Android device action. Trigger on any request like "click the Settings button", "swipe up on the screen",
  "start the app", "press back", "find element", "automate Android", or any multi-step device automation
  workflow. Always use this skill for Android automation tasks — even if the request doesn't say "u2cli"
  explicitly.
---

# uiautomator2 Android Automation

You have access to `u2cli`, a command-line tool for controlling Android devices via uiautomator2.

## Setup (required first time)

You need to install `uiautomator2-cli` in your Python environment (virtual environment is recommended):

```bash
# python -m venv .venv
pip install uiautomator2-cli
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
# uv venv
uv pip install uiautomator2-cli
```

## Device targeting

If multiple devices are connected, specify the target with `-s` (or set `ANDROID_SERIAL`):

```bash
.venv/bin/u2cli -s emulator-5554 click --text "OK"
export ANDROID_SERIAL=emulator-5554
```

## Core commands

### Discover the UI

Before automating, inspect what's on screen:

```bash
# Dump the UI hierarchy as a readable tree
.venv/bin/u2cli dump-hierarchy

# Take a screenshot to see the current screen
.venv/bin/u2cli screenshot /tmp/screen.png

# Show the foreground app
.venv/bin/u2cli current-app
```

### Click elements

```bash
# Click by text (exact match)
.venv/bin/u2cli click --text "Settings"

# Click by text containing a substring
.venv/bin/u2cli click --text-contains "Submit"

# Click by resource-id
.venv/bin/u2cli click --resource-id "com.android.settings:id/search"

# Click by content description (accessibility label)
.venv/bin/u2cli click --description "Navigate up"

# Click by XPath
.venv/bin/u2cli xpath-click "//android.widget.Button[@text='OK']"

# Click at absolute coordinates (pixels)
.venv/bin/u2cli click-coord 540 960

# Click at relative coordinates (0.0–1.0 fraction of screen size)
.venv/bin/u2cli click-coord 0.5 0.5
```

### Type and edit text

```bash
# Type into the focused field (clears first by default)
.venv/bin/u2cli send-keys "Hello World"

# Type without clearing
.venv/bin/u2cli send-keys --no-clear " extra"

# Set text directly on a specific element
.venv/bin/u2cli set-text "new value" --resource-id "com.app:id/input"

# Clear text from an element
.venv/bin/u2cli clear-text --resource-id "com.app:id/input"
```

### Swipe and scroll

```bash
# Swipe from one point to another (pixel coords or 0-1 relative)
.venv/bin/u2cli swipe 0.5 0.8 0.5 0.2          # swipe up (scroll down)
.venv/bin/u2cli swipe 0.5 0.2 0.5 0.8          # swipe down (scroll up)
.venv/bin/u2cli swipe 200 800 200 200 --duration 0.5

# High-level directional swipe across the screen
.venv/bin/u2cli swipe-ext up                    # scroll down the page
.venv/bin/u2cli swipe-ext down                  # scroll up the page
.venv/bin/u2cli swipe-ext left --scale 0.8      # swipe left 80% of screen width
.venv/bin/u2cli swipe-ext right

# Scroll a specific scrollable element
.venv/bin/u2cli scroll --scrollable --action forward
.venv/bin/u2cli scroll --resource-id "com.app:id/list" --action toEnd
.venv/bin/u2cli scroll --scrollable --to-text "Item 50"  # scroll until text is visible
```

### Press hardware/soft keys

```bash
# Named keys: home, back, menu, enter, delete, recent,
#             volume_up, volume_down, power, camera, search, space
.venv/bin/u2cli press back
.venv/bin/u2cli press home
.venv/bin/u2cli press enter
.venv/bin/u2cli press volume_up

# By keycode integer
.venv/bin/u2cli press 3    # HOME keycode
```

### App management

```bash
# Start an app by package name
.venv/bin/u2cli app-start com.android.settings
.venv/bin/u2cli app-start com.example.myapp --activity .MainActivity
.venv/bin/u2cli app-start com.example.myapp --wait --stop  # stop first, then start and wait

# Stop an app
.venv/bin/u2cli app-stop com.example.myapp

# List installed / running apps
.venv/bin/u2cli app-list
.venv/bin/u2cli app-list-running

# Get app version info
.venv/bin/u2cli app-info com.android.settings

# Clear app data (like "Clear Data" in settings)
.venv/bin/u2cli app-clear com.example.myapp

# Install / uninstall
.venv/bin/u2cli app-install /path/to/app.apk
.venv/bin/u2cli app-uninstall com.example.myapp
```

### Wait for elements

```bash
# Wait for an element to appear (default timeout 20s)
.venv/bin/u2cli wait --text "Welcome" --timeout 10

# Wait for an element to disappear
.venv/bin/u2cli wait --text "Loading..." --gone --timeout 30

# Check if an element exists right now (no waiting)
.venv/bin/u2cli exists --resource-id "com.app:id/button"
.venv/bin/u2cli xpath-exists "//android.widget.TextView[@text='Done']"
```

### Get information from elements

```bash
# Get text content of an element
.venv/bin/u2cli get-text --resource-id "com.app:id/label"
.venv/bin/u2cli xpath-get-text "//android.widget.TextView[@content-desc='status']"

# Get full element details (bounds, class, enabled, etc.)
.venv/bin/u2cli element-info --text "OK"

# Get device info
.venv/bin/u2cli device-info
.venv/bin/u2cli window-size
.venv/bin/u2cli ui-info
```

### Screen control

```bash
.venv/bin/u2cli screen-on
.venv/bin/u2cli screen-off
.venv/bin/u2cli screenshot /tmp/output.png
.venv/bin/u2cli orientation             # get orientation
.venv/bin/u2cli orientation portrait    # set orientation
```

### Shell commands

```bash
# Run any adb shell command
.venv/bin/u2cli shell "pm list packages -3"
.venv/bin/u2cli shell "dumpsys window displays"
.venv/bin/u2cli shell "input keyevent 4"
```

## Selector reference

Most element-targeting commands accept the same set of selectors. You can combine them:

| Option | Matches when... |
|--------|----------------|
| `--text TEXT` | element text equals TEXT exactly |
| `--text-contains TEXT` | element text contains substring |
| `--text-matches REGEX` | element text matches regex |
| `--text-starts-with TEXT` | element text starts with prefix |
| `--resource-id ID` | resource-id equals ID (e.g. `com.pkg:id/btn`) |
| `--class-name CLASS` | UI class name (e.g. `android.widget.Button`) |
| `--description TEXT` | content-description equals TEXT |
| `--description-contains TEXT` | content-description contains substring |
| `--index N` | sibling index |
| `--instance N` | global instance (0-based, if multiple matches) |
| `--clickable` / `--scrollable` / `--enabled` / `--focused` / `--checked` | boolean state flags |

## Scripting tip

Every `u2cli` command prints the equivalent Python code alongside its result — copy that code directly into a script if you need to string multiple steps together.

## Common workflows

### Open Settings → Wi-Fi and toggle

```bash
.venv/bin/u2cli app-start com.android.settings
.venv/bin/u2cli wait --text "Network & internet" --timeout 5
.venv/bin/u2cli click --text "Network & internet"
.venv/bin/u2cli click --text "Internet"
```

### Type in a search box

```bash
.venv/bin/u2cli click --resource-id "com.android.settings:id/search"
.venv/bin/u2cli send-keys "Bluetooth"
```

### Scroll a list to find an item, then click it

```bash
.venv/bin/u2cli scroll --scrollable --to-text "Developer options"
.venv/bin/u2cli click --text "Developer options"
```

### Multi-step app login

```bash
.venv/bin/u2cli app-start com.example.myapp --wait
.venv/bin/u2cli wait --text "Log in" --timeout 10
.venv/bin/u2cli click --resource-id "com.example.myapp:id/username"
.venv/bin/u2cli send-keys "user@example.com"
.venv/bin/u2cli click --resource-id "com.example.myapp:id/password"
.venv/bin/u2cli send-keys "mypassword"
.venv/bin/u2cli click --text "Log in"
.venv/bin/u2cli wait --text "Home" --timeout 15
```

### Take a screenshot after each step for debugging

```bash
.venv/bin/u2cli screenshot /tmp/step1_before_click.png
.venv/bin/u2cli click --text "Submit"
.venv/bin/u2cli screenshot /tmp/step2_after_click.png
```
