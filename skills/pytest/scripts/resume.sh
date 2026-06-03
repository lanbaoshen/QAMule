#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage:
  bash skills/pytest/scripts/resume.sh LOG_FILE [--result true|false] [--reason TEXT]
  bash skills/pytest/scripts/resume.sh LOG_FILE --json JSON_STRING
  bash skills/pytest/scripts/resume.sh LOG_FILE --continue-only

Behavior:
  - Reads the latest QAMULE_PAUSE_EVENT from LOG_FILE
  - Optionally writes a JSON result to result_path when the pause event provides one
  - Sends the configured signal to the paused pytest process

Examples:
  bash skills/pytest/scripts/resume.sh "$log" --continue-only
  bash skills/pytest/scripts/resume.sh "$log" --result true --reason "verified by external agent"
  bash skills/pytest/scripts/resume.sh "$log" --json '{"status":"confirmed","reason":"observed by agent"}'
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

log_file="${1:-${log:-}}"
shift $(( $# > 0 ? 1 : 0 ))

if [[ -z "$log_file" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -e "$log_file" ]]; then
  echo "[FATAL] Log file not found: $log_file" >&2
  exit 2
fi

json_payload=''
bool_result=''
reason=''
continue_only=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json)
      if [[ $# -lt 2 ]]; then
        echo "[FATAL] --json requires a value" >&2
        exit 2
      fi
      json_payload="$2"
      shift 2
      ;;
    --result)
      if [[ $# -lt 2 ]]; then
        echo "[FATAL] --result requires true or false" >&2
        exit 2
      fi
      bool_result="$2"
      shift 2
      ;;
    --reason)
      if [[ $# -lt 2 ]]; then
        echo "[FATAL] --reason requires text" >&2
        exit 2
      fi
      reason="$2"
      shift 2
      ;;
    --continue-only)
      continue_only=1
      shift
      ;;
    *)
      echo "[FATAL] Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -n "$json_payload" && -n "$bool_result" ]]; then
  echo "[FATAL] Use either --json or --result/--reason, not both" >&2
  exit 2
fi

if [[ "$continue_only" -eq 1 && ( -n "$json_payload" || -n "$bool_result" || -n "$reason" ) ]]; then
  echo "[FATAL] --continue-only cannot be combined with result options" >&2
  exit 2
fi

last_event_line="$(grep 'QAMULE_PAUSE_EVENT ' "$log_file" | tail -n 1)"

if [[ -z "$last_event_line" ]]; then
  echo "[FATAL] No QAMULE_PAUSE_EVENT found in log: $log_file" >&2
  exit 2
fi

event_json="${last_event_line#QAMULE_PAUSE_EVENT }"

pause_meta="$(
  EVENT_JSON="$event_json" python3 - <<'PY'
import json
import os
import sys

event = json.loads(os.environ["EVENT_JSON"])
pid = event.get("pid")
signal_name = event.get("signal")
result_path = event.get("result_path", "")
reason = event.get("reason", "")
if not isinstance(pid, int) or not isinstance(signal_name, str):
    raise SystemExit(2)
print(pid)
print(signal_name)
print(result_path)
print(reason)
PY
)"

if [[ $? -ne 0 || -z "$pause_meta" ]]; then
  echo "[FATAL] Failed to parse pause event metadata" >&2
  exit 2
fi

pause_pid="$(printf '%s\n' "$pause_meta" | sed -n '1p')"
pause_signal="$(printf '%s\n' "$pause_meta" | sed -n '2p')"
result_path="$(printf '%s\n' "$pause_meta" | sed -n '3p')"
pause_reason="$(printf '%s\n' "$pause_meta" | sed -n '4p')"

if [[ -n "$json_payload" || -n "$bool_result" || -n "$reason" ]]; then
  if [[ -z "$result_path" ]]; then
    echo "[FATAL] Latest pause event does not expose result_path" >&2
    exit 2
  fi

  if [[ -n "$json_payload" ]]; then
    PAYLOAD_JSON="$json_payload" python3 - <<'PY' > /dev/null
import json
import os

json.loads(os.environ["PAYLOAD_JSON"])
PY
    if [[ $? -ne 0 ]]; then
      echo "[FATAL] --json must be valid JSON" >&2
      exit 2
    fi
    printf '%s\n' "$json_payload" > "$result_path"
  else
    if [[ "$bool_result" != "true" && "$bool_result" != "false" ]]; then
      echo "[FATAL] --result must be true or false" >&2
      exit 2
    fi
    RESULT_BOOL="$bool_result" RESULT_REASON="$reason" python3 - <<'PY' > "$result_path"
import json
import os
import sys

payload = {"result": os.environ["RESULT_BOOL"] == "true"}
reason = os.environ.get("RESULT_REASON", "")
if reason:
    payload["reason"] = reason
json.dump(payload, sys.stdout, ensure_ascii=True)
sys.stdout.write("\n")
PY
  fi
  printf 'Wrote pause result to: %s\n' "$result_path"
fi

kill -"$pause_signal" "$pause_pid"
printf 'Sent %s to pytest pid %s for pause reason %s\n' "$pause_signal" "$pause_pid" "$pause_reason"
