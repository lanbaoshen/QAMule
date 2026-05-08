---
name: kb
description: 'Manage the QA knowledge base (kb/). Use when needing to read app screens, flows, selectors before testing; or when persisting newly discovered screens, selectors, flows, quirks, or dependencies after device interactions.'
---

# Knowledge Base Management

Persistent KB at `kb/`. Accelerates future QA by caching screens, flows, selectors, and quirks.

If `kb/` is not existent, you need to create the structure first. Follow the template below to create the necessary files and directories.

## Structure

```
kb/
  app/
    _app.md          # Entry point: screen & flow index, reset steps, quirks
    deps.md          # Dependent apps table (package → scenarios → KB path)
    screens/         # One file per screen
    flows/           # One file per business flow
  deps/
    {package}/       # Dependency app knowledge
```

### _app.md
- Package name, Screen Index (table: screen → file → entry point), Flow Index (table: flow → file → screens involved), Reset to Initial State (table: method → steps → initial state indicator), Known Issues & Quirks

### screens/*.md
- How to reach, Key indicators (confirm on-screen), Elements table (element → selector type → value → notes)

### flows/*.md
- Preconditions, Screens involved, Numbered steps (action → selector), Expected result, Error handling table (scenario → symptom → recovery)

### deps.md
- Table: app/component → package → scenarios → KB path

## Read

1. Read `kb/app/_app.md` → load only the screen/flow files relevant to the current task.
2. For cross-app dialogs, check `kb/app/deps.md` → load from `kb/deps/{package}/`.

## Write

Update KB only when you discover something new (screen, selector, flow, quirk, or dependency). Skip otherwise.

**Before writing, classify ownership:** check `current-app` (or the foreground package) against the main app package in `kb/app/_app.md`. If the screen belongs to a different package, it is a **dependency** — write to `kb/deps/{package}/`, NOT `kb/app/screens/`.

- New screen (main app) → `kb/app/screens/{name}.md`
- New screen (other app) → `kb/deps/{package}/{name}.md`
- New flow → `kb/app/flows/{name}.md`
- New dependency → `kb/deps/{package}/`
- Quirk → append to `kb/app/_app.md` under "Known Issues & Quirks"

After writing, keep `kb/app/_app.md` index tables and `kb/app/deps.md` in sync.

## Conventions

- File names: lowercase, underscores (e.g. `app_tab.md`)
