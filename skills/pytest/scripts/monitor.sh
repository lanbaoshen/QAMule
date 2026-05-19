#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage:
  bash skills/pytest/scripts/monitor.sh LOG_FILE

Behavior:
  - Prints "Test paused; inspect debug information." when the current last line matches
    "Send ... to continue:"
  - Prints "Test finished." when the current last line contains
    "QAMule pytest exit code="
  - Prints the current last line before exiting
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

while :; do
  last_line="$(tail -n 1 "$log_file" 2>/dev/null)"

  if [[ "$last_line" =~ Send[[:space:]].*to[[:space:]]continue: ]]; then
    echo "Test paused; inspect debug information."
    printf 'Last line: %s\n' "$last_line"
    exit 2
  fi

  if [[ "$last_line" == *"QAMule pytest exit code="* ]]; then
    echo "Test finished."
    printf 'Last line: %s\n' "$last_line"
    exit 0
  fi

  sleep 0.2
done
