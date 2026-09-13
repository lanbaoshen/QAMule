---
name: problem-triage
description: Use only after a QAMule pytest test run has failed, including a --pause-on-failure pause, to diagnose the failure from evidence and choose the next action.
user-invocable: false
---

# Problem Triage

Use this skill only after a pytest run has produced a failure. Do not use it while writing tests, before a run completes, or for a successful run.

## Diagnose The Failure

1. Confirm the failed test, assertion, and expected user-visible outcome.
2. Inspect the failure output, pause state, artifacts, logs, and current UI or device state.
3. Read relevant `knowledge-base` documents for verified prerequisites, quirks, and dependency behavior.
4. Classify the most likely cause:
   - `precondition_missing`: login, permission, setup, feature flag, or required state is absent.
   - `environment_interference`: device, OS, network, locale, or host state blocks the flow.
   - `test_or_automation_gap`: selector, wait, fixture, assertion, or scripted flow no longer matches reality.
   - `data_issue`: account, fixture, cache, or backend data is missing, stale, or inconsistent.
   - `external_dependency`: backend, third-party app, SDK, or service failed or changed behavior.
   - `product_issue`: behavior contradicts an anchored requirement or stable expected flow.
   - `unknown`: available evidence cannot distinguish the cause.
5. Take the next sound action: mark an external blocker; or gather one targeted piece of evidence.

## Rules

- Treat a running pytest session as an immutable test round. Do not edit test code, fixtures, test data, configuration, or app build.
- A failure pause is for evidence collection and classification only. Do not run focused verification until the original session has finished.
- Do not call behavior a product issue without an anchored expectation.
- Keep the diagnosis brief: failed objective, observed state, cause class, evidence, and next action.
- Add a fact to `knowledge-base` only when it is confirmed, reusable, and has clear scope. Do not record guesses or one-off failures.
