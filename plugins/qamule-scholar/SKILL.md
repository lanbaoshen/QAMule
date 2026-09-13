---
name: qamule-scholar
description: Record Android-device interactions in its browser workspace, and locate the resulting recording artifacts.
disable-model-invocation: true
argument-hint: <start-server> or <recording-folder>
---

# QAMule Scholar

Use QAMule Scholar to explain how a human can project an ADB-authorized Android device in a local browser workspace and record device interactions with local microphone transcription.

Install `qamule-scholar`:

```bash
uv tool install qamule-scholar
```

Start Scholar from the desired working directory:

```bash
qamule-scholar
```

The first launch checks for the local `poloniumrock/SenseVoiceSmallOnnx` int8 model. If it is missing, Scholar asks for confirmation before downloading it through ModelScope. The human must run this in an interactive terminal and decide whether to confirm the download.

Once the service is up and running, ask the user to record their content in their browser.

## Recording Artifacts

QAMule Scholar writes the recording below `./qamule-scholar`, relative to the directory where they started the command. The recording directory is the artifact they should provide to the agent:

```text
qamule-scholar/
	recording-<UTC timestamp>-<id>/
		recording.json
		transcript.txt
		step_000/
			screenshot.jpg
			hierarchy.txt
			hierarchy.xml
```

`recording.json` stores the complete timeline, including the user's voice (intent) and actual actions. You can use this to understand what the user did and why they did it.

Each action will be preceded by a hierarchy and a screenshot. Prefer the lightweight `hierarchy.txt` when inspecting a step. Use `hierarchy.xml` only when `hierarchy.txt` is unavailable or its reduced representation does not provide the detail needed for the task.

You can use the `tap-node` command to quickly find clicked nodes.

```bash
qamule-scholar tap-node --step <step_index> --depth <depth> <recording-folder>
```

example:

```bash
qamule-scholar tap-node --step 0 --depth 5 qamule-scholar/recording-20260902T032957Z-091a1393
```
