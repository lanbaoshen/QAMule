---
name: qamule-pytest-dispcap
description: Record Android display videos during pytest test runs
user-invocable: false
---
# QAMule Pytest Dispcap

## Capture Display

```bash
uv run pytest tests --dispcap-device NAME[:display=ID[,ID...]][:size=WIDTHxHEIGHT][:bitrate=RATE][:fps=FPS]
```

`--dispcap-device` can be repeated. `NAME` must match a registered `--device` name (Default device is `d`. If omitted, `d` is used).

## Inspect Artifacts

```text
pytest-artifacts/<session>/<case>/dispcap/
	<device>.mp4
	manifest.json
```

The manifest records capture settings, timing, test outcome, and per-device errors.

## Retention

Remove videos for passed cases while retaining failed and skipped case videos:

```bash
uv run pytest tests --dispcap-device d --dispcap-passed-remove
```
