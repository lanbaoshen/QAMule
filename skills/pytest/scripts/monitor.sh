#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage:
  bash skills/pytest/scripts/monitor.sh LOG_FILE

Behavior:
  - Prints "Test paused; inspect debug information." when the current last line is a
    QAMULE_PAUSE_EVENT record
  - Prints "Test finished." when the current last line contains
    "QAMule pytest exit code="
  - Prints a concise summary before exiting
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

log_file="${1:-${log:-}}"

if [[ -z "$log_file" ]]; then
  usage >&2
  exit 2
fi

if [[ ! -e "$log_file" ]]; then
  echo "[FATAL] Log file not found: $log_file" >&2
  exit 2
fi

extract_json_string_field() {
  local line="$1"
  local field="$2"

  printf '%s\n' "$line" | sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p"
}

build_pause_summary() {
  local line="$1"
  local reason=''
  local task=''
  local nodeid=''
  local signal_name=''
  local summary=''

  reason="$(extract_json_string_field "$line" 'reason')"
  task="$(extract_json_string_field "$line" 'task')"
  nodeid="$(extract_json_string_field "$line" 'nodeid')"
  signal_name="$(extract_json_string_field "$line" 'signal')"

  if [[ -n "$reason" ]]; then
    summary="reason=$reason"
  fi

  if [[ "$reason" == 'checkpoint' && -n "$task" ]]; then
    summary+="${summary:+ }task=$task"
  fi

  if [[ -n "$nodeid" ]]; then
    summary+="${summary:+ }nodeid=$nodeid"
  fi

  if [[ -n "$signal_name" ]]; then
    summary+="${summary:+ }signal=$signal_name"
  fi

  printf '%s\n' "$summary"
}

while :; do
  last_line="$(tail -n 1 "$log_file" 2>/dev/null)"

  if [[ "$last_line" == QAMULE_PAUSE_EVENT* ]]; then
    pause_summary="$(build_pause_summary "$last_line")"
    echo "Test paused; inspect debug information."
    if [[ -n "$pause_summary" ]]; then
      printf 'Summary: %s\n' "$pause_summary"
    fi
    exit 2
  fi

  if [[ "$last_line" == *"QAMule pytest exit code="* ]]; then
    echo "Test finished."
    printf 'Summary: %s\n' "${last_line#*QAMule pytest exit code=}"
    exit 0
  fi

  sleep 0.2
done
