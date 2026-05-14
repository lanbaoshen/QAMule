---
name: testcase
description: "Inspect existing pytest coverage in tests/. Use when checking whether a feature already has automated tests, listing related cases, or deciding whether to add a new test. Trigger keywords: existing test, test inventory, test coverage, find test, list tests, 有没有现有用例, 已有测试, 覆盖范围."
---

# Testcase Inventory

Use this skill before writing a new test or doing manual validation if you need to know what is already covered in `tests/`.

## Search Workflow

### 1. Extract Search Terms

Collect a small set of likely terms from the request:

- Chinese feature words
- English feature words
- package, page, or flow names
- domain aliases already used in the repo

Example:

```text
下载|download|app_download
```

### 2. Search tests/

Search `tests/` by both file path and content. Prefer one regex with alternation instead of multiple passes.

```bash
rg -n -i "下载|download|app_download" tests
```

### 3. Summarize Matches

For each relevant hit, report:

- file path
- test function name
- what behavior it appears to cover
- whether the match is direct coverage or only adjacent coverage

### 4. Decide Next Action

- If strong matches exist, reuse or extend those tests.
- If only partial matches exist, call out the gap explicitly.
- If no match exists, state that no automated test was found and proceed with manual validation or new test creation.

## Coverage Analysis

When the user asks what is covered or what is missing:

1. List all test files and functions in `tests/`.
2. Extract short intent from names, docstrings, and comments.
3. Group matches by feature or flow.
4. Highlight obvious gaps relevant to the request.
