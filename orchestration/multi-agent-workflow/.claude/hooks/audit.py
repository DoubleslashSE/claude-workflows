#!/usr/bin/env python3
"""
PostToolUse Audit Hook

Logs all tool usage for observability and debugging:
- Records tool name, input, and timestamp
- Tracks session and correlation IDs
- Writes to .claude/audit.log as JSONL

Usage in settings.json:
{
  "hooks": {
    "PostToolUse": [{
      "matcher": ".*",
      "command": "python .claude/hooks/audit.py"
    }]
  }
}
"""

import sys
import json
from datetime import datetime, timezone
from pathlib import Path


# Maximum length for input summary in log
MAX_INPUT_LENGTH = 500

# Log file location
LOG_FILE = Path('.claude/audit.log')


def truncate_string(s: str, max_length: int) -> str:
    """Truncate a string to max_length with ellipsis if needed."""
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + '...'


def sanitize_input(tool_input: dict) -> dict:
    """Remove sensitive data and truncate large values for logging."""
    sanitized = {}
    sensitive_keys = {'password', 'secret', 'token', 'api_key', 'apikey', 'auth'}

    for key, value in tool_input.items():
        # Skip sensitive keys
        if any(s in key.lower() for s in sensitive_keys):
            sanitized[key] = '[REDACTED]'
        elif isinstance(value, str):
            sanitized[key] = truncate_string(value, MAX_INPUT_LENGTH)
        elif isinstance(value, (dict, list)):
            sanitized[key] = truncate_string(json.dumps(value), MAX_INPUT_LENGTH)
        else:
            sanitized[key] = value

    return sanitized


def main():
    """Main hook entry point. Logs tool usage and returns empty response."""
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Build log entry
    log_entry = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'event': input_data.get('hook_event_name', 'PostToolUse'),
        'tool': input_data.get('tool_name', 'unknown'),
        'session_id': input_data.get('session_id', 'unknown'),
        'tool_use_id': input_data.get('tool_use_id', 'unknown'),
        'input': sanitize_input(input_data.get('tool_input', {})),
    }

    # Add response info if available (for PostToolUse)
    tool_response = input_data.get('tool_response')
    if tool_response:
        if isinstance(tool_response, str):
            log_entry['output_preview'] = truncate_string(tool_response, 200)
        elif isinstance(tool_response, dict):
            # Check for error
            if 'error' in tool_response:
                log_entry['error'] = truncate_string(str(tool_response['error']), 200)
            else:
                log_entry['output_preview'] = truncate_string(json.dumps(tool_response), 200)

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except IOError:
        # If we can't write the log, don't block the operation
        pass

    # Return empty response (don't affect tool execution)
    print(json.dumps({}))


if __name__ == '__main__':
    main()
