---
name: qamule-jira-troubleshoot
description: Use when qamule-jira is unavailable, authentication fails, testcase data is stale, project inference fails, or a Jira or Xray command returns an error.
user-invocable: false
---

# Troubleshooting

## Missing Command

```bash
uv add "qamule-pytest-jira"
```

## Authentication

Authentication must persist across terminal sessions. Do not stop after exporting variables in the current shell.

On macOS with zsh, add or update these entries in `~/.zprofile`:

```bash
export QAMULE_JIRA_URL="https://jira.example.com"
export QAMULE_JIRA_TOKEN="<token>"
```

Ask the user to enter the token directly in their terminal or profile, never in chat.
Do not print it or write it into the workspace. Update existing entries instead of appending duplicates.

Reload the profile and verify both variables without exposing their values:

```bash
source ~/.zprofile
test -n "$QAMULE_JIRA_URL" && test -n "$QAMULE_JIRA_TOKEN"
```

For other shells, persist the variables in the corresponding login profile.
