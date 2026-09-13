#!/usr/bin/env bash

device_output="$(adb devices 2>&1)"
escaped_device_output="$(
    printf '%s' "$device_output" | LC_ALL=C awk '
        function json_escape(value, result, position, character) {
            result = ""
            for (position = 1; position <= length(value); position++) {
                character = substr(value, position, 1)
                if (character == "\\") result = result "\\\\"
                else if (character == "\"") result = result "\\\""
                else if (character == "\t") result = result "\\t"
                else if (character == "\r") result = result "\\r"
                else result = result character
            }
            return result
        }
        NR > 1 { printf "\\n" }
        { printf "%s", json_escape($0) }
    '
)"

printf '{"systemMessage":"Android device list injected from adb devices.\\n%s","hookSpecificOutput":{"additionalContext":"%s"}}\n' \
    "$escaped_device_output" "$escaped_device_output"
