---
name: live-pause-failure-triage
description: "Guide failure investigation only for pytest live pause `kind=failure` stops. Use when a pytest live pause stops on failure and you need to inspect the scene, classify likely cause, decide whether the issue belongs to test, environment, product, or external dependency, consult KB for known quirks, and produce a structured resume reason. Trigger keywords: live pause failure, failure pause, triage failure, investigate pause, paused failure, resume reason, 权限弹窗, 登录失效, 环境问题, 失败调研."
user-invocable: false
---

# Live Pause Failure Triage

Live pause failure triage is the investigation workflow for `kind=failure` pauses in pytest live pause.

This skill does not define how to start pytest or how pause transport works. Those runtime mechanics belong to the `pytest` skill.

This skill defines how to investigate the paused scene, how to use KB during that investigation, and how to produce a defensible resume reason.

## Goal

When a test pauses on failure, determine the most likely cause class and the most appropriate next action without making up product conclusions.

The outcome should answer:

- what was observed;
- whether the observed state is relevant to the test goal;
- whether the likely owner is test, environment, product, or external dependency;
- what should happen next.

## Boundaries

- Do not use live pause failure triage to replace assertions that the test can express directly.
- Do not encode project-specific facts here if they belong in KB.
- Do not write speculative conclusions back to KB.
- Do not mechanically dismiss dialogs or blockers before identifying whether they are the cause or only a symptom.

## Use KB During Triage

Before deciding on root cause, consult `kb` for reusable project facts:

1. Read relevant flow or screen preconditions.
2. Check known quirks in `kb/app/_app.md`.
3. For system dialogs or cross-app screens, check dependency knowledge under `kb/app/deps.md` and `kb/deps/{package}/`.

Use KB for stable facts such as:

- known permission prompts and when they appear;
- login or environment prerequisites;
- ROM or Android-version differences;
- known dependency app dialogs or selectors;
- confirmed recovery paths.

If the current observation is new, stable, and likely reusable, write it back to KB after the investigation.

## Standard Triage Loop

1. Confirm the failing objective.
   - What was the test trying to verify?
   - Which assertion or step failed?

2. Inspect the paused scene.
   - What screen is visible now?
   - What package is foreground?
   - Is there a system dialog, dependency app, login wall, loading state, or crash?

3. Check project knowledge.
   - Is this state already documented in KB as a known precondition, quirk, dependency, or flow branch?

4. Classify the likely cause.
   - `precondition_missing`: a requirement such as login, permission, seed data, or first-run completion was not satisfied.
   - `environment_interference`: system or device state blocked the test, such as ROM prompts, network loss, overlays, battery restrictions.
   - `test_gap`: selector drift, stale assumption, insufficient wait, over-strict assertion, or missing scripted branch.
   - `product_issue`: the app behavior itself appears incorrect for the intended flow.
   - `external_dependency`: backend, WebView, account provider, map SDK, chooser, or other external system failed.
   - `unknown`: evidence is insufficient or contradictory.

5. Decide the next action.
   - Continue after investigation if the pause only needs documentation and resume.
   - Update test setup if the issue is a reusable precondition problem.
   - Update the test if the script no longer matches the actual flow.
   - Report a product issue if the app behavior itself appears wrong.
   - Mark the run blocked if an external dependency or insufficient evidence prevents a sound conclusion.

6. Resume with a structured reason.
   - Always summarize the observed blocker, classification, likely owner, and next action.

## High-Frequency Scenarios

### Permission Prompt

Ask:

1. Is the permission request expected for this flow?
2. Should it be handled as a shared precondition or within this business flow?
3. Is the prompt from the app's expected behavior or from an unexpected regression?

Typical outcomes:

- Expected first-run permission not prepared -> `precondition_missing` or `environment_interference`
- Expected in-flow permission branch not covered by the test -> `test_gap`
- Unexpected permission request timing -> `product_issue`

### Login or Session Loss

Ask:

1. Did the test assume an authenticated state?
2. Is the session expiry expected in this environment?
3. Should authentication be restored by fixture/setup instead of per-test logic?

### Loading, Timeout, or Wrong Screen

Ask:

1. Did the app fail to navigate, or is the test asserting too early?
2. Is the current page a loading, retry, or interstitial state already known in KB?
3. Is the issue reproducible or likely transient?

### Dependency App or System Screen

Ask:

1. Is the foreground package the main app or a dependency?
2. Does KB already describe this dependency screen?
3. Should recovery happen through a known path, or is this a new dependency behavior worth recording?

## Resume Reason Template

Use a concise structured reason in this shape:

`observed=<what blocked the test>; impact=<how it affected the objective>; classification=<one class>; likely_owner=<test|environment|product|external>; next_action=<recommended follow-up>`

Example:

`observed=system camera permission dialog covered the home screen; impact=home assertion could not execute on the intended page; classification=precondition_missing; likely_owner=test; next_action=grant camera permission in shared setup or model the permission branch explicitly`

## KB Write-Back Rule

Write back to KB only when all of the following are true:

1. The observation is confirmed, not guessed.
2. The observation is likely reusable in future runs.
3. The observation has a meaningful scope such as app version, Android version, ROM, login state, or entry path.

Do not write back one-off noise or unresolved suspicions.
