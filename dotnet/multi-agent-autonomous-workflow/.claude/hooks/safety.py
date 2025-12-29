#!/usr/bin/env python3
"""
PreToolUse Safety Hook

Validates tool usage before execution:
- Blocks dangerous operations (rm -rf, DROP TABLE, etc.)
- Requires confirmation for sensitive operations (git push, db migrations)
- Protects production files from accidental edits

Usage in settings.json:
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash|Edit|Write",
      "command": "python .claude/hooks/safety.py"
    }]
  }
}
"""

import sys
import json
import re
from pathlib import Path


# Patterns that should be auto-blocked (never allowed)
BLOCKED_PATTERNS = [
    r'rm\s+-rf\s+/',           # rm -rf /
    r'rm\s+-rf\s+\*',          # rm -rf *
    r'rm\s+-r\s+/',            # rm -r /
    r'DROP\s+DATABASE',        # DROP DATABASE
    r'DROP\s+TABLE',           # DROP TABLE (be careful)
    r'TRUNCATE\s+TABLE',       # TRUNCATE TABLE
    r'DELETE\s+FROM\s+\w+\s*;', # DELETE FROM table; (no WHERE)
    r'--force\s+push',         # force push
    r'push\s+--force',         # push --force
    r'push\s+-f',              # push -f
    r'sudo\s+rm',              # sudo rm
    r'format\s+c:',            # format c:
    r'del\s+/f\s+/s\s+/q',     # Windows delete force
    r'rd\s+/s\s+/q\s+c:',      # Windows rmdir on C:
]

# Patterns that require human confirmation
CONFIRM_PATTERNS = [
    r'git\s+push(?!\s+--dry-run)',  # git push (except dry-run)
    r'dotnet\s+ef\s+database\s+update',  # EF migrations
    r'dotnet\s+ef\s+migrations\s+remove',  # Remove migration
    r'railway\s+up',            # Railway deploy
    r'supabase\s+db\s+push',    # Supabase push
    r'supabase\s+db\s+reset',   # Supabase reset
    r'npm\s+publish',           # npm publish
    r'docker\s+push',           # Docker push
]

# Production file paths that require confirmation to edit
PRODUCTION_PATHS = [
    'src/Doubleslash.Auctions.CustomerApi',
    'src/Doubleslash.Auctions.AdminApi',
    'src/Doubleslash.Auctions.Worker',
    '.github/workflows',
    'appsettings.Production.json',
]

# Files that should never be modified by automation
PROTECTED_FILES = [
    '.env',
    '.env.production',
    'credentials.json',
    'secrets.json',
    'appsettings.secrets.json',
]


def check_bash_command(command: str) -> dict:
    """Check a bash command for dangerous patterns."""
    command_lower = command.lower()

    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': f'Blocked dangerous pattern: {pattern}'
                }
            }

    # Check patterns requiring confirmation
    for pattern in CONFIRM_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'ask',
                    'permissionDecisionReason': f'Sensitive operation requires confirmation: {pattern}'
                }
            }

    return {}


def check_file_edit(file_path: str) -> dict:
    """Check if a file edit should be blocked or require confirmation."""
    path = Path(file_path)
    path_str = str(path).replace('\\', '/')

    # Check protected files
    for protected in PROTECTED_FILES:
        if path.name == protected or path_str.endswith(protected):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': f'Protected file cannot be modified: {protected}'
                }
            }

    # Check production paths
    for prod_path in PRODUCTION_PATHS:
        if prod_path in path_str:
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'ask',
                    'permissionDecisionReason': f'Editing production file requires confirmation: {file_path}'
                }
            }

    return {}


def main():
    """Main hook entry point. Reads input from stdin, outputs decision to stdout."""
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # If we can't parse input, allow the operation (fail open for usability)
        print(json.dumps({}))
        return

    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    result = {}

    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        result = check_bash_command(command)

    elif tool_name in ('Edit', 'Write'):
        file_path = tool_input.get('file_path', '')
        result = check_file_edit(file_path)

    print(json.dumps(result))


if __name__ == '__main__':
    main()
