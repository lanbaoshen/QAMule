---
name: testcase
description: "Search and list existing pytest test cases in the workspace. Use when the user requests testing a feature, to check if automated tests already exist before manual testing. Also use for test coverage analysis, listing all tests, or finding which test points are covered. Trigger keywords: test coverage, existing tests, find test, list tests, what tests exist, 测试覆盖, 已有用例."
---

# Test Inventory

Search `tests/` for existing automated test cases.

## Procedure

### 1. Extract Keywords

From the user's test request, extract:
- **Chinese keywords** — e.g. "下载", "安装", "播放"
- **English keywords** — e.g. "download", "install", "play"
- **Feature names** — e.g. "app_download", "store"

### 2. Search File Names and Docstrings

Search `tests/` directory for the extracted keywords against file names and module docstrings (first line `"""..."""`).

Use alternation to search **all** extracted keywords (both Chinese and English) at once:
```
grep -r -l "下载|download|app_download" tests/
```

### 3. Search Comments and Function Docstrings

If Step 2 finds no matches, broaden the search to function docstrings and code comments (`# Step N: ...`).

### 4. Handle No Match

If no matching tests are found, inform the user that no existing tests cover the requested feature and proceed with manual testing.

## Coverage Analysis

When the user asks about test coverage or what's covered:

1. List all test files and functions in `tests/`
2. Extract docstrings to describe what each test covers
3. Cross-reference with `kb/app/flows/` to identify gaps
4. Report covered vs uncovered flows
