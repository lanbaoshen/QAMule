---
name: testcase
description: "Inspect existing pytest coverage in tests/. Use when checking whether a feature already has automated tests, listing related cases, or deciding whether to add a new test. Trigger keywords: existing test, test inventory, test coverage, find test, list tests, 有没有现有用例, 已有测试, 覆盖范围."
---

# Testcase Inventory

Use this skill before writing a new test or doing manual validation if you need to know what is already covered in `tests/`.

## Retrieval Modes

- Use pytest collection to list cases, get node IDs, or filter by file/function name.
- Use `grep` to find tests by feature, flow, or domain terms.
- Start with pytest for structural inventory; use `grep` for semantic search.

## Search Workflow

### 1. Choose Retrieval Method

Use pytest collection for structure-oriented requests:

```bash
uv run pytest tests --collect-only -q
```

Use selectors such as file path or `-k` for narrower filtering:

```bash
uv run pytest tests --collect-only -q -k "login"
```

Use `grep` instead when searching feature words in paths, comments, or test bodies.

### 2. Extract Search Terms

Collect a small set of likely terms from the request:

- Chinese feature words
- English feature words
- package, page, or flow names
- domain aliases already used in the repo

Example:

```text
下载|download|app_download
```

### 3. Search tests/

Search `tests/` by path and content. Prefer one regex with alternation.

```bash
grep -RniE "下载|download|app_download" tests
```

### 4. Summarize Matches

For each relevant hit, report:

- file path
- test function name
- covered behavior
- whether the match is direct coverage or only adjacent coverage

If useful, also report the exact pytest node ID.

### 5. Decide Next Action

- If strong matches exist, reuse or extend those tests.
- If only partial matches exist, call out the gap explicitly.
- If no match exists, state that no automated test was found and proceed with manual validation or new test creation.

## Coverage Analysis

When the user asks what is covered or what is missing:

1. Start from `uv run pytest tests --collect-only -q` to list collected files and functions.
2. Extract short intent from names, docstrings, and comments.
3. Group matches by feature or flow.
4. Highlight obvious gaps relevant to the request.
