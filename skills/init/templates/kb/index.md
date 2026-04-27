# KB Index

## Loading rules

| When | Read |
|------|------|
| App-related task | `kb/app/_overview.md` + `kb/app/_index.md` (required) |
| Operating a specific screen | `kb/app/screens/{screen}.md` |
| Executing a cross-screen flow | `kb/app/flows/{flow}.md` |
| Task needs system/auxiliary ops | `kb/helpers/_index.md` |
| Specific auxiliary flow needed | `kb/helpers/{file}.md` |

## Key principles

- **Code over kb**: write reusable operations as Python functions; kb only records where they live and documents flows code cannot fully capture.
- **Pitfalls belong to their owner**: screen quirks → `screens/{screen}.md`, flow timing → `flows/{flow}.md`, global rules → `_overview.md`.
- **`_index.md` is the single source of truth**: always update it after discovering a new screen, flow, or helper function.

## Directory structure

```
kb/
  index.md                    ← this file
  app/
    _overview.md              ← always read: package name, entry point, global conventions
    _index.md                 ← always read: all known screens, flows, inline actions, helper functions
    screens/
      {screen}.md             ← on demand: element selectors + navigation path + screen pitfalls
    flows/
      {flow}.md               ← on demand: cross-screen steps + timing issues
  helpers/
    _index.md                 ← on demand: Python helper functions + documented auxiliary flows
    settings.md               ← on demand: complex system setting operations
    system.md                 ← on demand: ROM-variant dialogs, edge-case system interactions
```

## Update policy

| Scenario | Action |
|----------|--------|
| New screen discovered | Create `screens/{name}.md`, add row to `app/_index.md` |
| New cross-screen flow discovered | Create `flows/{flow}.md`, add row to `app/_index.md` |
| Re-explored an existing screen | Overwrite `screens/{name}.md` |
| Better path found for a flow | Overwrite `flows/{flow}.md` |
| New Python helper written | Add row to `helpers/_index.md` |
| New auxiliary flow documented | Create `helpers/{file}.md`, add row to `helpers/_index.md` |
| New bug / edge case found | Add to the owning `screens/{name}.md` or `flows/{flow}.md` pitfalls section |
