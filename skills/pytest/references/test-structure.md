# Test Structure Conventions

## Directory structure

```
tests/
  {package_name}/
    conftest.py          ← fixtures with teardown (setup/cleanup)
    actions.py           ← reusable steps, plain functions, no teardown
    test_{module}.py     ← test functions, grouped by feature/screen
```

One test file per feature or screen. Keep files under ~150 lines.

---

## Test function style

Use plain functions. Do not use classes or Page Object Model (POM).

```python
import pytest
import uiautomator2 as u2

@pytest.mark.smoke
def test_login_success(phone: u2.Device, launch_app):
    phone(text="用户名").set_text("user@example.com")
    phone(text="密码").set_text("password123")
    phone(text="登录").click()
    assert phone(text="首页").exists(timeout=5)
```

- Each test is **self-contained** and readable without jumping to other files
- Preconditions come from fixtures declared in `conftest.py`
- Reusable steps are called from `actions.py`

---

## Data-driven tests

Use `@pytest.mark.parametrize`:("username,password,expected_error", [
    ("", "123456", "请填写用户名"),
    ("user@example.com", "", "请填写密码"),
    ("user@example.com", "wrong", "密码错误"),
])
def test_login_validation(phone: u2.Device, launch_app, username, password, expected_error):
    phone(text="用户名").set_text(username)
    phone(text="密码").set_text(password)
    phone(text="登录").click()
    assert phone(text=expected_error).exists(timeout=3)
```

---

## Mark taxonomy

| Mark | Usage |
|------|-------|
| `@pytest.mark.smoke` | Critical path, run on every build |
| `@pytest.mark.regression` | Full regression suite |
| `@pytest.mark.slow` | Tests that take > 30s |

Declare custom marks in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "smoke: critical path tests",
    "regression: full regression suite",
    "slow: tests that take > 30s",
]
```

---

## Decision table

| Situation | Solution |
|-----------|----------|
| Group related tests | Same file or `@pytest.mark` |
| Shared precondition with teardown | `conftest.py` fixture |
| Reusable steps, no teardown | `actions.py` plain function |
| Same test with different inputs | `@pytest.mark.parametrize` |
| Ordered multi-step flow | Single `test_complete_{flow}` function |
