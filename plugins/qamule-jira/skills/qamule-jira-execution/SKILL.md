---
name: qamule-jira-execution
description: Use when linking pytest tests to Jira Xray or reading, creating, importing, or organizing Xray Test Executions.
user-invocable: false
---

# QAMule Jira Execution

## Collect Results

Mark tests with their Xray Test keys:

```python
import pytest

@pytest.mark.xray("TEST-123")
def test_login(d):
    assert d.serial is not None
```

Run pytest with `--xray-project-key TEST` when one project cannot be inferred. Results are written to `pytest-artifacts/<session-id>/jira/xray-test-results.json`

## Merge Results

When several runs must become one Test Execution, merge their JSON files locally and import only the merged file. Parse JSON structurally; do not merge with text replacement.

- Require every input to contain a `tests` array and compatible execution metadata. Stop and ask the user when project, Test Plan, or environment metadata conflict.
- Group test results by `testKey`. Keep tests that occur in only one input.
- For duplicate keys, a result whose normalized status is `PASS` or `PASSED` wins over every non-passing result. If both candidates have the same pass priority, keep the one with the later `finish` timestamp; when timestamps are absent or equal, keep the result from the later input file.
- Keep the selected test result as one complete object. Do not combine its status, timestamps, evidence, or comments with fields from another run.
- Write a new JSON file without modifying the source artifacts. Before import, report the input count, unique test count, duplicate count, and each conflict that was resolved in favor of a passing result.

Import the merged file once using the command below. Importing each source file separately does not implement these precedence rules.

## Manage Executions

```bash
uv run qamule-jira execution EXEC-123 --field summary --field status
uv run qamule-jira execution create --project-key TEST --summary "Regression run"
uv run qamule-jira execution EXEC-123 add-tests TEST-123 TEST-124
uv run qamule-jira execution EXEC-123 add-to-plan PLAN-123
uv run qamule-jira execution import pytest-artifacts/<session-id>/jira/xray-test-results.json
```

Inspect result files before import. Creation, association, and import write remote Xray data; obtain explicit user approval unless already requested.
