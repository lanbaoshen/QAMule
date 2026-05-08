## Shared Setup

When 2+ tests share common precondition steps, extract a fixture:

```python
@pytest.fixture
def at_sub_page(d: u2.Device):
    """Launch app and navigate to a sub-page."""
    d.app_start("com.example.app", activity=".MainActivity")
    d(text="Category").click()
    assert d(text="Target").wait(timeout=5)
    return d

def test_action_on_target(at_sub_page: u2.Device):
    at_sub_page(text="Target").click()
    ...
```

Do not pre-extract for a single test.

## Parametrize

Same flow, multiple targets → use parametrize:

```python
@pytest.mark.parametrize("item", ["Item A", "Item B"])
def test_action_on_item(d: u2.Device, item: str):
    ...
    d(text=item).click()
    ...
```
