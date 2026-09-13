---
name: qamule-jira-testcase
description: Use when retrieving Jira Xray test cases or converting them into QAMule pytest tests.
user-invocable: false
---

# QAMule Jira Testcase

## Fetch

```bash
uv run qamule-jira testcase TEST-123 TEST-124
```

Output includes each test's summary, preconditions, and steps with `action`,
`data`, and `expected`. Verify missing or empty content in Jira; do not invent
requirements.

**Mark the automated test with the same `@pytest.mark.xray("TEST-123")` key.**
