# AGENTS.md

This project is a fully autonomous android test automation harness base on `uiautomator2` (control Android devices) and `pytest` (python test framework) without human intervention.

Comment and docstring style should follow Google Python Style Guide.

## Design Philosophy

> **Explore once, solidify into a script, only intervene when it breaks.**

Having AI operate the device in real time on every test run is slow and expensive. Instead:

1. **Explore** — AI explores the app live on device once to discover UI and flows.
2. **Solidify** — The exploration is converted into a pytest script that runs without AI involvement.
3. **Remember** — `kb/` records what was discovered so future tasks never re-explore the same ground.
4. **Repair** — When a script fails, AI re-inspects the device, fixes the script, and updates `kb/`.

`kb/` is the AI's memory. `tests/` is the solidified output. Together they keep execution fast and AI intervention minimal.

Only read when the task involves the app under test (writing/fixing tests, exploring UI, automating flows):
1. `kb/app/_overview.md` — package name, entry point, global conventions
2. `kb/app/_index.md` — known screens, flows, inline actions, helper functions

See `kb/index.md` for loading rules and directory structure.

### Finding test cases

`tests/README.md` is the index of all test cases. Check it first before searching the filesystem. Test files follow the naming convention `tests/test_{feature}.py`.
