---
name: pytest-authoring
description: "Define how pytest-based UI automation tests should be authored, including test boundaries, layering, marker usage, fixture scope, parametrization, and execution-time stability. Use when writing or modifying pytest UI tests, fixtures, helpers, or conftest files. Trigger keywords: write pytest case, add UI test, fixture, conftest, marker, parametrize, flaky test."
user-invocable: false
---

# Pytest Authoring

Authoring conventions for pytest-based UI automation tests.

## Test Boundaries

- Each test should verify one behavior or one tightly scoped failure mode.
- Prefer small, composable tests over long scripts with many unrelated assertions.
- Name tests by observable behavior, not internal implementation.
- Keep business intent in the test body; move reusable mechanics into fixtures or helpers.

## Behavior Scope And Preconditions

- A test may include prerequisite steps required to reach the target state.
- The test name, core assertions, and review scope should remain centered on the behavior under test.
- Do not treat every UI interaction as a separate test if those interactions together verify one user-visible behavior.
- If a later step introduces a new independent success criterion or failure mode, split it into a separate test.

## UI Test Layering

- For UI automation, separate three responsibilities: test entry, scenario logic, and reusable mechanics.
- The entry layer owns collection, markers, and light wiring only.
- The scenario layer owns user-facing behavior, assertions, and deliberate validation steps.
- The mechanics layer owns reusable device actions, waits, parsing, and low-level helpers.
- A scenario may include a short flow when that flow is required to verify one behavior cleanly.
- Directory names may vary by repo, but do not mix all three responsibilities back into one large file.

## Markers

- Use markers to express suite intent and execution cost.
- Add at least one stable suite or feature marker.
- Add environment, dependency, or cost markers when needed.
- Reuse existing marker vocabulary instead of creating near-duplicates.
- Only introduce a new marker when it improves selection or scheduling in a durable way.

## Fixtures And State

- Use fixtures to share setup, not to hide the behavior under test.
- Keep fixtures deterministic and explicit about side effects.
- Default to the narrowest useful scope.
- Use `function` scope for stateful UI setup unless a wider scope is clearly safe.
- Only widen scope to `module` or `session` when the saved cost is material and state leakage is controlled.
- Return ready-to-use objects or stable prepared state from fixtures.
- Do not put core business assertions inside fixtures unless they validate setup prerequisites.
- Fixtures may prepare prerequisite state, but should not perform the test's core business validation.
- Avoid repeated expensive setup or state preparation when it can be safely shared.
- Extract stable prerequisite setup into broader-scope fixtures only after confirming that tests stay isolated.
- Prefer lightweight state reset over full environment rebuild when the resulting state is equivalent.
- Do not optimize by sharing mutable state across unrelated tests.

## Wait And Synchronization

- Do not use fixed sleep in entry or scenario code unless a short bounded backoff is required and justified.
- Before click or input, wait for actionable state (exists, visible, enabled, focused when relevant).
- After each state-changing action, wait for a postcondition that proves the action took effect.
- Use bounded polling with explicit timeout and interval; do not use unbounded loops.
- Keep timeout values explicit and consistent within a suite.

## Parametrization

- Use `@pytest.mark.parametrize` for the same behavior under multiple inputs, states, or device shapes.
- Add `ids=` when parameter names are not obvious from the values.
- Do not parametrize unrelated behaviors into one test.

## Assertions

- Assert user-visible or externally observable outcomes.
- Prefer a few strong assertions over many weak ones.
- For stateful flows, assert the relevant state transition, not just that an interaction was performed.
- Do not rely on indirect checks when selectors, text checks, or state polling can verify the result directly.

## Flake Control

- Do not add blind retries in test bodies.
- If a retry is required for a known transient condition, keep attempts bounded and log the retry reason.
- Prefer condition-based waits and deterministic setup over rerun-based stabilization.

## Review Checklist

- The test name states the behavior being verified.
- Prerequisite steps exist only to reach the target state.
- Entry, scenario, and mechanics responsibilities are separated cleanly.
- Selector choice follows stability priority and avoids raw coordinates in scenario code.
- Markers make suite selection and execution cost clear.
- Fixture scope is no broader than necessary.
- Core business assertions remain in the scenario, not hidden in fixtures.
- Repeated setup is extracted only when reuse does not leak state.
- Waits are condition-based with explicit bounds, not fixed or unbounded sleeps.
- Parametrization is used for data variation, not to merge different scenarios.
- Stateful flows verify observable transition, not only successful interaction.
- Retry behavior is bounded and explicit, with no blind retry loops.
