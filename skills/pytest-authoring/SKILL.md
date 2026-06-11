---
name: pytest-authoring
description: "Define how pytest tests should be authored for QAMule, including testcase boundaries, marker usage, fixture scope, parametrization, and execution-time optimization. Use when writing or modifying pytest tests, fixtures, or conftest files. Trigger keywords: write pytest case, add test, fixture, conftest, marker, parametrize, optimize test time."
user-invocable: false
---

# Pytest Authoring

Authoring conventions for pytest-based QAMule tests.

## Scope

- Use this skill for how tests are written.
- Keep run commands, pause workflow, and live inspection procedures in the pytest skill.

## Test Boundaries

- Each test should verify one behavior or one tightly scoped failure mode.
- Prefer small, composable tests over long scripts with many unrelated assertions.
- Name tests by observable behavior, not internal implementation.
- Keep business intent in the test body; move reusable mechanics into fixtures or helpers.

## UI Test Layering

- For UI automation, separate three responsibilities: test entry, scenario logic, and reusable mechanics.
- The entry layer owns collection, markers, and light wiring only.
- The scenario layer owns user-facing behavior, assertions, and checkpoints.
- The mechanics layer owns reusable device actions, waits, parsing, and low-level helpers.
- Directory names may vary by repo, but do not mix all three responsibilities back into one large file.

## Markers

- Use markers to express suite intent and execution cost.
- Add at least one stable suite or feature marker, such as `smoke`, `regression`, `settings`, or `multi_device`.
- Add an environment or cost marker when needed, such as `slow`, `serial`, or `requires_login`.
- Reuse existing marker vocabulary instead of creating near-duplicates.
- Only introduce a new marker when it improves selection or scheduling in a durable way.

## Fixtures And State

- Use fixtures to share setup, not to hide the behavior under test.
- Keep fixtures deterministic and explicit about side effects.
- Default to the narrowest useful scope.
- Use `function` scope for stateful UI setup unless a wider scope is clearly safe.
- Only widen scope to `module` or `session` when the saved cost is material and state leakage is controlled.
- Return ready-to-use objects from fixtures.
- Do not put core business assertions inside fixtures unless they validate setup prerequisites.
- Avoid repeated login, app launch, or navigation when they can be safely shared.
- Extract stable prerequisite setup into broader-scope fixtures only after confirming that tests stay isolated.
- Prefer lightweight state reset over full environment rebuild when the resulting state is equivalent.
- Do not optimize by sharing mutable state across unrelated tests.

## Parametrization

- Use `@pytest.mark.parametrize` for the same behavior under multiple inputs, states, or device shapes.
- Add `ids=` when parameter names are not obvious from the values.
- Do not parametrize unrelated behaviors into one test.

## Assertions

- Assert user-visible or externally observable outcomes.
- Prefer a few strong assertions over many weak ones.
- Do not use live checkpoints for conditions that selectors, text checks, or state polling can verify directly.

## Review Checklist

- The test name states the behavior being verified.
- Entry, scenario, and mechanics responsibilities are separated cleanly.
- Markers make suite selection and execution cost clear.
- Fixture scope is no broader than necessary.
- Repeated setup is extracted only when reuse does not leak state.
- Parametrization is used for data variation, not to merge different scenarios.
