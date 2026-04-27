# Running Tests — Command Reference

```bash
# Auto-detect device, run all tests
.venv/bin/pytest tests/

# Named device
.venv/bin/pytest --device phone:emulator-5554 tests/

# Specific app tests, verbose
.venv/bin/pytest --device phone:d74e53a3 tests/com.example.app/ -sv

# Dry-run (collection only)
.venv/bin/pytest --device phone:d74e53a3 --co -q

# Pause on failure (agent workflow: stop before teardown so agent can inspect device)
.venv/bin/pytest --pause-on-failure tests/
```
