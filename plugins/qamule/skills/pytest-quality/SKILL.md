---
name: pytest-quality
description: Use when writing, reviewing, refactoring, or debugging robust QAMule pytest UI tests with uiautomator2 selectors, waits, fixtures, assertions, coverage reporting, helpers, or flaky failures.
user-invocable: false
---

# Pytest Quality

Write independent tests that prove one user-visible outcome and leave enough evidence to make a failure repairable.

## Boundaries

- This skill owns test design, synchronization, isolation, helper boundaries, assertions, and flaky-test repair.

## Test Contract

Before writing or changing a test, read the relevant test, fixture, and verified knowledge. Define:

1. The actor and known starting state.
2. One action and observable outcome.
3. Required synchronization, data, and cleanup.

Name the test after its outcome and keep one behavior per test:

```python
def test_authenticated_user_can_save_a_profile_change(...):
    """
    1. Save a valid display name | Verify: saved value is displayed.
    """
    ...
```

Put success, validation failure, permission denial, and recovery in separate tests unless they are essential to one user journey.

## Structure

- Fixtures own setup, cleanup, and shared data lifecycle.
- Tests own the narrative and business assertion.
- Helpers own repeated interaction with one UI boundary; give them explicit, meaningful inputs and names.
- Pass the device fixture into helpers. Do not use global device connections, mutable module state, or test-to-test dependencies.
- Extract a page or flow helper only for repeated UI interactions or synchronization that obscures the test story; keep it scoped to one UI boundary.
- When creating a helper module, add a brief file-level comment or docstring at the top that states its purpose and shows how to call its primary API.
- Helpers may verify UI readiness, but keep the final user-visible business assertion in the test; do not hide it in methods such as `save_and_verify()`.
- Prefer explicit, straight-line Arrange, Act, Assert code. Change one concern at a time when refactoring.

## UI And State

- Prefer `resourceId`, accessibility description, scoped text, then an anchored parent/child selector. Avoid `index`, `instance`, class-only, and coordinate selectors; isolate a necessary fallback and verify its result.
- Wait for an observable state before and after interaction. Bound waits and scrolling. Never use raw `time.sleep()` or retries that hide failures.
- Start from known app, account, permission, and navigation state. Use unique data when needed, and clean up reliably.
- Treat dialogs, permissions, loading, and network errors as explicit states.
- Assert a user-visible result, not a successful click or lack of exception.

## Coverage Report

When writing or modifying a pytest case under `tests/test*`, add the case test points as a triple-quoted docstring immediately below the test function definition.
Prefer a short ordered list of concrete verification points so the scenario intent stays visible in the test file:

```python
def test_authenticated_user_can_save_a_profile_change(...):
    """
    1. Save a valid display name | Verify: saved value is displayed.
    2. Display-name validation | Verify: empty value is rejected.
    3. Offline save recovery | Verify: saved value reappears after reconnect.
    """
    ...
```

Use a coverage marker instead of duplicating coverage status or gaps in the
docstring:

```python
@pytest.mark.partial(reason="Invalid-character validation needs controllable test data.")
def test_authenticated_user_can_save_a_profile_change(...):
    """
    1. Display-name validation | Verify: empty value is rejected.
    """
    ...
```

```python
@pytest.mark.not_covered(reason="Offline save recovery needs a controllable network fixture.")
def test_authenticated_user_can_save_a_profile_change(...):
    """
    1. Save a valid display name | Verify: saved value is displayed.
    2. Offline save recovery | Verify: saved value reappears after reconnect.
    """
    ...
```

Register the custom `partial` and `not_covered` markers in the project's pytest configuration. Use `partial` only when a running case covers part of an expected check.
Use `not_covered` on the nearest related executable case when an expected check has no automated coverage;
it is metadata and must not turn into an empty, skipped, or passing placeholder test. Each `reason` must name the affected check, missing scope, and next test or prerequisite.
Keep the testdocstring synchronized whenever the test point or verification changes.
Use pytest marker selection to filter incomplete coverage with `-m partial` or `-m not_covered`.

After writing or updating tests, compare expected checks from the request, acceptance criteria, linked knowledge, and explored flow with the checks in the test docstrings.
Include this table in the final response:

| Expected feature or check | Coverage | Verification | Gap or case annotation |
| --- | --- | --- | --- |
| Expected behavior | Covered, Partial, or Not covered | Assertion, observation, or helper used | Missing check and reason, if any |

- Mark incomplete coverage with `@pytest.mark.partial(reason="...")` or `@pytest.mark.not_covered(reason="...")`;
state the gap and next test or prerequisite in the marker reason.
- Derive the test point and verification columns from the owning test function's docstring. Derive `Partial` and `Not covered` status and gap from their respective marker reasons.
- Do not hide missing coverage with `skip`, `xfail`, a passing placeholder, or a broad retry.
- For a known product defect, retain the expected assertion and reference its tracked issue using the project's existing convention.

## Review Checklist

- Does the name describe one outcome, and can the test run in isolation?
- Are selectors semantic, waits observable, and assertions user-visible?
- Are helpers focused, state/data cleaned up, and failures preserved as artifacts rather than swallowed, skipped, or broadly retried?
- Does every test function docstring use a short ordered list of test points and verification methods, and does every incomplete case have the appropriate `partial` or `not_covered` marker with a useful reason?
- Does the final coverage table account for every expected check and identify every remaining gap?
- For flaky failures: inspect artifacts and hierarchy, identify the cause(selector, sync, state, environment, or product), fix it narrowly, then run the focused test through the QAMule protocol.
