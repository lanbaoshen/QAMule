# u2cli Complete Command Reference

## Click elements

```bash
# Click by text (exact match)
.venv/bin/u2cli click --text "Settings"

# Click by text containing a substring
.venv/bin/u2cli click --text-contains "Submit"

# Click by resource-id
.venv/bin/u2cli click --resource-id "com.android.settings:id/search"

# Click by content description (accessibility label)
.venv/bin/u2cli click --description "Navigate up"

# Click with timeout (wait for element before clicking)
.venv/bin/u2cli click --text "OK" --timeout 10

# Long-click an element (with custom duration)
.venv/bin/u2cli long-click --text "Item" --duration 2.0

# Click by XPath
.venv/bin/u2cli xpath-click "//android.widget.Button[@text='OK']"

# Click at absolute coordinates (pixels) or relative (0.0–1.0)
.venv/bin/u2cli click-coord 540 960
.venv/bin/u2cli click-coord 0.5 0.5

# Double-click at coordinates
.venv/bin/u2cli double-click 540 960 --duration 0.1
```

## Type and edit text

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

## Swipe and scroll

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

# Swipe on a specific element
.venv/bin/u2cli swipe-element --direction up --resource-id "com.app:id/card"
.venv/bin/u2cli swipe-element --direction left --text "Dismiss" --steps 20

# Scroll a scrollable element
.venv/bin/u2cli scroll --scrollable --action forward
.venv/bin/u2cli scroll --resource-id "com.app:id/list" --action toEnd
.venv/bin/u2cli scroll --scrollable --to-text "Item 50"  # scroll until text is visible
.venv/bin/u2cli scroll --scrollable --action backward --direction horiz
```

## Press hardware/soft keys

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

## App management

```bash
# Start an app by package name
.venv/bin/u2cli app-start com.android.settings
.venv/bin/u2cli app-start com.example.myapp --activity .MainActivity
.venv/bin/u2cli app-start com.example.myapp --wait --stop  # stop first, then start and wait

# Wait for app to be running / in foreground
.venv/bin/u2cli app-wait com.example.myapp --timeout 15
.venv/bin/u2cli app-wait com.example.myapp --front  # wait for foreground

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

## Wait for elements

```bash
# Wait for an element to appear (default timeout 20s)
.venv/bin/u2cli wait --text "Welcome" --timeout 10

# Wait for an element to disappear
.venv/bin/u2cli wait --text "Loading..." --gone --timeout 30

# Check if an element exists right now (no waiting)
.venv/bin/u2cli exists --resource-id "com.app:id/button"
.venv/bin/u2cli xpath-exists "//android.widget.TextView[@text='Done']"
```

## Get information from elements

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

## Screen control

```bash
.venv/bin/u2cli screen-on
.venv/bin/u2cli screen-off
.venv/bin/u2cli screenshot /tmp/output.png
.venv/bin/u2cli orientation             # get orientation
.venv/bin/u2cli orientation portrait    # set orientation
.venv/bin/u2cli open-notification       # pull down notification shade
.venv/bin/u2cli open-quick-settings     # pull down quick settings
.venv/bin/u2cli open-url "https://example.com"  # open URL via intent
```

## Dump hierarchy options

```bash
.venv/bin/u2cli dump-hierarchy                    # simplified tree (default)
.venv/bin/u2cli dump-hierarchy --raw              # raw XML from uiautomator2
.venv/bin/u2cli dump-hierarchy --max-depth 3      # limit depth
.venv/bin/u2cli dump-hierarchy --compressed       # use compressed hierarchy
.venv/bin/u2cli dump-hierarchy -o /tmp/tree.txt   # save to file
```

## Shell commands

```bash
# Run any adb shell command
.venv/bin/u2cli shell "pm list packages -3"
.venv/bin/u2cli shell "dumpsys window displays"
.venv/bin/u2cli shell "input keyevent 4"
```
