---
name: qamule-jira-issue
description: Manage Jira issues with qamule-jira, including queries, templates, and creation.
user-invocable: false
---

# QAMule Jira Issue

## Read

```bash
uv run qamule-jira issue TEST-123 --field summary --field status
uv run qamule-jira jql 'project = TEST AND status = Open' --field summary
```

## Create

1. Find a template in `jira-issue-template/` matching the project and issue type.
2. If none exists, guide the user to create a clearly named template from Jira metadata. A reference issue may be queried when its fields are useful:

   ```bash
   uv run qamule-jira jql 'key = TEST-123' --field project --field issuetype --field priority
   uv run qamule-jira issue template --project-key TEST --issue-type Task --field Team jira-issue-template/test-task.json
   ```

3. Generate a separate, clearly named data file from the template, such as `jira-issue-data/create-login-regression-task.json`. Fill and inspect it; never modify or submit the template.
4. After user approval, create the issue from the data file:

   ```bash
   uv run qamule-jira issue create jira-issue-data/create-login-regression-task.json
   ```

The user's exact request to create the issue counts as approval.
