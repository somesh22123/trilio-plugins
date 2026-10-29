#!/usr/bin/env python3
"""PreToolUse hook: ask the user before a shell command changes Trilio resources.

Reads the hook event on stdin. For a Bash command that runs kubectl, oc or helm
with a mutating verb against anything named trilio, it returns
permissionDecision "ask" so the user confirms first. Everything else passes.
"""
import json
import re
import sys

MUTATING = re.compile(
    r"\b(?:kubectl|oc)\b[^|;&]*\b(?:delete|patch|edit|apply|replace|scale|annotate|label)\b"
    r"|\bhelm\b[^|;&]*\b(?:uninstall|delete|upgrade|rollback)\b"
)
TRILIO = re.compile(r"trilio", re.IGNORECASE)


def decide(event):
    if event.get("tool_name") != "Bash":
        return None
    command = event.get("tool_input", {}).get("command", "")
    if MUTATING.search(command) and TRILIO.search(command):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": "This command changes Trilio resources. Confirm before it runs.",
            }
        }
    return None


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    result = decide(event)
    if result:
        print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
